from django import forms
from .models import Post, Comments, Contact


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs = {'class': 'form-control', 'placeholder': 'Gönderinizin başlığı'}
        self.fields['body'].widget.attrs = {'class': 'form-control', 'placeholder': 'Gönderinizin içeriği'}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment_text']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        self.fields['comment_text'].widget.attrs = {'class': 'form-control'}


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'topic', 'text']

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control', 'style': 'margin-bottom:30px;'}
