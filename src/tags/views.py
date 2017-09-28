from django.shortcuts import render
# Create your views here.
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import View
from mixins.mixins import LoginRequiredMixin
from tags.models import TagTeacher, TagOpening, FavTeacher, FavOpening
# from analytics.models import TagView
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from teacher.models import Teacher
from opening.models import Opening
from student.models import Student
from django.contrib import messages
from messaging.models import Message
# from variables.models import MStatusType
from django.http import HttpResponse, Http404, HttpResponseRedirect


#let the company favorite a specific teacher
def FavTeacherSub(request, pk):
    objw = get_object_or_404(Teacher, pk=pk)
    objc = get_object_or_404(Student, user=request.user)

    try:
        test = FavTeacher.objects.get(teacher_id = objw.id).student.get(id=objc.id)
        obj = FavTeacher.objects.get(teacher_id=objw.id)
        obj.student.remove(objc.id)
        obj.save
        messages.info(request, "Unfavorited!")

    except:
        obj = FavTeacher.objects.get_or_create(teacher_id=objw.id)[0]
        obj.student.add(objc.id)
        obj.save
        messages.info(request, "Favorited!")

    return HttpResponseRedirect(objw.get_absolute_url())


#let the teacher favorite a specific opening
def FavOpeningSub(request, pk):
    objo = get_object_or_404(Opening, pk=pk)
    objw = get_object_or_404(Teacher, user=request.user)

    try:
        test = FavOpening.objects.get(opening_id = objo.id).teacher.get(id=objw.id)
        obj = FavOpening.objects.get(opening_id=objo.id)
        obj.teacher.remove(objw.id)
        obj.save
        messages.info(request, "Unfavorited!")

    except:
        obj = FavOpening.objects.get_or_create(opening_id=objo.id)[0]
        obj.teacher.add(objw.id)
        obj.save
        messages.info(request, "Favorited!")

    return HttpResponseRedirect(objo.get_absolute_url())





