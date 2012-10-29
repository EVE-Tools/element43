from django.conf import settings
from apps.common.util import validate_characters, calculate_character_access_mask


def element43_settings(request):
    """
    Adds element43 specific settings and characters with certain permissions to the context.
    """

    # Wallet / Journal chars
    # Check if user is authenticated, if not - just use context without characters
    try:
        if request.user.is_authenticated:
            journal_chars = validate_characters(request.user, calculate_character_access_mask(['WalletJournal']))
            transaction_chars = validate_characters(request.user, calculate_character_access_mask(['WalletTransactions']))
    except TypeError:
        return {'IMAGE_SERVER': settings.IMAGE_SERVER}

    return {'IMAGE_SERVER': settings.IMAGE_SERVER, 'characters_journal': journal_chars, 'characters_transaction': transaction_chars}
