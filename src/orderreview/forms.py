from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField, Field, Reset
from crispy_forms.bootstrap import TabHolder, Tab, InlineCheckboxes, AppendedText, InlineRadios
from orderreview.models import ReviewTeacher


class OrderCompleteReviewForm(forms.ModelForm):

	class Meta:
		model = ReviewTeacher
		fields = [
			"score",
			"gradebefore",
			"gradeafter",
			"review",
			# "anonymous"

		]

	def __init__(self, *args, **kwargs):
		super(OrderCompleteReviewForm, self).__init__(*args, **kwargs)
		self.fields['score'].label = "Please Rate your Tutor"
		self.fields['score'].help_text = "Please rate with 5 being the best and 1 being the worst experience"
		self.fields['review'].label = "Feedback"
		# self.fields['anonymous'].help_text = "Please tick if you are want to remain anonymous"
		self.helper = FormHelper(self)
		# self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', value='Submit Review', css_class='buttonspace btn-success'))
		self.helper.layout = Layout(
					# Div(InlineRadios('score'), css_class='col-xs-12 col-md-12 col-lg-12'),
					Div(InlineRadios('gradebefore'), css_class='col-xs-12 col-md-12 col-lg-12'),
					Div(InlineRadios('gradeafter'), css_class='col-xs-12 col-md-12 col-lg-12')
		)

	int_choices = [tuple([x, x]) for x in range(1, 6)]


	grade_choices = (
		('100-95', '100-95'),
		('94-90', '94-90'),
		('89-85', '89-85'),
		('84-80', '84-80'),
		('79-75', '79-75'),
		('74-70', '74-70'),
		('69-65', '69-65'),
		('64-60', '64-60'),
		('59-55', '59-55'),
		('54-50', '54-50'),
		('49-45', '49-45'),
		('45-40', '45-40'),
		('0-39', '0-39'),
	)

	score = forms.ChoiceField(
		# widget=forms.RadioSelect,
		widget=forms.Select,

		choices=int_choices
	)


	gradebefore = forms.ChoiceField(
		widget=forms.RadioSelect,
		choices=grade_choices,
		label="Student grades before tutor engagement",
		required=False
	)

	gradeafter = forms.ChoiceField(
		widget=forms.RadioSelect,
		choices=grade_choices,
		label="Student grades after tutor engagement",
		required=False
	)

class OrderCancelReviewForm(forms.ModelForm):

	class Meta:
		model = ReviewTeacher
		fields = [
			"reason",
			"comments",
		]

	def __init__(self, *args, **kwargs):
		super(OrderCancelReviewForm, self).__init__(*args, **kwargs)
		self.fields['reason'].label = "Reason for cancellation"
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', value='Submit cancellation', css_class='buttonspace btn-success'))
		self.helper.layout = Layout(
					Div(('reason'), css_class='col-xs-12 col-md-12 col-lg-12')
		)

	reasons = (
		('No response', 'No response from the applicant'),
		('Unable to perform task', 'Applicant is unable to perform task'),
		('Unable to provide documention', 'Applicant is unable to provide valid documention'),
		('Job Canceled', 'Job has been canceled'),
		('Others', 'Other reasons')
	)

	reason = forms.ChoiceField(
		widget=forms.RadioSelect,
		choices=reasons
	)




class ReviewFormComment(forms.ModelForm):

	class Meta:
		model = ReviewTeacher
		fields = [
			"reviewcomment",
		]

	def __init__(self, *args, **kwargs):
		super(ReviewFormComment, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.fields['reviewcomment'].label = "Comment on your review"
		self.helper.add_input(Submit('submit', value='Submit Comment', css_class='buttonspace btn-success'))
		self.helper.layout = Layout(
					Div(('reviewcomment'), css_class='col-xs-12 col-md-12 col-lg-12')
		)

	# reasons = (
	# 	('No response', 'No response from the applicant'),
	# 	('Unable to perform task', 'Applicant is unable to perform task'),
	# 	('Unable to provide documention', 'Applicant is unable to provide valid documention'),
	# 	('Job Canceled', 'Job has been canceled'),
	# 	('Others', 'Other reasons')
	# )

	# reason = forms.ChoiceField(
	# 	widget=forms.RadioSelect,
	# 	choices=reasons
	# )


