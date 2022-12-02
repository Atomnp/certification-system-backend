from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


"""
You will have to create app password for email_sender email account
follow this link : 
https://towardsdatascience.com/automate-sending-emails-with-gmail-in-python-449cc0c3c317

"""


def get_certificate_name(path_from_media_root):
    return path_from_media_root.split("/")[-1].split(".")[0]


def send_bulk_email(
    certificates, filter_already_sent, subject="Your certificate is ready"
):

    fail_count = 0
    success_count = 0
    for certificate in certificates:
        # certificate_id = get_certificate_name(certificate.image.name)
        certificate_id = certificate.id
        html_message = render_to_string(
            "email.html",
            {
                "name": certificate.name,
                "event": certificate.event.name,
                "category": certificate.category.name,
                "link": f"{settings.VERIFICATION_BASE_URL}{certificate_id}",
            },
        )
        if not certificate.email_sent or not filter_already_sent:
            try:
                send_mail(
                    subject,
                    message="",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[certificate.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                certificate.email_sent = True
                certificate.save()
                success_count += 1

            except Exception as e:
                fail_count += 1
                print(e)
                certificate.email_sent = False
                certificate.save()
    return fail_count, success_count
