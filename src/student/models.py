from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.urls import reverse
import shutil
from django.core.files.storage import FileSystemStorage
from django.core.validators import RegexValidator
from django.contrib.admin.widgets import AdminDateWidget
from django.db.models.signals import pre_save, post_save
from variables.models import Country, Level_Expertise, Region


# def image_upload_to(instance, filename):
# 	student_name = instance.user
# 	student_id = instance.id
# 	basename, file_extension = filename.split(".")
# 	new_filename = "%s-%s.%s" %(basename, student_id, file_extension)
# 	olddir = "%s/student_sub/%s/img" %(settings.MEDIA_ROOT, student_id)
# 	shutil.rmtree(olddir, ignore_errors=True)
# 	return "student_sub/%s/img/%s" %(student_id, new_filename)

# def doc_upload_to1(instance, filename):
# 	student_name = instance.user
# 	student_id = instance.id
# 	basename, file_extension = filename.split(".")
# 	new_filename = "%s-%s.%s" %(basename, student_id, file_extension)
# 	olddir = "%s/student_sub/%s/docs1" %(settings.MEDIA_ROOT, student_id)
# 	shutil.rmtree(olddir, ignore_errors=True)
# 	return "student_sub/%s/docs1/%s" %(student_id, new_filename)

function = (
	('Student', 'Student'),
	('Teacher', 'Teacher')
)

class Student(models.Model):
	phone_regex = RegexValidator(regex=r'^\d{4}-\d{4}$', message="Phone number must be entered in the format: 'XXXX-XXXX'.")
	# phone_regex = RegexValidator(regex=r'^\d{8}$', message="Phone number must be entered in the format: 'XXXXXXX'.")

	function = models.CharField(max_length=20, null=True, blank=True)
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=60)
	last_name = models.CharField(max_length=60)
	contact = models.CharField(max_length=20,validators=[phone_regex], blank=False, null=False) # validators should be a list

	# street = models.CharField(max_length=120, null=True, blank=True)
	# city = models.CharField(max_length=120, null=True, blank=True)
	# state = models.CharField(max_length=120, null=True, blank=True)
	# zipcode = models.CharField(max_length=120, null=True, blank=True)
	# country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)

	parent = models.BooleanField(default=False)
	postal_code = models.CharField(max_length=6, null=True, blank=True)
	region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	
	
	# image = models.ImageField(blank=True, null=True, upload_to=image_upload_to)
	# doc1 = models.ImageField(blank=True, null=True, upload_to=doc_upload_to1)

	def get_absolute_url(self):
		return reverse('StudentDetail', kwargs={'pk': self.pk})

	def get_update(self):
		return reverse('StudentUpdate', kwargs={'pk': self.pk})

	def __str__(self):
		return str(self.user.username)

	def test(self):
		test = self.id
		# test = settings.TEST
		return test


def student_post_save_receiver(sender, instance, *args, **kwargs):
	if not instance.function:
		instance.function = 'Student'

post_save.connect(student_post_save_receiver, sender=Student)

