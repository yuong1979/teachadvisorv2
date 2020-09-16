from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, FormMixin
from django.views.generic.detail import DetailView
from billing.models import Transaction, UserCheckOut, ImageSubscription, UserCredit, CreditToCash, FeaturedUser_0, FeaturedUser_1, AnalyticsSubscription, StudentBISubscription
from billing.forms import CreditForm, ImgSubForm, FeatureSubForm, AnaSubForm, StudentBISubForm
from billing.control import feat_days_choices_dict, img_days_choices_dict, ana_days_choices_dict, studentbi_days_dict
from mixins.mixins import GetCheckoutMixin, LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages
import braintree
import datetime
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY








#adding subscribtion for users profiles to be featured
class FeatureSub(LoginRequiredMixin, TemplateView, FormView):
	template_name = 'featsub.html'
	form_class = FeatureSubForm

	def get_user_cred(self, *args, **kwargs):
		user = self.request.user
		usercred_obj = get_object_or_404(UserCredit, user=user)
		usercred = usercred_obj.credit
		return usercred

	def get_context_data(self, *args, **kwargs):
		context = super(FeatureSub, self).get_context_data(*args, **kwargs)
		context["user_subject"] = self.request.user.teacher.first_subject
		context["usercred"] = self.get_user_cred()
		return context

	def form_valid(self, form):

		creditfeat = form.cleaned_data.get("creditfeat")
		subject = self.request.user.teacher.first_subject
		todate = datetime.datetime.now().date()
		# todate = todate.replace(tzinfo=None)
		usersubexit = False

		#do a get or create in case the subject for the feature does not exist yet in modelfeature1
		featuredusersub = FeaturedUser_0.objects.get_or_create(
			subject=subject
			)

		if featuredusersub[1] == True:
			featuredusersub[0].subenddate = datetime.datetime.now()
			featuredusersub[0].save()
			featuresub1 = featuredusersub[0]
		else:
			usersubdate = featuredusersub[0].subenddate
			# usersubdate = usersubdate.replace(tzinfo=None)

			if usersubdate > todate:
				usersubexit = True
			else:
				featuresub1 = featuredusersub[0]

		#do a get or create in case the subject for the feature does not exist yet in modelfeature2
		featuredusersub = FeaturedUser_1.objects.get_or_create(
			subject=subject
			)


		if featuredusersub[1] == True:
			featuredusersub[0].subenddate = datetime.datetime.now()
			featuredusersub[0].save()
			featuresub2 = featuredusersub[0]
		else:
			usersubdate = featuredusersub[0].subenddate
			# usersubdate = usersubdate.replace(tzinfo=None)

			if usersubdate > todate:
				usersubexit = True
			else:
				featuresub2 = featuredusersub[0]

		# choose the model to store the user subscription in - if feature1 has user then go feature2 if not exit
		try:
			feature = featuresub1
		except:
			try:
				feature = featuresub2
			except:

				if usersubexit == True:
					messages.warning(self.request, "There is still a user subscribed please try later")
					return redirect("Home")

		#if not enough credits to purchase the selected
		usercred = self.get_user_cred()
		if int(usercred) < int(creditfeat):
			messages.warning(self.request, "You do not have enough credits for this purchase, please top up some credits to add days to your subscription")
			return redirect('AddCredits')

		days = feat_days_choices_dict[creditfeat]
		# #creditchange
		# if creditfeat == '400':
		# 	days = '3'
		# if creditfeat == '800':
		# 	days = '7'
		# if creditfeat == '1600':
		# 	days = '14'

		tdelta = datetime.timedelta(days=int(days))

		#deducting credits from users account
		usercred_obj = get_object_or_404(UserCredit, user=self.request.user)
		usercred_obj.credit = int(self.get_user_cred()) - int(creditfeat)
		usercred_obj.save()

		##extending the users subscription date
		feature.user = self.request.user
		feature.subenddate = todate + tdelta
		feature.save()

		messages.success(self.request, "Your profile will now be featured for " + str(days) + " days ")
		return super(FeatureSub, self).form_valid(form)

	def get_success_url(self):
		return reverse('Home')










class ImageSub(LoginRequiredMixin, TemplateView, FormView):
	template_name = 'docsub.html'
	form_class = ImgSubForm

	def get_user_cred(self, *args, **kwargs):
		user = self.request.user
		usercred_obj = get_object_or_404(UserCredit, user=user)
		usercred = usercred_obj.credit
		return usercred

	def get_user_subend(self, *args, **kwargs):
		user = self.request.user
		usersub = get_object_or_404(ImageSubscription, user=user)
		usersubenddate = usersub.subenddate
		return usersubenddate

	def get_context_data(self, *args, **kwargs):
		context = super(ImageSub, self).get_context_data(*args, **kwargs)
		context["usercred"] = self.get_user_cred()
		return context   

	def form_valid(self, form):
		creditimg = form.cleaned_data.get("creditimg")
		usercred = self.get_user_cred()
		#if not enough credits to purchase the selected
		if int(usercred) < int(creditimg):
			messages.warning(self.request, "Please top up some credits to add days to your subscription")
			return redirect('AddCredits')

		days = img_days_choices_dict[creditimg]
		# #creditchange
		# if creditimg == '100':
		# 	days = '30'
		# if creditimg == '300':
		# 	days = '90'
		# if creditimg == '500':
		# 	days = '365'

		todate = datetime.datetime.now()
		usersubdate = self.get_user_subend()
		tdelta = datetime.timedelta(days=int(days))

		#deducting credits from users account
		usercred_obj = get_object_or_404(UserCredit, user=self.request.user)
		usercred_obj.credit = int(self.get_user_cred()) - int(creditimg)
		usercred_obj.save()

		#extending the users subscription date
		subscription = get_object_or_404(ImageSubscription, user=self.request.user)
		subscription.subenddate = todate + tdelta
		subscription.save()

		messages.success(self.request, "You have successfully added " + str(days) + " days to your image subscription")
		return super(ImageSub, self).form_valid(form)


	def get_success_url(self):
		return reverse('Home')








class AnalyticsSub(LoginRequiredMixin, TemplateView, FormView):
	template_name = 'anasub.html'
	form_class = AnaSubForm

	def get_user_cred(self, *args, **kwargs):
		user = self.request.user
		usercred_obj = get_object_or_404(UserCredit, user=user)
		usercred = usercred_obj.credit
		return usercred

	def get_user_subend(self, *args, **kwargs):
		user = self.request.user
		usersub = get_object_or_404(AnalyticsSubscription, user=user)
		usersubenddate = usersub.subenddate
		return usersubenddate

	def get_context_data(self, *args, **kwargs):
		context = super(AnalyticsSub, self).get_context_data(*args, **kwargs)
		context["usercred"] = self.get_user_cred()
		return context   

	def form_valid(self, form):
		creditana = form.cleaned_data.get("creditana")
		usercred = self.get_user_cred()
		#if not enough credits to purchase the selected
		if int(usercred) < int(creditana):
			messages.warning(self.request, "Please top up some credits to add days to your subscription")
			return redirect('AddCredits')

		days = ana_days_choices_dict[creditana]
		# #creditchange
		# if creditana == '100':
		# 	days = '30'
		# if creditana == '300':
		# 	days = '90'
		# if creditana == '500':
		# 	days = '365'

		todate = datetime.datetime.now()
		usersubdate = self.get_user_subend()
		tdelta = datetime.timedelta(days=int(days))

		#deducting credits from users account
		usercred_obj = get_object_or_404(UserCredit, user=self.request.user)
		usercred_obj.credit = int(self.get_user_cred()) - int(creditana)
		usercred_obj.save()

		#extending the users subscription date
		subscription = get_object_or_404(AnalyticsSubscription, user=self.request.user)
		subscription.subenddate = todate + tdelta
		subscription.save()

		messages.success(self.request, "You have successfully added " + str(days) + " days to your analytics subscription")
		return super(AnalyticsSub, self).form_valid(form)


	def get_success_url(self):
		return reverse('Home')













class StudentBISub(LoginRequiredMixin, TemplateView, FormView):
	template_name = 'bisub.html'
	form_class = StudentBISubForm

	def get_user_cred(self, *args, **kwargs):
		user = self.request.user
		usercred_obj = get_object_or_404(UserCredit, user=user)
		usercred = usercred_obj.credit
		return usercred

	def get_user_subend(self, *args, **kwargs):
		user = self.request.user
		usersub = get_object_or_404(StudentBISubscription, user=user)
		usersubenddate = usersub.subenddate
		return usersubenddate

	def get_context_data(self, *args, **kwargs):
		context = super(StudentBISub, self).get_context_data(*args, **kwargs)
		context["usercred"] = self.get_user_cred()
		return context   

	def form_valid(self, form):
		creditbi = form.cleaned_data.get("creditbi")
		usercred = self.get_user_cred()
		#if not enough credits to purchase the selected
		if int(usercred) < int(creditbi):
			messages.warning(self.request, "Please top up some credits to add days to your subscription")
			return redirect('AddCredits')

		days = studentbi_days_dict[creditbi]
		# #creditchange
		# if creditbi == '100':
		# 	days = '30'
		# if creditbi == '300':
		# 	days = '90'
		# if creditbi == '500':
		# 	days = '365'

		todate = datetime.datetime.now()
		usersubdate = self.get_user_subend()
		tdelta = datetime.timedelta(days=int(days))

		#deducting credits from users account
		usercred_obj = get_object_or_404(UserCredit, user=self.request.user)
		usercred_obj.credit = int(self.get_user_cred()) - int(creditbi)
		usercred_obj.save()

		#extending the users subscription date
		subscription = get_object_or_404(StudentBISubscription, user=self.request.user)
		subscription.subenddate = todate + tdelta
		subscription.save()

		messages.success(self.request, "You have successfully added " + str(days) + " days to your analytics subscription")
		return super(StudentBISub, self).form_valid(form)


	def get_success_url(self):
		return reverse('Home')







class StripeAddCredits(LoginRequiredMixin, GetCheckoutMixin, FormView):
	template_name = 'stripeaddcredits.html'
	form_class = CreditForm

	def get_context_data(self, *args, **kwargs):
		context = super(StripeAddCredits, self).get_context_data(*args, **kwargs)
		context["usercred"] = self.get_user_cred()
		return context

	def form_valid(self, form):
		credit = form.cleaned_data.get("credit")
		credit_pack = get_object_or_404(CreditToCash, label=credit)
		#save session for the credit package selected
		self.request.session["credit_id"] = credit_pack.id
		return super(StripeAddCredits, self).form_valid(form)

	def get_success_url(self):
		return reverse('StripePayment')


class StripePayment(LoginRequiredMixin, GetCheckoutMixin, TemplateView):
	template_name = 'stripepayment.html'

	def dispatch(self, *args, **kwargs):
		dispatch = super(StripePayment, self).dispatch(*args, **kwargs)
		#if credit package id is not selected to exit
		try:
			credit_id = self.request.session.get("credit_id")
		except:
			return reverse('Home')
		return dispatch

	def get_context_data(self, *args, **kwargs):
		context = super(StripePayment, self).get_context_data(*args, **kwargs)
		credit_id = self.request.session.get("credit_id")
		credit_pack = get_object_or_404(CreditToCash, id=credit_id)
		#convert dollars into cents for stripe to use
		context["creditcostcents"] = credit_pack.cashprice * 100
		context["creditcostdollars"] = credit_pack.cashprice

		context["description"] = "Payment for " + str(credit_pack.cashprice)

		context["credit"] = credit_pack.credits
		context["stripe_key"] = settings.STRIPE_PUBLIC_KEY

		return context




class StripeCheckOut(LoginRequiredMixin, GetCheckoutMixin, TemplateView):

	def dispatch(self, *args, **kwargs):
		dispatch = super(StripeCheckOut, self).dispatch(*args, **kwargs)
		#if credit package id is not selected to exit
		try:
			credit_id = self.request.session.get("credit_id")
		except:
			return reverse('Home')
		return dispatch

	def post(self, request, *args, **kwargs):

		try:
			credit_id = self.request.session.get("credit_id")
			credit_pack = get_object_or_404(CreditToCash, id=credit_id)
			#convert dollars into cents for stripe to use
			cash = credit_pack.cashprice * 100
			credit = credit_pack.credits
		except:
			return reverse('Home')

		token = request.POST.get("stripeToken")

		description = "user " + str(self.request.user) + " paid for " + str(credit) + " of credits"

		try:
			charge  = stripe.Charge.create(
			    amount      = cash,
			    currency    = "sgd",
			    source      = token,
			    description = description
			)

		except stripe.error.CardError as ce:
			return False, ce

		else:
			self.request.session["transaction_id"] = charge.id
			transaction = Transaction.objects.get_or_create(
				user=self.request.user,
				transaction_id=charge.id,
				success=True
				)[0]

			#saving the transaction as a record
			transaction.price=self.get_credit_cost()
			transaction.credit=self.get_credit()
			transaction.beforecredit=self.get_user_cred()
			transaction.aftercredit=int(self.get_user_cred()) + int(self.get_credit())
			transaction.save()
			#adding the credits to the account that the user has purchased
			credit = UserCredit.objects.get_or_create(
				user=self.request.user,
				)[0]

			credit.credit = int(self.get_user_cred()) + int(self.get_credit())
			credit.save()

			messages.success(request, "Thank you for your order. Please print this page.")
			
			return redirect("StripeInvoice")
	        # The payment was successfully processed, the user's card was charged.
	        # You can now redirect the user to another page or whatever you want



class StripeInvoice(LoginRequiredMixin, GetCheckoutMixin, TemplateView):
	template_name = 'invoice.html'

	def get_context_data(self, *args, **kwargs):
		context = super(StripeInvoice, self).get_context_data(*args, **kwargs)
		if self.request.user.is_authenticated:
			#retrieving contents of the transaction that the user has purchased
			context["user"] = self.get_transaction().user
			context["transaction_id"] = self.get_transaction().transaction_id
			context["price"] = self.get_transaction().price
			context["creditpurchased"] = self.get_transaction().credit
			context["currentcredit"] = self.get_transaction().aftercredit
			context["timestamp"] = self.get_transaction().timestamp
			messages.success(self.request, "You have succcessfully purchased " + str(self.get_transaction().credit) + " credits")
			del self.request.session["credit_id"]
			del self.request.session["transaction_id"]

		elif not self.request.user.is_authenticated:
			return Http404

		return context













# def payment_form(request):
#     context = { "stripe_key": settings.STRIPE_PUBLIC_KEY }
#     return render(request, "testpayment.html", context)


# def checkout(request):
#     # new_car = Car(
#     #     model = "Honda Civic",
#     #     year  = 2017
#     # )
#     if request.method == "POST":
#         token    = request.POST.get("stripeToken")

#     try:
#         charge  = stripe.Charge.create(
#             amount      = 2000,
#             currency    = "sgd",
#             source      = token,
#             description = "The product charged to the user"
#         )
#         # new_car.charge_id   = charge.id

#     except stripe.error.CardError as ce:
#         return False, ce

#     else:
#         # new_car.save()
#         return redirect("checkoutdone")
#         # The payment was successfully processed, the user's card was charged.
#         # You can now redirect the user to another page or whatever you want

# def checkoutfinish(request):
#     context = {}
#     return render(request, "testcheckoutdone.html", context)






class AddCredits(LoginRequiredMixin, GetCheckoutMixin, FormView):
	template_name = 'addcredit.html'
	form_class = CreditForm

	def get_context_data(self, *args, **kwargs):
		context = super(AddCredits, self).get_context_data(*args, **kwargs)
		context["usercred"] = self.get_user_cred()
		return context

	def form_valid(self, form):
		credit = form.cleaned_data.get("credit")
		credit_pack = get_object_or_404(CreditToCash, label=credit)
		#save session for the credit package selected
		self.request.session["credit_id"] = credit_pack.id
		return super(AddCredits, self).form_valid(form)

	def get_success_url(self):
		return reverse('CheckOut')


class CheckOut(LoginRequiredMixin, GetCheckoutMixin, TemplateView):
	template_name = 'checkout.html'

	def dispatch(self, *args, **kwargs):
		dispatch = super(CheckOut, self).dispatch(*args, **kwargs)
		#if credit package id is not selected to exit
		try:
			credit_id = self.request.session.get("credit_id")
		except:
			return reverse('Home')
		return dispatch

	def get_context_data(self, *args, **kwargs):
		context = super(CheckOut, self).get_context_data(*args, **kwargs)
		credit_id = self.request.session.get("credit_id")
		credit_pack = get_object_or_404(CreditToCash, id=credit_id)
		context["creditcost"] = credit_pack.cashprice
		context["credit"] = credit_pack.credits

		if self.request.user.is_authenticated():
			#creating user token for using checking out
			testuser = self.request.user
			user_checkout = UserCheckOut.objects.get_or_create(user=testuser)[0]
			user_checkout.user = self.request.user
			user_checkout.save()
			context["client_token"] = user_checkout.get_client_token()

		elif not self.request.user.is_authenticated():
			return Http404
		return context

	def get_success_url(self):
		return reverse('CheckOutFinal')


class CheckOutFinal(LoginRequiredMixin, GetCheckoutMixin, TemplateView):

	def dispatch(self, *args, **kwargs):
		dispatch = super(CheckOutFinal, self).dispatch(*args, **kwargs)
		#if credit package id is not selected to exit
		try:
			credit_id = self.request.session.get("credit_id")
		except:
			return reverse('Home')
		return dispatch

	def post(self, request, *args, **kwargs):
		# print request.POST
		nonce = request.POST.get("payment_method_nonce")

		if nonce:
			result = braintree.Transaction.sale({
					"amount":self.get_credit_cost(),
					"payment_method_nonce": nonce,
					# "billing":{
					#     "postal_code":"%s" %(order.billing_address.zipcode)
					# },
					"options":{
					"submit_for_settlement":True
					}
				})

			if result.is_success:
				self.request.session["transaction_id"] = result.transaction.id
				transaction = Transaction.objects.get_or_create(
					user=self.request.user,
					transaction_id=result.transaction.id,
					success=True
					)[0]

				#saving the transaction as a record
				transaction.price=self.get_credit_cost()
				transaction.credit=self.get_credit()
				transaction.beforecredit=self.get_user_cred()
				transaction.aftercredit=int(self.get_user_cred()) + int(self.get_credit())
				transaction.save()
				#adding the credits to the account that the user has purchased
				credit = UserCredit.objects.get_or_create(
					user=self.request.user,
					)[0]

				credit.credit = int(self.get_user_cred()) + int(self.get_credit())
				credit.save()

				messages.success(request, "Thank you for your order. Please print this page.")
				return redirect("Invoice")	 

			else:
				messages.warning(request, "There is a problem with your order")
				messages.warning(request, "%s" %(result.message))
				return redirect("CheckOut")


		return redirect("CheckOut")

		def get(self, request, *args, **kwargs):
			return redirect("Invoice")



class Invoice(LoginRequiredMixin, GetCheckoutMixin, TemplateView):
	template_name = 'invoice.html'

	def get_context_data(self, *args, **kwargs):
		context = super(Invoice, self).get_context_data(*args, **kwargs)
		if self.request.user.is_authenticated():
			#retrieving contents of the transaction that the user has purchased
			context["user"] = self.get_transaction().user
			context["transaction_id"] = self.get_transaction().transaction_id
			context["price"] = self.get_transaction().price
			context["creditpurchased"] = self.get_transaction().credit
			context["currentcredit"] = self.get_transaction().aftercredit
			context["timestamp"] = self.get_transaction().timestamp
			messages.success(self.request, "You have succcessfully purchased " + str(self.get_transaction().credit) + " credits")
			del self.request.session["credit_id"]
			del self.request.session["transaction_id"]

		elif not self.request.user.is_authenticated():
			return Http404

		return context




