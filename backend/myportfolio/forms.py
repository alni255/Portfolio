from django import forms
from django.core.validators import MinLengthValidator
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom complet',
                'minlength': '2'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'votre@email.com'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sujet de votre message',
                'minlength': '5'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Votre message...',
                'rows': '5',
                'minlength': '10'
            }),
        }
        labels = {
            'name': 'Nom complet',
            'email': 'Adresse email',
            'subject': 'Sujet',
            'message': 'Message',
        }
        error_messages = {
            'name': {
                'required': 'Le nom est obligatoire.',
                'min_length': 'Le nom doit contenir au moins 2 caractères.'
            },
            'email': {
                'required': 'L\'email est obligatoire.',
                'invalid': 'Veuillez entrer une adresse email valide.'
            },
            'subject': {
                'required': 'Le sujet est obligatoire.',
                'min_length': 'Le sujet doit contenir au moins 5 caractères.'
            },
            'message': {
                'required': 'Le message est obligatoire.',
                'min_length': 'Le message doit contenir au moins 10 caractères.'
            },
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Le nom doit contenir au moins 2 caractères.")
        return name

    def clean_subject(self):
        subject = self.cleaned_data.get('subject', '').strip()
        if len(subject) < 5:
            raise forms.ValidationError("Le sujet doit contenir au moins 5 caractères.")
        return subject

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < 10:
            raise forms.ValidationError("Le message doit contenir au moins 10 caractères.")
        return message