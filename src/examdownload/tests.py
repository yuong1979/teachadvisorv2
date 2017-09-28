"""Tests for exadownload module."""
import os
import random

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from faker import Factory

from billing.models import UserCredit
from examdownload.models import Exam
from examdownload.models import TemporaryLink
from student.models import Student


class GoToCheckBoxPageTestCase(TestCase):
    """Check box page."""

    def setUp(self):
        """Setups one exam and it's subject."""
        user = User.objects.create_user('john', 'lennon@thebeatles.com',
                                        'johnpassword')
        user.save()
        student = Student.objects.create(function='Student',
                                         first_name='John',
                                         last_name='Malkovich',
                                         contact='1234-5678',
                                         user=user)
        student.save()
        UserCredit.objects.create(user=user, credit=100).save()

        self.filename = 'test_file1.txt'
        self.exam = Exam.objects.create(
            title='100 questions test',  # noqa pylint: disable=no-member
            exam_type='Test',  # pylint: disable=no-member
            description='Test with 100 hard questions',  # noqa pylint: disable=no-member
            publish=True,
            subject='Math',
            level='First',
            school='Hardcore school',
            docs=self.filename,
            creditcost=50,
        )
        self.exam.save()
        self.full = settings.MEDIA_ROOT + '/' + self.filename
        with open(self.full, 'w') as fhandler:
            fhandler.write("Hello some data.\nAnother data.\nEOF")

    def tearDown(self):
        """Tear down test case."""
        if os.path.exists(self.full):
            os.remove(self.full)

    def test_post_without_agreement(self):
        """Test post with no agreement."""
        get_params = {'exam': self.exam.id}
        client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                        enforce_csrf_checks=True)
        client.login(username='john', password='johnpassword')
        get_request = client.get(reverse('examdownload_confirm'), get_params)
        post_params = {
            'exam': self.exam.id,
            'csrfmiddlewaretoken': get_request.context['csrf_token']
        }
        response = client.post(reverse('examdownload_confirm'),
                               post_params)
        self.assertInHTML('<label style="color: red;">'
                          'Please check &quot;I agree and confirm '
                          'download&quot; to proceed'
                          '</label>',
                          str(response.content).strip())

    def test_post_with_wrong_id(self):
        """Test post with no agreement."""
        get_params = {'exam': self.exam.id}
        client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                        enforce_csrf_checks=True)
        client.login(username='john', password='johnpassword')
        get_request = client.get(reverse('examdownload_confirm'), get_params)
        post_params = {
            'exam': -321,
            'agreement': 'on',
            'csrfmiddlewaretoken': get_request.context['csrf_token']
        }
        response = client.post(reverse('examdownload_confirm'),
                               post_params)
        self.assertInHTML('<label style="color: red;">Exam with id #-321 '
                          'does not exist</label>',
                          response.content)

    def test_simple_get(self):
        """Test form rendered."""
        client = Client()
        client.login(username='john', password='johnpassword')
        get_params = {'exam': self.exam.id}
        response = client.get(reverse('examdownload_confirm'), get_params)
        content = response.content

        title_html = ("<label>Please check to confirm that {} credits will be "
                      "deducted from your account </label>"
                      .format(self.exam.creditcost))
        self.assertInHTML(title_html, content)

    def test_redirect_if_not_args(self):
        """Test redirest get if without args."""
        client = Client()
        client.login(username='john', password='johnpassword')
        response = client.get(reverse('examdownload_confirm'))
        self.assertIsInstance(response, TemplateResponse)
        self.assertEqual(response.status_code, 404)

    def test_error_if_not_valid_id(self):
        """Test redirest get if with not found id."""
        client = Client()
        client.login(username='john', password='johnpassword')
        get_params = {'exam': 'strangeid'}
        response = client.get(reverse('examdownload_confirm'), get_params)
        self.assertIsInstance(response, TemplateResponse)
        self.assertEqual(response.status_code, 406)

    def test_redirect_if_not_found_id(self):
        """Test redirest get if with not found id."""
        client = Client()
        client.login(username='john', password='johnpassword')
        get_params = {'exam': -123}
        response = client.get(reverse('examdownload_confirm'), get_params)
        self.assertIsInstance(response, TemplateResponse)
        self.assertEqual(response.status_code, 406)
        self.assertInHTML('<label style="color: red;">Exam with id #-123 '
                          'does not exist</label>',
                          response.content)

    def test_post_form(self):
        """Test post form."""
        get_params = {'exam': self.exam.id}
        client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                        enforce_csrf_checks=True)
        client.login(username='john', password='johnpassword')
        get_request = client.get(reverse('examdownload_confirm'), get_params)
        post_params = {
            'agreement': 'true',
            'exam': self.exam.id,
            'csrfmiddlewaretoken': get_request.context['csrf_token']
        }
        response = client.post(reverse('examdownload_confirm'),
                               post_params)

        links = TemporaryLink.objects.all()
        self.assertEqual(len(links), 1)
        link = links[0]
        self.assertIn(str(link.id), response.content)

        url_to = reverse('examdownload_download', args=(link.id,))

        file_response = client.get(url_to)
        file_content = "Hello some data.\nAnother data.\nEOF"
        self.assertEqual(file_response.content,
                         file_content)
        self.assertEqual(file_response['X-Sendfile'],
                         self.filename)
        self.assertEqual(file_response['Content-Disposition'],
                         'attachment; filename={}'
                         .format(self.filename))
        self.assertEqual(int(file_response['Content-Length']),
                         len(file_content))

    def test_post_form_redirect(self):
        """Test post form."""
        get_params = {'exam': self.exam.id}
        client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                        enforce_csrf_checks=True)
        client.login(username='john', password='johnpassword')
        get_request = client.get(reverse('examdownload_confirm'), get_params)
        post_params = {
            'agreement': 'true',
            'exam': self.exam.id,
            'csrfmiddlewaretoken': get_request.context['csrf_token']
        }
        response = client.post(reverse('examdownload_confirm'),
                               post_params)
        links = TemporaryLink.objects.all()
        self.assertEqual(len(links), 1)
        link = links[0]
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
        url_should_be = reverse('examdownload_download', args=(link.id,))
        self.assertInHTML('<iframe width="1" height="1" frameborder="0" src='
                          '"{}">'
                          '</iframe>'.format(url_should_be),
                          response.content)

    def test_post_form_bad_id(self):
        """Test post form."""
        get_params = {'exam': self.exam.id}
        client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                        enforce_csrf_checks=True)
        client.login(username='john', password='johnpassword')
        get_request = client.get(reverse('examdownload_confirm'), get_params)
        post_params = {
            'agreement': 'true',
            'exam': self.exam.id,
            'csrfmiddlewaretoken': get_request.context['csrf_token']
        }
        response = client.post(reverse('examdownload_confirm'),
                               post_params)

        links = TemporaryLink.objects.all()
        self.assertEqual(len(links), 1)
        link = links[0]
        self.assertIn(str(link.id), response.content)
        temp = '12345678-1234-1234-1234-123456789012'
        url_to = reverse('examdownload_download', args=(temp,))
        response = client.get(url_to)
        self.assertInHTML('<h3>Page {} does not exists</h3>'.format(url_to),
                          response.content)

    def test_post_form_bad_useragent(self):
        """Test post form."""
        get_params = {'exam': self.exam.id}
        client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                        enforce_csrf_checks=True)
        client.login(username='john', password='johnpassword')
        get_request = client.get(reverse('examdownload_confirm'), get_params)
        post_params = {
            'agreement': 'true',
            'exam': self.exam.id,
            'csrfmiddlewaretoken': get_request.context['csrf_token']
        }
        response = client.post(reverse('examdownload_confirm'),
                               post_params)

        links = TemporaryLink.objects.all()
        self.assertEqual(len(links), 1)
        link = links[0]
        url_to = '/download/' + str(link.id)
        url_to = reverse('examdownload_download', args=(link.id,))
        response = client.get(url_to, HTTP_USER_AGENT='Chromium')
        self.assertInHTML('<h3>Page {} does not exists</h3>'.format(url_to),
                          response.content)


class GetIndexPageTestCase(TestCase):
    """Test data viewed from database."""

    faker = None

    @classmethod
    def setUpClass(cls):
        """Set up faker and lessons list."""
        super(GetIndexPageTestCase, cls).setUpClass()
        cls.faker = Factory.create()

    def setUp(self):
        """Set up data for test."""
        user = User.objects.create_user('john', 'lennon@thebeatles.com',
                                        'johnpassword')
        user.save()
        student = Student.objects.create(function='Student',
                                         first_name='John',
                                         last_name='Malkovich',
                                         contact='1234-5678',
                                         user=user)
        student.save()
        UserCredit.objects.create(user=user, credit=100).save()

        data = self._get_exam_data()
        data['subject'] = 'Math'
        data['school'] = 'School 01'
        Exam.objects.create(**data).save()

        data = self._get_exam_data()
        data['subject'] = 'Math'
        data['school'] = 'School 01'
        Exam.objects.create(**data).save()

        data = self._get_exam_data()
        data['subject'] = 'Math'
        data['school'] = 'School 02'
        Exam.objects.create(**data).save()

        data = self._get_exam_data()
        data['subject'] = 'History'
        data['school'] = 'School 01'
        Exam.objects.create(**data).save()

        data = self._get_exam_data()
        data['subject'] = 'History'
        data['school'] = 'School 04'
        Exam.objects.create(**data).save()

        data = self._get_exam_data()
        data['subject'] = 'History'
        data['school'] = 'School 04'
        data['publish'] = False
        Exam.objects.create(**data).save()

    def _get_exam_data(self):
        return {
            'title': self.faker.sentence(nb_words=4),  # noqa pylint: disable=no-member
            'exam_type': self.faker.name(),  # pylint: disable=no-member
            'description': self.faker.sentence(nb_words=4),  # noqa pylint: disable=no-member
            'publish': True,
            'level': 'One',
            'docs': 'file1.docx',
            'creditcost': 50,
        }

    def test_view_subjects(self):
        """Test get return proper data."""
        client = Client()
        client.login(username='john', password='johnpassword')
        resp = client.get(reverse('examdownload_subjects_list'))
        last_subject = '__NONE__'
        index = 0
        for subject in (Exam.objects.order_by('subject')
                        .values_list('subject', flat=True)):
            if subject != last_subject:
                last_subject = subject
                index += 1
                subject_html = ("<button data-toggle=\"collapse\" data"
                                "-target=\"#demo{}\" class='btn btn-primary"
                                " buttonspace'>{}</button>"
                                .format(index, subject))
                self.assertInHTML(subject_html, resp.content)

    def test_view_schools(self):
        """Test response contains schools."""
        client = Client()
        client.login(username='john', password='johnpassword')
        resp = client.get(reverse('examdownload_subjects_list'))
        for school in set(Exam.objects.values_list('school', flat=True)):
            school_html = '<h1>{}</h1>'.format(school)
            self.assertInHTML(school_html, resp.content)

    def test_view_exams(self):
        """Test response contains schools."""
        client = Client()
        client.login(username='john', password='johnpassword')
        resp = client.get(reverse('examdownload_subjects_list'))
        for exam_title, publish in set(Exam.objects
                                       .values_list('title', 'publish')):
            exam_title_html = ("<input class='col-xs-11 btn "
                               "btn-primary buttonspace' data-action='"
                               "show-spinner' type=\"submit\"value=\"{}\">"
                               .format(exam_title))
            if publish:
                self.assertInHTML(exam_title_html, resp.content)
            else:
                self.assertNotIn(exam_title, resp.content)


class SubjectExecTestCase(TestCase):
    """Test data viewed from database."""

    faker = None
    lessons = None

    @classmethod
    def setUpClass(cls):
        """Set up faker and lessons list."""
        cls.faker = Factory.create()
        super(SubjectExecTestCase, cls).setUpClass()

    def _get_random_school(self):  # pylint: disable=no-self-use
        return random.choice([
            '#001 School',
            '#001 School',
            '#001 School',
            '#004 HighSchool',
            '#005 HighSchool',
            '#006 HighSchool',
        ])

    def _get_random_exam(self):
        return {
            'title': self.faker.sentence(nb_words=4),  # noqa pylint: disable=no-member
            'school': self._get_random_school(),
            'exam_type': self.faker.name(),  # pylint: disable=no-member
            'description': self.faker.sentence(nb_words=4),  # noqa pylint: disable=no-member
            'publish': random.choice([True, False]),
            'docs': 'file1.docx',
            'level': 'Zero',
            'creditcost': 50,
        }

    def setUp(self):
        """Setups database."""
        self.exams = []
        for i in range(10):
            data = self._get_random_exam()
            if i < 5:
                data['subject'] = 'Math'
            else:
                data['subject'] = 'History'
            exam = Exam.objects.create(**data)
            exam.save()
            self.exams.append(exam)

    def test_subject_has_exam(self):
        """Test models."""
        first = self.exams[0]
        self.assertEqual(first.subject, 'Math')
        count_of_exams = Exam.objects.count()
        self.assertEqual(count_of_exams, 10)
