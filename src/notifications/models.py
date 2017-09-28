from __future__ import unicode_literals
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from messaging.models import Message
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.conf import settings
from django.db import models
from notifications.signals import notify

import datetime
import pytz


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

class NotificationQuerySet(models.query.QuerySet):
	def get_user(self, user):
		return self.filter(recipient=user)

	# def mark_all_read(self,recipient):
	# 	qs = self.unread().get_user(recipient)
	# 	qs.update(read=True)

	# def mark_all_unread(self,recipient):
	# 	qs = self.read().get_user(recipient)
	# 	qs.update(read=False)

	def unread(self):
		return self.filter(read=False)

	# def read(self):
	# 	return self.filter(read=True)

	def recent(self):
		return self.unread().order_by('-timestamp')[:15]


class NotificationManager(models.Manager):
	def get_queryset(self):
		return NotificationQuerySet(self.model, using=self._db)

	# def get_all_unread(self, user):
	# 	return self.get_queryset().get_user(user).unread()

	# def get_all_read(self, user):
	# 	return self.get_queryset().get_user(user).read()

	def all_for_user(self, user):
		return self.get_queryset().get_user(user)


class Notification(models.Model):
	sender = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
	recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="notifications")
	action = models.CharField(max_length=255)
	message = models.ForeignKey(Message, null=True)
	read = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	objects = NotificationManager()

	def __unicode__(self):
		context = {
			"sender": self.sender,
			"recipient": self.recipient,
			"action": self.action,
			"message":self.message,
			"msg_con":self.message.content[:20],
			"verify_read": reverse("notifications_read", kwargs={"id": self.id}),
			"message_url":self.message.get_absolute_url(),
		}
		return "%(sender)s: <a href='%(verify_read)s?next=%(message_url)s'>%(msg_con)s</a>" %context


	# def __unicode__(self):
	# 	return str(self.action)




def new_notification(sender, recipient, action, message, *args, **kwargs):
	# new_notification_create = Notification.objects.create( sender=sender, recipient=recipient, action=action, message=message)
	new_note = Notification(
		sender=sender,
		recipient=recipient,
		action=action,
		message=message
		)
	for option in ("action","message"):
		obj = kwargs.pop(option, None)
		if obj is not None:
			setattr(new_note, option, obj)
	new_note.save()

	email = recipient.email
	pmsg_id = message.parent_id
	msg_id = message.id

	#if the messages has been sent 1 minute ago ignore the email sending
	lastsent = Notification.objects.filter(sender=sender, recipient=recipient, read=False).order_by('-timestamp')
	if lastsent.count() == 1:
		send_email(action=action, email=email, message=message, username=sender, msg_id=msg_id, pmsg_id=pmsg_id)
	else:
		seclastsent = lastsent[1]
		timelastsent = seclastsent.timestamp
		timesend = datetime.datetime.now(tz=pytz.UTC)
		timediff = timesend - timelastsent
		noofsec = timediff.seconds
		#change this back to 60 seconds when done
		if noofsec > 60:
			send_email(action=action, email=email, message=message, username=sender, msg_id=msg_id, pmsg_id=pmsg_id)


notify.connect(new_notification)


def send_email(action, email, message, username, msg_id, pmsg_id):

	action = action
	to_email = [email]
	message = str(message)

	msg = Message.objects.get(id=msg_id)
	msg = msg.content
	parent_msg = Message.objects.get(id=pmsg_id)

	msg_link = parent_msg.get_absolute_url()

	# retrieving the site
	if settings.TYPE == "base":
		current_site = "http://127.0.0.1:8000"
		from_email = settings.EMAIL_HOST_USER
	else:
		current_site = Site.objects.get_current().domain
		from_email = settings.DEFAULT_FROM_EMAIL
		
	html_message ="<p>" + str(username) + ": " + str(msg) + "<br><br><a href='" + current_site + msg_link + "'"+">Click here to respond</p>"

	# subject = str(current_site) + ": You have recieved a message from " + str(username)

	if action == "Messaged":
		subject = str(current_site) + ": Message from %s" %(username)
	elif action == "Application":
		subject = str(current_site) + ": Application from %s" %(username)
	elif action == "Offer":
		subject = str(current_site) + ": Offer from %s" %(username)
	elif action == "Acceptance":
		subject = str(current_site) + ": Acceptance from %s" %(username)
	elif action == "Cancel":
		subject = str(current_site) + ": Cancellation job from %s" %(username)
	elif action == "Complete":
		subject = str(current_site) + ": Completed job from %s" %(username)
	elif action == "Review":
		subject = str(current_site) + ": Review from %s" %(username)

	# elif action == "rej":
	# 	contact_message = "Rejection from %s : %s" %(username, message)
	else:
		subject = "Reply from %s" %(username)

	# to_email = ["yuong1979@gmail.com"]
	# to_email = [email, from_email]

	send_mail(
			subject=subject,
			message="",
			html_message=html_message,
			from_email=from_email,
			recipient_list=to_email,
			fail_silently=False,
			)
