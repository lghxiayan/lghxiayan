from django import forms


class PubBlogForm(forms.Form):
    title = forms.CharField(max_length=200)
    content = forms.CharField(max_length=200)
    category = forms.IntegerField()
