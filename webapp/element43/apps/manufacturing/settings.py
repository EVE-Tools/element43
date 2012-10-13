from django.conf import settings

MANUFACTURING_MAX_BLUEPRINT_HISTORY = getattr(settings,
                                              'MANUFACTURING_MAX_BLUEPRINT_HISTORY',
                                              10)

MANUFACTURING_BLUEPRINT_HISTORY_SESSION = getattr(settings,
                                                  'MANUFACTURING_MAX_BLUEPRINT_HISTORY',
                                                  'manufacturing_blueprint_history')
