# Datetime Packages
from time import mktime
from datetime import timedelta
from datetime import datetime
import pytz

# Celery Imports
from celery.task import Task, PeriodicTask
from celery.utils.log import get_task_logger

# Feedparser
import feedparser

# Models
from models import Feed, FeedItem

# Logger object
LOGGER = get_task_logger(__name__)


class EnqueueFeedUpdates(PeriodicTask):
    """
    Updates the research agents for all characters.
    """

    # Run every minute
    run_every = timedelta(minutes=1)

    def run(self, **kwargs):

        # Get feeds that need to be updated
        feeds = Feed.objects.filter(next_update__lte=pytz.utc.localize(datetime.utcnow()))

        # Enqueue Tasks
        for feed in feeds:
            UpdateFeed.apply_async(args=[feed.id])


class UpdateFeed(Task):
    """
    Update a feed's items. Remove all old items from the DB.
    """

    def run(self, feed_id):

        # Get feed object
        feed = Feed.objects.get(id=feed_id)

        # Debug log
        LOGGER.debug("Updating feed %s", feed.name)

        # Set User-Agent header
        feedparser.USER_AGENT = "Element43Feedreader/Git +https://element-43.com/"

        # Fetch feed
        document = feedparser.parse(feed.url)

        if document.status == 200:
            # Remove all existing entries of that feed
            FeedItem.objects.filter(feed=feed).delete()

            # Add current content
            for item in document.entries:
                # Create item
                feed_item = FeedItem(feed=feed,
                                     title=item.title,
                                     description=item.summary,
                                     link=item.link,
                                     published=pytz.utc.localize(datetime.fromtimestamp(mktime(item.published_parsed))))

                # Save item to DB
                feed_item.save()

        else:
            # Log HTTP error
            LOGGER.warn("Error fetching feed %s - server returned status code %d .", feed.name, document.status)

        # Set next update to be 5 minutes from now
        five_minutes_from_now = datetime.utcnow() + timedelta(minutes=5)
        feed.next_update = pytz.utc.localize(five_minutes_from_now)
        feed.save()

        LOGGER.debug("Finished updating feed %s", feed.name)
