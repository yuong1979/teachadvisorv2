from django.contrib import admin

# Register your models here.
from orders.models import Order



class UserCheckOutAdmin(admin.ModelAdmin):
	list_display = ['oteacher', 'ostudent', 'oopening', 'subject', 'level', 'tutor_rating', 'grp_tuition', 'years_of_exp', 'location', 'price', 'status',]
	class Meta:
		model = Order



admin.site.register(Order)

