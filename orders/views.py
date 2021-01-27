from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, Coupon
from cart.cart import Cart
from suds.client import Client
from django.http import HttpResponse
from django.contrib import messages
from .forms import CouponForm
from django.views.decorators.http import require_POST
from django.utils import timezone


@login_required
def detail(request, order_id):
	order = get_object_or_404(Order, id=order_id)
	form = CouponForm()
	return render(request, 'orders/order.html', {'order':order, 'form':form})

@login_required
def order_create(request):
	cart = Cart(request)
	order = Order.objects.create(user=request.user)
	for item in cart:
		OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
		cart.clear()
	return redirect('orders:detail', order.id)


# ZARINPAL_MERCHANT = 'test'
# ZARINPAL_PAYMENT_BASE_URL = 'https://wwww.sandbox.zarinpal.com'
MERCHANT = 'd5d4c08c-c912-11e9-821b-000c295eb8fc'
client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
# client = Client(ZARINPAL_PAYMENT_BASE_URL)
description = "پرداخت "
mobile = '09022002276'
CallbackURL = 'http://localhost:8000/orders/verify/'

@login_required
def payment(request,order_id, price):
	global amount, o_id
	amount = price
	o_id = order_id
	result = client.service.PaymentRequest(MERCHANT, amount, description, request.user.email, mobile, CallbackURL)
	if result.Status == 100:
		return redirect('https://sandbox.zarinpal.com/pg/StartPay/' + str(result.Authority))
	else:
		return HttpResponse('Error code: ' + str(result.Status))

@login_required
def verify(request):
	if request.GET.get('Status') == 'OK':
		result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
		if result.Status == 100:
			order = Order.objects.get(id=o_id)
			order.paid = True
			order.save()
			messages.success(request, 'Transaction was successful', 'success')
			return redirect('shop:home')
		elif result.Status == 101:
			return HttpResponse('Transaction submitted')
		else:
			return HttpResponse('Transaction failed.')
	else:
		return HttpResponse('Transaction failed or canceled by user')

@require_POST
def coupon_apply(request, order_id):
	now = timezone.now()
	form = CouponForm(request.POST)
	if form.is_valid():
		code = form.cleaned_data['code']
		try:
			coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
			
			order = Order.objects.get(id=order_id)
			order.discount = coupon.discount
			order.save()
			return redirect('orders:detail', order_id)
		except Coupon.DoesNotExist:
			messages.error(request, 'This coupon does not exist', 'danger')
			return redirect('orders:detail', order_id)

	








