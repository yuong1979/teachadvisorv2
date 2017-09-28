from django.contrib import admin

# Register your models here.

from variables.models import Country, Subject_Expertise, Level_Expertise, Educational_Level, Region, Education, Education_School, Expertise_Type

admin.site.register(Country)
admin.site.register(Subject_Expertise)
admin.site.register(Level_Expertise)
admin.site.register(Educational_Level)
admin.site.register(Education)
admin.site.register(Region)
# admin.site.register(FunctionType)
admin.site.register(Education_School)
admin.site.register(Expertise_Type)
