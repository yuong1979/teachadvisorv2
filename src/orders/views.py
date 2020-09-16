from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.views.generic import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, FormMixin
from teacher.models import Teacher
from student.models import Student
from opening.models import Opening
from orders.models import Order
from messaging.models import Message
from billing.models import UserCredit
from billing.control import orderadd
from opening.forms import PriceForm
from tags.models import BlockUser, ViewTeacherRecord
from notifications.signals import notify
from mixins.mixins import LoginRequiredMixin, GetDetailsMixin, CheckBlk
from django.db.models import Q
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
import time
import braintree
import datetime

todate = datetime.datetime.now().date()



if settings.DEBUG:
    braintree.Configuration.configure(braintree.Environment.Sandbox,
        merchant_id = settings.BRAINTREE_MERCHANT_ID,
        public_key = settings.BRAINTREE_PUBLIC,
        private_key = settings.BRAINTREE_PRIVATE)


# def Test(request):
#     # run the function below for 5 seconds
#     t_end = time.time() + 5 * 1
#     while time.time() < t_end:
#         print "Do not interrupt"
#     return redirect("Home")


def OrderDetail(request):
    request.session["msg_id"] = request.GET.get("msg_id")
    return redirect("OrderDetailView")


class OrderDetailView(LoginRequiredMixin, TemplateView):
    model = Order
    template_name = 'orders/order_detail.html'

    def get_context_data(self, *args, **kwargs):

        msg_id = self.request.session.get("msg_id")
        msg = Message.objects.get(id=msg_id)

        try:
            teacher = msg.senduser.teacher
            student = msg.touser.student
        except:
            teacher = msg.touser.teacher
            student = msg.senduser.student

        opening = msg.re_opening
        order = Order.objects.get(oteacher=teacher, ostudent=student, oopening=opening, teacherorder=True, studentorder=True)
        context = super(OrderDetailView, self).get_context_data(*args, **kwargs)
        context["msg"] = msg
        context["id"] = order.id
        context["teacher"] = order.oteacher
        context["student"] = order.ostudent
        context["opening"] = order.oopening
        context["price"] = order.price
        context["status"] = order.status
        context["datetime"] = order.timestamp
        context["subject"] = order.oopening.subject
        context["level"] = order.oopening.level
        context["region"] = order.oopening.region
        context["group_tuition"] = order.oopening.group_tuition

        return context





# class OrderListView(LoginRequiredMixin, ListView):
#     model = Order
#     template_name = 'orders/order_list.html'
#     # success_url = '/'
#     # title = 'List'

#     def get_queryset(self, *args, **kwargs):
#         qs = super(OrderListView, self).get_queryset(**kwargs).filter()

#         try:
#             user = self.request.user.student
#             qs = Order.objects.filter(Q(ostudent=user)).order_by('-id')
#             # qs = Order.objects.filter(Q(ostudent=user) & Q(status='In Progress'))
#         except:
#             user = self.request.user.teacher
#             qs = Order.objects.filter(Q(oteacher=user)).order_by('-id')
#             # qs = Order.objects.filter(Q(ostudent=user) & Q(status='In Progress'))
#         # else:
#         #     return Http404
#         return qs






def AppOffConf(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    parent_msg_id = msg.parent_id
    msg = get_object_or_404(Message, pk=parent_msg_id)
    request.session["msg_id"] = msg.id
    return redirect("OpeningConfirmAppOff")

class OpeningConfirmAppOff(LoginRequiredMixin, GetDetailsMixin, FormMixin, TemplateView):
    template_name = 'opening/opening_confirm_appoff.html'
    form_class = PriceForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        #if request user is student to check if they are offering more then one person
        result = CheckOfferExit(request=self.request, opening=self.get_opening(), student=self.get_student())
        if result:
            return result
        result = OrderExit(request=self.request, opening=self.get_opening(), student=self.get_student(), teacher=self.get_teacher())
        if result:
            return result
        return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context = super(OpeningConfirmAppOff, self).get_context_data(*args, **kwargs)
        context["opening"] = self.get_opening()

        try:
            test = self.request.user.student
            context["type"] = "Offer"
        except:
            test = self.request.user.teacher
            context["type"] = "Application"

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            price = form.cleaned_data.get("price")
            new_order, created = Order.objects.get_or_create(
              ostudent=self.get_student(),
              oteacher=self.get_teacher(),
              oopening=self.get_opening(),
              omessage=self.get_msg(),
              )
            try:
                test = self.request.user.student
                new_order.studentorder=True
                new_order.teacherorder=False
                new_order.price=price
                new_order.status="Offer"
                new_order.save()
                mtype="offer"
            except:
                test = self.request.user.teacher
                new_order.studentorder=False
                new_order.teacherorder=True
                new_order.price=price
                new_order.status="Application"
                new_order.save()
                mtype="application"

            if created:
                Counter=False
            else:
                Counter=True
            MsgAppOffSave(student=self.get_student(), teacher=self.get_teacher(), opening=self.get_opening(), price=price, mtype=mtype, counter=Counter, accepted=False)

            return self.form_valid(form)

    def get_success_url(self):
        msg = self.get_msg()
        messages.success(self.request, "Your offer has been sent.")
        return reverse('MessageDetail', kwargs={'pk': msg.id})





def WithConf(request, pk):
    #if both student and teacher has accepted, you cannot withdraw, you can only cancel
    msg_id = request.GET.get("msg_id")
    request.session["msg_id"] = msg_id
    return redirect("Withdraw")

class Withdraw(LoginRequiredMixin, GetDetailsMixin, TemplateView):
    template_name = 'opening/opening_withdraw.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        result = WithExit(request=self.request, opening=self.get_opening(), student=self.get_student(), teacher=self.get_teacher())
        if result:
            return result

        return self.render_to_response(context)


    def get_context_data(self, *args, **kwargs):
        context = super(Withdraw, self).get_context_data(*args, **kwargs)
        context["opening"] = self.get_opening()

        try:
            user = self.request.user.teacher
            context["type"] = "application"
        except:
            user = self.request.user.student
            context["type"] = "offer"

        context["msg"] = self.get_msg()
        return context

    def post(self, request, *args, **kwargs):

        opening = self.get_opening()
        student = self.get_student()
        teacher = self.get_teacher()
        msg = self.get_msg()


        #change the message back to message instead of anything else
        #overwrite the mainmessage status
        if msg.msgtype != "Messaged":
            p_id = msg.parent_id
            mainmessage = get_object_or_404(Message, id=p_id)
            mainmessage.msgtype = "Messaged"
            mainmessage.save()

        #delete the message
        msg.delete()


        #delete the order
        order = get_object_or_404(Order, oopening=opening, ostudent=student, oteacher=teacher)
        order.delete()
        return redirect("MessageDetail", pk=msg.parent_id)









#goes to the accept confirmation page where user can confirm the acceptance of offer
def AcceptConf(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    parent_msg_id = msg.parent_id
    msg = get_object_or_404(Message, pk=parent_msg_id)
    request.session["msg_id"] = msg.id
    return redirect("Accept")

class Accept(LoginRequiredMixin, GetDetailsMixin, TemplateView):
    template_name = 'opening/opening_accept.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        #if request user is student to check if they are offering more then one person
        result = CheckOfferExit(request=self.request, opening=self.get_opening(), student=self.get_student())
        if result:
            return result

        result = OrderExit(request=self.request, opening=self.get_opening(), student=self.get_student(), teacher=self.get_teacher())
        if result:
            return result

        return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context = super(Accept, self).get_context_data(*args, **kwargs)
        context["opening"] = self.get_opening()

        curr_order = Order.objects.get(
          ostudent=self.get_student(),
          oteacher=self.get_teacher(),
          oopening=self.get_opening(),
          omessage=self.get_msg(),
          )

        context["order"] = curr_order
        return context

    #confirms the order
    def post(self, request, *args, **kwargs):

        price = request.POST.get("price_id")

        msg_id = self.request.session.get("msg_id")

        opening = self.get_opening()
        curr_order = Order.objects.get(
          ostudent=self.get_student(),
          oteacher=self.get_teacher(),
          oopening=self.get_opening(),
          omessage=self.get_msg(),
          )


        try:
            test = self.request.user.teacher
            curr_order.teacherorder=True
            curr_order.status="Job In Progress"

            curr_order.subject=self.get_opening().subject
            curr_order.level=self.get_opening().level
            curr_order.tutor_rating=self.get_teacher().review_score
            curr_order.grp_tuition=self.get_opening().group_tuition
            curr_order.expertise=self.get_teacher().expertise_type
            curr_order.years_of_exp=self.get_teacher().years_of_experience
            curr_order.location=self.get_opening().region

            curr_order.save()
            opening.job_active = False
            opening.save()
            MsgAppOffSave(student=self.get_student(), teacher=self.get_teacher(), opening=self.get_opening(), price=price, mtype="application", counter=False, accepted=True)
            messages.success(self.request, "You have accepted this offer. Please refer to your orders and select complete when you finish this tuition job for student's review")
        except:
            pass

        try:
            test = self.request.user.student
            curr_order.studentorder=True
            curr_order.status="Job In Progress"

            curr_order.subject=self.get_opening().subject
            curr_order.level=self.get_opening().level
            curr_order.tutor_rating=self.get_teacher().review_score
            curr_order.grp_tuition=self.get_opening().group_tuition
            curr_order.expertise=self.get_teacher().expertise_type
            curr_order.years_of_exp=self.get_teacher().years_of_experience
            curr_order.location=self.get_opening().region

            curr_order.save()
            opening.job_active = False
            opening.save()
            MsgAppOffSave(student=self.get_student(), teacher=self.get_teacher(), opening=self.get_opening(), price=price, mtype="offer", counter=False, accepted=True)
            messages.success(self.request, "You have accepted this application. When the tutor has completed you will be updated and be able to review tutor's performance")
        except:
            pass

        teacheruser = self.get_teacher().user
        teacherusercred = get_object_or_404(UserCredit, user=teacheruser)
        teacherusercred.credit = teacherusercred.credit + orderadd
        teacherusercred.save()    

        studentuser = self.get_student().user
        studentusercred = get_object_or_404(UserCredit, user=studentuser)
        studentusercred.credit = studentusercred.credit + orderadd
        studentusercred.save()

        messages.success(self.request, "Thank you for accepting, both tutor and student has been awarded " + str(orderadd) + " credits for using this service")

        return redirect("MessageDetail", pk=msg_id)






 

 



def MsgAppOffSave(student, teacher, opening, price, mtype, counter, accepted):



    #delete the last offer or application if counteroffer is selected
    if counter==True:
        try:
            msg = Message.objects.filter(senduser=teacher.user, touser=student.user, re_opening=opening, mainmessage=False, msgtype="Application")
            msg.delete()
            msg = Message.objects.filter(senduser=student.user, touser=teacher.user, re_opening=opening, mainmessage=False, msgtype="Offer")
            msg.delete()
        except:
            msg = Message.objects.filter(senduser=student.user, touser=teacher.user, re_opening=opening, mainmessage=False, msgtype="Offer")
            msg.delete()
            msg = Message.objects.filter(senduser=teacher.user, touser=student.user, re_opening=opening, mainmessage=False, msgtype="Application")
            msg.delete()

    #if counter offer/application update application of offer message with counter
    if counter==True:
        offertitle = "Offer for job of the " + str(opening)
        applytitle = "Application for the job of a " + str(opening)
        offercontent = "COUNTER OFFER: " + str(student.first_name) + " has offered the job of the " + str(opening) + " at $" + str(price) + "/Hour. This order is currently pending acceptance from " + str(teacher.first_name) + " ."
        applycontent = "COUNTER OFFER: " + str(teacher.first_name) + " has applied for the job of the " + str(opening) + " at $" + str(price) + "/Hour. This order is currently pending acceptance from " + str(student.first_name) + " ."
        if mtype == "offer":
            new_msg = Message.objects.get_or_create(
                senduser=student.user,
                touser=teacher.user,
                title="Offer for job of the " + str(opening),
                re_opening=opening,
                content=offercontent,
                msgtype="Offer",
                )[0]
            #relabeling the mainmessage
            RelabelMain(student=student.user, teacher=teacher.user, re_opening=opening, new_msg=new_msg)
            #updating notifications
            notify.send(sender=student.user, recipient=teacher.user, action='Offer', message=new_msg)
        if mtype == "application":
            new_msg = Message.objects.get_or_create(
                senduser=teacher.user,
                touser=student.user,
                title="Application for the job of a " + str(opening),
                re_opening=opening,
                content=applycontent,
                msgtype="Application"
                )[0]
            #relabeling the mainmessage
            RelabelMain(student=student.user, teacher=teacher.user, re_opening=opening, new_msg=new_msg)
            #updating notifications
            notify.send(sender=teacher.user, recipient=student.user, action='Application', message=new_msg)



    #if counter offer/application for the first time
    if counter==False:
        if accepted == False:
            offertitle = "Offer for job of the " + str(opening)
            applytitle = "Application for the job of a " + str(opening)
            offercontent = "OFFER: " + str(student.first_name) + " has offered the job of the " + str(opening) + " at $" + str(price) + "/Hour. This order is currently pending acceptance from " + str(teacher.first_name) + " ."
            applycontent = "APPLICATION: " + str(teacher.first_name) + " has applied for the job of the " + str(opening) + " at $" + str(price) + "/Hour. This order is currently pending acceptance from " + str(student.first_name) + " ."

            if mtype == "offer":
                new_msg = Message.objects.get_or_create(
                    senduser=student.user,
                    touser=teacher.user,
                    title="Offer for job of the " + str(opening),
                    re_opening=opening,
                    content=offercontent,
                    msgtype="Offer",
                    )[0]
                #relabeling the mainmessage
                RelabelMain(student=student.user, teacher=teacher.user, re_opening=opening, new_msg=new_msg)
                #updating notifications
                notify.send(sender=student.user, recipient=teacher.user, action='Offer', message=new_msg)

            if mtype == "application":
                new_msg = Message.objects.get_or_create(
                    senduser=teacher.user,
                    touser=student.user,
                    title="Application for the job of a " + str(opening),
                    re_opening=opening,
                    content=applycontent,
                    msgtype="Application"
                    )[0]
                #relabeling the mainmessage
                RelabelMain(student=student.user, teacher=teacher.user, re_opening=opening, new_msg=new_msg)
                #updating notifications
                notify.send(sender=teacher.user, recipient=student.user, action='Application', message=new_msg)

    #if application or offer is accepted
        if accepted == True:
            offertitle = "Job of the " + str(opening) + " accepted"
            applytitle = "Job of the " + str(opening) + " accepted"
            offercontent = "ACCEPTED: " + str(student.first_name) + " has accepted " + str(opening) + " at $" + str(price) + "/Hour. This order is in progress."
            applycontent = "ACCEPTED: " + str(teacher.first_name) + " has accepted " + str(opening) + " at $" + str(price) + "/Hour. This order is in progress."

            if mtype == "offer":
                new_msg = Message.objects.get_or_create(
                    senduser=student.user,
                    touser=teacher.user,
                    title="Offer for job of the " + str(opening),
                    re_opening=opening,
                    content=offercontent,
                    msgtype="Job In Progress",
                    )[0]
                #relabeling the mainmessage
                RelabelMain(student=student.user, teacher=teacher.user, re_opening=opening, new_msg=new_msg) 
                #updating notifications
                notify.send(sender=student.user, recipient=teacher.user, action='Acceptance', message=new_msg)

            if mtype == "application":
                new_msg = Message.objects.get_or_create(
                    senduser=teacher.user,
                    touser=student.user,
                    title="Application for the job of a " + str(opening),
                    re_opening=opening,
                    content=applycontent,
                    msgtype="Job In Progress"
                    )[0]
                #relabeling the mainmessage
                RelabelMain(student=student.user, teacher=teacher.user, re_opening=opening, new_msg=new_msg)
                #updating notifications
                notify.send(sender=teacher.user, recipient=student.user, action='Acceptance', message=new_msg)

    return None







def RelabelMain(student, teacher, re_opening, new_msg):

    try:
        msg = Message.objects.get(
            senduser=student, 
            touser=teacher,
            re_opening=re_opening,
            mainmessage=True)

    except:
        msg = Message.objects.get(
            senduser=teacher, 
            touser=student,
            re_opening=re_opening,
            mainmessage=True)

    parent_id = msg.parent_id
    maintitle = msg.title

    new_msg.title=maintitle
    new_msg.mainmessage=False
    new_msg.parent_id=parent_id
    new_msg.save()


    #updating the viewteacherrecords
    vtr = ViewTeacherRecord.objects.get_or_create(teacher=teacher.teacher, date=todate)[0]
    orderc = Order.objects.filter(oteacher=teacher.teacher, teacherorder=True, studentorder=True).count()
    vtr.ordercount = orderc
    vtr.save()


    #overwrite the mainmessage status so that on the filter it can filter for all "completed" or all "reviewed"...
    if new_msg.msgtype != "Messaged":
        nmsgtype = new_msg.msgtype
        p_id = new_msg.parent_id
        mainmessage = get_object_or_404(Message, id=p_id)
        mainmessage.msgtype = nmsgtype
        mainmessage.save()





# if it is already offered then exit student can only offer job to one person
def CheckOfferExit(request, opening, student):
    try:
        test = request.user.student
        offercount = Order.objects.filter(ostudent=student,oopening=opening,studentorder=True).count()
        if offercount > 0:
            try:
                msg = Message.objects.get(re_opening=opening, mainmessage=True, msgtype="Offer")
            except:
                msg = Message.objects.get(re_opening=opening, mainmessage=True, msgtype="Job In Progress")
            messages.warning(request, "You can only offer opening to one tutor")
            return redirect("MessageDetail", pk=msg.parent_id)
    except:
        pass



# if the apply or offer or reject button is selected, the conditions below are checked, if it meets any the user action is disallowed and the function exits
def OrderExit(request, opening, student, teacher):

    if Order.objects.filter(oopening=opening, status="Job In Progress").exists():
        try:
            msg = Message.objects.filter(senduser=student.user , touser=teacher.user , re_opening=opening).first()
        except:
            msg = Message.objects.filter(senduser=teacher.user , touser=student.user , re_opening=opening).first()
        messages.warning(request, "This order is in progress")
        return redirect("MessageDetail", pk=msg.parent_id)

    if opening.job_active == False:
        messages.warning(request,"The opening " + str(opening) + " is no longer available")
        return redirect("Home")

    if Order.objects.filter(oopening=opening, status="Completed").exists():
        messages.warning(request, "This order has been completed")
        return redirect("Home")

    if Order.objects.filter(oopening=opening, status="Canceled").exists():
        messages.warning(request, "This order has been canceled")
        return redirect("Home")

    #exit if the user has been blocked
    result = CheckBlk(request=request, user1=student.user, user2=teacher.user)
    if result:
        return result

    try:
        test = request.user.student
        if Order.objects.filter(oopening=opening, oteacher=teacher, ostudent=student, studentorder=True).exists():
            msg = Message.objects.get(senduser=student.user , touser=teacher.user , re_opening=opening, msgtype="Offer")
            messages.warning(request, "You have made the offer for this opening to " + str(teacher))
            return redirect("MessageDetail", pk=msg.parent_id)
    except:
        pass
    try:
        test = request.user.teacher
        if Order.objects.filter(oopening=opening, oteacher=teacher, ostudent=student, teacherorder=True).exists():
            msg = Message.objects.get(touser=student.user , senduser=teacher.user , re_opening=opening, msgtype="Application")
            messages.warning(request, "You have applied for " + str(opening))
            return redirect("MessageDetail", pk=msg.parent_id)
    except:
        pass

    return None




def WithExit(request, opening, student, teacher):

    if Order.objects.filter(oopening=opening, status="Job In Progress").exists():
        try:
            msg = Message.objects.filter(senduser=student.user , touser=teacher.user , re_opening=opening).first()
        except:
            msg = Message.objects.filter(senduser=teacher.user , touser=student.user , re_opening=opening).first()
        messages.warning(request, "This order is in progress")
        return redirect("MessageDetail", pk=msg.parent_id)

    if opening.job_active == False:
        messages.warning(request,"The opening " + str(opening) + " is no longer available")
        return redirect("Home")

    if Order.objects.filter(oopening=opening, status="Completed").exists():
        messages.warning(request, "This order has been completed")
        return redirect("Home")

    if Order.objects.filter(oopening=opening, status="Canceled").exists():
        messages.warning(request, "This order has been canceled")
        return redirect("Home")

    #exit if the user has been blocked
    result = CheckBlk(request=request, user1=student.user, user2=teacher.user)
    if result:
        return result

    return None

