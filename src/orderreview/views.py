from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, ListView
from teacher.models import Teacher
from billing.models import UserCredit
from billing.control import reviewadd
from orders.models import Order
from orderreview.models import ReviewTeacher
from messaging.models import Message
from orderreview.forms import OrderCancelReviewForm, OrderCompleteReviewForm, ReviewFormComment
from notifications.signals import notify
from mixins.mixins import LoginRequiredMixin, GetDetailsMixin
from django.contrib import messages
from django.urls import reverse



#Create your views here.

def Finish(request):
    try:
        test = request.user.student
        request.session["order_id"] = request.POST.get("order_id")
        request.session["msg_id"] = request.POST.get("msg_id")
        return redirect("OrderCancelReview")
    except:
        test = request.user.teacher
        request.session["order_id"] = request.POST.get("order_id")
        request.session["msg_id"] = request.POST.get("msg_id")
        return redirect("OrderCompleteConfirm")



class OrderCompleteConfirm(LoginRequiredMixin, GetDetailsMixin, TemplateView):
    template_name = 'review/order_complete_conf.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        #if id is not selected to exit
        try:
            order_id = self.request.session.get("order_id")
            msg_id = self.request.session.get("msg_id")
        except:
            return redirect('Home')

        completeorder = Order.objects.get(pk=order_id)

        #if review already exists to exit
        try:
            test = ReviewTeacher.objects.get(opening = completeorder.oopening)
            messages.warning(self.request,"You have already reviewed " + str(opening))
            return redirect('Home')
        except:
            pass
        return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        context = super(OrderCompleteConfirm, self).get_context_data(**kwargs)
        context["title"] = "Please confirm that you have completed"
        context["opening"] = self.get_order().oopening
        context["msg"] = self.get_msg()
        return context


    def post(self, request, *args, **kwargs):
        subject = self.get_order().oopening.subject
        level = self.get_order().oopening.level
        grp_tuition = self.get_order().oopening.group_tuition
        price = self.get_order().price
        student = self.get_order().ostudent
        teacher = self.get_order().oteacher
        opening = self.get_order().oopening
        parent_id = self.get_msg().parent_id
        parent_title = self.get_msg().title
        completemsg = self.get_msg()

        #updating the order status
        order = self.get_order()
        order.status = "Completed"
        order.save()

        #updating the msg
        new_msg = Message.objects.get_or_create(
            senduser=teacher.user,
            touser=student.user,
            title=parent_title,
            re_opening=opening,
            content="COMPLETED: This tuition task has been completed by " + str(teacher.first_name) + " and pending review from "+ str(student.first_name),
            msgtype="Completed",
            mainmessage=False,
            parent_id=parent_id,
            )[0]
        new_msg.save()

        #overwrite the mainmessage status
        if new_msg.msgtype != "Messaged":
            nmsgtype = new_msg.msgtype
            p_id = new_msg.parent_id
            mainmessage = get_object_or_404(Message, id=p_id)
            mainmessage.msgtype = nmsgtype
            mainmessage.save()

        #deactivating the opening
        opening.job_active = False
        opening.save()

        del self.request.session["order_id"]
        del self.request.session["msg_id"]

        #notification
        notify.send(sender=teacher.user, recipient=student.user, action='Complete', message=new_msg)

        messages.success(request, "Thank you for your confirmation")

        return redirect("MessageDetail", pk=completemsg.id)






class OrderCancelReview(LoginRequiredMixin, GetDetailsMixin, FormView, TemplateView):
    form_class = OrderCancelReviewForm
    template_name = 'review/order_review.html'
    success_url = 'home/'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        #if id is not selected to exit
        try:
            order_id = self.request.session.get("order_id")
            msg_id = self.request.session.get("msg_id")
        except:
            return redirect('Home')

        cancelorder = Order.objects.get(pk=order_id)

        #if review already exists to exit the loop
        try:
            test = ReviewTeacher.objects.get(opening = cancelorder.oopening)
            messages.warning(self.request,"You have already reviewed " + str(opening))
            return redirect('Home')
        except:
            pass
        return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        context = super(OrderCancelReview, self).get_context_data(**kwargs)
        # order_id = self.request.session.get("order_id")
        # msg_id = self.request.session.get("msg_id")
        cancelorder = self.get_order()
        # cancelmsg = self.get_msg()
        # context["order"] = "Please enter your feedback"
        context["title"] = "Cancellation of order " + str(cancelorder)

        return context

    def form_valid(self, form):

        reason = form.cleaned_data.get("reason")
        comments = form.cleaned_data.get("comments")

        subject = self.get_order().oopening.subject
        level = self.get_order().oopening.level
        grp_tuition = self.get_order().oopening.group_tuition
        price = self.get_order().price
        student = self.get_order().ostudent
        teacher = self.get_order().oteacher
        opening = self.get_order().oopening

        message = self.get_msg()
        order = self.get_order()

        parent_id = self.get_msg().parent_id
        parent_title = self.get_msg().title
        cancelmsg = self.get_msg()

        #updating the order status
        order = self.get_order()
        order.status = "Canceled"
        order.save()

        #updating the msg
        new_msg = Message.objects.get_or_create(
            senduser=student.user,
            touser=teacher.user,
            title=parent_title,
            re_opening=opening,
            content="CANCELED: This tuition task has been canceled by " + str(student.first_name),
            msgtype="Canceled",
            mainmessage=False,
            parent_id=parent_id,
            )[0]
        new_msg.save()

        #overwrite the mainmessage status
        if new_msg.msgtype != "Messaged":
            nmsgtype = new_msg.msgtype
            p_id = new_msg.parent_id
            mainmessage = get_object_or_404(Message, id=p_id)
            mainmessage.msgtype = nmsgtype
            mainmessage.save()

        #updating the review
        obj = ReviewTeacher.objects.get_or_create(
            teacher=teacher,
            student=student,
            opening=opening,

            message=message,
            order=order,

            subject=subject,
            level=level,
            group_tuition=grp_tuition,
            price=price,
            cnc="Cancel",
            reason=reason,
            comments=comments
            )[0]


        #deactivating the opening
        opening.job_active = False
        opening.save()

        del self.request.session["order_id"]
        del self.request.session["msg_id"]

        #notification
        notify.send(sender=student.user, recipient=teacher.user, action='Cancel', message=new_msg)

        messages.success(self.request, "You have successfully canceled this job")

        return redirect("MessageDetail", pk=cancelmsg.id)




#takes in the msg_id submitted by the review task message
def RecordMsg(request):
    pk = request.POST.get("msg_id")
    msg = get_object_or_404(Message, pk=pk)
    parent_msg_id = msg.parent_id
    msg = get_object_or_404(Message, pk=parent_msg_id)
    request.session["msg_id"] = msg.id
    return redirect("OrderCompleteReview")


class OrderCompleteReview(LoginRequiredMixin, GetDetailsMixin, FormView, TemplateView):
    form_class = OrderCompleteReviewForm
    template_name = 'review/order_review.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        #if id is not selected to exit
        try:
            # order_id = self.request.session.get("order_id")
            msg_id = self.request.session.get("msg_id")
        except:
            return redirect('Home')

        opening = self.get_msg().re_opening
        
        # if review is existing already exit and state you have already reviewed
        try:
            test = ReviewTeacher.objects.get(opening = opening)
            messages.warning(self.request,"You have already reviewed " + str(opening))
            return redirect('Home')
        except:
            pass

        context['additionjs'] = True
        return self.render_to_response(context)


    def get_order(self, *args, **kwargs):
        order = Order.objects.filter(oteacher=self.get_teacher(), ostudent=self.get_student(), oopening=self.get_opening()).first()
        return order


    def get_context_data(self, **kwargs):
        context = super(OrderCompleteReview, self).get_context_data(**kwargs)
        context["title"] = "Please review the tuition job done by " + str(self.get_teacher().first_name) + " for " + str(self.get_opening())
        return context


    def form_valid(self, form):

        score = form.cleaned_data.get("score")
        gradebefore = form.cleaned_data.get("gradebefore")
        gradeafter = form.cleaned_data.get("gradeafter")
        review = form.cleaned_data.get("review")

        subject = self.get_order().oopening.subject
        level = self.get_order().oopening.level
        grp_tuition = self.get_order().oopening.group_tuition
        price = self.get_order().price
        student = self.get_order().ostudent
        teacher = self.get_order().oteacher
        opening = self.get_order().oopening

        message = self.get_msg()
        order = self.get_order()

        parent_id = self.get_msg().parent_id
        parent_title = self.get_msg().title
        reviewmsg = self.get_msg()

        #updating the review
        obj = ReviewTeacher.objects.get_or_create(
            teacher=teacher,
            student=student,
            opening=opening,

            message=message,
            order=order,

            subject=subject,
            level=level,
            group_tuition=grp_tuition,
            price=price,
            gradebefore=gradebefore,
            gradeafter=gradeafter,
            cnc="Complete",
            score=score,
            review=review
            )[0]

        #updating the msg
        new_msg = Message.objects.get_or_create(
            senduser=student.user,
            touser=teacher.user,
            title=parent_title,
            re_opening=opening,
            content="REVIEWED: This tuition task has reviewed by " + str(student.first_name),
            msgtype="Reviewed",
            mainmessage=False,
            parent_id=parent_id,
            )[0]
        new_msg.save()

        #overwrite the mainmessage status
        if new_msg.msgtype != "Messaged":
            nmsgtype = new_msg.msgtype
            p_id = new_msg.parent_id
            mainmessage = get_object_or_404(Message, id=p_id)
            mainmessage.msgtype = nmsgtype
            mainmessage.save()

        #notification
        notify.send(sender=student.user, recipient=teacher.user, action='Review', message=new_msg)


        #if the order is reviewed to reward the student with a certain amount of credits
        # reviewadd = 0
        studentuser = student.user
        studentusercred = get_object_or_404(UserCredit, user=studentuser)
        studentusercred.credit = studentusercred.credit + reviewadd
        studentusercred.save()

        messages.success(self.request, "Your Review has been sent.")
        return redirect("MessageDetail", pk=reviewmsg.id)



#takes in the msg_id submitted by the review task message
def ReviewDetail(request):
    pk = request.POST.get("msg_id")
    review_id = ReviewTeacher.objects.filter(message_id=pk).first().id
    request.session["review_id"] = review_id
    return redirect("ReviewDetailView")


class ReviewDetailView(TemplateView, FormView, GetDetailsMixin):
    model = ReviewTeacher
    template_name = 'review/review_detail.html'
    form_class = ReviewFormComment

    def get_context_data(self, **kwargs):
        context = super(ReviewDetailView, self).get_context_data(**kwargs)
        review_id = self.request.session.get("review_id")
        # del self.request.session["review_id"]
        review = get_object_or_404(ReviewTeacher, id=review_id)
        context["review"] = review

        return context

    #add reviewcomment
    def form_valid(self, form):
        reviewcomment = form.cleaned_data.get("reviewcomment")
        review_id = self.request.session.get("review_id")
        review = get_object_or_404(ReviewTeacher, id=review_id)
        # reviewmsg = review.message

        if not review.reviewcomment:
            review.reviewcomment = reviewcomment
            review.save()

        messages.success(self.request, "Your comment has been submitted.")
        return redirect("ReviewDetailView")








def ReviewList(request):
    request.session["teacher_id"] = request.GET.get('teacher_id')
    return redirect('ReviewListView')

class ReviewListView(ListView):
    model = ReviewTeacher
    template_name = 'review/review_list.html'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):

        try:
            self.request.session.get("teacher_id")
        except:
            messages.warning(self.request, "Please select teacher first.")
            return redirect("TeacherList")

        return super(ReviewListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ReviewListView, self).get_context_data(**kwargs)
        teacher_id = self.request.session.get("teacher_id")
        teacher = Teacher.objects.get(id = teacher_id)
        context["Teacher_Name"] = str(teacher.last_name) + " " + str(teacher.first_name)
        context["Teacher_Detail_URL"] =  teacher.get_absolute_url()
        return context

    def get_queryset(self, *args, **kwargs):
        teacher_id = self.request.session.get("teacher_id")
        qs = super(ReviewListView, self).get_queryset(**kwargs).filter(teacher=teacher_id, cnc="Complete").order_by("-id")
        return qs

