from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from shop.models import Product, Category
from .forms import CartAddForm
from django.views.decorators.http import require_POST
from shop.models import Bookmark
from django.contrib.auth.models import AbstractBaseUser

def detail(request):
	cart = Cart(request)
	return render(request, 'cart/cart2.html', {'cart':cart})

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
	bookmark_find = Bookmark.objects.get(product = product_find , user = request.user)
	bookmark_find.active =True
	bookmark_find.save()
	bookmarks = {
		'bookmarks': Bookmark.objects.filter(user=request.user, active =True),
	}
	print(bookmark_find)

	return  render(request,'cart/wishlist2.html',bookmarks)


def bookmark_remove(request, product_id):

	print('bookmark remove')
	product_find = get_object_or_404(Product, id=product_id)
	bookmark_find = Bookmark.objects.get(product = product_find , user = request.user)
	bookmark_find.active = False
	bookmark_find.save()

	print(bookmark_find)

	bookmarks = {
		'bookmarks': Bookmark.objects.filter(user=request.user, active =True),
	}
	return  render(request,'cart/wishlist2.html',bookmarks)

# def search_view(request,your_search_query):
# 	print('ccvv')
# 	resualt=Product.objects.filter(Q(name__icontains=your_search_query))
# 	print(resualt)
# 	return render(request, 'cart/search.html',{'resaults':resualt})
def search(request):
	search_post = request.GET.get('search')
	resaults= Product.objects.filter(Q(name=search_post))
	return render(request, 'cart/search.html', {'resaults': resaults})




def about(request):
  return render(request,'cart/about.html')

def searchcategory(request,category_id):
	# search_post = request.GET.get('category')
	category = Category.objects.get(id = category_id)
	resaults = Product.objects.filter(Q(category =category))
	print(resaults)
	return  render(request , 'cart/search.html' ,  {'resaults': resaults})

def searchbrand(request , brand):
	resaults = Product.objects.filter(Q(brand = brand))
	return  render(request , 'cart/search.html' ,  {'resaults': resaults})
