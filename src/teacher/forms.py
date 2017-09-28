from django import forms
from django.utils import timezone
from teacher.models import Teacher
import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField, Field, Reset, HTML, Button
from crispy_forms.bootstrap import TabHolder, Tab, InlineCheckboxes, AppendedText, InlineRadios
from variables.models import Country, Subject_Expertise, Level_Expertise, Educational_Level, Education, Region, Education_School, Expertise_Type
from tags.models import TagTeacher
from django.core.urlresolvers import reverse
from billing.models import ImageSubscription



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


exp_choices = (
    ('0',  'None'),
    ('1',  '1 year'),
    ('2',  '2 years'),
    ('3',  '3 years'),
    ('4',  '4 years'),
    ('5',  '5 years'),
    ('6',  '6 years'),
    ('7',  '7 years'),
    ('8',  '8 years'),
    ('9',  '9 years'),
    ('10',  '10 years'),
    ('11',  '11 years'),
    ('12',  '12 years'),
    ('13',  '13 years'),
    ('14',  '14 years'),
    ('15',  '15 years'),
    ('16',  '16 years'),
    ('17',  '17 years'),
    ('18',  '18 years'),
    ('19',  '19 years'),
    ('20',  '20 years')
)




class TeacherAddForm(forms.ModelForm):
    # tags = forms.CharField(label='Please add relevant skills - special needs, piano, java-programming', required=False)

    class Meta:
        model = Teacher
        fields = [

            "title",
            "first_name",
            "last_name",
            "contact",
            "birth_date",
            "gender",

            "first_subject",
            "first_level",
            "second_subject",
            "second_level",
            "third_subject",
            "third_level",

            "educational_level",
            "education",
            "education_school",
            "expertise_type",
            "years_of_experience",
            "description",
            "website_url",

            "salary_expectation",
            "salary_negotiable",
            "group_tuition",
            "region",
            "postal_code",
            "active",

            "image",
            # "doc1",
            # "doc1description",
            # "doc2",
            # "doc2description",
            # "doc3",
            # "doc3description",
            # "doc4",
            # "doc4description",
            # "doc5",
            # "doc5description",
            # "doc6",
            # "doc6description",
        ]

        labels = {
            'last_name': 'Surname',
            'contact': 'Contact No. (xxxx-xxxx)',
            'birth_date': 'Date of Birth',
            'first_level': 'Level',
            'first_subject': 'Subject',
            'second_level': 'Level',
            'second_subject': 'Subject',
            'third_level': 'Level',
            'third_subject': 'Subject',
            'educational_level': 'Your level of education',
            'education': 'Your UnderGraduate/PostGraduate courses',
            'education_school': 'Your educational institute',
            'expertise_type': 'Your current status',
            'description': 'A description of your special skills - "special needs", "piano", "java-programming"',
            'website_url': 'Your website (if any)',
            'salary_expectation': 'Asking Rate/Hour',
            'salary_negotiable': 'Negotiable',
            'postal_code': 'Your Postal Code',
            'group_tuition': 'Provide group tuitions',
            'active': 'Profile active',
            'image': 'Load your profile image',

        }

        help_texts = {
            'title': 'Please market your services - i.e Reliable JC Math Tutor',
            'contact': 'Your contact number is used for verification and will be kept confidential',
            # 'active': 'Please choose active if you want your profile to be public.',
            'website_url': 'Your website and/or linkedin profile(if any)',
            # 'tags': 'Please add your specialised skills - "special needs", "nuclear-physics", "java-programming",',
        }

        widgets = {
            'birth_date': forms.SelectDateWidget(years=range(1960, datetime.date.today().year), attrs=({'style': 'width: 30%; display: inline-block;'}))
        }


    def __init__(self, *args, **kwargs):
        super(TeacherAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', value='Save Details', css_class='buttonspace btn-success'))

        self.helper.layout = Layout(

            HTML("""<br><br>"""),

            Fieldset(
                'Personal details',

                Div(Field('title'), css_class='col-xs-12 col-sm-10 col-md-8'),
                HTML("""<div class="row"></div>"""),

                Div(Field('first_name'), css_class='col-xs-12 col-sm-10 col-md-8'),
                HTML("""<div class="row"></div>"""),

                Div(Field('last_name'), css_class='col-xs-12 col-sm-10 col-md-8'),
                HTML("""<div class="row"></div>"""),

                Div(Field('contact'), css_class='col-xs-12 col-sm-10 col-md-8'),
                HTML("""<div class="row"></div>"""),

                Div(Field('birth_date'), css_class='col-xs-12 col-sm-10 col-md-8'),
                HTML("""<div class="row"></div>"""),

                Div(Field('postal_code'), css_class='col-xs-12 col-sm-4 col-md-4'),
                HTML("""<div class="row"></div>"""),

                Div(InlineRadios('gender'), css_class='col-xs-12 col-sm-10 col-md-8'),
                HTML("""<div class="row"></div>"""),

            ),

            HTML("""<br><br>"""),

            Fieldset(
                'Your primary subject specialization',

                Div(Field('first_subject'), css_class='col-xs-12 col-sm-10 col-md-8'),
                HTML("""<div class="row"></div>"""),
                Div(InlineCheckboxes('first_level'), css_class='col-xs-12'),

            ),

            HTML("""<br><br>"""),

            Fieldset(
                'Your secondary subject specialization',

                Div(Field('second_subject'), css_class='col-xs-12 col-sm-10 col-md-8'),
                HTML("""<div class="row"></div>"""),
                Div(InlineCheckboxes('second_level'), css_class='col-xs-12'),
            ),

            HTML("""<br><br>"""),

            Fieldset(
                'Your other subject specialization',

                Div(Field('third_subject'), css_class='col-xs-12 col-sm-10 col-md-8'),
                HTML("""<div class="row"></div>"""),
                Div(InlineCheckboxes('third_level'), css_class='col-xs-12'),
            ),

            HTML("""<br><br>"""),

            Fieldset(
                'Educational qualifications',

                Div(InlineCheckboxes('educational_level'), css_class='col-xs-12'),

                Div(Field('education'), css_class='col-xs-12 col-sm-10 col-md-8'),

                Div(InlineCheckboxes('education_school'), css_class='col-xs-12'),

                Div(InlineRadios('expertise_type'), css_class='col-xs-12'),

                Div(Field('years_of_experience'), css_class='col-xs-6 col-sm-4'),

                Div(Field('description'), css_class='col-xs-12'),

                Div(Field('website_url'), css_class='col-xs-12'),

                # Div(Field('tags'), css_class='col-xs-12'),

            ),

            HTML("""<br><br>"""),

            Fieldset(
                'Tuition Rates',

                Div(Field('salary_expectation'), css_class='col-xs-6 col-sm-4'),
                HTML("""<div class="col-xs-6 col-md-6 col-lg-6"><br></div>"""),

                Div(Field('salary_negotiable'), css_class='col-xs-6'),
                HTML("""<div class="row"></div>"""),
            ),



            HTML("""<br><br>"""),

            Fieldset(
                'Region Availabilty',
                Div(InlineCheckboxes('region'), css_class='col-xs-12'),
            ),



            HTML("""<br><br>"""),

            Fieldset(
                'Group Tuition',
                Div(Field('group_tuition'), css_class='col-xs-12'),
            ),


            HTML("""<br><br>"""),

            Fieldset(
                'Actively looking for new jobs',
                Div(Field('active'), css_class='col-xs-12'),
            ),


            HTML("""<br><br>"""),

            Fieldset(
                'Select your profile picture',
                Div(Field('image'), css_class='col-xs-12'),

            ),

            HTML("""<br>"""),

            # Fieldset(
            #     'Loading images/documents (Requires subscription)',

            #     Div(Field('doc1'), css_class='col-xs-12'),
            #     Div(Field('doc1description'), css_class='col-xs-12 col-sm-10 col-md-8'),
            #     HTML("""<br>"""),
            #     Div(Field('doc2'), css_class='col-xs-12'),
            #     Div(Field('doc2description'), css_class='col-xs-12 col-sm-10 col-md-8'),
            #     HTML("""<br>"""),
            #     Div(Field('doc3'), css_class='col-xs-12'),
            #     Div(Field('doc3description'), css_class='col-xs-12 col-sm-10 col-md-8'),
            #     HTML("""<br>"""),
            #     Div(Field('doc4'), css_class='col-xs-12'),
            #     Div(Field('doc4description'), css_class='col-xs-12 col-sm-10 col-md-8'),
            #     HTML("""<br>"""),
            #     Div(Field('doc5'), css_class='col-xs-12'),
            #     Div(Field('doc5description'), css_class='col-xs-12 col-sm-10 col-md-8'),
            #     HTML("""<br>"""),
            #     Div(Field('doc6'), css_class='col-xs-12'),
            #     Div(Field('doc6description'), css_class='col-xs-12 col-sm-10 col-md-8'),
            #     HTML("""<br>"""),

            # ),

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


    first_level = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Level_Expertise.objects.all(),
        label="Level",
        required=True
    )


    first_level = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Level_Expertise.objects.all(),
        label="Level",
        required=True
    )

    second_level = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Level_Expertise.objects.all(),
        label="Level",
        required=False
    )

    third_level = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Level_Expertise.objects.all(),
        label="Level",
        required=False
    )


    educational_level = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        queryset=Educational_Level.objects.all(),
        label="Your Level of Education"
    )

    education_school = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        queryset=Education_School.objects.all(),
        label="Your Education Institute"
    )


    years_of_experience = forms.ChoiceField(
        required=True,
        choices=exp_choices,
        label="Years of Experience"
    )


    salary_expectation = forms.ChoiceField(
        required=True,
        choices=pay_choices,
        label="Asking Rate/Hour"
    )

    region = forms.ModelMultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        queryset=Region.objects.all(),
        label="Your Preferred Locations"
    )


    doc1 = forms.ImageField(
        label="Load document 1",
        required=False,
    )


    doc2 = forms.ImageField(
        label="Load document 2",
        required=False,
    )

    doc3 = forms.ImageField(
        label="Load document 3",
        required=False,
    )

    doc4 = forms.ImageField(
        label="Load document 4",
        required=False,
    )

    doc5 = forms.ImageField(
        label="Load document 5",
        required=False,
    )

    doc6 = forms.ImageField(
        label="Load document 6",
        required=False,
    )


    doc1description = forms.CharField(
        label="Name document 1",
        required=False,
    )

    doc2description = forms.CharField(
        label="Name document 2",
        required=False,
    )

    doc3description = forms.CharField(
        label="Name document 3",
        required=False,
    )

    doc4description = forms.CharField(
        label="Name document 4",
        required=False,
    )

    doc5description = forms.CharField(
        label="Name document 5",
        required=False,
    )

    doc6description = forms.CharField(
        label="Name document 6",
        required=False,
    )

    # def clean_tags(self):
    #     tags = self.cleaned_data.get("tags")
    #     tags_list = tags.split(",")
    #     for i in tags_list:
    #         if not i == " ":
    #             if len(i) > 30:
    #                 raise forms.ValidationError("please make sure your tags stay below 30 characters")
    #     return tags




    def common_clean_images(self, name):

        image = self.cleaned_data.get(name, False)
        if image and getattr(self.instance, name) != image:
            if image.size > 2.0*1024*1024:
                raise forms.ValidationError("Image file too large ( > 2.0 mb )")
        return image



    def clean_image(self):
        return self.common_clean_images('image')

    def clean_doc1(self):
        return self.common_clean_images('doc1')

    def clean_doc2(self):
        return self.common_clean_images('doc2')

    def clean_doc3(self):
        return self.common_clean_images('doc3')

    def clean_doc4(self):
        return self.common_clean_images('doc4')

    def clean_doc5(self):
        return self.common_clean_images('doc5')

    def clean_doc6(self):
        return self.common_clean_images('doc6')






















class TeacherEditForm(forms.ModelForm):
    # tags = forms.CharField(label='Please add relevant skills - special needs, piano, java-programming', required=False)

    class Meta:
        model = Teacher
        fields = [

            "title",
            "first_name",
            "last_name",
            "contact",
            "birth_date",
            "gender",

            "first_subject",
            "first_level",
            "second_subject",
            "second_level",
            "third_subject",
            "third_level",

            "educational_level",
            "education",
            "education_school",
            "expertise_type",
            "years_of_experience",
            "description",
            "website_url",

            "salary_expectation",
            "salary_negotiable",
            "group_tuition",
            "region",
            "postal_code",
            "active",

            # "advimage",
            "image",
            "doc1",
            "doc1description",
            "doc2",
            "doc2description",
            "doc3",
            "doc3description",
            "doc4",
            "doc4description",
            "doc5",
            "doc5description",
            "doc6",
            "doc6description",
        ]

        labels = {
            'last_name': 'Surname',
            'contact': 'Contact No. (xxxx-xxxx)',
            'birth_date': 'Date of Birth',
            'first_level': 'Level',
            'first_subject': 'Subject',
            'second_level': 'Level',
            'second_subject': 'Subject',
            'third_level': 'Level',
            'third_subject': 'Subject',
            'educational_level': 'Your level of education',
            'education': 'Your UnderGraduate/PostGraduate courses',
            'education_school': 'Your educational institute',
            'expertise_type': 'Your current status',
            'description': 'A description of your special skills - "special needs", "piano", "java-programming"',
            'website_url': 'Your website (if any)',
            'salary_expectation': 'Asking Rate/Hour',
            'salary_negotiable': 'Negotiable',
            'postal_code': 'Your Postal Code',
            'group_tuition': 'Provide group tuitions',
            'active': 'Profile active',
            'image': 'Load your profile image',
            # "advimage": 'Load your advertisement image',
        }

        help_texts = {
            'title': 'Please market your services - i.e Reliable JC Math Tutor',
            'contact': 'Your contact number is used for verification and will kept confidential',
            # 'active': 'Please choose active if you want your profile to be public.',
            'website_url': 'Your website and/or linkedin profile(if any)',
            # 'tags': 'Please add your specialised skills - "special needs", "nuclear-physics", "java-programming",',
        }

        widgets = {
            'birth_date': forms.SelectDateWidget(years=range(1960, datetime.date.today().year), attrs=({'style': 'width: 30%; display: inline-block;'}))
        }


    def __init__(self, *args, **kwargs):

        # this line should be before a super call
        self.request = kwargs.pop('request', None)



        super(TeacherEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', value='Save Details', css_class='buttonspace btn-success'))


        render_upload = True
        if not render_upload:
            upload_fields = [
                "doc1",
                "doc1description",
                "doc2",
                "doc2description",
                "doc3",
                "doc3description",
                "doc4",
                "doc4description",
                "doc5",
                "doc5description",
                "doc6",
                "doc6description"
            ]
            for f in upload_fields:
                self.fields.pop(f)


        # old image sub that requires users to be subscribed before they can use image loading
        # imgsub = ImageSubscription.objects.filter(user=self.request.user).first()
        # render_upload = True if imgsub and imgsub.subenddate > timezone.now().date() else False
        # if not render_upload:
        #     upload_fields = [
        #         "doc1",
        #         "doc1description",
        #         "doc2",
        #         "doc2description",
        #         "doc3",
        #         "doc3description",
        #         "doc4",
        #         "doc4description",
        #         "doc5",
        #         "doc5description",
        #         "doc6",
        #         "doc6description"
        #     ]
        #     for f in upload_fields:
        #         self.fields.pop(f)


        self.helper.layout = Layout(

            HTML("""<br><br>"""),

            Fieldset(
                'Personal details',

                Div(Field('title'), css_class='col-xs-12 col-sm-10 col-md-8'),
                HTML("""<div class="row"></div>"""),

                Div(Field('first_name'), css_class='col-xs-12 col-sm-10 col-md-8'),
                HTML("""<div class="row"></div>"""),

                Div(Field('last_name'), css_class='col-xs-12 col-sm-10 col-md-8'),
                HTML("""<div class="row"></div>"""),

                Div(Field('contact'), css_class='col-xs-12 col-sm-10 col-md-8'),
                HTML("""<div class="row"></div>"""),

                Div(Field('birth_date'), css_class='col-xs-12 col-sm-10 col-md-8'),
                HTML("""<div class="row"></div>"""),

                Div(Field('postal_code'), css_class='col-xs-12 col-sm-4 col-md-4'),
                HTML("""<div class="row"></div>"""),

                Div(InlineRadios('gender'), css_class='col-xs-12 col-sm-10 col-md-8'),
                HTML("""<div class="row"></div>"""),

            ),

            HTML("""<br><br>"""),

            Fieldset(
                'Your primary subject specialization',

                Div(Field('first_subject'), css_class='col-xs-12 col-sm-10 col-md-8'),
                HTML("""<div class="row"></div>"""),
                Div(InlineCheckboxes('first_level'), css_class='col-xs-12'),

            ),

            HTML("""<br><br>"""),

            Fieldset(
                'Your secondary subject specialization',

                Div(Field('second_subject'), css_class='col-xs-12 col-sm-10 col-md-8'),
                HTML("""<div class="row"></div>"""),
                Div(InlineCheckboxes('second_level'), css_class='col-xs-12'),
            ),

            HTML("""<br><br>"""),

            Fieldset(
                'Your other subject specialization',

                Div(Field('third_subject'), css_class='col-xs-12 col-sm-10 col-md-8'),
                HTML("""<div class="row"></div>"""),
                Div(InlineCheckboxes('third_level'), css_class='col-xs-12'),
            ),

            HTML("""<br><br>"""),

            Fieldset(
                'Educational qualifications',

                Div(InlineCheckboxes('educational_level'), css_class='col-xs-12'),

                Div(Field('education'), css_class='col-xs-12 col-sm-10 col-md-8'),

                Div(InlineCheckboxes('education_school'), css_class='col-xs-12'),

                Div(InlineRadios('expertise_type'), css_class='col-xs-12'),

                Div(Field('years_of_experience'), css_class='col-xs-6 col-sm-4'),

                Div(Field('description'), css_class='col-xs-12'),

                Div(Field('website_url'), css_class='col-xs-12'),

                # Div(Field('tags'), css_class='col-xs-12'),

            ),

            HTML("""<br><br>"""),

            Fieldset(
                'Tuition Rates',

                Div(Field('salary_expectation'), css_class='col-xs-6 col-sm-4'),
                HTML("""<div class="col-xs-6 col-md-6 col-lg-6"><br></div>"""),

                Div(Field('salary_negotiable'), css_class='col-xs-6'),
                HTML("""<div class="row"></div>"""),
            ),



            HTML("""<br><br>"""),

            Fieldset(
                'Region Availabilty',
                Div(InlineCheckboxes('region'), css_class='col-xs-12'),
            ),



            HTML("""<br><br>"""),

            Fieldset(
                'Group Tuition',
                Div(Field('group_tuition'), css_class='col-xs-12'),
            ),


            HTML("""<br><br>"""),

            Fieldset(
                'Actively looking for new jobs',
                Div(Field('active'), css_class='col-xs-12'),
            ),


            HTML("""<br><br>"""),

            Fieldset(
                'Select your profile picture',
                Div(Field('image'), css_class='col-xs-12'),

            ),

            HTML("""<br><br>"""),

            # Fieldset(
            #     'Select your advertisement image',
            #     Div(Field('advimage'), css_class='col-xs-12'),

            # ),

            HTML("""<br>"""),


            # Fieldset(
            #     'Loading images/documents',

            #     #implement an if else statement here based on user's imagesubscription object(below)
            #     # imgsub = get_object_or_404(ImageSubscription, user=user)
            #     # imgsubenddate = imgsub.subenddate

            #     # HTML("""<p><a href='{% url "ImageSub" %}' data-action='show-spinner' class='buttonspace1 btn btn-primary' > Subscribe <i class="fa fa-check-square-o fa-x"></i></a></p>"""),


            #     HTML("""<br>"""),
            #     Div(Field('doc1'), css_class='col-xs-12'),
            #     Div(Field('doc1description'), css_class='col-xs-12 col-sm-10 col-md-8'),
            #     HTML("""<br>"""),
            #     Div(Field('doc2'), css_class='col-xs-12'),
            #     Div(Field('doc2description'), css_class='col-xs-12 col-sm-10 col-md-8'),
            #     HTML("""<br>"""),
            #     Div(Field('doc3'), css_class='col-xs-12'),
            #     Div(Field('doc3description'), css_class='col-xs-12 col-sm-10 col-md-8'),
            #     HTML("""<br>"""),
            #     Div(Field('doc4'), css_class='col-xs-12'),
            #     Div(Field('doc4description'), css_class='col-xs-12 col-sm-10 col-md-8'),
            #     HTML("""<br>"""),
            #     Div(Field('doc5'), css_class='col-xs-12'),
            #     Div(Field('doc5description'), css_class='col-xs-12 col-sm-10 col-md-8'),
            #     HTML("""<br>"""),
            #     Div(Field('doc6'), css_class='col-xs-12'),
            #     Div(Field('doc6description'), css_class='col-xs-12 col-sm-10 col-md-8'),
            #     HTML("""<br>"""),

            # ),

        )
    
        if render_upload:
            self.helper.layout.append(
                Fieldset(
                    'Load scanned images of supporting documents',

                    Div(Field('doc1'), css_class='col-xs-12'),
                    Div(Field('doc1description'), css_class='col-xs-12 col-sm-10 col-md-8'),
                    HTML("""<br>"""),
                    Div(Field('doc2'), css_class='col-xs-12'),
                    Div(Field('doc2description'), css_class='col-xs-12 col-sm-10 col-md-8'),
                    HTML("""<br>"""),
                    Div(Field('doc3'), css_class='col-xs-12'),
                    Div(Field('doc3description'), css_class='col-xs-12 col-sm-10 col-md-8'),
                    HTML("""<br>"""),
                    Div(Field('doc4'), css_class='col-xs-12'),
                    Div(Field('doc4description'), css_class='col-xs-12 col-sm-10 col-md-8'),
                    HTML("""<br>"""),
                    Div(Field('doc5'), css_class='col-xs-12'),
                    Div(Field('doc5description'), css_class='col-xs-12 col-sm-10 col-md-8'),
                    HTML("""<br>"""),
                    Div(Field('doc6'), css_class='col-xs-12'),
                    Div(Field('doc6description'), css_class='col-xs-12 col-sm-10 col-md-8'),
                    HTML("""<br>"""),

                )
            )
        # old image subscription that requires the user to be subscribed before images can be loaded.
        # else:
        #     self.helper.layout.append(
        #         Fieldset(
        #             'Subscribe to Load Images and Documents',

        #             HTML("""<p><a href='{% url "ImageSub" %}' data-action='show-spinner' class='buttonspace1 btn btn-primary' > Subscribe <i class="fa fa-check-square-o fa-x"></i></a></p>"""),
        #             HTML("""<br>"""),
        #         )
        #     )



    first_level = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Level_Expertise.objects.all(),
        label="Level",
        required=True
    )


    first_level = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Level_Expertise.objects.all(),
        label="Level",
        required=True
    )

    second_level = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Level_Expertise.objects.all(),
        label="Level",
        required=False
    )

    third_level = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Level_Expertise.objects.all(),
        label="Level",
        required=False
    )

    educational_level = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        queryset=Educational_Level.objects.all(),
        label="Your Level of Education"
    )

    education_school = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        queryset=Education_School.objects.all(),
        label="Your Education Institute"
    )


    years_of_experience = forms.ChoiceField(
        required=True,
        choices=exp_choices,
        label="Years of Experience"
    )



    salary_expectation = forms.ChoiceField(
        required=True,
        choices=pay_choices,
        label="Asking Rate/Hour"
    )

    region = forms.ModelMultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        queryset=Region.objects.all(),
        label="Your Preferred Locations"
    )


    doc1 = forms.ImageField(
        label="Load document 1",
        required=False,
    )


    doc2 = forms.ImageField(
        label="Load document 2",
        required=False,
    )

    doc3 = forms.ImageField(
        label="Load document 3",
        required=False,
    )

    doc4 = forms.ImageField(
        label="Load document 4",
        required=False,
    )

    doc5 = forms.ImageField(
        label="Load document 5",
        required=False,
    )

    doc6 = forms.ImageField(
        label="Load document 6",
        required=False,
    )


    doc1description = forms.CharField(
        label="Name document 1",
        required=False,
    )

    doc2description = forms.CharField(
        label="Name document 2",
        required=False,
    )

    doc3description = forms.CharField(
        label="Name document 3",
        required=False,
    )

    doc4description = forms.CharField(
        label="Name document 4",
        required=False,
    )

    doc5description = forms.CharField(
        label="Name document 5",
        required=False,
    )

    doc6description = forms.CharField(
        label="Name document 6",
        required=False,
    )

    # def clean_tags(self):
    #     tags = self.cleaned_data.get("tags")
    #     tags_list = tags.split(",")
    #     for i in tags_list:
    #         if not i == " ":
    #             if len(i) > 30:
    #                 raise forms.ValidationError("please make sure your tags stay below 30 characters")
    #     return tags




    def common_clean_images(self, name):

        image = self.cleaned_data.get(name, False)
        if image and getattr(self.instance, name) != image:
            if image.size > 2.0*1024*1024:
                raise forms.ValidationError("Image file too large ( > 2.0 mb )")
        return image



    def clean_image(self):
        return self.common_clean_images('image')

    # def clean_advimage(self):
    #     return self.common_clean_images('advimage')

    def clean_doc1(self):
        return self.common_clean_images('doc1')

    def clean_doc2(self):
        return self.common_clean_images('doc2')

    def clean_doc3(self):
        return self.common_clean_images('doc3')

    def clean_doc4(self):
        return self.common_clean_images('doc4')

    def clean_doc5(self):
        return self.common_clean_images('doc5')

    def clean_doc6(self):
        return self.common_clean_images('doc6')

































class SearchTeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            # "region",
            # "educational_level",
            # "expertise_type",
            "group_tuition"
        ]

    def __init__(self, *args, **kwargs):
        super(SearchTeacherForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # self.helper.form_id = 'test'
        self.helper.form_method = 'get'
        self.helper.form_id = 'search-teachers-form'
        # self.helper.form_action = reverse('Home')
        # self.helper.add_input(Submit('submit', value='Refresh', css_class='col-sm-4 col-sm-offset-1'))
        # reset = Reset('reset', 'Reset', css_class='col-sm-4 col-sm-offset-1')
        # reset = Button('reset', 'Reset', css_class='col-sm-4 col-sm-offset-1')
        # reset = Submit('reset', 'Reset', css_class='col-sm-4 col-sm-offset-1')
        # self.helper.add_input(reset)
        # self.helper.form_class = 'form-horizontal'
        # self.helper.form_class = 'search'
        self.helper.form_class = 'search'

        self.helper.layout = Layout(

            TabHolder(

                # Tab('gender',
                #     Div(InlineCheckboxes('gender'), css_class='col-xs-12 col-md-12 col-lg-12'),
                # ),
                Tab('Subject/Level',
                    # HTML("""<br>test<br>"""),
                    HTML("""<div class="col-xs-12 col-12 col-lg-12"><h4><label>Subject</label></h4></div>"""),
                    Div(Field('subject_1'), css_class='col-xs-12 col-sm-4 col-lg-4'),

                    Div(Field('subject_2'), css_class='col-xs-12 col-sm-4 col-lg-4'),

                    Div(Field('subject_3'), css_class='col-xs-12 col-sm-4 col-lg-4'),

                    HTML("""<div class="col-xs-12 col-md-12 col-lg-12"><h4><label>Level</label></h4></div>"""),
                    # Div(InlineRadios('level_grp'), css_class='col-xs-12 col-md-12 col-lg-12'),
                    Div(InlineRadios('level'), css_class='col-xs-12 col-md-12 col-lg-12'),

                    ButtonHolder(
                        HTML('<a class="btn btn-default col-xs-12 col-sm-4 col-sm-offset-4 extra-top-15" href="{% url "TeacherList" %}">Reset</a>'),
                    ),
                    ),

                Tab('Region',

                    # Div(InlineCheckboxes('region'), css_class='col-xs-12 col-md-12 col-lg-12'),

                    HTML("""<div class="col-xs-12 col-md-12"><h4><label>Region Availabilty</label></h4></div>"""),

                    Div(InlineCheckboxes('region_1'), css_class='col-xs-12 col-sm-6'),

                    Div(InlineCheckboxes('region_2'), css_class='col-xs-12 col-sm-6'),

                    Div(InlineCheckboxes('region_3'), css_class='col-xs-12 col-sm-6'),

                    Div(InlineCheckboxes('region_4'), css_class='col-xs-12 col-sm-6'),

                    ButtonHolder(
                        HTML('<a class="btn btn-default col-xs-12 col-sm-4 col-sm-offset-4 extra-top-15" href="{% url "TeacherList" %}">Reset</a>'),
                    ),
                    ),

                Tab('Other Details',

                    HTML("""<div class="col-xs-12 col-sm-12"><h4><label>Other Details</label></h4></div>"""),
                    Div(Field('minimum_years'), css_class='col-xs-12 col-sm-4'),
                    Div(Field('maximum_pay'), css_class='col-xs-12 col-sm-4'),

                    # HTML("""<div class="col-xs-12 col-sm-12"><h4><label>Group Tuition</label></h4></div>"""),
                    Div(InlineRadios('group_tuition'), css_class='col-xs-12 col-sm-offset-1 col-sm-2 col-sm-offset-1'),

                    HTML("""<div class="col-xs-12 col-sm-12"><h4><label>Education and Expertise</label></h4></div>"""),
                    # HTML("""<div class="col-xs-12 col-sm-12"><span><p><b>Tutors education</b></p></span></div>"""),
                    Div(InlineCheckboxes('educational_level'), css_class='col-xs-12 col-sm-6'),

                    # HTML("""<div class="col-xs-12 col-sm-12"><span><p><b>Tutors current role</b></p></span></div>"""),
                    Div(InlineCheckboxes('expertise_type'), css_class='col-xs-12 col-sm-6'),

                    # HTML("""<div class="col-xs-12 col-sm-12"><h4><label>Group Tuition</label></h4></div>"""),
                    # Div(Field('group_tuition'), css_class='col-xs-12 col-sm-6'),



                    ButtonHolder(
                        HTML('<a class="btn btn-default col-xs-12 col-sm-4 col-sm-offset-4 extra-top-15" href="{% url "TeacherList" %}">Reset</a>'),
                    ),
                    ),


                Tab('Keyword',
                    
                    Div(Field('search'), css_class='col-xs-12 col-sm-offset-3 col-sm-6 col-sm-offset-3'),
                    ButtonHolder(
                        Submit('submit', 'Search', css_class='col-xs-12 col-sm-offset-4 col-sm-4 col-sm-offset-4'),
                        HTML("""<div class="col-xs-12"><br></div>"""),
                        HTML('<a class="btn btn-default col-xs-12 col-sm-offset-4 col-sm-4 col-sm-offset-4" href="{% url "TeacherList" %}">Reset</a>'),
                    ),
                    ),

            ),

            # ButtonHolder(
            #     Submit('submit', 'Refresh', css_class='col-xs-4 col-xs-offset-1'),
            #     HTML('<a class="btn btn-default col-xs-4 col-xs-offset-1" href="{% url "TeacherList" %}">Reset</a>'),
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


    # level_grp = (
    #     ('Lower Primary', 'Lower Primary'),
    #     ('Higher Primary', 'Higher Primary'),
    #     ('Lower Secondary', 'Lower Secondary'),
    #     ('Higher Secondary', 'Higher Secondary'),
    #     ('Junior College', 'Junior College'),
    #     ('University', 'University')
    #   )
  
    # level_grp = forms.ChoiceField(
    #     label='',
    #     choices=level_grp)

    level = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        queryset=Level_Expertise.objects.all(),
        label=""
    )

    educational_level = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        queryset=Educational_Level.objects.all(),
        label="Tutor's Education"
    )

    expertise_type = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        queryset=Expertise_Type.objects.all(),
        label="Tutor's Current Role"
    )

    region_1 = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        queryset=Region.objects.filter(description='Central'),
        label="Central Locations"
    )

    region_2 = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        queryset=Region.objects.filter(description='North'),
        label="North Locations"
    )

    region_3 = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        queryset=Region.objects.filter(description='East'),
        label="East Locations"
    )

    region_4 = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        queryset=Region.objects.filter(description='West'),
        label="West Locations"
    )



    minimum_years = forms.ChoiceField(
        required=False,
        initial=0,
        choices=exp_choices,
        label="Minimum Years of Experience"
    )

    # minimum_years = forms.IntegerField(
    #     required=False,
    #     initial=0,
    #     min_value=0,
    #     max_value=20,
    #     label="Minimum Years of Experience"
    # )


    maximum_pay = forms.ChoiceField(
        required=False,
        choices=pay_choices,
        label="Maximum Rate/Hour"
    )

    # maximum_pay = forms.IntegerField(
    #     required=False,
    #     initial=120,
    #     min_value=10,
    #     max_value=300,
    #     label="Maxmium Salary per hour"
    # )

    gt_choices = (
        ('Yes',  'Yes'),
        ('No',  'No')
    )

    group_tuition = forms.ChoiceField(
        required=False,
        choices=gt_choices,
        label="Group Tuition"
    )

    # group_tuition = forms.BooleanField(
    #     required=False,
    #     label="Group Tuition"
    # )

    search = forms.CharField(
        label='Keyword Search',
        max_length=30,
        required=False
    )
