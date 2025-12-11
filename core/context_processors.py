from django.conf import settings

def whatsapp_phone(request):
    return {'whatsapp_phone': settings.WHATSAPP_PHONE}
