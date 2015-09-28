# Settings and e-mail
from django.conf import settings
from django.template import Context
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

import eveapi

from apps.api.models import APIKey

#
# Offers general purpose API exception handling for celery eveapi tasks
#


def handle_api_exception(exception, key):
    """
    Handles API exceptions.
    Usage:

        try:
            *some api stuff*

        except eveapi.Error, e:
            handle_api_exception(e, key)

        # If you want you can also catch other stuff
        except Exception, e:
            *custom exception handling*
            raise

    """

    # Handle different exceptions - currently only invalid keys are being handled
    if isinstance(exception, eveapi.AuthenticationError):

        # Reload key to avoid deactivating the same key several times at once,
        # since multiple tasks using the same key can run at the same time.

        key = APIKey.objects.get(id=key.id)

        if key.is_valid is True:

            print("AUTHENTICATION ERROR FOR KEY " + str(key.id) + " - INVALIDATING KEY AND SENDING NOTIFICATION TO USER!")

            # Invalidate key
            key.is_valid = False
            key.save()

            # Send mail to user
            text = get_template('mail/invalid_key.txt')
            html = get_template('mail/invalid_key.haml')

            mail_context = Context({'username': key.user.username, 'key_id': key.keyid})

            text_content = text.render(mail_context)
            html_content = html.render(mail_context)

            message = EmailMultiAlternatives('Element43 - One of your API keys has been invalidated!',
                                             text_content, settings.DEFAULT_FROM_EMAIL,
                                             [key.user.email])

            message.attach_alternative(html_content, "text/html")
            message.send()

        return

    elif isinstance(exception, eveapi.RequestError):
        raise exception

    elif isinstance(exception, eveapi.ServerError):
        raise exception

    else:
        print("EVEAPI ERROR!")
        raise exception
