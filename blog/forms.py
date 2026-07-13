from django import forms
from .models import Post
from .models import Comment



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'tags', 'text', 'image','thumbnail_img')

def clean_title(self):
    title = self.cleaned_data['title']

    if Post.objects.filter(title__iexact=title).exists():
        raise forms.ValidationError("A post with this title already exists.")
    
    return title

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']