from celery import shared_task
from .services.notify_user import Command

@shared_task
def update_prices_and_notify():
    Command().handle()
