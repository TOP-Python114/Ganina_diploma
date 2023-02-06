from django import forms


class UserForm(forms.Form):
    text = forms.CharField(label="Текст резюме:", widget=forms.Textarea)
