from braces.views import PermissionRequiredMixin
from django.http import HttpResponse
from django.core import serializers
from django.views.generic import View

from questionnaire.models import Theme


class ThemeAPIView(PermissionRequiredMixin, View):
    permission_required = 'auth.can_edit_questionnaire'
    template_name = 'questions/index.html'
    model = Theme

    def get(self, request, *args, **kwargs):
        data = Theme.objects.filter(region=request.user.user_profile.region)
        serialized_data = serializers.serialize('json', data)
        return HttpResponse(serialized_data, content_type="application/json")

