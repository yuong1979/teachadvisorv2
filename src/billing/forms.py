from django import forms
# from teacher.models import Teacher
# import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField, Field, Reset, HTML
from crispy_forms.bootstrap import TabHolder, Tab, InlineCheckboxes, AppendedText, InlineRadios
from billing.models import CreditToCash, FeaturedUser_0, FeaturedUser_1
from billing.control import feat_days_choices, img_days_choices, ana_days_choices, studentbi_days_choices
from teacher.models import Teacher
from variables.models import Country, Subject_Expertise, Level_Expertise, Educational_Level, Education, Region, Education_School, Expertise_Type



class FeatureSubForm(forms.Form):

	creditfeat = forms.ChoiceField(
		label='Number of Days/Credits',
		choices=feat_days_choices,
		widget=forms.RadioSelect(),
		required=True
		)

	def __init__(self, *args, **kwargs):
		super(FeatureSubForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', value='Purchase', css_class='btn-success buttonspace'))




class ImgSubForm(forms.Form):

	creditimg = forms.ChoiceField(
		label='Number of Days/Credits',
		choices=img_days_choices,
		widget=forms.RadioSelect(),
		required=True
		)

	def __init__(self, *args, **kwargs):
		super(ImgSubForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', value='Purchase', css_class='btn-success buttonspace'))




class AnaSubForm(forms.Form):

	creditana = forms.ChoiceField(
		label='Number of Days/Credits',
		choices=ana_days_choices,
		widget=forms.RadioSelect(),
		required=True
		)

	def __init__(self, *args, **kwargs):
		super(AnaSubForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', value='Purchase', css_class='btn-success buttonspace'))



class StudentBISubForm(forms.Form):

	creditbi = forms.ChoiceField(
		label='Number of Days/Credits',
		choices=studentbi_days_choices,
		widget=forms.RadioSelect(),
		required=True
		)

	def __init__(self, *args, **kwargs):
		super(StudentBISubForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', value='Purchase', css_class='btn-success buttonspace'))





class CreditForm(forms.ModelForm):

	class Meta:
		model = CreditToCash
		fields = [
			# "Credits",
		]

	credit = forms.ModelChoiceField(
		label='Amount of Credits/SGD', 
		queryset=CreditToCash.objects.all().order_by('id'),
		widget=forms.RadioSelect(),
		required=True
		)

	def __init__(self, *args, **kwargs):
		super(CreditForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', value='Purchase', css_class='btn-success buttonspace'))










