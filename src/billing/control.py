

#number of cash to credits is altered in 
# http://127.0.0.1:8000/admin/billing/credittocash/
# 700 - $50
# 250 - $20
# 100 - $10

#number of credit deducted per message - original - 50
msgcredit = 0
#number of credits to start off with - original - 500
creditstart = 0
#number of credits to add teacher/student places an order - original - 1
orderadd = 0
#number of credits to add to student when they do a review
reviewadd = 0

feat_days_choices = (
	('0',  '1 days for 0 credits (Trial)'),# original - 3 day for 40
	('80',  '7 days for 80 credits'),
	('160',  '14 days for 160 credits')
)
feat_days_choices_dict = {
'0':1,# original - 3 day for 40
'80':7, 
'160':14
}


img_days_choices = (
	('0',  '30 days for 0 credits'),# original - 100
	('0',  '90 days for 0 credits'),# original - 300
	('500',  '365 days for 500 credits')
)
img_days_choices_dict = {
'0':30,# original - 100
'0':90,# original - 300
'500':365
}


ana_days_choices = (
	('0',  '30 days for 0 credits'),# original - 40
	('0',  '90 days for 0 credits'),# original - 120
	('200',  '365 days for 200 credits')
)
ana_days_choices_dict = {
'0':30,# original - 40
'0':90,# original - 120
'200':365
}


studentbi_days_choices = (
	('100',  '30 days for 100 credits'),
	('300',  '90 days for 300 credits'),
	('500',  '365 days for 500 credits')
)
studentbi_days_dict = {
'100':30,
'300':90, 
'500':365
}