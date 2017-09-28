from django.contrib import admin

# Register your models here.
from notifications.models import Notification



# admin.site.register(Notification)



class NotificationAdmin(admin.ModelAdmin):
	list_display = ['sender','recipient','message','read','timestamp']
	inlines = [
	]
	class Meta:
		model = Notification


admin.site.register(Notification, NotificationAdmin)
