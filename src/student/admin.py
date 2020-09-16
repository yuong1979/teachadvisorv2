from django.contrib import admin

# Register your models here.
from student.models import Student


class StudentAdmin(admin.ModelAdmin):
	list_display = ['first_name','last_name','contact']
	inlines = [
	]
	class Meta:
		model = Student


admin.site.register(Student, StudentAdmin)
