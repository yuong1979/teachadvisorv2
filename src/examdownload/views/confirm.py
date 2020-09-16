"""View for app."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView

from examdownload.models import Exam
from examdownload.models import TemporaryLink
from billing.models import UserCredit


class ConfirmTemplateView(LoginRequiredMixin, TemplateView):  # noqa pylint: disable=too-many-ancestors
    """Subject list view."""
    login_url = '/accounts/login/'
    template_name = 'confirm.html'

    def get(self, request, *args, **kwargs):
        """Get response."""
        context = self.get_context_data(**kwargs)
        raw_exam = request.GET.get('exam', 'NOT')
        if raw_exam == 'NOT':
            self.template_name = 'not_found.html'
            context['page'] = request.get_full_path()
            return self.render_to_response(context, status=404)
        exam_id = -1
        try:
            exam_id = int(raw_exam)
        except ValueError:
            context['error'] = 'Index is wrong "{}"'.format(raw_exam)
            return self.render_to_response(context, status=406)
        try:
            exam = Exam.objects.get(id=exam_id, publish=True)
            context['exam'] = exam
        except Exam.DoesNotExist:
            context['error'] = ('Exam with id #{} does not exist'
                                .format(str(exam_id)))
            return self.render_to_response(context, status=406)
        if request.user.is_authenticated:
            try:
                usercost_instance = UserCredit.objects.get(user=request.user)
                if usercost_instance.credit - exam.creditcost < 0:
                    context['has_no_money'] = True
                context['user_credit'] = usercost_instance.credit
            except UserCredit.DoesNotExist:
                context['error'] = 'UserCredit NotFound, some error.'
                return self.render_to_response(context, status=403)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        """Post response."""
        context = self.get_context_data(**kwargs)

        exam_id = request.POST.get('exam', -1)
        try:
            exam = Exam.objects.get(id=exam_id, publish=True)
        except Exam.DoesNotExist:
            context['error'] = ('Exam with id #{} does not exist'
                                .format(str(exam_id)))
            return self.render_to_response(context, status=404)

        agreement = request.POST.get('agreement', False)
        if not agreement:
            context['warning'] = ('Please check "I agree and confirm '
                                  'download" to proceed')
            context['exam'] = exam
            return self.render_to_response(context)

        user_agent = request.META['HTTP_USER_AGENT']
        remote_addr = request.META['REMOTE_ADDR']
        link = TemporaryLink.objects.create(user=request.user,
                                            user_agent=user_agent,
                                            user_ip=remote_addr,
                                            exam=exam,
                                            downloaded_at=timezone.now())
        link.save()
        context['download'] = reverse('examdownload_download',
                                      args=(str(link.id),))
        self.template_name = 'download.html'
        return self.render_to_response(context)
