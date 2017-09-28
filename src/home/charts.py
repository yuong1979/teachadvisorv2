from django.shortcuts import render, render_to_response
from django.http import JsonResponse
from django.views.generic import TemplateView, View, FormView
from tags.models import ViewTeacherRecord, SearchWordTeacherRecord
from orders.models import Order

from home.forms import OrderChartForm
from django.contrib.auth.models import User
from datetime import date
import datetime
import json
import pandas as pd
from django.db.models import Q
import numpy as np



def json_serial(obj):
	"""JSON serializer for objects not serializable by default json code"""
	if isinstance(obj, date):
		serial = obj.isoformat()
		return serial
	raise TypeError ("Type not serializable")




class TeacherChart(View):

	def get(self, request):
		template = 'tcharts.html'

		enddate = datetime.datetime.now()
		tdelta = datetime.timedelta(days=30)
		startdate = enddate - tdelta
		startdate = startdate.date()

		#filtering all the search keywords for the start and enddate
		swdf = SearchWordTeacherRecord.objects.filter(date__range=[startdate, enddate])

		try:
			swdf = swdf.values_list('id','word','user','subject','date', flat=False)
			#inserting the collected data into a dateframe for manipulation
			swdf = pd.DataFrame(list(swdf))
			#giving the dataframe column names
			swdf.columns = ['id','word','user','subject','date']
			#do a groupby
			swdf = swdf.groupby(['word'], as_index=False)['user'].count()
			#selecting the required columns
			swdf = swdf[['word','user']]
			#sorting the values
			swdf.sort_values('user', ascending=True, inplace=True)
			#changing column names from user to users
			swdf.rename(columns={'user':'users'}, inplace=True)
			#only taking in the top 20 searches
			swdf = swdf.head(20)
			#adding the header to a list format
			swdfcolumn = [swdf.columns.values.tolist()]
			#adding the values to a list format
			swdf = swdf.values.tolist()
			#adding both together
			swdf = swdfcolumn + swdf

		except:
			dnotexist = "Data does not exist yet"



		#filtering for the correct teacher
		df = ViewTeacherRecord.objects.filter(teacher=self.request.user.teacher)



		try:

			df = df.values_list('id','teacher_id','uniquecount','nonuniquecount','msgtocount','msgfromcount','ordercount','date','updated','timestamp', flat=False)
			#inserting the collected data into a dateframe for manipulation
			df = pd.DataFrame(list(df))
			#giving the dataframe column names
			df.columns = ['id','teacher_id','uniquecount','nonuniquecount','msgtocount','msgfromcount','ordercount','date','updated','timestamp']
			df = df[['id','teacher_id','uniquecount','nonuniquecount','msgtocount','msgfromcount','ordercount','date']]
			#rename required columns
			df.rename(columns={'uniquecount':'Unique Views','nonuniquecount':'Views','msgtocount':'ToMessages', 'msgfromcount':'FromMessages','ordercount':'Orders'}, inplace=True)
			# exporting df out to a csv
			# df.to_csv('test.csv', header=True)
			# importing the df back from a csv
			# df = pd.read_csv('test.csv', index_col=0)

			#changing all zeros to NA
			for key in df.keys():
				df[key] = df[key].replace(0, np.NaN)

			#insert dates
			numdays = 30
			base = datetime.datetime.today().date()
			date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays)]
			dates = pd.DataFrame(date_list)
			dates.columns = ['date']


			df.date = pd.to_datetime(df.date)
			dates.date = pd.to_datetime(dates.date)
			#merge the complete dates with the dateframe
			df = pd.merge(dates ,df , on=['date'] , how='left')
			#order by dates
			df = df.sort_values('date',ascending=True)
			#make dates json serializable
			# df['date'] = df.date.apply(json_serial)
			df['date'] = df['date'].dt.strftime("%y-%m-%d")



			#changing all NA to ascending figures
			for key in df.keys():
				df[key] = df[key].fillna(method='pad').fillna(0)


			# for key in df.keys():
			# 	df[key] = df[key].fillna(method='pad')

			# df['Orders'].replace(to_replace=0.0, method='ffill')

			# for key in df.keys():
			# 	df[key].replace(to_replace=0, method='ffill').values



			# #get the difference instead of cumalation
			# df[['Unique Views', 'Views', 'Messages', 'Orders']] = df[['Unique Views', 'Views', 'Messages', 'Orders']].diff()
			# #fill all the NAs
			# df[['Unique Views', 'Views', 'Messages', 'Orders']] = df[['Unique Views', 'Views', 'Messages', 'Orders']].fillna(value=0)


			# #for bar chart
			# #selecting the required columns
			# dfb = df[['date','Views','ToMessages','Orders']]
			# #adding the header to a list format
			# dfbcolumn = [dfb.columns.values.tolist()]
			# #adding the values to a list format
			# dfb = dfb.values.tolist()
			# #adding both together
			# dfb = dfbcolumn + dfb


			# #for line chart
			# #selecting the required columns
			# dfl = df[['date','Unique Views','Views']]
			# #adding the header to a list format
			# dflcolumn = [dfl.columns.values.tolist()]
			# #adding the values to a list format
			# dfl = dfl.values.tolist()
			# #adding both together
			# dfl = dflcolumn + dfl

			#views
			#selecting the required columns
			dfv = df[['date','Views']]
			#adding the header to a list format
			dfvcolumn = [dfv.columns.values.tolist()]
			#adding the values to a list format
			dfv = dfv.values.tolist()
			#adding both together
			dfv = dfvcolumn + dfv

			#unique views
			#selecting the required columns
			dfu = df[['date','Unique Views']]
			#adding the header to a list format
			dfucolumn = [dfu.columns.values.tolist()]
			#adding the values to a list format
			dfu = dfu.values.tolist()
			#adding both together
			dfu = dfucolumn + dfu

			#from messages
			#selecting the required columns
			dfm = df[['date','FromMessages']]
			#adding the header to a list format
			dfmcolumn = [dfm.columns.values.tolist()]
			#adding the values to a list format
			dfm = dfm.values.tolist()
			#adding both together
			dfm = dfmcolumn + dfm

			#to messages vs from messages vs orders
			#selecting the required columns
			dft = df[['date','Orders']]
			#adding the header to a list format
			dftcolumn = [dft.columns.values.tolist()]
			#adding the values to a list format
			dft = dft.values.tolist()
			#adding both together
			dft = dftcolumn + dft


			#for pie chart
			#selecting the required columns
			dfp = df[['FromMessages','ToMessages','Orders']]
			dfpcolumn = [dfp.columns.values.tolist()]
			dfp = dfp.sum(axis=0)
			#think about how to do the minus the orders from messages and messages from views
			dfp = pd.DataFrame(dfp)
			# dfp.rename(columns={0:'count'}, inplace=True)
			dfp.reset_index(inplace=True)
			dfp.rename(columns={'index':'type', 0:'count'}, inplace=True)
			dfp = [dfp.columns.tolist()] + dfp.values.tolist()


		except:
			unotexist = "User data does not exist yet"


		context = {}

		try:
			context["unotexist"] = unotexist

		except:
			# context["datab"] = json.dumps(dfb)
			# context["datal"] = json.dumps(dfl)
			# context["datap"] = json.dumps(dfp)

			context["datav"] = json.dumps(dfv)
			context["datau"] = json.dumps(dfu)
			context["datam"] = json.dumps(dfm)
			context["datat"] = json.dumps(dft)
			context["datap"] = json.dumps(dfp)


		try:
			context["dnotexist"] = dnotexist
		except:
			context["dataw"] = json.dumps(swdf)


		return render(request, template, context)




#This shit is still work in progress
class StudentChart(FormView):
	form_class = OrderChartForm
	template_name = 'scharts.html'


	# def get(self, request):
	# 	template = 'tcharts.html'
	# 	df = Order.objects.filter()

	# 	context = {
	# 		# 'datab': json.dumps(dfb),
	# 		# 'datal': json.dumps(dfl),
	# 		# 'datap': json.dumps(dfp)
	# 	}
	# 	return render(request, template, context)


	def get_context_data(self, **kwargs):
		context = super(StudentChart, self).get_context_data(**kwargs)

		enddate = datetime.datetime.now()
		tdelta = datetime.timedelta(days=5)
		startdate = enddate - tdelta
		startdate = startdate.date()
		
		qs = Order.objects.filter().distinct()

		subject_1 = self.request.GET.get("subject_1")
		subject_2 = self.request.GET.get("subject_2")
		subject_3 = self.request.GET.get("subject_3")
		level_type = self.request.GET.get("level")
		educational_level = self.request.GET.getlist("educational_level")
		expertise_type = self.request.GET.getlist("expertise_type")
		minimum_years = self.request.GET.get("minimum_years")
		group_tuition = self.request.GET.get("group_tuition")

		if subject_1:
			subject = subject_1
		elif subject_2:
			subject = subject_2
		else:
			subject = subject_3

		try:
			if subject and level_type:
				qs = qs.filter(
					Q(subject=subject, level=level_type)
				).distinct()
			# if educational_level:
			# 	qs = qs.filter(educational_level__in=educational_level)
			# if expertise_type:
			# 	qs = qs.filter(expertise_type__in=expertise_type)
			# if minimum_years and not minimum_years == '0':
			# 	qs = qs.filter(years_of_experience__gte=minimum_years)
			if group_tuition:
				qs = qs.filter(group_tuition=True)

			qs = qs.distinct()

			qs = qs.filter(date__range=[startdate, enddate], teacherorder=True, studentorder=True)



		except:
			pass


		return context


	def get_initial(self):
		if not self.request.GET.get('submit'):
			return self.initial.clear()
		else:
			self.initial.clear()
			for key in self.request.GET:
				try:
					if key == "submit":
						pass
					else:
						self.initial[key] = self.request.GET[key]
				except KeyError:
					pass
			return self.initial.copy()






# #reading csv
# df = pd.read_csv('ZILL-Z98105_MSP.csv')
# # print df.head(10)
# df.to_csv('newcsv2.csv')
# print df.head()

# #reading a csv to and using the first column(non existent) as the index
# df1 = pd.read_csv('newcsv2.csv', index_col=0)
# print df1.head()
# #changing the column name
# df1.columns = ['Date','98105_HPI']
# print df1.head() 

# #output no headers
# df1.to_csv('newcsv3.csv', header=False)
# df2 = pd.read_csv('newcsv3.csv', index_col=0)
# print df2.head()