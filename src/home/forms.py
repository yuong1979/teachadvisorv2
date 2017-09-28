from django import forms
# from home.models import Registration
from teacher.models import Teacher
from student.models import Student
from orders.models import Order
from variables.models import Country, Subject_Expertise, Level_Expertise, Educational_Level, Education, Region, Education_School, Expertise_Type
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField, Field, Reset, HTML, Button
from crispy_forms.bootstrap import TabHolder, Tab, InlineCheckboxes, AppendedText, InlineRadios


class ContactForm(forms.Form):
	full_name = forms.CharField(required=False)
	email = forms.EmailField()
	message = forms.CharField(widget=forms.Textarea)


class OrderChartForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            # "educational_level",
            # "expertise_type",
            # "group_tuition"
        ]

    def __init__(self, *args, **kwargs):
        super(OrderChartForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'get'

        self.helper.layout = Layout(

            HTML("""<div class="col-xs-12 col-md-12 col-lg-12"><h4><label>Subject</label></h4></div>"""),
            HTML("""<div class="col-xs-12 col-md-12 col-lg-12"><span><b>Languages</b></span></div>"""),
            Div(InlineRadios('subject_1'), css_class='col-xs-12 col-md-12 col-lg-12'),

            HTML("""<div class="col-xs-12 col-md-12 col-lg-12"><span><b>Math & Sciences</b></span></div>"""),
            Div(InlineRadios('subject_2'), css_class='col-xs-12 col-md-12 col-lg-12'),

            HTML("""<div class="col-xs-12 col-md-12 col-lg-12"><span><b>Arts, Humanities & Others</b></span></div>"""),
            Div(InlineRadios('subject_3'), css_class='col-xs-12 col-md-12 col-lg-12'),

            HTML("""<div class="col-xs-12 col-md-12 col-lg-12"><h4><label>Level</label></h4></div>"""),
            Div(InlineRadios('level'), css_class='col-xs-12 col-md-12 col-lg-12'),
            # Div(InlineCheckboxes('educational_level'), css_class='col-xs-12 col-md-12 col-lg-12'),
            # Div(InlineCheckboxes('expertise_type'), css_class='col-xs-12 col-md-12 col-lg-12'),
            # Div(Field('minimum_years'), css_class='col-xs-12 col-md-6 col-lg-6'),
            # HTML("""<div class="col-xs-12 col-md-12 col-lg-12"><h4><label>Group Tuition</label></h4></div>"""),
            Div(Field('group_tuition'), css_class='col-xs-12'),

            ButtonHolder(
                Submit('submit', 'Refresh', css_class='col-sm-4 col-sm-offset-1'),
                HTML('<a class="btn btn-default col-sm-4 col-sm-offset-1" href="{% url "StudentChart" %}">Reset</a>'),
            ),
        )

    subject_1 = forms.ModelMultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple(),
        queryset=Subject_Expertise.objects.filter(description='Languages'),
        label=""
    )
    subject_2 = forms.ModelMultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple(),
        queryset=Subject_Expertise.objects.filter(description='Math & Sciences'),
        label=""
    )
    subject_3 = forms.ModelMultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple(),
        queryset=Subject_Expertise.objects.filter(description='Arts, Humanities & Others'),
        label=""
    )

    level = forms.ModelMultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple(),
        queryset=Level_Expertise.objects.all(),
        label=""
    )

    group_tuition = forms.BooleanField(
        required=False,
        label="Group Tuition"
    )

    # educational_level = forms.ModelMultipleChoiceField(
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple(),
    #     queryset=Educational_Level.objects.all(),
    #     label="Teacher's Education"
    # )

    # expertise_type = forms.ModelMultipleChoiceField(
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple(),
    #     queryset=Expertise_Type.objects.all(),
    #     label="Teacher's Current Role"
    # )

    # minimum_years = forms.IntegerField(
    #     required=False,
    #     initial=0,
    #     min_value=0,
    #     max_value=20,
    #     label="Minimum Years of Experience"
    # )



