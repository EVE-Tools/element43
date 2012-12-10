# Utility imports
import datetime
import pytz

from celery.task import PeriodicTask
from celery.task.schedules import crontab

from apps.common.util import cast_empty_string_to_int, cast_empty_string_to_float

# Models
from eve_db.models import StaStation
from apps.market_data.models import Orders
from apps.api.models import *

# API
from element43 import eveapi

# API error handling
from apps.api.api_exceptions import handle_api_exception

# Additional exception handling
from django.db import IntegrityError

class ProcessResearch(PeriodicTask):
    """
    Updates the research agents for all characters.
    """

    run_every = datetime.timedelta(minutes=5)

    def run(self, **kwargs):
        print 'UPDATING RESEARCH AGENTS'

        api = eveapi.EVEAPIConnection()

        update_timers = APITimer.objects.filter(apisheet="Research",
                                                nextupdate__lte=pytz.utc.localize(datetime.datetime.utcnow()))

        for update in update_timers:

            character = Character.objects.get(id=update.character_id)
            print ">>> Updating research agents for %s" % character.name

            # Try to fetch a valid key from DB
            try:
                apikey = APIKey.objects.get(id=character.apikey_id, is_valid=True)
            except APIKey.DoesNotExist:
                print('There is no valid key for %s.' % character.name)
                # End execution for this character
                continue

            # Try to authenticate and handle exceptions properly
            try:
                auth = api.auth(keyID=apikey.keyid, vCode=apikey.vcode)
                me = auth.character(character.id)

                # Get newest page - use maximum row count to minimize amount of requests
                sheet = me.Research()

            except eveapi.Error, e:
                handle_api_exception(e, apikey)

            # Clear all existing jobs for this character and add new ones. We don't want to keep expired data.
            Research.objects.filter(character=character).delete()

            for job in sheet.research:
                new_job = Research(character=character,
                                   agent_id=job.agentID,
                                   skill_id=job.skillTypeID,
                                   start_date=pytz.utc.localize(datetime.datetime.utcfromtimestamp(job.researchStartDate)),
                                   points_per_day=job.pointsPerDay,
                                   remainder_points=job.remainderPoints)
                new_job.save()

            # Update timer
            timer = APITimer.objects.get(character=character, apisheet='Research')
            timer.nextupdate = pytz.utc.localize(datetime.datetime.utcfromtimestamp(sheet._meta.cachedUntil))
            timer.save()

            print "<<<  %s's research import was completed successfully." % character.name


class ProcessWalletTransactions(PeriodicTask):
    """
    Processes char/corp wallet transactions.
    TODO: Add corp key handling.
    """

    run_every = datetime.timedelta(minutes=5)

    def run(self, **kwargs):
        print 'UPDATING TRANSACTIONS'

        api = eveapi.EVEAPIConnection()

        update_timers = APITimer.objects.filter(apisheet="WalletTransactions",
                                                nextupdate__lte=pytz.utc.localize(datetime.datetime.utcnow()))

        for update in update_timers:

            character = Character.objects.get(id=update.character_id)
            print ">>> Updating transactions for %s" % character.name

            # Try to fetch a valid key from DB
            try:
                apikey = APIKey.objects.get(id=character.apikey_id, is_valid=True)
            except APIKey.DoesNotExist:
                print('There is no valid key for %s.' % character.name)
                # End execution for this character
                continue

            # Try to authenticate and handle exceptions properly
            try:
                auth = api.auth(keyID=apikey.keyid, vCode=apikey.vcode)
                me = auth.character(character.id)

                # Get newest page - use maximum row count to minimize amount of requests
                sheet = me.WalletTransactions(rowCount=2560)

            except eveapi.Error, e:
                handle_api_exception(e, apikey)

            walking = True

            while walking:

                # Check if new set contains any entries
                if len(sheet.transactions):

                    # Process transactions
                    for transaction in sheet.transactions:

                        try:
                            MarketTransaction.objects.get(journal_transaction_id=transaction.journalTransactionID, character=character)
                            # If there already is an entry with this id, we can stop walking.
                            # So we don't walk all the way back every single time we run this task.
                            walking = False

                        except MarketTransaction.DoesNotExist:

                            try:
                                # If it does not exist, create transaction
                                entry = MarketTransaction(character=character,
                                                          date=pytz.utc.localize(datetime.datetime.utcfromtimestamp(transaction.transactionDateTime)),
                                                          transaction_id=transaction.transactionID,
                                                          invtype_id=transaction.typeID,
                                                          quantity=transaction.quantity,
                                                          price=transaction.price,
                                                          client_id=transaction.clientID,
                                                          client_name=transaction.clientName,
                                                          station_id=transaction.stationID,
                                                          is_bid=(transaction.transactionType == 'buy'),
                                                          journal_transaction_id=transaction.journalTransactionID)
                                entry.save()

                            # Catch integrity errors if
                            except IntegrityError:
                                print 'IntegrityError: Probably the SDE is outdated. typeID: %d, transactionID: %d' % (transaction.typeID, transaction.journalTransactionID)
                                continue

                    # Fetch next page if we're still walking
                    if walking:
                        # Get next page based on oldest id in db - use maximum row count to minimize amount of requests
                        oldest_id = MarketTransaction.objects.filter(character=character).order_by('date')[:1][0].journal_transaction_id
                        sheet = me.WalletTransactions(rowCount=2560, fromID=oldest_id)

                else:
                    walking = False

            # Update timer
            timer = APITimer.objects.get(character=character, apisheet='WalletTransactions')
            timer.nextupdate = pytz.utc.localize(datetime.datetime.utcfromtimestamp(sheet._meta.cachedUntil))
            timer.save()

            print "<<<  %s's transaction import was completed successfully." % character.name


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
                # End execution for this character
                continue

            # Try to authenticate and handle exceptions properly
            try:
                auth = api.auth(keyID=apikey.keyid, vCode=apikey.vcode)
                me = auth.character(character.id)

                # Get newest page - use maximum row count to minimize amount of requests
                sheet = me.WalletJournal(rowCount=2560)

            except eveapi.Error, e:
                handle_api_exception(e, apikey)

            walking = True

            while walking:

                # Check if new set contains any entries
                if len(sheet.transactions):

                    # Process journal entries
                    for transaction in sheet.transactions:

                        try:
                            JournalEntry.objects.get(ref_id=transaction.refID, character=character)
                            # If there already is an entry with this id, we can stop walking.
                            # So we don't walk all the way back every single time we run this task.
                            walking = False

                        except JournalEntry.DoesNotExist:

                            # Add entry to DB
                            entry = JournalEntry(ref_id=transaction.refID,
                                                 character=character,
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

                        # If we somehow got the same transaction multiple times in our DB, remove the redundant ones
                        except JournalEntry.MultipleObjectsReturned:
                            # Remove all duplicate items except for one
                            duplicates = JournalEntry.objects.filter(ref_id=transaction.refID, character=character)

                            for duplicate in duplicates[1:]:
                                print 'Removing duplicate JournalEntry with ID: %d (refID: %d)' % (duplicate.id, duplicate.ref_id)
                                duplicate.delete()


                    # Fetch next page if we're still walking
                    if walking:
                        # Get next page based on oldest id in db - use maximum row count to minimize number of requests
                        oldest_id = JournalEntry.objects.filter(character=character).order_by('date')[:1][0].ref_id
                        sheet = me.WalletJournal(rowCount=2560, fromID=oldest_id)

                else:
                    walking = False

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
                # End execution for this character
                continue

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
    Currently done once every 5 minutes
    """

    run_every = datetime.timedelta(minutes=5)

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
                # End execution for this character
                continue

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
