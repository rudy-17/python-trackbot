from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ContactForm
from django.core.mail import send_mail

def learn_more(request):
    return render(request, 'buyers/learn_more.html', {})

def search_tool_page(request):
    return render(request, 'buyers/search_tool.html', {})

def contact_page(request):
    form = ContactForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            country = form.cleaned_data['country']
            message = form.cleaned_data['message']
            # send_mail(
            #     subject,
            #     message,
            #     'wjeff.fortin@yahoo.com',
            #     ['info@beezytrack.com'],
            #     fail_silently=False,
            #     auth_user='wjeff.fortin@yahoo.com',
            #     auth_password='Beezytrack'
            # )
            return render(request, 'buyers/contact.html', {'form': form, 'status': True})
    return render(request, 'buyers/contact.html', {'form': form})
