"""Global context processor — tüm template'lerde erişilebilir site verileri"""
from .models import SiteSettings, SocialMedia, ContactInfo


def global_context(request):
    settings = SiteSettings.get_settings()
    contact = ContactInfo.get_contact()
    return {
        'site_settings': settings,
        'social_links': SocialMedia.objects.filter(is_active=True),
        'contact_info': contact,
        'whatsapp_number': settings.whatsapp_number or contact.whatsapp,
        'whatsapp_message': settings.whatsapp_default_message,
    }
