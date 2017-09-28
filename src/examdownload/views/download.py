"""Download View (by token)."""
import mimetypes

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils.encoding import smart_str
from django.utils import timezone
from django.views import View

from examdownload.models import TemporaryLink
from billing.models import UserCredit


class DownloadView(LoginRequiredMixin, View):
    """Simple view."""

    login_url = '/accounts/login/'

    def get(self, request, token, *args, **kwargs):
        """Get data."""
        link = None
        http_user_agent = request.META['HTTP_USER_AGENT']
        http_user_ip = request.META['REMOTE_ADDR']
        try:
            link = TemporaryLink.objects.get(id=token,
                                             active=True,
                                             user_ip=http_user_ip,
                                             user_agent=http_user_agent,
                                             exam__publish=True)
        except TemporaryLink.DoesNotExist:
            return TemplateResponse(request, 'not_found.html', status=404)

        exam = link.exam

        if request.user.is_authenticated():
            try:
                usercost_instance = UserCredit.objects.get(user=request.user)
                if usercost_instance.credit - exam.creditcost >= 0:
                    usercost_instance.credit -= exam.creditcost
                    usercost_instance.save()
                else:
                    return TemplateResponse(request, 'not_found.html', status=404)
            except UserCredit.DoesNotExist:
                return TemplateResponse(request, 'not_found.html', status=404)


        ext = '.' + exam.docs.name.split('.')[-1]
        link.active = False
        link.downloaded_at = timezone.now()
        link.save()
        mimetypes.init()
        mime = mimetypes.guess_type(ext)[0]
        filename = smart_str(exam.docs.name)
        exam.docs.open()
        response = HttpResponse(exam.docs.read(),
                                content_type=mime)
        exam.docs.close()
        response['Content-Disposition'] = ('attachment; filename={}'
                                           .format(filename))
        response['X-Sendfile'] = filename
        response['Content-Length'] = exam.docs.size
        return response
