# Utility imports
import datetime
import pytz

from celery.task import PeriodicTask
from celery.task.schedules import crontab

from apps.common.util import cast_empty_string_to_int, cast_empty_string_to_float

# Models
from eve_db.models import StaStation
from apps.market_data.models import Orders
from apps.api.models import SkillGroup, Skill, APITimer, Character, APIKey, CharSkill, MarketOrder, RefType, JournalEntry, MarketTransaction

# API
from element43 import eveapi

# API error handling
from apps.api.api_exceptions import handle_api_exception


class ProcessWalletJournal(PeriodicTask):
    """
    Processes char/corp journal. Done every 5 minutes.
    TODO: Add corp key handling.
    """

    run_every = datetime.timedelta(minutes=5)

    def run(self, **kwargs):
        print 'UPDATING JOURNAL ENTRIES'

        api = eveapi.EVEAPIConnection()

        update_timers = APITimer.objects.filter(apisheet="WalletJournal",
                                                nextupdate__lte=pytz.utc.localize(datetime.datetime.utcnow()))

        for update in update_timers:

            character = Character.objects.get(id=update.character_id)
            print ">>> Updating journal entries for %s" % character.name

            # Try to fetch a valid key from DB
            try:
                apikey = APIKey.objects.get(id=character.apikey_id, is_valid=True)
            except APIKey.DoesNotExist:
                print('There is no valid key for %s.' % character.name)
                raise

            # Try to authenticate and handle exceptions properly
            try:
                auth = api.auth(keyID=apikey.keyid, vCode=apikey.vcode)
                me = auth.character(character.id)
                sheet = me.WalletJournal()

            except eveapi.Error, e:
                handle_api_exception(e, apikey)

            for transaction in sheet.transactions:
                #
                # Import entries
                #

                # Now try to get the Entry
                try:
                    JournalEntry.objects.get(ref_id=transaction.refID, character=character)
                    # If this succeeds, it's already in the DB
                except JournalEntry.DoesNotExist:
                    # Add entry to DB

                    entry = JournalEntry(ref_id=transaction.refID,
                                         character=character,
                                         is_corporate_transaction=False,
                                         date=pytz.utc.localize(datetime.datetime.utcfromtimestamp(transaction.date)),
                                         ref_type_id=transaction.refTypeID,
                                         amount=transaction.amount,
                                         balance=transaction.balance,
                                         owner_name_1=transaction.ownerName1,
                                         owner_id_1=transaction.ownerID1,
                                         owner_name_2=transaction.ownerName2,
                                         owner_id_2=transaction.ownerID2,
                                         arg_name_1=transaction.argName1,
                                         arg_id_1=transaction.argID1,
                                         reason=transaction.reason,
                                         tax_receiver_id=cast_empty_string_to_int(transaction.taxReceiverID),
                                         tax_amount=cast_empty_string_to_float(transaction.taxAmount))
                    entry.save()

            # Update timer
            timer = APITimer.objects.get(character=character, apisheet='WalletJournal')
            timer.nextupdate = pytz.utc.localize(datetime.datetime.utcfromtimestamp(sheet._meta.cachedUntil))
            timer.save()

            print "<<<  %s's journal import was completed successfully." % character.name


class ProcessRefTypes(PeriodicTask):
    """
    Reloads the refTypeID to name mappings. Done daily at 00:00 just before history is processed.
    """

    run_every = crontab(hour=0, minute=0)

    def run(self, **kwargs):

        print '>>>  Updating refTypeIDs...'

        api = eveapi.EVEAPIConnection()
        ref_types = api.eve.RefTypes()

        for ref_type in ref_types.refTypes:
            # Try to find mapping in DB. If found -> update. If not found -> create
            try:
                type_object = RefType.objects.get(id=ref_type.refTypeID)
                type_object.name = ref_type.refTypeName
                type_object.save()

            except RefType.DoesNotExist:
                type_object = RefType(id=ref_type.refTypeID, name=ref_type.refTypeName)
                type_object.save()

        print '<<< Finished updating refTypeIDs.'


class ProcessMarketOrders(PeriodicTask):
    """
    Scan the db and refresh all market orders from the API.
    Done every 5 minutes.
    """

    run_every = datetime.timedelta(minutes=5)

    def run(self, **kwargs):
        api = eveapi.EVEAPIConnection()

        update_timers = APITimer.objects.filter(apisheet="MarketOrders",
                                                nextupdate__lte=pytz.utc.localize(datetime.datetime.utcnow()))

        for update in update_timers:

            character = Character.objects.get(id=update.character_id)
            print ">>> Market Orders: %s" % character.name

            # Try to fetch a valid key from DB
            try:
                apikey = APIKey.objects.get(id=character.apikey_id, is_valid=True)
            except APIKey.DoesNotExist:
                print('There is no valid key for %s.' % character.name)
                raise

            # Try to authenticate and handle exceptions properly
            try:
                auth = api.auth(keyID=apikey.keyid, vCode=apikey.vcode)
                me = auth.character(character.id)
                orders = me.MarketOrders()

            except eveapi.Error, e:
                handle_api_exception(e, apikey)

            for order in orders.orders:
                #
                # Import orders
                #

                # Look if we have this order in our DB
                try:
                    db_order = Orders.objects.get(id=order.orderID)

                    # Now that we found that order - let's update it
                    db_order.generated_at = pytz.utc.localize(datetime.datetime.utcnow())
                    db_order.price = order.price
                    db_order.volume_remaining = order.volRemaining
                    db_order.volume_entered = order.volEntered
                    db_order.is_suspicious = False

                    if order.orderState == 0:
                        db_order.is_active = True
                    else:
                        db_order.is_active = False

                    db_order.save()

                except Orders.DoesNotExist:

                    # Try to get the station of that order to get the region/system since it isn't provided by the API
                    station = StaStation.objects.get(id=order.stationID)
                    region = station.region
                    system = station.solar_system

                    new_order = Orders(id=order.orderID,
                                       generated_at=pytz.utc.localize(datetime.datetime.utcnow()),
                                       mapregion=region,
                                       invtype_id=order.typeID,
                                       price=order.price,
                                       volume_remaining=order.volRemaining,
                                       volume_entered=order.volEntered,
                                       minimum_volume=order.minVolume,
                                       order_range=order.range,
                                       is_bid=order.bid,
                                       issue_date=pytz.utc.localize(datetime.datetime.utcfromtimestamp(order.issued)),
                                       duration=order.duration,
                                       stastation=station,
                                       mapsolarsystem=system,
                                       is_suspicious=False,
                                       message_key='eveapi',
                                       uploader_ip_hash='eveapi',
                                       is_active=True)
                    new_order.save()

                # Now try to get the MarketOrder
                try:
                    market_order = MarketOrder.objects.get(id=order.orderID)

                    # If this succeeds, update market order
                    market_order.order_state = order.orderState
                    market_order.save()

                except MarketOrder.DoesNotExist:
                    market_order = MarketOrder(id_id=order.orderID,
                                               character=character,
                                               order_state=order.orderState,
                                               account_key=order.accountKey,
                                               escrow=order.escrow)
                    market_order.save()

            # Update timer
            timer = APITimer.objects.get(character=character, apisheet='MarketOrders')
            timer.nextupdate = pytz.utc.localize(datetime.datetime.utcfromtimestamp(orders._meta.cachedUntil))
            timer.save()

            print "<<<  %s's Market orders were completed successfully." % character.name


class ProcessCharacterSheet(PeriodicTask):
    """
    Scan the db an refresh all character sheets
    Currently done once every 15 minutes
    """

    run_every = datetime.timedelta(minutes=15)

    def run(self, **kwargs):
        print "BEGIN CHARACTER IMPORT"

        #define variables
        i_stats = {}
        implant = {}
        attributes = ['memory', 'intelligence', 'perception', 'willpower', 'charisma']

        #grab an api object
        api = eveapi.EVEAPIConnection()

        #scan to see if anyone is due for an update
        update_timers = APITimer.objects.filter(apisheet="CharacterSheet",
                                                nextupdate__lte=pytz.utc.localize(datetime.datetime.utcnow()))
        for update in update_timers:

            character = Character.objects.get(id=update.character_id)
            print ">>> Updating: %s" % character.name

            # Try to fetch a valid key from DB
            try:
                apikey = APIKey.objects.get(id=character.apikey_id, is_valid=True)
            except APIKey.DoesNotExist:
                print('There is no valid key for %s.' % character.name)
                raise

            # Try to authenticate and handle exceptions properly
            try:
                auth = api.auth(keyID=apikey.keyid, vCode=apikey.vcode)
                me = auth.character(character.id)
                sheet = me.CharacterSheet()
                i_stats['name'] = ""
                i_stats['value'] = 0

            except eveapi.Error, e:
                handle_api_exception(e, apikey)

            for attr in attributes:
                implant[attr] = i_stats

            # have to check because if you don't have an implant in you get nothing back
            try:
                implant['memory'] = {'name': sheet.attributeEnhancers.memoryBonus.augmentatorName,
                                     'value': sheet.attributeEnhancers.memoryBonus.augmentatorValue}
            except:
                pass
            try:
                implant['perception'] = {'name': sheet.attributeEnhancers.perceptionBonus.augmentatorName,
                                         'value': sheet.attributeEnhancers.perceptionBonus.augmentatorValue}
            except:
                pass
            try:
                implant['intelligence'] = {'name': sheet.attributeEnhancers.intelligenceBonus.augmentatorName,
                                           'value': sheet.attributeEnhancers.intelligenceBonus.augmentatorValue}
            except:
                pass
            try:
                implant['willpower'] = {'name': sheet.attributeEnhancers.willpowerBonus.augmentatorName,
                                        'value': sheet.attributeEnhancers.willpowerBonus.augmentatorValue}
            except:
                pass
            try:
                implant['charisma'] = {'name': sheet.attributeEnhancers.charismaBonus.augmentatorName,
                                       'value': sheet.attributeEnhancers.charismaBonus.augmentatorValue}
            except:
                pass
            try:
                character.alliance_name = sheet.allianceName
                character.alliance_id = sheet.allianceID
            except:
                character.alliance_name = ""
                character.alliance_id = 0

            character.corp_name = sheet.corporationName
            character.corp_id = sheet.corporationID
            character.clone_name = sheet.cloneName
            character.clone_skill_points = sheet.cloneSkillPoints
            character.balance = sheet.balance
            character.implant_memory_name = implant['memory']['name']
            character.implant_memory_bonus = implant['memory']['value']
            character.implant_perception_name = implant['perception']['name']
            character.implant_perception_bonus = implant['perception']['value']
            character.implant_intelligence_name = implant['intelligence']['name']
            character.implant_intelligence_bonus = implant['intelligence']['value']
            character.implant_willpower_name = implant['willpower']['name']
            character.implant_willpower_bonus = implant['willpower']['value']
            character.implant_charisma_name = implant['charisma']['name']
            character.implant_charisma_bonus = implant['charisma']['value']

            character.save()

            for skill in sheet.skills:
                try:
                    c_skill = CharSkill.objects.get(character=character, skill_id=skill.typeID)
                    c_skill.skillpoints = skill.skillpoints
                    c_skill.level = skill.level
                    c_skill.save()
                except:
                    new_skill = CharSkill(character=character,
                                          skill_id=skill.typeID,
                                          skillpoints=skill.skillpoints,
                                          level=skill.level)
                    new_skill.save()

            # Set nextupdate to cachedUntil
            update.nextupdate = pytz.utc.localize(datetime.datetime.utcfromtimestamp(sheet._meta.cachedUntil))
            update.save()
            print "<<< %s update complete" % character.name


class ProcessAPISkillTree(PeriodicTask):
    """
    Grab the skill list, iterate it and store to DB
    """

    run_every = datetime.timedelta(hours=24)

    def run(self, **kwargs):

        print "BEGIN SKILL IMPORT"
        #create our api object
        api = eveapi.EVEAPIConnection()

        #load the skilltree
        skilltree = api.eve.SkillTree()

        #start iterating
        for g in skilltree.skillGroups:
            new_group = SkillGroup(id=g.groupID, name=g.groupName)
            new_group.save()
            for skill in g.skills:
                try:
                    s_primary = skill.requiredAttributes.primaryAttribute
                except:
                    s_primary = ""
                try:
                    s_secondary = skill.requiredAttributes.secondaryAttribute
                except:
                    s_secondary = ""
                if skill.published:
                    published = True
                else:
                    published = False
                new_skill = Skill(id=skill.typeID,
                                  name=skill.typeName,
                                  group=new_group,
                                  published=published,
                                  description=skill.description,
                                  rank=skill.rank,
                                  primary_attribute=s_primary,
                                  secondary_attribute=s_secondary)
                new_skill.save()
        print "COMPLETED SKILL IMPORT"
