# Utility imports
import datetime
import pytz

# Celery
from celery.task import PeriodicTask
from celery.utils.log import get_task_logger

# User model
from django.contrib.auth.models import User

logger = get_task_logger(__name__)

class RemoveInactiveAccounts(PeriodicTask):
    """
    Removes accounts which haven't been activated in the last 48 hours.
    """

    run_every = datetime.timedelta(hours=1)

    def run(self, **kwargs):
        """
        Runs the task
        """

        logger.debug('Removing expired accounts.')

        expiration_time = pytz.utc.localize(datetime.datetime.utcnow() - datetime.timedelta(hours=48))

        accounts_to_delete = User.objects.filter(is_active=False, date_joined__lte=expiration_time)

        for account in accounts_to_delete:
            logger.info("Removed " + account.username)
            account.delete()
