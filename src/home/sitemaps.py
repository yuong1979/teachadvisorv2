from django.contrib import sitemaps
from django.urls import reverse
from django.contrib.sitemaps import Sitemap
from blog.models import BlogPost


class StaticViewSitemap(sitemaps.Sitemap):
	priority = 0.5
	changefreq = 'weekly'

	def items(self):
		return ['Home', 'Contact', 'Promotions', 'Promotions', 'TermsAndCondition', 'Disclaimer', 'PrivacyPolicy',
		'RefundPolicy', 'FAQTutor', 'FAQStudent', 'Customer_Support', 'Tutorials', 'AboutUs', 'Careers',
		'Press', 'Partnership', 'TeacherList', 'StudentList', 'OpeningList', 'blog_list']

	def location(self, item):
		return reverse(item)


class BlogSitemap(Sitemap):
	changefreq = "daily"
	priority = 0.5

	def items(self):
		return BlogPost.objects.filter(draft=False)

	def lastmod(self, obj):
		return obj.updated_at

	def location(self, obj):
		return "/" + obj.slug + "/"
