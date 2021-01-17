from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from shop.models import Product
from .forms import CartAddForm
from django.views.decorators.http import require_POST
from shop.models import Bookmark
from django.contrib.auth.models import AbstractBaseUser

def detail(request):
	cart = Cart(request)
	return render(request, 'cart/detail.html', {'cart':cart})

@require_POST
def cart_add(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	form = CartAddForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		cart.add(product=product, quantity=cd['quantity'])
	return redirect('cart:detail')

def cart_remove(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	cart.remove(product)
	return redirect('cart:detail')


def bookmark_add(request , product_id):

	product_find = get_object_or_404(Product, id=product_id)
	bookmark_find = Bookmark.objects.filter(product = product_find , user = request.user)
	bookmarks = {
		'bookmarks': Bookmark.objects.filter(user=request.user),
	}
	print(bookmark_find)
	if bookmark_find.exists():
		print('none')
		return render(request, 'cart/bookmark.html', bookmarks)

	else:

		new_object=Bookmark.objects.create(product = product_find , user = request.user)


	return  render(request,'cart/bookmark.html',bookmarks)


def bookmark_remove(request, product_id):

	product_find = get_object_or_404(Product, id=product_id)
	bookmark_find = Bookmark.objects.filter(product = product_find , user = request.user)
	print(bookmark_find)
	if bookmark_find.exists():
		print('aaall')

	else:
		bookmark_find = Bookmark.objects.filter(product=product_find, user=request.user).delete()
		bookmark_find.save()
		print('not found')
	bookmarks = {
		'bookmarks': Bookmark.objects.filter(user=request.user),
	}
	return  render(request,'cart/bookmark.html',bookmarks)

def search_view(request,your_search_query):
	print('ccvv')
	resualt=Product.objects.filter(Q(name__icontains=your_search_query))
	print(resualt)
	return render(request, 'cart/search.html',{'resaults':resualt})