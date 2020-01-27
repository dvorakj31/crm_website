import django.core.mail
from django_cron import CronJobBase, Schedule
from .models import WarningEmail, Customer, CustomerHistory, CustomerClone
from django.forms.models import model_to_dict

import datetime


class SendMails(CronJobBase):
    RUN_EVERY_DAY = 60 * 24

    schedule = Schedule(run_every_mins=RUN_EVERY_DAY)
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


class RestartDatabase(CronJobBase):
    RUN_AT_TIMES = ['7:00']
    RUN_AT_MINS = 1
    schedule = Schedule(run_at_times=['7:00'], run_every_mins=RUN_AT_MINS)
    code = 'crm_website.restart_database'

    def do(self):
        today = datetime.date.today()
        print(f'today = {today}')
        # if today.day not in [1, 2, 3] or today.weekday() > 4:
        #     return
        try:
            self._create_customer_history()
        except Exception as e:
            print(f'exception {e}')
        if today.day == 1 and today.month == 1:
            Customer.objects.filter(is_employer=True).update(withholding_tax=False)
            Customer.objects.filter(road_tax=True).update(submitted_road_tax=False)
            Customer.objects.filter(advance_tax=True).update(advance_tax=False)
        papers_clients = Customer.objects.filter(papers=True)
        for client in papers_clients:
            print(f'VAT: {client.name} {client._meta.db_table}')
        papers_clients = Customer.objects.filter(wage=True)
        for client in papers_clients:
            print(f'wage: {client.name}')
        papers_clients = Customer.objects.filter(submitted_wage_tax=True)
        for client in papers_clients:
            print(f'wage tax: {client.name}')
        papers_clients = Customer.objects.filter(submitted_tax=True)
        for client in papers_clients:
            print(f'sub tax: {client.name}')
        Customer.objects.filter(papers=True).update(papers=False)
        Customer.objects.filter(wage=True).update(wage=False)
        Customer.objects.filter(submitted_wage_tax=True).update(submitted_wage_tax=False)
        Customer.objects.filter(submitted_tax=True).update(submitted_tax=False)

    def _create_customer_history(self):
        for customer in Customer.objects.all():
            customer_dict = model_to_dict(customer, exclude=['id'])
            clone_dict = {k: customer_dict[k] for k in customer_dict if k in CustomerClone.__dict__}
            customer_clone = CustomerClone.objects.create(**clone_dict)
            CustomerHistory.objects.create(customer=customer_clone)
