from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from questionnaire.models import Region, Country, UserProfile


class UserProfileForm(UserCreationForm):
    region = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label=None)
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label=None)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['password2'].label = 'Confirm Password'

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email", "groups")

    def save(self, commit=True, *args, **kwargs):
        user = super(UserProfileForm, self).save(commit=commit, *args, **kwargs)
        if commit:
            self.save_m2m()
            user_profile, b = UserProfile.objects.get_or_create(user=user)
            user_profile.region = self.cleaned_data['region']
            user_profile.country = self.cleaned_data['country']
            user_profile.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        return self._clean_attribute(User, email=email)

    def clean_username(self):
        username = self.cleaned_data['username']
        return self._clean_attribute(User, username=username)

    def clean_country(self):
        country = self.cleaned_data['country']
        region = self.cleaned_data['region']
        if country not in region.countries.all():
            del self.cleaned_data['country']
            message = "%s does not belong to region %s" % (country.name, region.name)
            self._errors['country'] = self.error_class([message])
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