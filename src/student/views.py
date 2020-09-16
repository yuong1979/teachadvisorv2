from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from student.models import Student
from django.db.models import Q
from student.forms import StudentAddForm, StudentEditForm
# from variables.models import FunctionType
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.http import Http404
from mixins.mixins import UserChangeManagerMixin
from billing.models import UserCredit, StudentBISubscription
from billing.control import creditstart
import datetime

class StudentDetail(UserChangeManagerMixin,DetailView):
    model = Student
    success_url = '/student/'
    template_name = 'student/details.html'

    # def get_object(self, *args, **kwargs):
    #     obj = super(StudentDetail, self).get_object(*args, **kwargs)
    #     user = self.request.user
    #     if obj.user == user:
    #         return obj
    #     else:
    #         raise Http404

class StudentCreate(CreateView):
    model = Student
    form_class = StudentAddForm
    # fields = ['name']
    # success_url = '/company/'
    template_name = 'student/create.html'
    # function = FunctionType.objects.filter(title="Employer").first()

    def form_valid(self, form):
        i = form.save(commit=False)
        i.user = self.request.user
        # i.function = self.function
        i.save()
        valid_data = super(StudentCreate, self).form_valid(form)

        user = self.request.user

        #give free credits
        usercred = UserCredit.objects.get_or_create(user=user)[0]
        usercred.credit = creditstart
        usercred.save()

        #start an bi account for the user
        todate = datetime.datetime.now().date()
        subscription = StudentBISubscription.objects.get_or_create(
            user=user,
            subenddate=todate
            )[0]
        subscription.save()
        return valid_data

    def get_success_url(self):
        user = self.request.user
        obj = get_object_or_404(Student, user=user)
        pk = obj.pk
        url = reverse('StudentDetail', kwargs={'pk': pk})
        # messages.info(self.request, "Your profile has been created you have been provided " + str(creditstart) + " free credits to use.")
        messages.info(self.request, "Your profile has been created.")
        return url







class StudentUpdate(UserChangeManagerMixin,UpdateView): #if user is request user or staff can change
    model = Student
    form_class = StudentEditForm
    # fields = ['name']
    # success_url = '/company/'
    template_name = 'student/update.html'

    def get_success_url(self):
        user = self.request.user
        obj = get_object_or_404(Student, user=user)
        pk = obj.pk
        url = reverse('StudentDetail', kwargs={'pk': pk})
        messages.info(self.request, "Your profile has been updated.")
        return url

class StudentList(ListView):
    model = Student
    template_name = 'student/list.html'

    def get_queryset(self, *args, **kwargs):
        qs = super(StudentList, self).get_queryset(**kwargs).filter()
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(name__icontains=query)|
                Q(description__icontains=query)
                ).order_by("-name")
            return qs
        else:
            return qs



