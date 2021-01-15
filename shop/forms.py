from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class AddCommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('body',)
		widgets = {
			'body': forms.Textarea(attrs={'class':'form-control'})
		}
		error_messages = {
			'body':{
				'required': 'این فیلد اجباری است',
			}
		}
		help_texts = {
			'body':'max 400 char'
		}

class AddReplyForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('body',)
