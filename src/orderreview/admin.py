from django.contrib import admin

# Register your models here.
from orderreview.models import ReviewTeacher


class ReviewTeacherAdmin(admin.ModelAdmin):
	list_display = ['opening','subject','level','price','cnc','datebetween']
	inlines = [
	]
	class Meta:
		model = ReviewTeacher


admin.site.register(ReviewTeacher, ReviewTeacherAdmin)

