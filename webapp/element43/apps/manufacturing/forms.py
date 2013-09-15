from django import forms
from eve_db.models import InvBlueprintType

from apps.api.models import Character, CharSkill, Skill

class SelectBlueprintForm(forms.Form):
    """
    Form to select the blueprint the user wants to manufacture.
    """
    blueprint = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control required form-control'}))

    def clean_blueprint(self):
        blueprint_name = self.cleaned_data['blueprint']

        if len(blueprint_name) < 3:
            raise forms.ValidationError("Blueprint name '%s' is too short!" % blueprint_name)

        # Look if there is at least one blueprint that goes by the name given by the user
        blueprints = InvBlueprintType.objects.filter(blueprint_type__name__icontains=blueprint_name)

        # If there are no items at all in the result then raise an ValidationError
        if len(blueprints) == 0:
            raise forms.ValidationError("Could not find blueprint '%s'" % blueprint_name)

        return blueprint_name


class ManufacturingCalculatorForm(forms.Form):
    """
    This is the form where the user types in the information for the manufacturing job. Based
    on those information the calculations will be made.
    """

    def __init__(self, user, *args, **kwargs):
        super(ManufacturingCalculatorForm, self).__init__(*args, **kwargs)
        self.has_character = False

        # If the user is logged in and has characters associated with his account set 'has_characters'
        # to True and add the characters as choices to the 'character' field. The 'has_characters'
        # field on the form will be used in the template to determine what part of the form has to
        # be rendered.
        if user and user.is_authenticated():
            characters = Character.objects.filter(user=user)
            if len(characters) > 0:
                self.has_character = True
                self.fields['character'].choices = [(character.id, character.name) for character in list(characters)]

                # When the 'character' field is displayed the other to fields are obsolete. Therefor
                # they are removed from the form. I consider this a 'hack'. If someone finds a better
                # way feel free to refactor this code. By removing the two fields cleaning/validation
                # gets a whole lot easier.
                # Note: Although the two fields are removed their values will be set. This will happen
                # in the 'clean' method (see below).
                del self.fields['skill_industry']
                del self.fields['skill_production_efficiency']
        else:
            # remove the characters field
            del self.fields['character']

    def clean(self):
        cleaned_data = super(ManufacturingCalculatorForm, self).clean()

        if self.has_character:
            # The fields 'skill_industry' and 'skill_production_efficiency' have to be set
            # here, since they were removed from the form and not displayed to the user.
            character_id = cleaned_data['character']

            # The following is meant for a rare edge case. When a user is logged out, types
            # in job parameters, calculates the job and returns to the job parameter form and
            # then logs in, an exception would occur. The reason being that cleander_data['character']
            # is supposed to hold the character id but doesn't, because it was not set when
            # the form first was send (user wasn't logged in at that time). But when the user
            # logged in, after sending the form, this form would init (see __init__) with the
            # 'has_character' flag set to true, hence reaching this point without a character
            # id. To solve the problem the first id in the fields choices will be selected.
            # The user will have to manually select the right character.
            if not character_id:
                characters = self.fields['character'].choices
                character_id = self.fields['character'].choices[0][0]

                # Character is not valid (yet) so better remove it from cleaned_data.
                del cleaned_data['character']

                # If there are more then one character, then the user has to be informed
                # that he has to select a character
                if len(characters) > 1:
                    # field error
                    field_error = u"Please select a character."
                    self._errors['character'] = self.error_class([field_error])

                    # form error
                    form_error = u"You logged in while you were filling out this form."
                    form_error+= u"Therefor you have to select one of your characters."
                    raise forms.ValidationError(form_error)

            character = Character.objects.get(pk=character_id)

            # Get the characters skill levels. If the character doesn't have the skills trained
            # no CharSkill instance will be returned for that skill. Therefor we have to do some
            # more checking.
            # 3380 = Industry
            # 3388 = Production Efficiency
            skills = CharSkill.objects.values('skill__id', 'level').filter(character=character, skill__id__in=(3380, 3388)).order_by('skill__id')

            # Not really pretty but works. Basically set skill levels to 0 and if the query found
            # skills for that character override the default levels.
            cleaned_data['skill_industry'] = 0
            cleaned_data['skill_production_efficiency'] = 0

            if skills:
                for skill in skills:
                    if skill['skill__id'] == 3380:
                        cleaned_data['skill_industry'] = skill['level']
                    elif skill['skill__id'] == 3388:
                        cleaned_data['skill_production_efficiency'] = skill['level']

        return cleaned_data

    SKILL_INDUSTRY_CHOICES = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )

    SKILL_PRODUCTION_EFFICIENCY_CHOICES = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )

    # (typeID, typeName)
    HARDWIRING_CHOICES = (
        (0, "No Hardwiring"),
        (27170, "Zainou 'Beancounter' Industry BX-801"),
        (27167, "Zainou 'Beancounter' Industry BX-802"),
        (27171, "Zainou 'Beancounter' Industry BX-804")
    )

    # blueprint related fields
    blueprint_material_efficiency = forms.IntegerField(min_value=-10,
                                                       max_value=1000,
                                                       initial=0,
                                                       widget=forms.TextInput(attrs={'class': 'form-control input-sm required'}))

    blueprint_production_efficiency = forms.IntegerField(min_value=-10,
                                                         max_value=1000,
                                                         initial=0,
                                                         widget=forms.TextInput(attrs={'class': 'form-control input-sm required'}))

    blueprint_runs = forms.IntegerField(min_value=0,
                                        max_value=10000,
                                        initial=1,
                                        widget=forms.TextInput(attrs={'class': 'form-control input-sm required'}))

    blueprint_price = forms.DecimalField(min_value=0,
                                         max_digits=32,
                                         decimal_places=2,
                                         initial=0,
                                         required=True,
                                         widget=forms.TextInput(attrs={'class': 'form-control input-sm required'}))

    # Player skill and item related fields
    #
    # Note about the fields 'character', 'skill_industry' and 'skill_production_efficiency':
    #
    # If the user is logged in and has characters added to his profile only the character
    # field will be displayed. If the user doesn't have characters associated with his
    # profile or is not logged in the fields 'skill_industry' and 'skill_production_efficiency'
    # will be displayed. Additionally, if the 'character' field is displayed it will be
    # dynamically initialized by the forms __init__ method (see above).
    character = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control required form-control'}))

    skill_industry = forms.ChoiceField(choices=SKILL_INDUSTRY_CHOICES,
                                       initial=5,
                                       required=True,
                                       widget=forms.Select(attrs={'class': 'form-control input-sm required'}))

    skill_production_efficiency = forms.ChoiceField(choices=SKILL_PRODUCTION_EFFICIENCY_CHOICES,
                                                    initial=5,
                                                    required=True,
                                                    widget=forms.Select(attrs={'class': 'form-control input-sm required'}))

    hardwiring = forms.ChoiceField(choices=HARDWIRING_CHOICES,
                                   required=True,
                                   widget=forms.Select(attrs={'class': 'form-control required form-control'}))

    # production slot fields
    slot_production_time_modifier = forms.FloatField(min_value=0,
                                                     max_value=10,
                                                     initial="1.00",
                                                     required=True,
                                                     widget=forms.TextInput(attrs={'class': 'form-control input-sm required'}))

    slot_material_modifier = forms.FloatField(min_value=0,
                                              max_value=10,
                                              initial="1.00",
                                              required=True,
                                              widget=forms.TextInput(attrs={'class': 'form-control input-sm required'}))

    # fields for calculating profit
    target_sell_price = forms.DecimalField(min_value=0,
                                           max_digits=32,
                                           decimal_places=2,
                                           initial="0",
                                           required=True,
                                           widget=forms.TextInput(attrs={'class': 'form-control input-sm required'}))

    brokers_fee = forms.DecimalField(min_value=0,
                                     max_value=10,
                                     decimal_places=2,
                                     initial="0.00",
                                     required=False,
                                     widget=forms.TextInput(attrs={'class': 'form-control input-sm required'}))

    sales_tax = forms.DecimalField(min_value=0,
                                   max_value=10,
                                   decimal_places=2,
                                   initial="0.00",
                                   required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control input-sm required'}))

    def clean_blueprint_runs(self):
        """
        Returns the cleaned value for the form field 'blueprint_runs'.
        If the given value is 0 it will be set to 1 automatically.
        """
        blueprint_runs = self.cleaned_data['blueprint_runs']

        if blueprint_runs == 0:
            self.cleaned_data['blueprint_runs'] = 1

        return blueprint_runs
