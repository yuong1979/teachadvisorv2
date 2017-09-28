"""Admin page."""
from django.contrib import admin

from examdownload.models import Exam
from examdownload.models import TemporaryLink


class CommonAdmin(admin.ModelAdmin):
    """Common docstring."""
    pass


class ExamAdmin(admin.ModelAdmin):
	list_display = ['__unicode__','exam_type','subject','school','level','publish','creditcost']
	inlines = [
	]
	class Meta:
		model = Exam






admin.site.register(Exam, ExamAdmin)
admin.site.register(TemporaryLink, CommonAdmin)



