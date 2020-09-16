from __future__ import unicode_literals
from student.models import Student
from opening.models import Opening
from teacher.models import Teacher
from messaging.models import Message
from variables.models import Country, Educational_Level, Education, Subject_Expertise, Level_Expertise, Region, Expertise_Type, Education_School
from django.urls import reverse
from django.conf import settings
from django.db import models




import braintree
if settings.DEBUG:
	braintree.Configuration.configure(braintree.Environment.Sandbox,
		merchant_id = settings.BRAINTREE_MERCHANT_ID,
		public_key = settings.BRAINTREE_PUBLIC,
		private_key = settings.BRAINTREE_PRIVATE)



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



class Order(models.Model):

	oteacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
	ostudent = models.ForeignKey(Student, on_delete=models.CASCADE)
	oopening = models.ForeignKey(Opening, on_delete=models.CASCADE)
	omessage = models.ForeignKey(Message, on_delete=models.CASCADE)

	#to collect data for statistics
	subject = models.ForeignKey(Subject_Expertise, null=True, blank=True, on_delete=models.CASCADE)
	level = models.ForeignKey(Level_Expertise, null=True, blank=True, on_delete=models.CASCADE)
	#rating for the tutor when order was accepted
	tutor_rating = models.DecimalField(decimal_places=0, max_digits=3, null=True, blank=True)
	grp_tuition = models.BooleanField(default=False)
	expertise = models.ForeignKey(Expertise_Type, null=True, blank=True, on_delete=models.CASCADE)
	years_of_exp = models.PositiveIntegerField(null=True, blank=True)
	location = models.ForeignKey(Region,null=True, blank=True, on_delete=models.CASCADE)

	timestamp = models.DateTimeField(auto_now=True)
	date = models.DateField(auto_now=True)
	teacherorder = models.BooleanField(default=False)
	studentorder = models.BooleanField(default=False)
	price = models.IntegerField(null=True, blank=True)
	status = models.CharField(max_length=30, choices=order_status, default="Inactive")
	# order_id = models.CharField(max_length=20, null=True, blank=True)

	# objects = OrderManager()


	def __str__(self):
		return str(self.oopening)

	def get_order_opening(self):
		return reverse('OpeningDetail', kwargs={'pk': self.oopening.id})

	# def mark_completed(self, order_id=None):
	# 	self.status = "Paid"
	# 	if order_id and not self.order_id:
	# 		self.order_id = order_id
	# 	self.save()



