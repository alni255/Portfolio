from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
import json
from .forms import ContactForm
from .models import ContactMessage


def index(request):
    return render(request, 'myportfolio/index.html')

def about(request):
    return render(request, 'myportfolio/about.html')

def get_client_ip(request):
    """Récupère l'adresse IP du client"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@csrf_exempt
@require_POST
def contact_view(request):
    try:
        # récupérer les données du formulaire
        form = ContactForm(request.POST)

        # infos supplémentaires
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        if form.is_valid():
            contact_message = form.save(commit=False)
            contact_message.ip_address = ip_address
            contact_message.user_agent = user_agent
            contact_message.save()

            # contenu de l’email
            subject = f"Portfolio - {contact_message.name}: {contact_message.subject}"
            message = f"""
            Nouveau message reçu depuis votre portfolio :

            Nom: {contact_message.name}
            Email: {contact_message.email}
            Sujet: {contact_message.subject}
            Date: {contact_message.created_at.strftime('%d/%m/%Y à %H:%M')}
            IP: {ip_address}

            Message:
            {contact_message.message}

            ---
            ID: {contact_message.id}
            Ce message a été envoyé automatiquement depuis votre portfolio.
            """

            try:
                # envoi du mail principal
                send_mail(
                    subject=subject,
                    message=message.strip(),
                    from_email=None,  # DEFAULT_FROM_EMAIL dans settings
                    recipient_list=['aplatform660@gmail.com'],
                    fail_silently=False,
                )

                # mail de confirmation
                confirmation_subject = "Confirmation de réception - El-anis Mohamed Youssouf"
                confirmation_message = f"""
                Bonjour {contact_message.name},

                J'ai bien reçu votre message et je vous remercie de m'avoir contacté.

                Votre message :
                "{contact_message.message[:100]}{'...' if len(contact_message.message) > 100 else ''}"

                Je vous répondrai dans les plus brefs délais.

                Cordialement,
                El-anis Mohamed Youssouf

                ---
                Ceci est un message automatique de confirmation.
                ID: {contact_message.id}
                """

                send_mail(
                    subject=confirmation_subject,
                    message=confirmation_message.strip(),
                    from_email=None,
                    recipient_list=[contact_message.email],
                    fail_silently=True,
                )

                return JsonResponse({
                    'success': True,
                    'message': 'Votre message a été envoyé avec succès ! Je vous répondrai très rapidement.'
                })

            except Exception as e:
                contact_message.admin_notes = f"Erreur envoi email: {str(e)}"
                contact_message.save()
                return JsonResponse({
                    'success': False,
                    'message': "Votre message a été enregistré mais une erreur est survenue lors de l'envoi. Je vous contacterai directement."
                })

        else:
            return JsonResponse({
                'success': False,
                'message': 'Veuillez corriger les erreurs dans le formulaire.',
                'errors': form.errors
            })

    except Exception as e:
        print("Erreur serveur dans contact_view:", e)
        return JsonResponse({
            'success': False,
            'message': 'Une erreur serveur est survenue. Veuillez réessayer plus tard.'
        })
    

# views.py - AJOUTEZ CETTE VUE
def test_email_config(request):
    try:
        send_mail(
            'Test configuration email',
            'Si vous recevez ceci, la configuration email fonctionne!',
            None,
            ['aplatform660@gmail.com'],
            fail_silently=False,
        )
        return JsonResponse({'success': True, 'message': 'Email de test envoyé!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erreur: {str(e)}'})
    


def learnhub_demo(request):
    return render(request, 'myportfolio/learnhub_demo.html')

def bookclass_demo(request):
    return render(request, 'myportfolio/bookclass_demo.html')




