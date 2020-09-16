from django.contrib import admin

# Register your models here.

from billing.models import Transaction, UserCredit, ImageSubscription, CreditToCash, FeaturedUser_0, FeaturedUser_1, UserCheckOut, AnalyticsSubscription, StudentBISubscription, UserMicell


class TransactionAdmin(admin.ModelAdmin):
	list_display = ['user','credit','price','success']
	inlines = [
	]
	class Meta:
		model = Transaction


class UserCreditAdmin(admin.ModelAdmin):
	list_display = ['credit']
	inlines = [
	]
	class Meta:
		model = UserCredit


class ImageSubscriptionAdmin(admin.ModelAdmin):
	list_display = ['subenddate','updated']
	inlines = [
	]
	class Meta:
		model = ImageSubscription

class AnalyticsSubscriptionAdmin(admin.ModelAdmin):
	list_display = ['subenddate','updated']
	inlines = [
	]
	class Meta:
		model = AnalyticsSubscription

class StudentBISubscriptionAdmin(admin.ModelAdmin):
	list_display = ['subenddate','updated']
	inlines = [
	]
	class Meta:
		model = StudentBISubscription

class CreditToCashAdmin(admin.ModelAdmin):
	list_display = ['credits','cashprice','discount']
	inlines = [
	]
	class Meta:
		model = CreditToCash


# latest version of django
# class PriceToDaysAdmin(admin.ModelAdmin):
#     list_display = ('id','label','cashprice','daystoadd','subplan','discount','active')

#     def __str__(self,obj):
#         return obj.__str__()


class FeaturedUser_0Admin(admin.ModelAdmin):
	list_display = ['subenddate','user','updated']
	inlines = [
	]
	class Meta:
		model = FeaturedUser_0

class FeaturedUser_1Admin(admin.ModelAdmin):
	list_display = ['subenddate','user','updated']
	inlines = [
	]
	class Meta:
		model = FeaturedUser_1


admin.site.register(Transaction, TransactionAdmin)

admin.site.register(UserCredit, UserCreditAdmin)

admin.site.register(ImageSubscription, ImageSubscriptionAdmin)

admin.site.register(AnalyticsSubscription, AnalyticsSubscriptionAdmin)

admin.site.register(StudentBISubscription, StudentBISubscriptionAdmin)

admin.site.register(CreditToCash, CreditToCashAdmin)

admin.site.register(FeaturedUser_0, FeaturedUser_0Admin)

admin.site.register(FeaturedUser_1, FeaturedUser_1Admin)

admin.site.register(UserCheckOut)

admin.site.register(UserMicell)
