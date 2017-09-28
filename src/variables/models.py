from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Subject_Expertise(models.Model):
	title = models.CharField(max_length=50, unique=True)
	description = models.TextField(null=True, blank=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.title

class Level_Expertise(models.Model):
	title = models.CharField(max_length=50, unique=True)
	description = models.TextField(null=True, blank=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.title

class Educational_Level(models.Model):
	title = models.CharField(max_length=50, unique=True)
	description = models.TextField(null=True, blank=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.title

class Education(models.Model):
	title = models.CharField(max_length=50, unique=True)
	description = models.TextField(null=True, blank=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.title

class Education_School(models.Model):
	title = models.CharField(max_length=50, unique=True)
	description = models.TextField(null=True, blank=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.title

class Expertise_Type(models.Model):
	title = models.CharField(max_length=50, unique=True)
	description = models.TextField(null=True, blank=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.title


class Region(models.Model):
	title = models.CharField(max_length=50, unique=True)
	description = models.TextField(null=True, blank=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.title


class Country(models.Model):
	title = models.CharField(max_length=50, unique=True)
	description = models.TextField(null=True, blank=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.title


