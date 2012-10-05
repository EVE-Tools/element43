# Utility imports
import datetime
from celery.task.schedules import crontab
from celery.task import PeriodicTask, Task

# API Models
from apps.api.models import SkillGroup, Skill

# API
from element43 import eveapi

class ProcessAPISkillTree(PeriodicTask):
    """
    Grab the skill list, iterate it and store to DB
    """
    
    # for testing, run every 5 mins
    run_every = datetime.timedelta(minutes=5)

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
                    published = True;
                else:
                    published = False;
                new_skill = Skill(id=skill.typeID,
                                  name=skill.typeName,
                                  group = new_group,
                                  published = published,
                                  description = skill.description,
                                  rank = skill.rank,
                                  primary_attribute = s_primary,
                                  secondary_attribute = s_secondary)
                new_skill.save()
        print "COMPLETED SKILL IMPORT"