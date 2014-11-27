from django.contrib.auth.models import User
from django.db import models

from questionnaire.models.base import BaseModel


class UserProfile(BaseModel):
    user = models.OneToOneField(User, related_name="user_profile")
    region = models.ForeignKey("Region", blank=True, null=True)
    country = models.ForeignKey("Country", blank=True, null=True)
    organization = models.ForeignKey("Organization", blank=True, null=True)

    def is_global_admin(self):
        return self.region == None

    def can_delete(self, obj):
        return (not self. region and obj.is_core) or (self.region and self.region == obj.region and not obj.is_core)