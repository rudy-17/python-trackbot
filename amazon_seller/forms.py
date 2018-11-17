from django import forms

class AmazonLoginForm(forms.Form):
    email_widget = forms.TextInput(
        attrs={'type': 'email','placeholder':('E-mail address'), 'autofocus': 'autofocus', 'class': 'form-control'}
    )
    email = forms.EmailField(label=(""), widget=email_widget)

    password_widget = forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}
    )
    password = forms.CharField(label=(""), widget=password_widget)
