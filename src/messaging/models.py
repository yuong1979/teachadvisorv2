from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from opening.models import Opening
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from django.urls import reverse


class MessageManager(models.Manager):
	def filter_by_instance(self, instance):
		get = instance.id
		instance = get_object_or_404(Message, pk=get)
		content_type = ContentType.objects.get_for_model(instance.__class__)# you can use message as well
		# comments = Comment.objects.filter(content_type=content_type, object_id=get)
		qs = super(MessageManager, self).filter(content_type=content_type, object_id=get)
		return qs

	def filter_message_list(self, instance):
		get = instance.id
		return self.get_queryset().filter(id=get)
	# def active(self, *args, **kwargs):
	# 	return self.get_queryset().filter(id=1)



order_status = (
		('Inactive', 'Inactive'),
		('Messaged', 'Messaged'),
		('Rejected', 'Rejected'),
		('Application', 'Application'),
		('Offer', 'Offer'),
		('Job In Progress', 'Job In Progress'),
		('Completed', 'Completed'),
		('Canceled', 'Canceled'),
		('Reviewed', 'Reviewed'),
	)


class Message(models.Model):

	senduser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	touser = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='to_user', on_delete=models.CASCADE)
	mainmessage = models.BooleanField(default=False)
	title = models.CharField(max_length=120) #- company opening and date
	re_opening = models.ForeignKey(Opening, on_delete=models.CASCADE)

	msgtype = models.CharField(max_length=30, choices=order_status, default="Inactive")

	content = models.TextField()
	timestamp = models.DateTimeField(auto_now=True)
	date = models.DateField(auto_now=True)

	parent_id = models.PositiveIntegerField(null=True, blank=True)# if this is replied to than using the message id if now use this
	# paid = models.BooleanField(default=False)

	objects = MessageManager()


	def __str__(self):
		return str(self.title)

	def get_absolute_url(self):
		return reverse("MessageDetail", kwargs={"pk":self.pk})

	def get_status(self):
		# parent_id = Message.objects.get(id=self.id).parent_id
		# msg = Message.objects.filter(parent_id=parent_id).first()
		status = self.msgtype
		return status

	def get_user_name(self):
		try:
			user = self.senduser.student.first_name
		except:
			user = self.senduser.teacher.first_name
		return user


		# parent_id = Message.objects.get(id=self.id).parent_id
		# msg = Message.objects.filter(parent_id=parent_id).first()
		# status = msg.msgtype
		# return status

	class Meta:
		ordering = ["-timestamp","title"] #reversing the order of the entries





