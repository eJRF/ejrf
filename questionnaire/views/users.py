from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView
from questionnaire.forms.filter import UserFilterForm
from questionnaire.forms.user_profile import UserProfileForm
from questionnaire.models import Organization, Region, Country

FORM_FIELD_QUERY_FIELD = {'region': 'user_profile__region', 'role': 'groups',
                          'organization': 'user_profile__organization'}


class UsersList(LoginRequiredMixin, ListView):

    def __init__(self, **kwargs):
        super(UsersList, self).__init__(**kwargs)
        self.template_name = 'users/index.html'
        self.model = User
        self.object_list = self.get_queryset()

    def get(self, *args, **kwargs):
        context = {'request': self.request, 'users': self.object_list, 'filter_form': UserFilterForm()}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = UserFilterForm(request.POST)
        form.is_valid()
        if form.is_valid():
            filtered_users = self._query_for(request)
            context = {'request': self.request,
                       'users': filtered_users,
                       'filter_form': form}
            return self.render_to_response(context)
        return self.get(args, kwargs)

    def _query_for(self, request):
        post_request = request.POST.iteritems()
        query_params = dict((self._get_query_field(key), value) for key, value in post_request if value.strip() != '' and key in FORM_FIELD_QUERY_FIELD.keys())
        return self.object_list.filter(**query_params)

    @staticmethod
    def _get_query_field(_key):
        return FORM_FIELD_QUERY_FIELD.get(_key)

    def get_queryset(self):
        return self.model.objects.order_by('user_profile__created')


class CreateUser(LoginRequiredMixin, CreateView):

    def __init__(self, **kwargs):
        super(CreateUser, self).__init__(**kwargs)
        self.form_class = UserProfileForm
        self.object = User
        self.template_name = "users/new.html"
        self.success_url = reverse('list_users_page')

    def form_valid(self, form):
        messages.success(self.request, "%s created successfully." % form.cleaned_data['groups'])
        return super(CreateUser, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateUser, self).get_context_data(**kwargs)
        context_vars = {'btn_label': "CREATE",
                        'title': "Create new user",
                        'organizations': Organization.objects.all(),
                        'regions': Region.objects.all(),
                        'countries': Country.objects.all()}
        context.update(context_vars)
        return context