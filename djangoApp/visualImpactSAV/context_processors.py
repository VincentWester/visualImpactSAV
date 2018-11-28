from .models.session_models import SessionMailAndPhone

def session_mail_and_phone(request):
    return {'session_mail_and_phone': SessionMailAndPhone.load_all_mail_and_phones()}
