from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import Http404, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView, DetailView
from teacher.models import Teacher
from student.models import Student
from opening.models import Opening
from tags.models import TagOpening, ViewOpening
from tags.views import FavOpening
from opening.forms import OpeningForm, SearchOpeningForm
from mixins.mixins import UserChangeManagerMixin, LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from itertools import chain

class OpeningDetail(LoginRequiredMixin, DetailView):
    model = Opening
    # success_url = '/openings/'
    template_name = 'opening/details.html'

    # def get_object(self, *args, **kwargs):
    #     obj = super(OpeningDetail, self).get_object(*args, **kwargs)
    #     return obj

    def get_context_data(self, *args, **kwargs):
        context = super(OpeningDetail, self).get_context_data(*args, **kwargs)
        user = self.get_object().user
        self.request.session["user_id"] = user.id
        self.request.session["opening_id"] = self.get_object().id
        obj = get_object_or_404(Student,user=user)
        # context["industry"] =  obj.industry_type.all()
        # context["logo"] =  obj.image
        context["tags"] = TagOpening.objects.filter(opening=self.get_object(), active=True)

        opening_id = self.get_object().id

        objo = self.get_object()

        try:
            test = self.request.user.teacher
            if objo.user.id != self.request.user.id:
                #update the number of views
                objw = get_object_or_404(Teacher,user=self.request.user)
                obj = ViewOpening.objects.get_or_create(opening_id=objo.id)[0]
                obj.teacher.add(objw.id)
                obj.save()
            #is it favorited by current user?
            context["Submit"] = "Favorite"
            if FavOpening.objects.filter(opening_id = objo.id).first() != None:
                if FavOpening.objects.filter(opening_id = objo.id).first().teacher.filter(id=objw.id).first() != None:
                    context["Submit"] = "Unfavorite"
        except:
            pass

        return context



class OpeningCreate(LoginRequiredMixin, FormView):
    model = Opening
    form_class = OpeningForm
    template_name = 'opening/create.html'

    def form_valid(self, form):
        user = self.request.user
        obj_comp = Student.objects.filter(user=user).first()

        i = form.save(commit=False)
        i.user = user
        i.hiring_student = obj_comp
        i.title = form.cleaned_data.get("title")
        i.subject = form.cleaned_data.get("subject")
        i.level = form.cleaned_data.get("level")
        i.description = form.cleaned_data.get("description")
        i.salary_range = form.cleaned_data.get("salary_range")
        i.negotiable = form.cleaned_data.get("negotiable")
        i.region = form.cleaned_data.get("region")
        # i.job_active = form.cleaned_data.get("job_active")
        i.save()

        pk = i.pk
        return redirect("OpeningDetail", pk=pk)


class OpeningUpdate(UserChangeManagerMixin,UpdateView): #if user is request user or staff can change
    model = Opening
    form_class = OpeningForm
    # fields = ['name']
    # success_url = '/openings/'
    template_name = 'opening/update.html'

    # def get_initial(self):
    #     initial = super(OpeningUpdate, self).get_initial()
    #     return initial

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        valid_data = super(OpeningUpdate, self).form_valid(form)
        return valid_data



class OpeningList(ListView, FormView):
    model = Opening
    form_class = SearchOpeningForm
    template_name = 'opening/list.html'
    paginate_by = 16

    def get_initial(self):
        if not self.request.GET.get('submit'):
            return self.initial.clear()
        else:
            self.initial.clear()
            for key in self.request.GET:
                try:
                    if key == "region_1":
                        self.initial[key] = self.request.GET.getlist('region_1')
                    elif key == "region_2":
                        self.initial[key] = self.request.GET.getlist('region_2')
                    elif key == "region_3":
                        self.initial[key] = self.request.GET.getlist('region_3')
                    elif key == "region_4":
                        self.initial[key] = self.request.GET.getlist('region_4')

                    elif key == "submit":
                        pass
                    else:
                        self.initial[key] = self.request.GET[key]
                except KeyError:
                    pass
            return self.initial.copy()


    def get_queryset(self, *args, **kwargs):
        qs = super(OpeningList, self).get_queryset(**kwargs).filter(job_active=True, private=False).order_by('-date_modified')

        subject_1 = self.request.GET.get("subject_1")
        subject_2 = self.request.GET.get("subject_2")
        subject_3 = self.request.GET.get("subject_3")

        level_type = self.request.GET.get("level_grp")

        region1 = self.request.GET.getlist("region_1")
        region2 = self.request.GET.getlist("region_2")
        region3 = self.request.GET.getlist("region_3")
        region4 = self.request.GET.getlist("region_4")
        region = list(chain(region1, region2, region3, region4))

        minimum_pay = self.request.GET.get("minimum_pay")
        group_tuition = self.request.GET.get("group_tuition")
        search = self.request.GET.get("search")

        
        if subject_1:
            subject = subject_1
        elif subject_2:
            subject = subject_2
        else:
            subject = subject_3

        # level = None
        # if level_type:
        #     if level_type == "Lower Primary":
        #         level = ("1","2","3")
        #     if level_type == "Higher Primary":
        #         level = ("4","5","6")
        #     if level_type == "Lower Secondary":
        #         level = ("7","8")
        #     if level_type == "Higher Secondary":
        #         level = ("9","10")
        #     if level_type == "Junior College":
        #         level = ("11","12")
        #     if level_type == "University":
        #         level = ("14","15","16","17")


        title = None
        if level_type:
            if level_type == "Lower Primary":
                title = ("Primary 1","Primary 2","Primary 3")
            if level_type == "Higher Primary":
                title = ("Primary 4","Primary 5","Primary 6")
            if level_type == "Lower Secondary":
                title = ("Secondary 1","Secondary 2")
            if level_type == "Higher Secondary":
                title = ("Secondary 3","Secondary 4")
            if level_type == "Junior College":
                title = ("Junior College 1","Junior College 2")
            if level_type == "University":
                title = ("University 1","University 2","University 3","University 4")
            if level_type == "NA":
                title = ("NA","NA")


        try:

            if subject:
                qs = qs.filter(subject=subject)

            # if level:
            #     qs = qs.filter(level__in=level)

            if title:
                qs = qs.filter(level__title__in=title)

            if minimum_pay:
                qs = qs.filter(salary_range__gte=minimum_pay)
            if region:
                qs = qs.filter(region__in=region)

            if group_tuition:
                if group_tuition == "Yes":
                    qs = qs.filter(group_tuition=True)
                if group_tuition == "No":
                    qs = qs.filter(group_tuition=False)

            if search:
                qs = qs.filter(
                    Q(description__icontains=search) |
                    Q(title__icontains=search)
                    ).distinct()

            qs = qs.order_by('-date_modified')

        except:
            pass

        return qs





#this is the list of openings for one specific student that belongs to the request user
class POpeningList(ListView):
    model = Opening
    template_name = 'opening/p_list.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        qs = super(POpeningList, self).get_queryset(**kwargs).filter(user=user, job_active=True).order_by('-id')
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(POpeningList, self).get_context_data(*args, **kwargs)
        context["listtype"] = "active"
        return context   


class POpeningListInactive(ListView):
    model = Opening
    template_name = 'opening/p_list.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        qs = super(POpeningListInactive, self).get_queryset(**kwargs).filter(user=user, job_active=False).order_by('-id')
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(POpeningListInactive, self).get_context_data(*args, **kwargs)
        context["listtype"] = "inactive"
        return context   


class FavOpeningList(ListView):
    model = Opening
    template_name = 'opening/fav_list.html'
    paginate_by = 10


    def get_queryset(self, *args, **kwargs):

        try:
            test = self.request.user.student.favteacher_set.all()
        except:
            test = self.request.user.teacher.favopening_set.all()

        qs = super(FavOpeningList, self).get_queryset(**kwargs).filter(favopening__in=test,job_active=True).order_by('id')

        return qs







