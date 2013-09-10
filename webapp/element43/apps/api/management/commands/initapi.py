from django.conf import settings
from django.core.management.base import BaseCommand

from element43.apps.api.tasks import ProcessAPISkillTree, ProcessRefTypes, ProcessConquerableStations

class Command(BaseCommand):
    help = 'Loads basic values from CCP\'s API into the database'

    def handle(self, *args, **options):
        self.stdout.write('Fetching skilltree...')
        ProcessAPISkillTree.apply()

        self.stdout.write('Fetching reference types...')
        ProcessRefTypes.apply()

        self.stdout.write('Fetching conquerable stations...')
        ProcessConquerableStations.apply()

        self.stdout.write('Done.')