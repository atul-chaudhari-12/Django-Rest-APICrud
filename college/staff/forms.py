from django import forms


class PrincipleSignUpForm(forms.Form):
    
    first_name = forms.CharField(max_length=50)