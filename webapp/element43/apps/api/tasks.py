# Utility imports
import datetime
import pytz

from celery.task import PeriodicTask

# API Models
from apps.api.models import SkillGroup, Skill, APITimer, Character, APIKey, CharSkill

# API
from element43 import eveapi


class ProcessCharacterSheet(PeriodicTask):
    """
    Scan the db an refresh all character sheets
    Currently done once an hour
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

            apikey = APIKey.objects.get(id=character.apikey_id)
            auth = api.auth(keyID=apikey.keyid, vCode=apikey.vcode)
            me = auth.character(character.id)
            sheet = me.CharacterSheet()
            i_stats['name'] = ""
            i_stats['value'] = 0

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
                character.alliance_id = sheet_allianceID
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
            #character.cached_until = sheet.cachedUntil

            character.save()

            for skill in sheet.skills:
                try:
                    c_skill = CharSkill.objects.get(character=character.id, skill_id=skill.typeID)
                    c_skill.skillpoints = skill.skillpoints
                    c_skill.level = skill.level
                    c_skill.save()
                except:
                    new_skill = CharSkill(character=new_char,
                                          skill_id=skill.typeID,
                                          skillpoints=skill.skillpoints,
                                          level=skill.level)
                    new_skill.save()

            update.nextupdate = pytz.utc.localize(datetime.datetime.utcnow() + datetime.timedelta(hours=1))
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
