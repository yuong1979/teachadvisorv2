from django.contrib import admin

# Register your models here.
from messaging.models import Message



class MessageAdmin(admin.ModelAdmin):
	list_display = ['__unicode__','re_opening','mainmessage','msgtype','parent_id','timestamp']
	inlines = [
	]
	class Meta:
		model = Message

admin.site.register(Message, MessageAdmin)






