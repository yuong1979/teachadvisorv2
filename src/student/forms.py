from django import forms
from student.models import Student
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField, Field, Reset, HTML
from crispy_forms.bootstrap import TabHolder, Tab, InlineCheckboxes, AppendedText, InlineRadios
import datetime

class StudentAddForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = [

			"first_name",
			"last_name",
			"contact",
		]

		labels = {
			'last_name': 'Surname',
			'birth_date': 'Date of Birth',
			'contact': 'Contact No. (xxxx-xxxx) for verification purposes',
		}

        # help_texts = {
        #     'contact': 'Your contact number is used for verification and will be kept confidential',
        # }


		# help_texts = {
		# 	'contact': 'for verification purposes'
		# }

	def __init__(self, *args, **kwargs):
		super(StudentAddForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', value='Save Details', css_class='buttonspace btn-success'))
		self.helper.layout = Layout(

		HTML("""<br><br>"""),

		Fieldset(
			'Personal Details',

			Div(Field('first_name'), css_class='col-xs-12 col-sm-10 col-md-8'),
			HTML("""<div class="row"></div>"""),

			Div(Field('last_name'), css_class='col-xs-12 col-sm-10 col-md-8'),
			HTML("""<div class="row"></div>"""),

			Div(Field('contact'), css_class='col-xs-12 col-sm-10 col-md-8'),
			HTML("""<div class="row"></div>"""),

		),


		HTML("""<br><br>"""),

		Fieldset(
			'Terms and Conditions',
			Div(Field('termsandconditions'), css_class='col-xs-12 col-md-12'),
		)

		)


	termsandconditions = forms.BooleanField(
		required=True,
		label="""
        I understand and agree to the teach-advisor 
        <a href='/termsandconditions/' >Terms and conditions</a>, 
        <a href='/disclaimer/' >Disclaimer</a>,
        <a href='/privacypolicy/' >Privacy Policy</a> and 
        <a href='/refundpolicy/' >Refund Policy</a>.
        """
	)




class StudentEditForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = [

			"first_name",
			"last_name",
			"contact",
		]

		labels = {
			'last_name': 'Surname',
			'birth_date': 'Date of Birth',
			'contact': 'Contact No. (xxxx-xxxx) for verification purposes',
		}


        # help_texts = {
        #     'contact': 'Your contact number is used for verification and will be kept confidential',
        # }



	def __init__(self, *args, **kwargs):
		super(StudentEditForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', value='Save Details', css_class='buttonspace btn-success'))
		self.helper.layout = Layout(

		HTML("""<br><br>"""),

		Fieldset(
			'Personal Details',

			Div(Field('first_name'), css_class='col-xs-12 col-sm-10 col-md-8'),
			HTML("""<div class="row"></div>"""),

			Div(Field('last_name'), css_class='col-xs-12 col-sm-10 col-md-8'),
			HTML("""<div class="row"></div>"""),

			Div(Field('contact'), css_class='col-xs-12 col-sm-10 col-md-8'),
			HTML("""<div class="row"></div>"""),

		),

		)