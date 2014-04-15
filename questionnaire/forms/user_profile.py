from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms
from django.forms import ModelForm
from questionnaire.models import Region, Country, UserProfile, Organization


class UserProfileForm(UserCreationForm):
    groups = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label=None, required=True,
                                    widget=forms.RadioSelect(attrs={'class': 'radio-roles'}), label="Roles")
    organization = forms.ModelChoiceField(queryset=Organization.objects.all(), empty_label="Choose an Organization", required=False)
    region = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label="Choose a Region", required=False)

    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="Choose a County", required=False,
                                     )

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['password2'].label = 'Confirm Password'
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")

    def save(self, commit=True, *args, **kwargs):
        user = super(UserProfileForm, self).save(commit=commit, *args, **kwargs)
        if commit:
            user.groups.add(self.cleaned_data['groups'])
            user.save()
            self.save_m2m()
            user_profile, b = UserProfile.objects.get_or_create(user=user)
            user_profile.region = self.cleaned_data['region']
            user_profile.country = self.cleaned_data['country']
            user_profile.organization = self.cleaned_data['organization']
            user_profile.save()
        return user

    def _check_regional_admin(self, message):
        organization = self.cleaned_data.get('organization', None)
        region = self.cleaned_data.get('region', None)
        if not organization:
            self._errors['organization'] = self.error_class([message])
        if not region:
            self._errors['region'] = self.error_class([message])

    def _check_global_admin(self, message):
        organization = self.cleaned_data.get('organization', None)
        if not organization:
            self._errors['organization'] = self.error_class([message])

    def _check_country_admin(self, message):
        country = self.cleaned_data.get('country', None)
        if not country:
            self._errors['country'] = self.error_class([message])

    def clean(self):
        group = self.cleaned_data.get('groups', None)
        message = "This field is required."
        if not group:
            self._errors['groups'] = self.error_class([message])
        elif group.name == 'Regional Admin':
            self._check_regional_admin(message)
        elif group.name == 'Global Admin':
            self._check_global_admin(message)
        else:
            self._check_country_admin(message)
        return super(UserProfileForm, self).clean()

    def clean_email(self):
        email = self.cleaned_data['email']
        return self._clean_attribute(User, email=email)

    def clean_username(self):
        username = self.cleaned_data['username']
        return self._clean_attribute(User, username=username)

    def clean_country(self):
        country = self.cleaned_data.get('country', None)
        region = self.cleaned_data.get('region', None)
        if (country is not None and region is not None) and country not in region.countries.all():
            message = "%s does not belong to region %s" % (country.name, region.name)
            self._add_error_country_messages(message)
        return country

    def _clean_attribute(self, _class, **kwargs):
        attribute_name = kwargs.keys()[0]
        data_attr = kwargs[attribute_name]
        users_with_same_attr = _class.objects.filter(**kwargs)
        if users_with_same_attr and self.initial.get(attribute_name, None) != str(data_attr):
            message = "%s is already associated to a different user." % data_attr
            self._errors[attribute_name] = self.error_class([message])
            del self.cleaned_data[attribute_name]
        return data_attr

    def _add_error_country_messages(self, message):
        del self.cleaned_data['country']
        self._errors['country'] = self.error_class([message])


class EditUserProfileForm(ModelForm):

    class Meta:
        model = User
        fields = ("username", "email", "is_active")

    def __init__(self, *args, **kwargs):
        super(EditUserProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data['email']
        return self._clean_attribute(User, email=email)

    def clean_username(self):
        username = self.cleaned_data['username']
        return self._clean_attribute(User, username=username)

    def _clean_attribute(self, _class, **kwargs):
        attribute_name = kwargs.keys()[0]
        data_attr = kwargs[attribute_name]
        users_with_same_attr = _class.objects.filter(**kwargs)
        if users_with_same_attr and self.initial.get(attribute_name, None) != str(data_attr):
            message = "%s is already associated to a different user." % data_attr
            self._errors[attribute_name] = self.error_class([message])
            del self.cleaned_data[attribute_name]
        return data_attr