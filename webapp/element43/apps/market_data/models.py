from django.db import models

class UUDIFMessage(models.Model):
    """
    A raw JSON UUDIF market message. This is typically only used on local
    development workstations.
    """

    key = models.CharField(max_length=255, unique=True,
        help_text="I'm assuming this is a unique hash for the message.")
    received_dtime = models.DateTimeField(auto_now_add=True,
        help_text="Time of initial receiving.")
    is_order = models.BooleanField(
        help_text="If True, this is an order. If False, this is history.")
    message = models.TextField(
        help_text="Full JSON representation of the message.")


    class Meta(object):
        verbose_name = "UUDIF Message"
        verbose_name_plural = "UUDIF Messages"