from django.db import models

#
# Newsfeed
#


class Feed(models.Model):
    """
    Holds information about a news-feed which gets updated regularly by a Celery task.
    """

    url = models.URLField(help_text='Newsfeed URL')
    name = models.CharField(help_text='Name of the feed', max_length=100)
    icon_file = models.CharField(help_text="Name of the feed's icon file", max_length=100)
    next_update = models.DateTimeField(help_text='Timestamp for next update')

    class Meta(object):
        verbose_name = "Newsfeed"
        verbose_name_plural = "Newsfeeds"


#
# News Item
#


class FeedItem(models.Model):
    """
    Holds information about a news item in a news-feed.
    """

    feed = models.ForeignKey('feedreader.Feed', help_text='FKey relationship to feed table')
    title = models.CharField(help_text='Title of the item', max_length=100)
    description = models.TextField(help_text='Short description of the item')
    link = models.URLField(help_text='Link to the text')
    published = models.DateTimeField(help_text='Time the item was published')


    class Meta(object):
        verbose_name = "Feed Item"
        verbose_name_plural = "Feed Items"

