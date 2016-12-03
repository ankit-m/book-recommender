from django import forms

class IdeaForm(forms.Form):
    idea = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 10}))
