from django import forms
from .models import ContactMessage, Newsletter


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Adınız Soyadınız',
                'id': 'contact-name', 'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input', 'placeholder': 'E-posta Adresiniz',
                'id': 'contact-email', 'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Telefon Numaranız',
                'id': 'contact-phone',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Konu',
                'id': 'contact-subject', 'required': True,
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-input form-textarea', 'placeholder': 'Mesajınız',
                'id': 'contact-message', 'rows': 5, 'required': True,
            }),
        }


class NewsletterForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'newsletter-input',
            'placeholder': 'E-posta adresinizi girin',
            'id': 'newsletter-email',
            'required': True,
        })
    )
