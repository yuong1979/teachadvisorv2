from __future__ import unicode_literals
from teacher.models import Teacher
from opening.models import Opening
from student.models import Student
from messaging.models import Message
from orders.models import Order
from variables.models import Country, Subject_Expertise, Level_Expertise, Educational_Level, Education, Region, Education_School, Expertise_Type
from django.urls import reverse
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
import datetime

#implement favourite views and tags

# class TagQuerySet(models.query.QuerySet):
# 	def active(self):
# 		return self.filter(active=True)

class TagTeacherManager(models.Manager):
	def active(self, *args, **kwargs):
		return self.get_queryset().filter(active=True)
			
class TagTeacher(models.Model):
	title = models.CharField(max_length=120, unique=True)
	teacher = models.ManyToManyField(Teacher, blank=True)
	active = models.BooleanField(default=True)
	count = models.IntegerField(default=0)

	objects = TagTeacherManager()

	def __unicode__(self):
		return str(self.title)


class TagOpeningManager(models.Manager):
	def active(self, *args, **kwargs):
		return self.get_queryset().filter(job_active=True)
			
class TagOpening(models.Model):
	title = models.CharField(max_length=120, unique=True)
	opening = models.ManyToManyField(Opening, blank=True)
	active = models.BooleanField(default=True)
	count = models.IntegerField(default=0)

	objects = TagOpeningManager()

	def __unicode__(self):
		return str(self.title)


#everytime a teacher a viewed it will store the identity of the student on this model
class ViewTeacherUnique(models.Model):
	teacher = models.OneToOneField(Teacher, blank=True, default=None, on_delete=models.CASCADE)
	student = models.ManyToManyField(Student, blank=True, default=None)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return str(self.teacher)

	def get_student_count(self):
		count = self.student.count()
		return count

#everytime a teacher is viewed it will store ONE count of the view on this model
class ViewTeacherNonUnique(models.Model):
	teacher = models.OneToOneField(Teacher, blank=True, default=None, on_delete=models.CASCADE)
	count = models.IntegerField(default=0)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return str(self.teacher)



class ViewOpening(models.Model):
	opening = models.OneToOneField(Opening, blank=True, default=None, on_delete=models.CASCADE)
	teacher = models.ManyToManyField(Teacher, blank=True, default=None)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return str(self.opening)


class BlockUser(models.Model):
	blocker = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True, default=None, related_name='blocker_u', on_delete=models.CASCADE)
	blocked = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, default=None, related_name='blocked_u')
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return str(self.blocker)


class FavTeacher(models.Model):
	teacher = models.OneToOneField(Teacher, blank=True, default=None, on_delete=models.CASCADE)
	student = models.ManyToManyField(Student, blank=True, default=None)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return str(self.teacher)

class FavOpening(models.Model):
	opening = models.OneToOneField(Opening, blank=True, default=None, on_delete=models.CASCADE)
	teacher = models.ManyToManyField(Teacher, blank=True, default=None)
	# updated = models.DateTimeField(auto_now=True)
	# timestamp = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return str(self.opening)



class SearchWordTeacherRecord(models.Model):
	word = models.CharField(max_length=30, null=False, blank=False)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	subject = models.ForeignKey(Subject_Expertise, null=True, blank=True, on_delete=models.CASCADE)
	level = models.ForeignKey(Level_Expertise, null=True, blank=True, on_delete=models.CASCADE)
	date = models.DateField(auto_now=True)

	def __unicode__(self):
		return str(self.word)



class ViewTeacherRecord(models.Model):
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
	uniquecount = models.IntegerField(default=0)
	nonuniquecount = models.IntegerField(default=0)
	msgtocount = models.IntegerField(default=0)
	msgfromcount = models.IntegerField(default=0)
	ordercount = models.IntegerField(default=0)
	# testcount = models.IntegerField(default=0)
	date = models.DateField()
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return str(self.teacher)







#collects the data every start of the day when a student views the teacher for the first time
def update_viewteacherrecord(sender, instance, *args, **kwargs):

	todate = datetime.datetime.now().date()
	#delete the records beyond a certain date - enddate
	tdelta = datetime.timedelta(days=120)
	enddate = todate - tdelta

	# #delete the records beyond a certain date
	ViewTeacherRecord.objects.filter(date__lte=enddate).delete()


post_save.connect(update_viewteacherrecord, sender=ViewTeacherNonUnique)































# #collects the data every start of the day when a student views the teacher for the first time
# def update_viewteacherrecord(sender, instance, *args, **kwargs):

# 	todate = datetime.datetime.now().date()
# 	#delete the records beyond a certain date - enddate
# 	tdelta = datetime.timedelta(days=120)
# 	enddate = todate - tdelta

# 	#if the entry for that date does not exist then create it, if not leave it.
# 	testexist = ViewTeacherRecord.objects.filter(teacher=instance.teacher, date=todate)
# 	if testexist:
# 		pass
# 	else:
# 		#extracting the variables to be stored in records
# 		nucount = instance.count

# 		try:
# 			vtu = ViewTeacherUnique.objects.get(teacher=instance.teacher)
# 			ucount = vtu.get_student_count()
# 		except:
# 			ucount = 0

# 		# msgc = Message.objects.filter(touser=instance.teacher.user, mainmessage=True, date=todate).count()
# 		# orderc = Order.objects.filter(oteacher=instance.teacher, date=todate).count()

# 		#need to remove todate and then test - remove todate because I need to get the as of todate cumulative sum
# 		msgc = Message.objects.filter(touser=instance.teacher.user, mainmessage=True).count()
# 		orderc = Order.objects.filter(oteacher=instance.teacher).count()

# 		#creating the new record
# 		viewteacherrecord = ViewTeacherRecord.objects.get_or_create(
# 			teacher=instance.teacher,
# 			date=todate
# 			)[0]

# 		viewteacherrecord.uniquecount = ucount
# 		viewteacherrecord.nonuniquecount = nucount
# 		viewteacherrecord.msgfromcount = msgc
# 		viewteacherrecord.ordercount = orderc
# 		viewteacherrecord.save()

# 		# #delete the records beyond a certain date
# 		ViewTeacherRecord.objects.filter(date__lte=enddate).delete()


# post_save.connect(update_viewteacherrecord, sender=ViewTeacherNonUnique)


