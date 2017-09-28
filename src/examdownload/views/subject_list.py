"""Subjects List Template View (index)."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from examdownload.models import Exam


class SubjectsListTemplateView(LoginRequiredMixin, TemplateView):  # noqa pylint: disable=too-many-ancestors
    """Subject list view."""
    login_url = '/accounts/login/'
    template_name = 'prelims.html'

    def get_context_data(self, **kwargs):
        """Get context."""
        context = (super(SubjectsListTemplateView, self)
                   .get_context_data(**kwargs))
        context['exams'] = (Exam.objects.filter(publish=True)
                            .order_by('subject', 'school'))
        return context
