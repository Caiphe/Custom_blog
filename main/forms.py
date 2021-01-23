from django import forms
from tinymce import TinyMCE
from .models import Post, Comment


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, "cols": 30, 'rows': 10}
        )
    )
    
    class Meta:
        model = Post
        fields = [
            'title','overview','content',
            'category',
            'featured','thumbnail','previous_post','next_post'
        ]


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder' : " Type Your comment",
        'id': "userComment",
        'row' : 2
    }))
    class Meta:
        model = Comment
        fields = ('content', )
