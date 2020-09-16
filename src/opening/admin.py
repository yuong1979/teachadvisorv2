from django.contrib import admin

# Register your models here.
from opening.models import Opening


# class OpeningAdmin(admin.ModelAdmin):
# 	list_display = ['__unicode__','hiring_student','job_active']
# 	inlines = [
# 	]
# 	class Meta:
# 		model = Opening

class OpeningAdmin(admin.ModelAdmin):
	list_display = ['hiring_student','job_active','trial_acc']
	inlines = [
	]
	class Meta:
		model = Opening

admin.site.register(Opening, OpeningAdmin)

