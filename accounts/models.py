from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import MyUserManager


class User(AbstractBaseUser):
	email = models.EmailField(max_length=100, unique=True)
	full_name = models.CharField(max_length=100)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	objects = MyUserManager()
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['full_name']

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.is_admin



	# def save_profile(sender, **kwargs):
	# 	if kwargs['created']:
	# 		p1 = Profile(user=kwargs['instance'])
	# 		p1.save()
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(null=True, blank=True)
	age = models.PositiveSmallIntegerField(null=True, blank=True)
	phone = models.CharField(null=True, blank=True,max_length=100)
