from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-input', 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email (will not be published)', 'class': 'form-input', 'required': True}),
            'body': forms.Textarea(attrs={'placeholder': 'Write your comment here...', 'class': 'form-textarea', 'rows': 4, 'required': True}),
        }
