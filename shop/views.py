from django.shortcuts import render, get_object_or_404
from .models import Category, Product,Comment
from cart.forms import CartAddForm
from .forms import  AddCommentForm, AddReplyForm,CommentForm
from django.contrib import messages
from django.views.decorators.http import require_POST


def home(request, slug=None):

	products = Product.objects.filter(available=True)
	categories = Category.objects.filter(is_sub=False)
	if slug:
		category = get_object_or_404(Category, slug=slug)
		products = products.filter(category=category)
	return render(request,'shop/home.html', {'products':products, 'categories':categories})


def product_detail(request, slug):
	product = get_object_or_404(Product, slug=slug)
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

def favorite_products(request,slug):
  product=get_object_or_404(Product, slug=slug)
  if product.favorite.filter(slug=slug).exist():
    product.favorite.remove(request.user)
  else:
    product.favorite.add(request.user)
    return render(request, 'shop/favorite.html',{'product': product})

