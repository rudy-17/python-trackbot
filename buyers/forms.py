from django import forms
from django.core.exceptions import ValidationError


class ContactForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your name"
            }
        ),
        label=("Your Name:")
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email"
            }
        ), label=("Email:")
    )
    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Subject"
            }
        ), label=("Subject:")
    )
    CHOICES = (('India', 'India'), ('America', 'America'), ('Japan', 'Japan'))
    country = forms.ChoiceField(
        choices = CHOICES,
        widget=forms.Select(attrs={'class':'form-control'})
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Message",
                "rows": "6",
            }
        ), label=("Message:")
    )

    def clean_email(self):
        e = self.cleaned_data['email']
        if not e:
            raise ValidationError("Email is required")
        return e
