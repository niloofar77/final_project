from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body','rate')

class AddCommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('body','rate')
		widgets = {
			'body': forms.Textarea(attrs={'class':'form-control'}),
			'rate':forms.TextInput(attrs={'min':1,'max': '5','type': 'number'})

		}
		error_messages = {
			'body':{
				'required': 'این فیلد اجباری است',
			}
		}
		help_texts = {
			'body':'حداکثر ۴۰۰ کلمه'
		}

class AddReplyForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('body',)
