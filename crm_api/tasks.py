import django.core.mail
from django_cron import CronJobBase, Schedule
from .models import WarningEmail, Customer

import datetime


class SendMails(CronJobBase):
    RUN_EVERY_MINS = 60 * 24

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'crm_webiste.send_mails'

    def do(self):
        day = datetime.datetime.today().day
        warning_mail = WarningEmail.objects.filter(send_date__exact=day)
        if len(warning_mail) == 0:
            return
        warn_mail = warning_mail.first()
        if datetime.datetime.today().month in [1, 4, 7, 10]:
            vat_pay = Customer.objects.filter(vat__in=["mesicne", "ctvrtletne"])
        else:
            vat_pay = Customer.objects.filter(vat__exact="mesicne")
        messages = []
        connection = django.core.mail.get_connection()
        for customer in vat_pay:
            if customer.email:
                messages.append(
                    django.core.mail.EmailMessage(
                        subject=warn_mail.subject,
                        body=warn_mail.body,
                        from_email=django.core.mail.settings.EMAIL_HOST_USER,
                        to=[customer.email],
                        connection=connection
                    )
                )
        for message in messages:
            try:
                message.send()
            except Exception as e:
                print(f'send mail failed {e}')
        connection.close()
