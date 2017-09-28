from django.contrib import admin
from teacher.models import Teacher


# class TeacherAdmin(admin.ModelAdmin):
# 	list_display = ['__unicode__','first_name','last_name','contact']
# 	inlines = [
# 	]
# 	class Meta:
# 		model = Teacher

class TeacherAdmin(admin.ModelAdmin):
	list_display = ['__unicode__','first_name','last_name','contact','trial_acc']
	inlines = [
	]
	class Meta:
		model = Teacher


admin.site.register(Teacher, TeacherAdmin)
