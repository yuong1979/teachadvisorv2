from __future__ import unicode_literals
from variables.models import Country, Subject_Expertise, Level_Expertise, Educational_Level, Education, Region, Education_School, Expertise_Type
from student.models import Student
from opening.models import Opening
from teacher.models import Teacher
from messaging.models import Message
from orders.models import Order
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
import datetime


class ReviewTeacher(models.Model):
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	opening = models.ForeignKey(Opening, on_delete=models.CASCADE)
	message = models.ForeignKey(Message, on_delete=models.CASCADE)
	order = models.ForeignKey(Order, on_delete=models.CASCADE)

	subject = models.ForeignKey(Subject_Expertise, on_delete=models.CASCADE, null=True, blank=True)
	level = models.ForeignKey(Level_Expertise, on_delete=models.CASCADE, null=True, blank=True)
	group_tuition = models.BooleanField(default=False)
	price = models.IntegerField(null=True, blank=True)
	datebetween = models.IntegerField(null=True, blank=True)

	cnc = models.CharField(max_length=20, blank=True, null=True)
	reason = models.CharField(max_length=120, null=True, blank=True)
	comments = models.TextField(max_length=500,null=True, blank=True)
	score = models.IntegerField(null=True, blank=True)
	
	gradebefore = models.CharField(max_length=20, null=True, blank=True)
	gradeafter = models.CharField(max_length=20, null=True, blank=True)
	review = models.TextField(max_length=500,null=True, blank=True)
	reviewcomment = models.TextField(max_length=500,null=True, blank=True)
	anonymous = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)


	def __str__(self):
		return str(self.teacher)


	def get_teacher_url(self):
		teacher_id = self.teacher.id
		return reverse('TeacherDetail', kwargs={'pk': teacher_id})

	def get_message_url(self):
		msg = Message.objects.filter(senduser=self.student.user , touser=self.teacher.user , re_opening=self.opening).first()
		return reverse('MessageDetail', kwargs={'pk': msg.id})

	def get_grade(self):
		scorevariance = "From " + str(self.gradebefore) + " to " + str(self.gradeafter)
		return scorevariance

	def get_rscore(self):
		score = self.score
		if score is not None:
			score = round(score,1)
		else:
			score = 0.0
		return score



grade_choices = (
		('100-95', '100-95'),
		('94-90', '94-90'),
		('89-85', '89-85'),
		('84-80', '84-80'),
		('79-75', '79-75'),
		('74-70', '74-70'),
		('69-65', '69-65'),
		('64-60', '64-60'),
		('59-55', '59-55'),
		('54-50', '54-50'),
		('49-45', '49-45'),
		('45-40', '45-40'),
		('0-39', '0-39'),
	)


def update_review(sender, instance, *args, **kwargs):
	#to collect the number of days between opening create and review to identify possibility of fake reviews

	todate = datetime.datetime.now().date()
	# todate = todate.replace(tzinfo=None)
	# todate = todate.date()
	#get the date for the opening

	opening_date = instance.opening.timestamp.date()
	days_diff = todate - opening_date
	days_diff = days_diff.days

	if instance.datebetween is None:
		instance.datebetween = days_diff
		instance.save()

	#saving the new aggregate score to the teachers model
	new_agg_score = instance.teacher.get_score()
	instance.teacher.review_score = new_agg_score
	instance.teacher.save()


post_save.connect(update_review, sender=ReviewTeacher)