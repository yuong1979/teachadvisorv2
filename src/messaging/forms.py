from django import forms
from messaging.models import Message
from django.forms import Textarea
from teacher.models import Teacher
from billing.control import msgcredit
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField, Field, Reset, HTML, Button
from crispy_forms.bootstrap import TabHolder, Tab, InlineCheckboxes, AppendedText, InlineRadios


# class MessageText(Textarea):
# 	class Media:
# 		js = ('https://code.jquery.com/jquery-1.12.4.min.js', 'http://ned.im/noty/vendor/noty-2.4.1/js/noty/packaged/jquery.noty.packaged.js', 'js/customer_detail.js')


class MessageText(Textarea):
	class Media:
		js = ('https://code.jquery.com/jquery-1.12.4.min.js', 'http://ned.im/noty/vendor/noty-2.4.1/js/noty/packaged/jquery.noty.packaged.js')


class PostMessage(forms.ModelForm):

	class Meta:
		model =  Message
		fields = [
		"title",
		"content",
		]

	paid = forms.BooleanField(
		initial=True,
		label='Please confirm to agree that ' + str(msgcredit) + ' credits will be deducted from your account',
		required=True
	)


	def __init__(self, user_type, *args, **kwargs):
		super(PostMessage, self).__init__(*args, **kwargs)
		if user_type == "student":
			self.fields['paid'].widget = forms.HiddenInput()
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', value='Send', css_class='btn-success'))


class PostReply(forms.ModelForm):
	class Meta:
		model =  Message
		fields = [
		"content",
		]

		labels = {
			'content': 'Reply',
		}

		widgets = {
			'content': MessageText(),
		}


