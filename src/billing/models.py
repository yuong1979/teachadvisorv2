from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from variables.models import Country, Subject_Expertise, Level_Expertise, Educational_Level, Region, Education, Education_School, Expertise_Type
import braintree

class Transaction(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	price = models.DecimalField(max_digits=100, decimal_places=2, default=0, null=True)
	beforecredit = models.IntegerField(default=0)
	credit = models.IntegerField(default=0)
	aftercredit = models.IntegerField(default=0)
	transaction_id = models.CharField(max_length=120, null=False, blank=False, default="")
	success = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	# transaction_id 
	# payment method
	# last_four

	def __unicode__(self):
		return "%s" %(self.transaction_id)

class UserCredit(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	credit = models.IntegerField(default=0)

	def __unicode__(self):
		return "%s" %(self.user)


#where user can earn credits through sharing and verification.
class UserMicell(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	user_verify = models.BooleanField(default=False)
	FBshare = models.BooleanField(default=False)
	FBlike = models.BooleanField(default=False)
	TWtweet = models.BooleanField(default=False)
	TWfollow = models.BooleanField(default=False)
	INSTfollow = models.BooleanField(default=False)
	emailUnsub = models.BooleanField(default=False)

	def __unicode__(self):
		return "%s" %(self.user)



class CreditToCash(models.Model):
	label = models.CharField(max_length=120, null=False, blank=False, default="")
	cashprice = models.IntegerField(default=0)
	credits = models.IntegerField(default=0)
	discount = models.DecimalField(max_digits=100, decimal_places=2, default=0, null=True)

	def __unicode__(self):
		return str(self.label)

class ImageSubscription(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	subenddate = models.DateField()
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __unicode__(self):
		return "%s" %(self.user)

class AnalyticsSubscription(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	subenddate = models.DateField()
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __unicode__(self):
		return "%s" %(self.user)

class FeaturedUser_0(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
	subenddate = models.DateField(null=True, blank=True)
	subject = models.OneToOneField(Subject_Expertise, null=True, blank=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __unicode__(self):
		return "%s" %(self.subject)

class FeaturedUser_1(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
	subenddate = models.DateField(null=True, blank=True)
	subject = models.OneToOneField(Subject_Expertise, null=True, blank=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __unicode__(self):
		return "%s" %(self.subject)

class StudentBISubscription(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	subenddate = models.DateField()
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __unicode__(self):
		return "%s" %(self.user)

class UserCheckOut(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)
	# email = models.EmailField(unique=True)
	braintree_id = models.CharField(max_length=120, null=True, blank=True)

	def __unicode__(self):
		return self.user.email

	# def __init__(self, ):
	# 	self.customer_id = self.get_braintree_id()

	def get_braintree_id(self, ):
		if not self.braintree_id:
			result = braintree.Customer.create({
				"email":self.user.email,
				})
			if result.is_success:
				self.braintree_id = result.customer.id
				self.save()
			return self.braintree_id
		return self.braintree_id

	def get_client_token(self):
		customer_id  = self.get_braintree_id
		if customer_id:
			client_token = braintree.ClientToken.generate({
				"customer_id": customer_id()
			})
			return client_token
		return None


def update_braintree_id(sender, instance, *args, **kwargs):
	if not instance.braintree_id:
		instance.get_braintree_id()

post_save.connect(update_braintree_id, sender=UserCheckOut)




