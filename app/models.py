from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db import models

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	class Meta:
		verbose_name_plural = 'User Profile'
	def __unicode__(self):
		return str(self.user)

class ScanResults(models.Model):
	ip = models.CharField(max_length=20)
	hostname = models.CharField(max_length=1000, null=True, blank=True)
	otherResults = models.CharField(max_length=1000, null=True, blank=True)
	def __unicode__(self):
		return str(self.ip)