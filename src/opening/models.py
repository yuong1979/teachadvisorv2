from __future__ import unicode_literals
from student.models import Student
from variables.models import Country, Educational_Level, Subject_Expertise, Level_Expertise, Region
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.files.storage import FileSystemStorage
from django.core.validators import RegexValidator
from django.contrib.admin.widgets import AdminDateWidget

class Opening(models.Model):

	hiring_student = models.ForeignKey(Student, on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	title = models.CharField(max_length=60)
	subject = models.ForeignKey(Subject_Expertise, on_delete=models.CASCADE)
	level = models.ForeignKey(Level_Expertise, on_delete=models.CASCADE)
	description = models.TextField(null=True, blank=True)
	salary_range = models.DecimalField(decimal_places=0, max_digits=3, null=True, blank=True)
	negotiable = models.BooleanField(default=False)
	# country = models.ForeignKey(Country, on_delete=models.CASCADE)
	region = models.ForeignKey(Region, on_delete=models.CASCADE)
	job_active = models.BooleanField(default=True)
	group_tuition = models.BooleanField(default=False)
	private = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	date_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
	
	trial_acc = models.BooleanField(default=False)

	def get_absolute_url(self):
		return reverse('OpeningDetail', kwargs={'pk': self.pk})

	def get_update(self):
		return reverse('OpeningUpdate', kwargs={'pk': self.pk})

	def get_subject_type(self):
		test = self.hiring_student.subject
		return test

	def __unicode__(self):
		return self.title