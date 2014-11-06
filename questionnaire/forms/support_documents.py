import os

from django.core.exceptions import ValidationError
from django import forms

from eJRF.settings import ACCEPTED_EXTENSIONS
from questionnaire.models import SupportDocument


class SupportDocumentUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SupportDocumentUploadForm, self).__init__(*args, **kwargs)
        self.fields['path'].label = 'Support document'

    class Meta:
        model = SupportDocument
        fields = ['questionnaire', 'path', 'country']
        widgets = {'questionnaire': forms.HiddenInput(), 'country': forms.HiddenInput()}

    def clean_path(self):
        _file = self.cleaned_data['path']
        name, extension = os.path.splitext(str(_file))
        if extension.lower() not in ACCEPTED_EXTENSIONS:
            raise ValidationError('%s file type is not an allowed, Please upload %s files only' % (
            extension, ', '.join(ACCEPTED_EXTENSIONS)))
        return _file