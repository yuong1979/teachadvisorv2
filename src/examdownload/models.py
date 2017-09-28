"""Model for examdownload file."""
from __future__ import unicode_literals

import uuid

from django.contrib.auth.models import User
from django.db import models


class Exam(models.Model):
    """Exam model."""

    title = models.CharField(max_length=120)
    school = models.CharField(max_length=120)
    exam_type = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    subject = models.CharField(max_length=120)
    level = models.CharField(max_length=120)
    publish = models.BooleanField(default=False)
    docs = models.FileField()
    creditcost = models.IntegerField()

    def __unicode__(self):  # pragma: no cover
        """Return unicode repr."""
        return self.title


class TemporaryLink(models.Model):
    """Represents temporary link for download."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,  # noqa pylint: disable=invalid-name
                          editable=False)
    user = models.ForeignKey(User, related_name='temporarylinks')
    user_agent = models.CharField(max_length=200)
    user_ip = models.CharField(max_length=100)
    exam = models.ForeignKey(Exam, related_name='temporarylinks')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    downloaded_at = models.DateTimeField()

    def __unicode__(self):  # pragma: no cover
        """Return unicode repr."""
        return '{} ({})'.format(self.user, self.id)
