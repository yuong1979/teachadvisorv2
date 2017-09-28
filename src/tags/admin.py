from django.contrib import admin

# Register your models here.
from tags.models import TagTeacher, TagOpening, ViewTeacherUnique, ViewOpening, FavTeacher, FavOpening, ViewTeacherRecord, ViewTeacherNonUnique, SearchWordTeacherRecord, BlockUser


class SearchWordTeacherRecordAdmin(admin.ModelAdmin):
	list_display = ['__unicode__','user','subject','level','date']
	inlines = [
	]
	class Meta:
		model = SearchWordTeacherRecord


class ViewTeacherRecordAdmin(admin.ModelAdmin):
	list_display = ['__unicode__',
					'uniquecount',
					'nonuniquecount',
					'msgtocount',
					'msgfromcount',
					'ordercount',
					# 'testcount',
					'date',
					'updated']
	inlines = [
	]
	class Meta:
		model = ViewTeacherRecord


admin.site.register(TagTeacher)
admin.site.register(TagOpening)

admin.site.register(ViewTeacherUnique)
admin.site.register(ViewTeacherNonUnique)
admin.site.register(ViewOpening)

admin.site.register(FavTeacher)
admin.site.register(FavOpening)

admin.site.register(ViewTeacherRecord, ViewTeacherRecordAdmin)
admin.site.register(SearchWordTeacherRecord, SearchWordTeacherRecordAdmin)

admin.site.register(BlockUser)
