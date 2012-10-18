# Utility imports
import datetime
import pytz

# Template and context-related imports
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# API Models
from apps.api.models import APIKey, Character, CharSkill, APITimer

# Forms
from apps.user_settings.forms import ProfileForm, APIKeyForm

# API
from element43 import eveapi

# Char management utilities
from apps.common.util import manage_character_api_timers


@login_required
def settings(request):
    rcontext = RequestContext(request, {})
    return render_to_response('settings/settings.haml', rcontext)


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request=request)
        if form.is_valid():

            # Change email
            if form.cleaned_data.get('email'):
                request.user.email = form.cleaned_data.get('email')

            # Change Password
            if form.cleaned_data.get('new_password'):
                request.user.set_password(form.cleaned_data.get('new_password'))

            request.user.save()

            # Add success message
            messages.success(request, 'Saved new profile data.')
            # Redirect home
            return HttpResponseRedirect(reverse('settings'))
    else:
        form = ProfileForm(request=request)

    rcontext = RequestContext(request, {})
    return render_to_response('settings/settings.haml', {'form': form}, rcontext)


@login_required
def characters(request):
    characters = Character.objects.filter(user=request.user)

    if not characters:
        # Message and redirect
        messages.info(request, 'Currently there are no characters associated with your account. You need to add them via an API key first.')
        return HttpResponseRedirect(reverse('manage_api_keys'))

    rcontext = RequestContext(request, {'characters': characters})
    return render_to_response('settings/characters.haml', rcontext)


@login_required
def remove_character(request, char_id):
    try:
        # Delete only matching character to prevent unauthorized deletions
        char = Character.objects.get(user=request.user, id=char_id)
        char.delete()
    except:
        # Message and redirect
        messages.error(request, 'There is no such character.')
        return HttpResponseRedirect(reverse('manage_characters'))

    # Message and redirect
    messages.info(request, 'Character was removed.')
    return HttpResponseRedirect(reverse('manage_characters'))


@login_required
def api_key(request):
    # Get Keys
    char_keys = APIKey.objects.filter(user=request.user, is_character_key=True)
    corp_keys = APIKey.objects.filter(user=request.user, is_character_key=False)

    # Form
    if request.method == 'POST':
        form = APIKeyForm(request.POST)
        if form.is_valid():

            # Add success message
            messages.success(request, 'Your key is valid.')
            # Redirect home
            return HttpResponseRedirect(reverse('add_characters', kwargs={'api_id': form.cleaned_data.get('api_id'),
                                                                          'api_verification_code': form.cleaned_data.get('api_verification_code')}))
    else:
        form = APIKeyForm()

    rcontext = RequestContext(request, {})
    return render_to_response('settings/api_key.haml', {'form': form, 'char_keys': char_keys, 'corp_keys': corp_keys}, rcontext)


@login_required
def remove_api_key(request, apikey_id):
    try:
        # Delete only matching character to prevent unauthorized deletions
        key = APIKey.objects.get(user=request.user, keyid=apikey_id)
        is_character_key = key.is_character_key
        key.delete()
    except:
        # Message and redirect
        messages.error(request, 'There is no such key.')
        return HttpResponseRedirect(reverse('manage_api_keys'))

    # Message and redirect
    if is_character_key:
        messages.info(request, 'The key and all associated characters were removed.')
    else:
        messages.info(request, 'The key was removed.')

    return HttpResponseRedirect(reverse('manage_api_keys'))


@login_required
def api_character(request, api_id, api_verification_code):

    """
    Validate key / ID combination. If it's valid, check security bitmask.
    """

    # Try to authenticate with supplied key / ID pair and fetch api key meta data.
    try:
        # Fetch info
        api = eveapi.EVEAPIConnection()
        auth = api.auth(keyID=api_id, vCode=api_verification_code)
        key_info = auth.account.APIKeyInfo()
    except:
        # Message and redirect
        messages.error(request, """Verification of your API key failed.
                                   Please follow the instructions on the right half of this page to generate a valid one.""")
        return HttpResponseRedirect(reverse('manage_api_keys'))

    if key_info.key.type == "Character" or key_info.key.type == "Account":

        # Now check the access mask
        min_access_mask = 8

        # attributes & implants
        implant = {}
        i_stats = {}
        attributes = ['memory', 'intelligence', 'perception', 'willpower', 'charisma']

        # Do a simple bitwise operation to determine if we have sufficient rights with this key.
        if not ((min_access_mask & key_info.key.accessMask) == min_access_mask):
            # Message and redirect
            messages.error(request, """The API key you supplied does not have sufficient rights.
                                       Please follow the instructions on the right half of this page to generate a valid one.""")
            return HttpResponseRedirect(reverse('manage_api_keys'))

        # Get characters associated with this key
        characters = auth.account.Characters().characters

        # If form is submitted, add characters to account
        if request.method == 'POST':
            post_characters = request.POST.getlist('characters')

            added_chars = False

            for char in characters:
                if str(char.characterID) in post_characters:
                    # Add key to DB if it does not exist
                    if not APIKey.objects.filter(keyid=api_id, vcode=api_verification_code):

                        # Handle keys which never expire
                        try:
                            key_expiration = datetime.datetime.fromtimestamp(key_info.key.expires)
                        except:
                            key_expiration = "9999-12-31 00:00:00"

                        key = APIKey(user=request.user,
                                     keyid=api_id,
                                     vcode=api_verification_code,
                                     expires=key_expiration,
                                     accessmask=key_info.key.accessMask,
                                     is_valid=True,
                                     is_character_key=True)

                        key.save()

                    else:
                        key = APIKey.objects.get(user=request.user, keyid=api_id, vcode=api_verification_code)

                    # If char already is assigned to another key, just move it
                    try:
                        char_to_move = Character.objects.get(id=char.characterID, user=request.user)
                        char_to_move.apikey_id = key.id
                        char_to_move.save()

                        # Update timers
                        manage_character_api_timers(char_to_move)

                        added_chars = True

                    except Character.DoesNotExist:
                        # Add character
                        me = auth.character(char.characterID)
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
                            a_name = sheet.allianceName
                            a_id = sheet.allianceID

                        except:
                            a_name = ""
                            a_id = 0

                        new_char = Character(id=char.characterID,
                                            name=char.name,
                                            user=request.user,
                                            apikey=key,
                                            corp_name=sheet.corporationName,
                                            corp_id=sheet.corporationID,
                                            alliance_name=a_name,
                                            alliance_id=a_id,
                                            dob=pytz.utc.localize(datetime.datetime.utcfromtimestamp(sheet.DoB)),
                                            race=sheet.race,
                                            bloodline=sheet.bloodLine,
                                            ancestry=sheet.ancestry,
                                            gender=sheet.gender,
                                            clone_name=sheet.cloneName,
                                            clone_skill_points=sheet.cloneSkillPoints,
                                            balance=sheet.balance,
                                            implant_memory_name=implant['memory']['name'],
                                            implant_memory_bonus=implant['memory']['value'],
                                            implant_perception_name=implant['perception']['name'],
                                            implant_perception_bonus=implant['perception']['value'],
                                            implant_intelligence_name=implant['intelligence']['name'],
                                            implant_intelligence_bonus=implant['intelligence']['value'],
                                            implant_willpower_name=implant['willpower']['name'],
                                            implant_willpower_bonus=implant['willpower']['value'],
                                            implant_charisma_name=implant['charisma']['name'],
                                            implant_charisma_bonus=implant['charisma']['value'])
                        new_char.save()

                        new_apitimer = APITimer(character=new_char,
                                                corporation=None,
                                                apisheet="CharacterSheet",
                                                nextupdate=pytz.utc.localize(datetime.datetime.utcfromtimestamp(sheet._meta.cachedUntil)))
                        new_apitimer.save()

                        # Update other timers
                        manage_character_api_timers(new_char)

                        for skill in sheet.skills:
                            new_skill = CharSkill(character=new_char,
                                                  skill_id=skill.typeID,
                                                  skillpoints=skill.skillpoints,
                                                  level=skill.level)
                            new_skill.save()

                        added_chars = True

            # Change message depending on what we did
            if added_chars:
                messages.success(request, "Successfully added the selected character(s) to your account.")
            else:
                messages.info(request, "No characters were added.")
            return HttpResponseRedirect(reverse('manage_characters'))

    else:
        # This must be a corporation key then
        # Add key to DB if it does not exist
        if not APIKey.objects.filter(keyid=api_id, vcode=api_verification_code):

            # Handle keys which never expire
            try:
                key_expiration = datetime.datetime.fromtimestamp(key_info.key.expires)
            except:
                key_expiration = "9999-12-31 00:00:00"

            key = APIKey(user=request.user,
                         keyid=api_id,
                         vcode=api_verification_code,
                         expires=key_expiration,
                         accessmask=key_info.key.accessMask,
                         is_valid=True,
                         is_character_key=False)

            key.save()

            messages.success(request, "Successfully added your corporate key.")

        else:
            messages.info(request, "No keys were added.")

        return HttpResponseRedirect(reverse('manage_api_keys'))

    rcontext = RequestContext(request, {'chars': characters})
    return render_to_response('settings/api_character.haml', rcontext)
