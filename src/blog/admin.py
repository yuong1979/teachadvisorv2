from django.contrib import admin
from django.db import models
from pagedown.widgets import AdminPagedownWidget

from .models import BlogPost


# Register your models here.


class BlogPostAdmin(admin.ModelAdmin):
    exclude = ['slug', ]
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }


admin.site.register(BlogPost, BlogPostAdmin)
