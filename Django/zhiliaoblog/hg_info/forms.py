from django import forms


class PubInfoForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(max_length=200)
    category = forms.IntegerField()
