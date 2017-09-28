from django import forms
from teacher.models import Teacher
import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField, Field, Reset, HTML
from crispy_forms.bootstrap import TabHolder, Tab, InlineCheckboxes, AppendedText, InlineRadios
from opening.models import Opening
from variables.models import Level_Expertise, Region, Subject_Expertise, Educational_Level, Expertise_Type





pay_choices = (
    ('', '---'),
    ('5',  '$5/Hour'),
    ('10',  '$10/Hour'),
    ('15',  '$15/Hour'),
    ('20',  '$20/Hour'),
    ('25',  '$25/Hour'),
    ('30',  '$30/Hour'),
    ('35',  '$35/Hour'),
    ('40',  '$40/Hour'),
    ('45',  '$45/Hour'),
    ('50',  '$50/Hour'),
    ('55',  '$55/Hour'),
    ('60',  '$60/Hour'),
    ('65',  '$65/Hour'),
    ('70',  '$70/Hour'),
    ('75',  '$75/Hour'),
    ('80',  '$80/Hour'),
    ('85',  '$85/Hour'),
    ('90',  '$90/Hour'),
    ('95',  '$95/Hour'),
    ('100',  '$100/Hour'),
    ('105',  '$105/Hour'),
    ('110',  '$110/Hour'),
    ('115',  '$115/Hour'),
    ('120',  '$120/Hour'),
    ('125',  '$125/Hour'),
    ('130',  '$130/Hour'),
    ('135',  '$135/Hour'),
    ('140',  '$140/Hour'),
    ('145',  '$145/Hour'),
    ('150',  '$150/Hour'),
    ('155',  '$155/Hour'),
    ('160',  '$160/Hour'),
    ('165',  '$165/Hour'),
    ('170',  '$170/Hour'),
    ('175',  '$175/Hour'),
    ('180',  '$180/Hour'),
    ('185',  '$185/Hour'),
    ('190',  '$190/Hour'),
    ('195',  '$195/Hour'),
    ('200',  '$200/Hour'),
)




class PriceForm(forms.Form):
    price = forms.ChoiceField(label='Your offer - $/hr ', choices=pay_choices )


class OpeningForm(forms.ModelForm):

	class Meta:
		model = Opening
		fields = [

			"title",
			"subject",
			"level",
			"description",
			"salary_range",
			"negotiable",
			"region",
			# "private",
			"group_tuition",
			# "job_active"
			

		]

		labels = {
			'salary_range': 'Your offering Rate/Hour',
			'negotiable': 'Negotiable',
			'description': 'Please state other requirements',
			'region': 'Your region',
			# 'private': 'Hide this job from public',
			'group_tuition': 'Group tuition',
		}

		help_texts = {
			'title': 'Please state what you are looking for, i.e a JC2 math tutor',
			# 'job_active': 'Please choose active to activate this opening.',
			# 'negotiable': 'Is the salary negotiable.',
		}


	def __init__(self, *args, **kwargs):
		super(OpeningForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', value='Save Details', css_class='buttonspace btn-success'))

		self.helper.layout = Layout(

            HTML("""<br><br>"""),

            Fieldset(
            	'Job Details',

            	Div(Field('title'), css_class='col-xs-12 col-sm-10 col-md-8'),
            	HTML("""<div class="row"></div>"""),

				Div(Field('subject'), css_class='col-xs-12 col-sm-10 col-md-8'),
				HTML("""<div class="row"></div>"""),

				Div(InlineRadios('level'), css_class='col-xs-12'),

				HTML("""<div class="col-sm-12"><br></div>"""),

				Div(Field('description'), css_class='col-xs-12'),

            ),

            HTML("""<br>"""),

            Fieldset(
            	'Other Details',

				Div(Field('salary_range'), css_class='col-xs-6 col-sm-4'),
				HTML("""<div class="col-xs-6 col-md-6 col-lg-6"><br></div>"""),

				Div(Field('negotiable'), css_class='col-xs-6'),
				HTML("""<div class="row"></div>"""),

				Div(InlineRadios('region'), css_class='col-xs-12'),
				HTML("""<div class="row"></div>"""),

				Div(Field('group_tuition'), css_class='col-xs-12'),

				# HTML("""<div class="row"></div>"""),

				# Div(Field('job_active'), css_class='col-xs-12'),
            ),

		)



	salary_range = forms.ChoiceField(
		required=False,
		choices=pay_choices,
		label="Offering Rate/Hour"
	)





class SearchOpeningForm(forms.ModelForm):

	class Meta:
		model = Opening
		fields = [

				# "subject",
				# "level",
				# "region",

		]

	def __init__(self, *args, **kwargs):
		super(SearchOpeningForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		# self.helper.form_id = 'test'
		self.helper.form_method = 'get'
		self.helper.form_id = 'search-openings-form'
		# self.helper.form_action = reverse('Home')
		# self.helper.add_input(Submit('submit', value='Refresh', css_class='btn-block btn-success'))
		# self.helper.add_input(Reset('name', 'Reset')) #implement this when jquery is up and remove submit
		# self.helper.form_class = 'form-horizontal'
		# self.helper.form_class = 'search'
		self.helper.form_class = 'search'


		self.helper.layout = Layout(

			TabHolder(

				Tab('Subject/Level',

                    HTML("""<div class="col-xs-12 col-md-12 col-lg-12"><h4><label>Subject</label></h4></div>"""),

                    Div(Field('subject_1'), css_class='col-xs-12 col-sm-4 col-lg-4'),

                    Div(Field('subject_2'), css_class='col-xs-12 col-sm-4 col-lg-4'),

                    Div(Field('subject_3'), css_class='col-xs-12 col-sm-4 col-lg-4'),

                    HTML("""<div class="col-xs-12 col-md-12 col-lg-12"><h4><label>Level</label></h4></div>"""),
                    Div(InlineRadios('level_grp'), css_class='col-xs-12 col-md-12 col-lg-12'),

                    ButtonHolder(
                        HTML('<a class="btn btn-default col-xs-12 col-sm-4 col-sm-offset-4 extra-top-15" href="{% url "OpeningList" %}">Reset</a>'),
                    ),

				),
				Tab('Region',

                    HTML("""<div class="col-xs-12 col-sm-12"><h4><label>Preferred Regions</label></h4></div>"""),

                    Div(InlineCheckboxes('region_1'), css_class='col-xs-12 col-sm-6'),
                    Div(InlineCheckboxes('region_2'), css_class='col-xs-12 col-sm-6'),
                    Div(InlineCheckboxes('region_3'), css_class='col-xs-12 col-sm-6'),
                    Div(InlineCheckboxes('region_4'), css_class='col-xs-12 col-sm-6'),

                    ButtonHolder(
                        HTML('<a class="btn btn-default col-xs-12 col-sm-4 col-sm-offset-4 extra-top-15" href="{% url "OpeningList" %}">Reset</a>'),
                    ),

				),

                Tab('Other Details',
                	HTML("""<div class="col-xs-12 col-sm-12"><h4><label>Other Details</label></h4></div>"""),
                	Div(Field('minimum_pay'), css_class='col-xs-12 col-sm-6'),
                    
                    # HTML("""<div class="col-xs-12 col-sm-12"><h4><label>Group Tuition</label></h4></div>"""),
                    Div(InlineRadios('group_tuition'), css_class='col-xs-12 col-sm-6'),

                    ButtonHolder(
                        HTML('<a class="btn btn-default col-xs-12 col-sm-4 col-sm-offset-4 extra-top-15" href="{% url "OpeningList" %}">Reset</a>'),
                    ),

                ),

                Tab('Keyword',
					Div(Field('search'), css_class='col-xs-12 col-sm-offset-3 col-sm-6 col-sm-offset-3'),
                    ButtonHolder(
                        Submit('submit', 'Search', css_class='col-xs-12 col-sm-offset-4 col-sm-4 col-sm-offset-4'),
                        HTML("""<div class="col-xs-12"><br></div>"""),
                        HTML('<a class="btn btn-default col-xs-12 col-sm-offset-4 col-sm-4 col-sm-offset-4" href="{% url "OpeningList" %}">Reset</a>'),
                    ),
                    ),
			),

            # ButtonHolder(
            #     Submit('submit', 'Refresh', css_class='col-xs-4 col-xs-offset-1'),
            #     HTML('<a class="btn btn-default col-xs-4 col-xs-offset-1" href="{% url "OpeningList" %}">Reset</a>'),
            # ),


		)




	subject_1 = forms.ModelChoiceField(
		# required=True,
		# widget=forms.CheckboxSelectMultiple(),
		queryset=Subject_Expertise.objects.filter(description='Languages'),
		label="Languages"
	)
	subject_2 = forms.ModelChoiceField(
		# required=True,
		# widget=forms.CheckboxSelectMultiple(),
		queryset=Subject_Expertise.objects.filter(description='Math & Sciences'),
		label="Math & Sciences"
	)
	subject_3 = forms.ModelChoiceField(
		# required=True,
		# widget=forms.CheckboxSelectMultiple(),
		queryset=Subject_Expertise.objects.filter(description='Arts, Humanities & Others'),
		label="Arts, Humanities & Others"
	)


	level_grp = (
		('Lower Primary', 'Lower Primary'),
		('Higher Primary', 'Higher Primary'),
		('Lower Secondary', 'Lower Secondary'),
		('Higher Secondary', 'Higher Secondary'),
		('Junior College', 'Junior College'),
		('University', 'University'),
		('NA', 'NA')
	)

	level_grp = forms.ChoiceField(
		label='', 
		choices=level_grp )


	region_1 = forms.ModelMultipleChoiceField(
		required=False,
		widget=forms.CheckboxSelectMultiple(),
		queryset=Region.objects.filter(description='Central'),
		label="Central locations"
	)

	region_2 = forms.ModelMultipleChoiceField(
		required=False,
		widget=forms.CheckboxSelectMultiple(),
		queryset=Region.objects.filter(description='North'),
		label="North locations"
	)

	region_3 = forms.ModelMultipleChoiceField(
		required=False,
		widget=forms.CheckboxSelectMultiple(),
		queryset=Region.objects.filter(description='East'),
		label="East locations"
	)

	region_4 = forms.ModelMultipleChoiceField(
		required=False,
		widget=forms.CheckboxSelectMultiple(),
		queryset=Region.objects.filter(description='West'),
		label="West locations"
	)



	minimum_pay = forms.ChoiceField(
		required=False,
		# initial=120,
		choices=pay_choices,
		label="Minimum Rate/Hour"
	)

	gt_choices = (
		('Yes',  'Yes'),
		('No',  'No')
	)

	group_tuition = forms.ChoiceField(
		required=False,
		choices=gt_choices,
		label="Group Tuition"
	)

	search = forms.CharField(
		label='Keyword Search', 
		max_length=30,
		required = False
	)