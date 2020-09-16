from __future__ import unicode_literals
from billing.models import ImageSubscription
from variables.models import Country, Educational_Level, Education, Subject_Expertise, Level_Expertise, Region, Expertise_Type, Education_School
from django.db import models
from django.db.models import Avg, Max
from django.db.models.signals import pre_save, post_save
from django.core.files.storage import FileSystemStorage
from django.core.validators import RegexValidator
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.utils import timezone
import datetime
import shutil

def image_upload_to(instance, filename):
	teacher_name = instance.user
	# teacher_id = instance.id
	basename, file_extension = filename.split(".")
	new_filename = "%s-%s.%s" %(basename, teacher_name, file_extension)
	olddir = "%s/teacher_sub/%s/img" %(settings.MEDIA_ROOT, teacher_name)
	shutil.rmtree(olddir, ignore_errors=True)
	return "teacher_sub/%s/img/%s" %(teacher_name, new_filename)

def advimage_upload_to(instance, filename):
	teacher_name = instance.user
	# teacher_id = instance.id
	basename, file_extension = filename.split(".")
	new_filename = "%s-%s.%s" %(basename, teacher_name, file_extension)
	olddir = "%s/teacher_sub/%s/advimg" %(settings.MEDIA_ROOT, teacher_name)
	shutil.rmtree(olddir, ignore_errors=True)
	return "teacher_sub/%s/advimg/%s" %(teacher_name, new_filename)


def doc_upload_to1(instance, filename):
	teacher_name = instance.user
	teacher_id = instance.id
	basename, file_extension = filename.split(".")
	new_filename = "%s-%s.%s" %(basename, teacher_name, file_extension)
	olddir = "%s/teacher_sub/%s/docs1" %(settings.MEDIA_ROOT, teacher_name)
	shutil.rmtree(olddir, ignore_errors=True)
	return "teacher_sub/%s/docs1/%s" %(teacher_name, new_filename)

def doc_upload_to2(instance, filename):
	teacher_name = instance.user
	# teacher_id = instance.id
	basename, file_extension = filename.split(".")
	new_filename = "%s-%s.%s" %(basename, teacher_name, file_extension)
	olddir = "%s/teacher_sub/%s/docs2" %(settings.MEDIA_ROOT, teacher_name)
	shutil.rmtree(olddir, ignore_errors=True)
	return "teacher_sub/%s/docs2/%s" %(teacher_name, new_filename)

def doc_upload_to3(instance, filename):
	teacher_name = instance.user
	# teacher_id = instance.id
	basename, file_extension = filename.split(".")
	new_filename = "%s-%s.%s" %(basename, teacher_name, file_extension)
	olddir = "%s/teacher_sub/%s/docs3" %(settings.MEDIA_ROOT, teacher_name)
	shutil.rmtree(olddir, ignore_errors=True)
	return "teacher_sub/%s/docs3/%s" %(teacher_name, new_filename)

def doc_upload_to4(instance, filename):
	teacher_name = instance.user
	# teacher_id = instance.id
	basename, file_extension = filename.split(".")
	new_filename = "%s-%s.%s" %(basename, teacher_name, file_extension)
	olddir = "%s/teacher_sub/%s/docs4" %(settings.MEDIA_ROOT, teacher_name)
	shutil.rmtree(olddir, ignore_errors=True)
	return "teacher_sub/%s/docs4/%s" %(teacher_name, new_filename)

def doc_upload_to5(instance, filename):
	teacher_name = instance.user
	# teacher_id = instance.id
	basename, file_extension = filename.split(".")
	new_filename = "%s-%s.%s" %(basename, teacher_name, file_extension)
	olddir = "%s/teacher_sub/%s/docs5" %(settings.MEDIA_ROOT, teacher_name)
	shutil.rmtree(olddir, ignore_errors=True)
	return "teacher_sub/%s/docs5/%s" %(teacher_name, new_filename)

def doc_upload_to6(instance, filename):
	teacher_name = instance.user
	# teacher_id = instance.id
	basename, file_extension = filename.split(".")
	new_filename = "%s-%s.%s" %(basename, teacher_name, file_extension)
	olddir = "%s/teacher_sub/%s/docs6" %(settings.MEDIA_ROOT, teacher_name)
	shutil.rmtree(olddir, ignore_errors=True)
	return "teacher_sub/%s/docs6/%s" %(teacher_name, new_filename)


function = (
	('Student', 'Student'),
	('Teacher', 'Teacher')
)

gender = (
	('Male', 'Male'),
	('Female', 'Female')
)

class Teacher(models.Model):
	phone_regex = RegexValidator(regex=r'^\d{4}-\d{4}$', message="Phone number must be entered in the format: 'XXXX-XXXX'.")
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	function = models.CharField(max_length=20, null=True, blank=True)

	title = models.CharField(max_length=120)
	first_name = models.CharField(max_length=60)
	last_name = models.CharField(max_length=60)
	contact = models.CharField(max_length=20, validators=[phone_regex], blank=False, null=False) # validators should be a list
	birth_date = models.DateField(blank=True, null=True)
	gender = models.CharField(max_length=6, choices=gender, blank=True, null=True)

	first_subject = models.ForeignKey(Subject_Expertise, on_delete=models.CASCADE, null=True, blank=True)
	first_level = models.ManyToManyField(Level_Expertise, blank=True)

	# featured_subscribed = BooleanField

	second_subject = models.ForeignKey(Subject_Expertise, on_delete=models.CASCADE, null=True, blank=True, related_name="subject2")
	second_level = models.ManyToManyField(Level_Expertise, blank=True, related_name="level2")

	third_subject = models.ForeignKey(Subject_Expertise, on_delete=models.CASCADE, null=True, blank=True, related_name="subject3")
	third_level = models.ManyToManyField(Level_Expertise, blank=True, related_name="level3")

	educational_level = models.ManyToManyField(Educational_Level)
	education = models.ManyToManyField(Education)
	education_school = models.ManyToManyField(Education_School)
	expertise_type = models.ForeignKey(Expertise_Type, on_delete=models.CASCADE, null=True, blank=True)
	years_of_experience = models.PositiveIntegerField(null=False, blank=False)
	description = models.TextField(null=True, blank=True)
	group_tuition = models.BooleanField(default=False)
	website_url = models.CharField(max_length=60, null=True, blank=True)

	salary_expectation = models.DecimalField(decimal_places=0, max_digits=3, null=True, blank=True)
	salary_negotiable = models.BooleanField(default=False)

	region = models.ManyToManyField(Region)
	postal_code = models.CharField(max_length=6, null=True, blank=True)

	# street = models.CharField(max_length=120, null=True, blank=True)
	# city = models.CharField(max_length=120, null=True, blank=True)
	# state = models.CharField(max_length=120, null=True, blank=True)
	# zipcode = models.CharField(max_length=120, null=True, blank=True)
	# country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)

	review_score = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)

	active = models.BooleanField(default=True) #deactivate after two months?
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	date_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
	trial_acc = models.BooleanField(default=False)
	docs_verified = models.BooleanField(default=False)

	image = models.ImageField(blank=True, null=True, upload_to=image_upload_to)

	# advimage = models.ImageField(blank=True, null=True, upload_to=advimage_upload_to)



	doc1 = models.ImageField(blank=True, null=True, upload_to=doc_upload_to1)
	doc1description = models.CharField(max_length=60, blank=True, null=True)
	doc2 = models.ImageField(blank=True, null=True, upload_to=doc_upload_to2)
	doc2description = models.CharField(max_length=60, blank=True, null=True)
	doc3 = models.ImageField(blank=True, null=True, upload_to=doc_upload_to3)
	doc3description = models.CharField(max_length=60, blank=True, null=True)
	doc4 = models.ImageField(blank=True, null=True, upload_to=doc_upload_to4)
	doc4description = models.CharField(max_length=60, blank=True, null=True)
	doc5 = models.ImageField(blank=True, null=True, upload_to=doc_upload_to5)
	doc5description = models.CharField(max_length=60, blank=True, null=True)
	doc6 = models.ImageField(blank=True, null=True, upload_to=doc_upload_to6)
	doc6description = models.CharField(max_length=60, blank=True, null=True)


	def __str__(self):
		return str(self.user.username)



	def get_absolute_url(self):
		return reverse('TeacherDetail', kwargs={'pk': self.pk})

	def get_update(self):
		return reverse('TeacherUpdate', kwargs={'pk': self.pk})

	def get_score(self):
		score = self.reviewteacher_set.filter(cnc="Complete").aggregate(Avg('score')).values()[0]
		if score is not None:
			score = round(score,1)
		else:
			score = 0.0
		return score

	def get_job_count(self):
		job_count = self.reviewteacher_set.filter(cnc="Complete").count()
		return job_count

	def get_last_active(self):
		last_active = self.reviewteacher_set.all().aggregate(Max('timestamp')).values()[0]
		return last_active

	def get_sub_status(self):
		usersubdate = get_object_or_404(ImageSubscription, user = self.user)
		tday = timezone.now().date()
		subscribed = False
		if usersubdate.subenddate > tday and self.doc1:
			subscribed = True
		return subscribed


def teacher_post_save_receiver(sender, instance, *args, **kwargs):
	if not instance.function:
		instance.function = 'Teacher'

post_save.connect(teacher_post_save_receiver, sender=Teacher)




