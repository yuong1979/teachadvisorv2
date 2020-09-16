from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.views.generic.base import View
from messaging.models import Message
from notifications.models import Notification
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# from django.conf import settings
import json


def allin(request):
	notifications = Notification.objects.all_for_user(request.user)
	context = {
		"notifications":notifications,
	}
	return render(request, "notifications/allin.html", context)

@login_required
def read(request, id):
	try:
		next = request.GET.get('next', None)
		notification = Notification.objects.get(id=id)
		if notification.recipient == request.user:
			notification.read = True
			notification.save()
			if next is not None:
				return HttpResponseRedirect(next)
			else:
				return HttpResponseRedirect(reverse("notifications_all"))
		else:
			raise Http404
	except:
		raise HttpResponseRedirect(reverse("notifications_all"))


@login_required
def get_notifications_ajax(request):
	if request.is_ajax() and request.method == 'POST':
		notifications = Notification.objects.all_for_user(request.user).recent()
		count = notifications.count()
		notes = []
		for note in notifications:
			notes.append(str(note))
		data = {
			"notifications":notes,
			"count": count,
		}
		json_data = json.dumps(data)
		return HttpResponse(json_data, content_type="application/json")
	else:
		raise Http404


class MsgCountView(View):
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			notifications = Notification.objects.all_for_user(request.user).recent()
			count = notifications.count()
			request.session["unread_count"] = count
			return JsonResponse({"count": count })
		else:
			raise Http404


		# if request.is_ajax() and request.method == 'POST':
		# 	notifications = Notification.objects.all_for_user(request.user).recent()
		# 	count = notifications.count()
		# 	request.session["unread_count"] = count
		# 	return JsonResponse({"count": count })
		# else:
		# 	raise Http404


