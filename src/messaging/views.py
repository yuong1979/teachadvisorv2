from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, ModelFormMixin
from django.views.generic import TemplateView
from student.models import Student
from teacher.models import Teacher
from opening.models import Opening
from messaging.models import Message
from orders.models import Order
from orders.views import CheckOfferExit
from mixins.mixins import CheckBlk
from billing.models import UserCredit
from billing.control import msgcredit
from tags.models import BlockUser, ViewTeacherRecord
from messaging.forms import PostMessage, PostReply
from notifications.signals import notify
from mixins.mixins import LoginRequiredMixin
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.urls import reverse
# from django.conf import settings
# from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
import datetime

todate = datetime.datetime.now().date()


class PostMessageView(LoginRequiredMixin,FormView):
	template_name = 'msg_first.html'
	form_class = PostMessage
	success_url = '/messagelistall/'
	title = 'Message Box'

	def get_recipient(self):
		msg_user_id = self.request.session.get("user_id")

		try:
			recipient = Teacher.objects.get(user_id=msg_user_id)

		except Teacher.DoesNotExist:
			recipient = Student.objects.get(user_id=msg_user_id)#.user

		except Exception:
			raise Http404

		return recipient


	def get_opening(self):
		opening_id = self.request.session.get("opening_id")
		opening = Opening.objects.filter(id=opening_id).first()
		return opening

	def dispatch(self, request, *args, **kwargs): #exit the class if the user_id or opening_id has nothing in it

		user1 = self.request.user
		user2 = self.get_recipient().user
		opening = self.get_opening()

		result = checkmsg(request, user1, user2, opening)
		if result:
			return result

		try:
			self.request.session["user_id"]
			self.request.session["opening_id"]
		except:
			return redirect('Home')

		return super(PostMessageView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		"""This method is what injects forms with their keyword
		arguments."""

		try:
			test = self.request.user.student
			user = "student"
		except:
			user = "teacher"
		# grab the current set of form #kwargs
		kwargs = super(PostMessageView, self).get_form_kwargs()
		# Update the kwargs with the user_id, so that it can be pushed as a parameter into the form
		kwargs['user_type'] = user
		return kwargs


	def form_valid(self, form):

		#exit if the user has been blocked
		result = CheckBlk(request=self.request, user1=self.request.user, user2=self.get_recipient().user)
		if result:
			return result

		#take credits off if you are a tutor pass if you are a student
		try:
			self.request.user.teacher
			user = self.request.user
			usercred = get_object_or_404(UserCredit, user=user)

			if usercred.credit - msgcredit < 0:
				messages.warning(self.request, "You do not have any more credits please purchase some!")
				return redirect("Home")
			else:
				usercred.credit = usercred.credit - msgcredit
				usercred.save()
		except:
			pass

		# updating message
		i = form.save(commit=False)
		i.senduser = self.request.user
		i.touser = self.get_recipient().user
		i.title = form.cleaned_data.get("title")
		i.re_opening = self.get_opening()
		i.content = form.cleaned_data.get("content")
		i.msgtype = "Messaged"
		i.mainmessage = True
		i.save()
		i.parent_id = i.id
		i.paid = "True"
		i.save()



		#updating the viewteacherrecords
		try:
			#from teacher to student
			teacher = self.request.user.teacher
			student = self.get_recipient().user
			vtr = ViewTeacherRecord.objects.get_or_create(teacher=teacher, date=todate)[0]
			msgc = Message.objects.filter(mainmessage=True, date=todate).exclude(touser=teacher.user).count()
			vtr.msgtocount = msgc
			vtr.save()

		except:
			#from student to teacher
			teacher = self.get_recipient().user.teacher
			student = self.request.user
			vtr = ViewTeacherRecord.objects.get_or_create(teacher=teacher, date=todate)[0]
			msgc = Message.objects.filter(touser=teacher.user, mainmessage=True, date=todate).count()
			vtr.msgfromcount = msgc
			vtr.save()


		self.request.session["msg_id"] = i.id

		#updating notifications
		notify.send(sender=i.senduser, recipient=i.touser, action='Messaged', message=i)
		del self.request.session["opening_id"]
		del self.request.session["user_id"]

		return super(PostMessageView, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(PostMessageView, self).get_context_data(*args, **kwargs)
		context["title"] = self.title
		context["submit_btn_value"] = "Send"
		context["recipient"] = self.get_recipient().first_name
		context["opening"] = self.get_opening()
		return context

	def get_success_url(self):
		msg_id = self.request.session.get("msg_id")
		del self.request.session["msg_id"]
		messages.success(self.request, "Message sent!")
		messages.success(self.request, "Please discuss the tuition rates / location/ dates / by cash or cheque")
		return reverse('MessageDetail', kwargs={'pk': msg_id})




#listing all messages
class MessageListViewAll(LoginRequiredMixin,ListView):
	model = Message
	template_name = 'msg_list.html'
	success_url = '/'
	title = 'List'
	paginate_by = 10

	def get_queryset(self, *args, **kwargs):
		qs = super(MessageListViewAll, self).get_queryset(**kwargs).filter()
		r_user = self.request.user
		qs = Message.objects.filter(
			Q(senduser=r_user) | 
			Q(touser=r_user), mainmessage=True).order_by('-timestamp')
		return qs

	def get_context_data(self, *args, **kwargs):
		context = super(MessageListViewAll, self).get_context_data(*args, **kwargs)
		context["title"] = "All"
		return context


#listing messages only
class MessageListViewMsg(LoginRequiredMixin,ListView):
	model = Message
	template_name = 'msg_list.html'
	success_url = '/'
	title = 'List'
	paginate_by = 10

	def get_queryset(self, *args, **kwargs):
		qsm = super(MessageListViewMsg, self).get_queryset(**kwargs).filter()
		r_user = self.request.user
		qsm = Message.objects.filter(
			Q(senduser=r_user) | 
			Q(touser=r_user), mainmessage=True, msgtype__in=["Messaged"]).order_by('-timestamp')
		return qsm

	def get_context_data(self, *args, **kwargs):
		context = super(MessageListViewMsg, self).get_context_data(*args, **kwargs)
		context["title"] = "Msg"
		return context

#listing proposals only
class MessageListViewPpl(LoginRequiredMixin,ListView):
	model = Message
	template_name = 'msg_list.html'
	success_url = '/'
	title = 'List'
	paginate_by = 10

	def get_queryset(self, *args, **kwargs):
		qsp = super(MessageListViewPpl, self).get_queryset(**kwargs).filter()
		r_user = self.request.user
		qsp = Message.objects.filter(
			Q(senduser=r_user) | 
			Q(touser=r_user), mainmessage=True, msgtype__in=["Offer","Application"]).order_by('-timestamp')
		return qsp

	def get_context_data(self, *args, **kwargs):
		context = super(MessageListViewPpl, self).get_context_data(*args, **kwargs)
		context["title"] = "Ppl"
		return context

#listing work in progress only
class MessageListViewWip(LoginRequiredMixin,ListView):
	model = Message
	template_name = 'msg_list.html'
	success_url = '/'
	title = 'List'
	paginate_by = 10

	def get_queryset(self, *args, **kwargs):
		qsw = super(MessageListViewWip, self).get_queryset(**kwargs).filter()
		r_user = self.request.user
		qsw = Message.objects.filter(
			Q(senduser=r_user) | 
			Q(touser=r_user), mainmessage=True, msgtype__in=["Job In Progress"]).order_by('-timestamp')
		return qsw

	def get_context_data(self, *args, **kwargs):
		context = super(MessageListViewWip, self).get_context_data(*args, **kwargs)
		context["title"] = "Wip"
		return context

#listing work that has been done only
class MessageListViewDon(LoginRequiredMixin,ListView):
	model = Message
	template_name = 'msg_list.html'
	success_url = '/'
	title = 'List'
	paginate_by = 10

	def get_queryset(self, *args, **kwargs):
		qsd = super(MessageListViewDon, self).get_queryset(**kwargs).filter()
		r_user = self.request.user
		qsd = Message.objects.filter(
			Q(senduser=r_user) | 
			Q(touser=r_user), mainmessage=True, msgtype__in=["Completed","Reviewed","Canceled"]).order_by('-timestamp')
		return qsd

	def get_context_data(self, *args, **kwargs):
		context = super(MessageListViewDon, self).get_context_data(*args, **kwargs)
		context["title"] = "Don"
		return context

# "Completed","Reviewed","Canceled"
# "Job In Progress"


# order_status = (
# 		('Inactive', 'Inactive'),
# 		('Messaged', 'Messaged'),
# 		('Rejected', 'Rejected'),
# 		('Application', 'Application'),
# 		('Offer', 'Offer'),
# 		('Job In Progress', 'Job In Progress'),
# 		('Completed', 'Completed'),
# 		('Canceled', 'Canceled'),
# 		('Reviewed', 'Reviewed'),
# 	)







class MessageDetailView(LoginRequiredMixin,ModelFormMixin, DetailView):
	model = Message
	template_name = 'msg_detail.html'
	success_url = '/messagelistall/'
	title = 'Message Box Details'
	form_class = PostReply
	# success_url = reverse_lazy('success')

	def get_context_data(self, **kwargs):
		context = super(MessageDetailView, self).get_context_data(**kwargs)
		instance = self.get_object()
		mainmessage = Message.objects.filter(id=instance.parent_id)
		message = Message.objects.filter(parent_id=instance.parent_id).exclude(id=instance.parent_id).order_by('timestamp')

		try:
			test = self.request.user.student
			if self.request.user == instance.senduser:
				obj = instance.touser.teacher
			else:
				obj = instance.senduser.teacher
			modelobj = "Tutor"
		except:
			test = self.request.user.teacher
			obj = instance.re_opening
			modelobj = "Tuition Job"


		context['obj'] = obj
		context['modelobj'] = modelobj
		context['form'] = self.form_class()
		context["mainmessage"] = mainmessage
		context["message"] = message
		context["title"] = self.title
		context["submit_btn_value"] = "Send Reply"


		if instance.senduser == self.request.user:
			user = instance.senduser
			ouser = instance.touser
		else:
			user = instance.touser
			ouser = instance.senduser


        #is it favorited by current user?
		context["blocker"] = "Block"
		if BlockUser.objects.filter(blocker = user).first() != None:
			if BlockUser.objects.filter(blocker = user).first().blocked.filter(id=ouser.id).first() != None:
				context["blocker"] = "Unblock"


		# try:
		# 	test = BlockUser.objects.get(blocker = user).blocked.get(blocked_u__blocked=ouser)
		# 	context["blocker"] = "Unblock User"
		# except:
		# 	context["blocker"] = "Block User"

		return context

	def post(self, request, *args, **kwargs):

		instance = self.get_object()
		form = self.get_form()
		parent_id = instance.parent_id
		msg_id = instance.id
		senduser = request.user
		touser_obj = Message.objects.get(id=instance.parent_id)

		if touser_obj.touser == senduser:
			touser = touser_obj.senduser
		else:
			touser = touser_obj.touser

		#exit if the user has been blocked
		result = CheckBlk(request=self.request, user1=touser, user2=senduser)
		if result:
			return result

		if form.is_valid():

			i = form.save(commit=False)
			i.senduser = senduser
			i.touser = touser
			i.title = touser_obj.title
			i.re_opening = instance.re_opening
			i.content = form.cleaned_data.get("content")
			i.msgtype = "Messaged"
			i.mainmessage = False
			i.parent_id = parent_id
			i.save()

			#Update the message so that the time of the message is updated and when sorted by datetime the message goes to the top
			mainmessage = get_object_or_404(Message, id=parent_id)
			mainmessage.msgtype = "Messaged"
			mainmessage.save()

			#updating notifications
			notify.send(sender=senduser, recipient=touser, action='Messaged', message=i)
			messages.success(self.request, "Reply sent!")
			return redirect("MessageDetail", pk=msg_id)

		raise Http404






def checkmsg(request, user1, user2, opening):
	#check if message exists if it exists to go to that message if its rejected to redirect
	try:
		try:
			test = Message.objects.get(
				senduser=user1, 
				touser=user2,
				re_opening=opening,
				mainmessage=True)
			messages.warning(request, "Please send your message here")
			return redirect("MessageDetail", pk=test.parent_id)

		except:
			test = Message.objects.get(
				senduser=user2, 
				touser=user1,
				re_opening=opening,
				mainmessage=True)
			messages.warning(request, "Please send your message here")
			return redirect("MessageDetail", pk=test.parent_id)

	except:
		pass

	#if message has been closed already - to redirect
	if opening.job_active == False:
		messages.warning(request, "This tuition job is closed")
		return redirect("TeacherList")

	#getting the hiring student to see if he has offered more then once
	try:
		testu = user1.student
		student = user1
		teacher = user2
	except:
		testu = user1.teacher
		teacher = user1
		student = user2

	student_obj = get_object_or_404(Student, user=student)

	#if request user is student to check if they are offering more then one person
	result = CheckOfferExit(request=request, opening=opening, student=student_obj)
	if result:
		return result

	return None







#let the user block some other user
def BlockSub(request, pk):

	blkmsg = get_object_or_404(Message, id=pk)

	if request.user == blkmsg.touser:
		blocked = blkmsg.senduser
		blocker = blkmsg.touser
	else:
		blocked = blkmsg.touser
		blocker = blkmsg.senduser

	#adding a block entry in case it doesnt exist for users doing the blocking for the first time
	try: 
		BlockUser.objects.get(blocker = blocker)
	except:
		obj = BlockUser.objects.get_or_create(blocker_id=blocker.id)[0]

	if BlockUser.objects.get(blocker = blocker).blocked.filter(id=blocked.id).first() != None:
		obj = BlockUser.objects.get(blocker_id=blocker.id)
		obj.blocked.remove(blocked.id)
		obj.save
		messages.info(request, str(blocked) + " Unblocked.")
	else:
		obj = BlockUser.objects.get_or_create(blocker_id=blocker.id)[0]
		obj.blocked.add(blocked.id)
		obj.save
		messages.info(request, str(blocked) + " blocked and will not be able to send you messages.")

	return HttpResponseRedirect(blkmsg.get_absolute_url())







#displays a list of openings that the company wants to message the worker about
class OpeningSelectMsg(LoginRequiredMixin, TemplateView):
    template_name = 'opening/opening_select_msg.html'

    def get_context_data(self, *args, **kwargs):
        context = super(OpeningSelectMsg, self).get_context_data(*args, **kwargs)
        context["openings_list"] = self.request.user.opening_set.filter(job_active=True)
        return context

#lets the student select an opening to message the worker about
def Oselectmsgc(request):
    request.session["opening_id"] = request.POST.get("opening_id")
    return redirect("Messaging")


#lets the worker select an opening to message the company about about
def Oselectmsgw(request, pk):
    request.session["opening_id"] = pk
    return redirect("Messaging")




