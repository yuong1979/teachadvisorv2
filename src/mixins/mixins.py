from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from teacher.models import Teacher
from student.models import Student
from opening.models import Opening
from orders.models import Order
from messaging.models import Message
from tags.models import BlockUser
from billing.models import UserCredit, CreditToCash, Transaction
from django.contrib import messages

# from sellers.mixins import SellerAccountMixin

# class ProductManagerMixin(object):
#     def get_object(self, *args, **kwargs):
#         obj = super(ProductManagerMixin, self).get_object(*args, **kwargs)
#         user = self.request.user
#         if obj.user == user:
#             return obj
#         else:
#             raise Http404

class LoginRequiredMixin(object):
	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class UserChangeManagerMixin(object):
		def get_object(self, *args, **kwargs):
				obj = super(UserChangeManagerMixin, self).get_object(*args, **kwargs)
				user = self.request.user
				if obj.user == user:
						return obj
				else:
						raise Http404


class GetDetailsMixin(object):

		def get_msg(self, *args, **kwargs):
				msg_id = self.request.session.get("msg_id")
				msg = get_object_or_404(Message, pk=msg_id)
				# parent_msg_id = msg.parent_id
				# msg = get_object_or_404(Message, pk=parent_msg_id)
				return msg

		def get_opening(self, *args, **kwargs):
				msg = self.get_msg()
				opening = msg.re_opening
				return opening

		def get_student(self, *args, **kwargs):
				opening = self.get_opening()
				student = opening.hiring_student
				return student

		def get_teacher(self, *args, **kwargs):
				try:
						teacher = self.get_msg().senduser.teacher
				except:
						teacher = self.get_msg().touser.teacher
				return teacher

		def get_order(self, *args, **kwargs):
				order_id = self.request.session.get("order_id")
				order = Order.objects.get(pk=order_id)
				return order


class GetCheckoutMixin(object):

		def get_user_cred(self, *args, **kwargs):
			user = self.request.user
			usercred_obj = get_object_or_404(UserCredit, user=user)
			usercred = usercred_obj.credit
			return usercred

		def get_credit_cost(self, *args, **kwargs):
			credit_id = self.request.session.get("credit_id")
			credit_pack = get_object_or_404(CreditToCash, id=credit_id)
			creditcost = credit_pack.cashprice
			return creditcost

		def get_credit(self, *args, **kwargs):
			credit_id = self.request.session.get("credit_id")
			credit_pack = get_object_or_404(CreditToCash, id=credit_id)
			credit = credit_pack.credits
			return credit

		def get_transaction(self, *args, **kwargs):
				transaction_id = self.request.session.get("transaction_id")
				transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
				return transaction


# def CheckBlk(request, user1, user2):
#   #exit if someone has been blocked if blocked to redirect

#   try:
#     try:
#       test = BlockUser.objects.get(blocker = user1).blocked.filter(blocked_u__blocked=user2)
#       messages.warning(request, "This user is no longer accessible")
#       return redirect("MessageListViewAll")
#     except:
#       test = BlockUser.objects.get(blocker = user2).blocked.filter(blocked_u__blocked=user1)
#       messages.warning(request, "This user is no longer accessible")
#       return redirect("MessageListViewAll")
#   except:
#     pass



def CheckBlk(request, user1, user2):
    """Return redirect if user Blocked by user or reverse."""
    if check_any_block(user1, user2):
        messages.warning(request, "This user is no longer accessible")
        return redirect("MessageListViewAll")


def check_any_block(user1, user2):
    """Check any block relations."""
    return blocked(user1, user2) or blocked(user2, user1)


def blocked(user, by_user):
    """Return True if user blocked by_user."""
    try:
        BlockUser.objects.get(blocker=by_user,
                              blocked__in=[user])
        return True
    except BlockUser.DoesNotExist:
        pass
    return False


