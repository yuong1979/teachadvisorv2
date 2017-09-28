from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, ProcessFormView
from django.views.generic import ListView, DetailView, TemplateView
from teacher.models import Teacher
from student.models import Student
from orderreview.models import ReviewTeacher
from variables.models import Subject_Expertise, Level_Expertise
from billing.models import UserCredit, ImageSubscription, AnalyticsSubscription, FeaturedUser_0, FeaturedUser_1
from tags.models import TagTeacher, ViewTeacherNonUnique, SearchWordTeacherRecord, ViewTeacherUnique
from teacher.forms import TeacherAddForm, TeacherEditForm, SearchTeacherForm
from tags.models import ViewTeacherRecord
# from tags.views import FavTeacher
from billing.control import creditstart
from mixins.mixins import UserChangeManagerMixin, LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q, Avg, Max
from itertools import chain
import datetime

todate = datetime.datetime.now().date()


class TeacherDetail(LoginRequiredMixin, DetailView):
    model = Teacher
    success_url = '/teacher/'
    template_name = 'teacher/details.html'

    def get_object(self, *args, **kwargs):
        obj = super(TeacherDetail, self).get_object(*args, **kwargs)
        return obj

    def get_context_data(self, *args, **kwargs):
        context = super(TeacherDetail, self).get_context_data(*args, **kwargs)
        user = self.get_object().user
        self.request.session["user_id"] = user.id
        obj = get_object_or_404(Teacher,user=user)
        objw = self.get_object()

        context["tags"] = TagTeacher.objects.filter(teacher=obj, active=True)

        try:
            context["viewteacher"] = objw.viewteachernonunique.count
        except:
            context["viewteacher"] = 0

        try:
            context["favteacher"] = objw.favteacher.student.all().count()
        except:
            context["favteacher"] = 0

        context["review"] = objw.reviewteacher_set.filter(cnc="Complete")
        context["jobs"] = objw.get_job_count()
        context["score"] = objw.get_score()
        context["last_active"] = objw.get_last_active()

        try:
            context["imagepaid"] = objw.get_sub_status()
        except:
            context["imagepaid"] = False


        try:
            test = self.request.user.student
            if objw.user.id != self.request.user.id:
                objc = get_object_or_404(Student,user=self.request.user)

                #update the views of non unique
                objn = ViewTeacherNonUnique.objects.get_or_create(teacher_id=objw.id)[0]
                addcount = objn.count
                objn.count = addcount + 1
                objn.save()

                #update the views of unique
                obju = ViewTeacherUnique.objects.get_or_create(teacher_id=objw.id)[0]
                obju.student.add(objc.id)
                obju.save()

                #updating the viewteacherrecords
                vtr = ViewTeacherRecord.objects.get_or_create(teacher=obj, date=todate)[0]
                vtr.uniquecount = obju.get_student_count()
                vtr.nonuniquecount = objn.count
                vtr.save()


            #is it favorited by current user?
            context["Submit"] = "Favorite"
            if FavTeacher.objects.filter(teacher_id = objw.id).first() != None:
                if FavTeacher.objects.filter(teacher_id = objw.id).first().student.filter(id=objc.id).first() != None:
                    context["Submit"] = "Unfavorite"
        except:
            pass

        return context



class TeacherCreate(LoginRequiredMixin, CreateView):
    model = Teacher
    form_class = TeacherAddForm
    # success_url = '/worker/'
    template_name = 'teacher/create.html'

    def form_valid(self, form):
        i = form.save(commit=False)
        i.user = self.request.user
        i.save()

        user = self.request.user

        #create new account to give free credits
        usercred = UserCredit.objects.get_or_create(user=user)[0]
        usercred.credit = creditstart
        usercred.save()


        todate = datetime.datetime.now().date()
        # todate = todate.date()
        # tdelta = datetime.timedelta(days=1)
        # yesterdate = todate - tdelta

        #start an img loading account for the user
        usersubimg = ImageSubscription.objects.get_or_create(
            user=user,
            subenddate=todate
            )[0]
        usersubimg.save()


        #start an analytics account for the user
        usersubana = AnalyticsSubscription.objects.get_or_create(
            user=user,
            subenddate=todate
            )[0]
        usersubana.save()


        #start view teacher records for the user
        viewteacherrecord = ViewTeacherRecord.objects.create(
            teacher=user.teacher,
            date=todate,
            )
        viewteacherrecord.uniquecount = 0
        viewteacherrecord.nonuniquecount = 0
        viewteacherrecord.msgtocount = 0
        viewteacherrecord.msgfromcount = 0
        viewteacherrecord.ordercount = 0
        viewteacherrecord.save()



        #create form
        form.instance.user = user
        valid_data = super(TeacherCreate, self).form_valid(form)
        # tags = form.cleaned_data.get("tags")
        # if tags:
        #     tags_list = tags.split(",")
        #     for tag in tags_list:
        #         if not tag == " ":
        #             new_tag = TagTeacher.objects.get_or_create(title=str(tag.strip().lower()))[0]
        #             obj = get_object_or_404(Teacher, user=user)
        #             new_tag.teacher.add(obj)
        #             new_tag.count = new_tag.teacher.all().count()
        #             new_tag.save()

        return valid_data


    def get_success_url(self):
        user = self.request.user
        obj = get_object_or_404(Teacher, user=user)
        pk = obj.pk
        url = reverse('TeacherDetail', kwargs={'pk': pk})
        messages.info(self.request, "Your profile has been created you have been provided " + str(creditstart) + " free credits to use.")
        return url









class TeacherUpdate(UserChangeManagerMixin,UpdateView): #if user is request user or staff can change
    model = Teacher
    form_class = TeacherEditForm
    # fields = ['name']
    # success_url = '/worker/'
    template_name = 'teacher/update.html'

    def get_initial(self):
        initial = super(TeacherUpdate, self).get_initial()
        # tags = self.get_object().tagteacher_set.all()
        # initial["tags"] = ", ".join([x.title for x in tags])
        return initial


    # adding request to our form
    def get_form_kwargs(self):
        kwargs = super(TeacherUpdate, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs




    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        valid_data = super(TeacherUpdate, self).form_valid(form)
        
        # tags = form.cleaned_data.get("tags")
        # obj = self.get_object()
        # obj.tagteacher_set.clear()
        # if tags:
        #     tags_list = tags.split(",")
        #     for tag in tags_list:
        #         if not tag == " ":
        #             new_tag = TagTeacher.objects.get_or_create(title=str(tag.strip().lower()))[0]
        #             obj = get_object_or_404(Teacher, user=user)
        #             new_tag.teacher.add(obj)
        #             new_tag.count = new_tag.teacher.all().count()
        #             new_tag.save()

        return valid_data

    def get_success_url(self):
        user = self.request.user
        obj = get_object_or_404(Teacher, user=user)
        pk = obj.pk
        url = reverse('TeacherDetail', kwargs={'pk': pk})
        messages.info(self.request, "Your profile has been updated.")
        return url


class TeacherList(ListView, FormView):
    model = Teacher
    form_class = SearchTeacherForm
    template_name = 'teacher/list.html'
    paginate_by = 16


    def get_context_data(self, **kwargs):
        context = super(TeacherList, self).get_context_data(**kwargs)

        #searching for a selected subject and if that exists to pull the subject's featured user out
        try:
            subject_1 = self.request.GET.get("subject_1")
            subject_2 = self.request.GET.get("subject_2")
            subject_3 = self.request.GET.get("subject_3")

            if subject_1:
                subject = subject_1
            elif subject_2:
                subject = subject_2
            else:
                subject = subject_3
        except:
            pass

        try:
            FeatUser0 = FeaturedUser_0.objects.filter(subject=subject).first()
            context["featureduser0"] = FeatUser0.user.teacher
        except:
            pass

        try:
            FeatUser1 = FeaturedUser_1.objects.filter(subject=subject).first()
            context["featureduser1"] = FeatUser1.user.teacher
        except:
            pass

        return context

    def get_initial(self):
        #get the initial selection
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
                    elif key == "educational_level":
                        self.initial[key] = self.request.GET.getlist('educational_level')
                    elif key == "expertise_type":
                        self.initial[key] = self.request.GET.getlist('expertise_type')
                    elif key == "submit":
                        pass
                    else:
                        self.initial[key] = self.request.GET[key]
                except KeyError:
                    pass
            return self.initial.copy()

    def get_queryset(self, *args, **kwargs):
        qs = super(TeacherList, self).get_queryset().filter(active=True).distinct().order_by('-date_modified')

        subject_1 = self.request.GET.get("subject_1")
        subject_2 = self.request.GET.get("subject_2")
        subject_3 = self.request.GET.get("subject_3")
        # level_type = self.request.GET.get("level_grp")
        level = self.request.GET.get("level")
        educational_level = self.request.GET.getlist("educational_level")
        expertise_type = self.request.GET.getlist("expertise_type")
        maximum_pay = self.request.GET.get("maximum_pay")
        minimum_years = self.request.GET.get("minimum_years")

        region1 = self.request.GET.getlist("region_1")
        region2 = self.request.GET.getlist("region_2")
        region3 = self.request.GET.getlist("region_3")
        region4 = self.request.GET.getlist("region_4")
        region = list(chain(region1, region2, region3, region4))

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
        #         level = ("1", "2", "3")
        #     if level_type == "Higher Primary":
        #         level = ("4", "5", "6")
        #     if level_type == "Lower Secondary":
        #         level = ("7", "8")
        #     if level_type == "Higher Secondary":
        #         level = ("9", "10")
        #     if level_type == "Junior College":
        #         level = ("11", "12")
        #     if level_type == "University":
        #         level = ("14", "15", "16", "17")

        # test = self.request.user.student


        #storing word searches in the database
        try:
            #only take in queries that are registered as students
            test = self.request.user.student

            if search:

                search = search.lower()

                if subject:
                    subject = Subject_Expertise.objects.get(id=subject)
                else:
                    subject = None

                if level:
                    level = Level_Expertise.objects.get(id=level)
                else:
                    level = None

                wordrecord, created = SearchWordTeacherRecord.objects.get_or_create(
                    user=self.request.user,
                    word=search,
                    subject=subject,
                    level=level,
                    )
        except:
            pass


        #filtering for the required teacher profiles
        try:
            if subject:
                if level:
                    qs = qs.filter(
                        Q(first_subject=subject, first_level=level) |
                        Q(second_subject=subject, second_level=level) |
                        Q(third_subject=subject, third_level=level)
                    ).distinct()
                else:
                    # to show filtered results when subject is selected and level isn't
                    qs = qs.filter(
                        Q(first_subject=subject) |
                        Q(second_subject=subject) |
                        Q(third_subject=subject)
                    ).distinct()

            if level and not subject:
                qs = qs.filter(
                    Q(first_level=level) |
                    Q(second_level=level) |
                    Q(third_level=level)
                ).distinct()


            if educational_level:
                qs = qs.filter(educational_level__in=educational_level)
            if expertise_type:
                qs = qs.filter(expertise_type__in=expertise_type)
            if minimum_years and not minimum_years == '0':
                qs = qs.filter(years_of_experience__gte=minimum_years)
            if maximum_pay and not maximum_pay == '120':
                qs = qs.filter(salary_expectation__lte=maximum_pay)
            if region:
                qs = qs.filter(region__in=region)
            # if group_tuition:
            #     qs = qs.filter(group_tuition=True)

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





class FavTeacherList(ListView):
    model = Teacher
    template_name = 'teacher/fav_list.html'
    paginate_by = 10


    def get_queryset(self, *args, **kwargs):
        try:
            test = self.request.user.student.favteacher_set.all()
        except:
            test = self.request.user.teacher.favopening_set.all()
        qs = super(FavTeacherList, self).get_queryset(**kwargs).filter(favteacher__in=test).order_by('-date_modified')

        return qs








class ReviewList(ListView):
    model = ReviewTeacher
    template_name = 'review_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ReviewList, self).get_context_data(**kwargs)
        teacher_id = self.request.GET.get('teacher_id')
        teacher = Teacher.objects.get(id = teacher_id)
        context["Teacher_Name"] = str(teacher.last_name) + " " + str(teacher.first_name)
        return context

    def get_queryset(self, *args, **kwargs):
        teacher_id = self.request.GET.get('teacher_id')
        qs = super(ReviewList, self).get_queryset(**kwargs).filter(teacher=teacher_id, cnc="Complete").order_by("-id")
        
        return qs


