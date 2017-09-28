from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from django.utils.safestring import mark_safe
from markdown_deux import markdown

from django.db import models


# Create your models here.


class BlogPost(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=320)
    post_summary = models.TextField(blank=True, verbose_name="Pre Video Content")
    youtube_video_id = models.CharField(max_length=20, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/')
    slug = models.SlugField(unique=True, blank=True)
    draft = models.BooleanField(default=False, verbose_name="DRAFT: Click to make this post draft, unchecked for publish(default).")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title) + '-' + slugify(timezone.now().time())
        return super(BlogPost, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    def get_markdown_summary(self):
        post_summary = self.post_summary
        markdown_text = markdown(post_summary)
        return mark_safe(markdown_text)
