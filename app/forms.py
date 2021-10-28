from django import forms


class PostForm(forms.Form):
    title = forms.CharField(max_length=200, label='タイトル')
    content = forms.CharField(widget=forms.Textarea(), label='本文')
