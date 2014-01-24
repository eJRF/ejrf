from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView
from questionnaire.forms.user_profile import UserProfileForm


class UsersList(ListView):

    def __init__(self, **kwargs):
        super(UsersList, self).__init__(**kwargs)
        self.template_name = 'users/index.html'
        self.model = User
        self.object_list = self.get_queryset()

    def get(self, *args, **kwargs):
        context = {'request': self.request, 'users': self.object_list}
        return self.render_to_response(context)

    def get_queryset(self):
        return self.model.objects.order_by('user_profile__created')


class CreateUser(CreateView):

    def __init__(self, **kwargs):
        super(CreateUser, self).__init__(**kwargs)
        self.form_class = UserProfileForm
        self.object = User
        self.template_name = "users/new.html"
        self.success_url = reverse('list_users_page')

    def form_valid(self, form):
        messages.success(self.request, "User created successfully.")
        return super(CreateUser, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateUser, self).get_context_data(**kwargs)
        context.update({'btn_label': "Create", 'title': "Add new user"})
        return context