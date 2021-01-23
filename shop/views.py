from django.shortcuts import render, get_object_or_404, redirect
from persian import persian

from accounts.models import Profile
from .models import Category, Product,Comment
from cart.forms import CartAddForm
from .forms import  AddCommentForm, AddReplyForm,CommentForm
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.views.generic import ListView


def home(request, slug=None):

	products = Product.objects.filter(available=True)
	categories = Category.objects.filter(is_sub=False)
	if slug:
		category = get_object_or_404(Category, slug=slug)
		products = products.filter(category=category)
	return render(request,'shop/home.html', {'products':products, 'categories':categories})


def product_detail(request, slug):
	product = get_object_or_404(Product, slug=slug)
	# profile = Profile.objects.get(user = product.)
	comments = Comment.objects.filter(product=product)
	form = CartAddForm()
	if request.method == 'POST':
		comment_form = AddCommentForm(request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.product = product
			new_comment.user = request.user
			# print('dddv' + new_comment.user.full_name)
			new_comment.save()
			comment_form = AddCommentForm()
			messages.success(request, 'you comment submitted successfully')

	else:
		comment_form = AddCommentForm()

	return render(request, 'shop/product_details.html',{'product': product, 'form': form, 'comments': comments, 'comment_form': comment_form})
def searchcategory(request):
	search_post = request.GET.get('category')
	resaults = Product.category.objects.filter(Q(category=search_post))
	print(resaults)

	return  render(request , 'cart/search.html' ,  {'resaults': resaults})
