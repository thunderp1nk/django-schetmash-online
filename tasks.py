from datetime import timedelta

from django.db import IntegrityError

from celery import shared_task
from celery.task import periodic_task

from onlinekassa.api import schetmash
from onlinekassa.models import Receipt


@shared_task
def register_receipt(order_pk):
    try:
        receipt = Receipt.objects.select_related('order').create(
            order_id=order_pk
        )
    except IntegrityError:
        receipt = Receipt.objects.select_related('order').get(order_id=order_pk)

    response_dict = schetmash.register_receipt(receipt.order.to_schetmash_receipt_dict())
    if response_dict.get('status') == 'accept':
        receipt.ticket_id = response_dict.get('id')
        receipt.status = Receipt.RECEIPT_STATUS_PROCESSING
        receipt.save()
        get_receipt_status.apply_async(
            args=[receipt.ticket_id]
        )
    else:
        receipt.save_error_data(response_dict.get('message'))


@shared_task
def get_receipt_status(ticket_id, number_of_try=0):
    response_dict = schetmash.get_receipt_status(ticket_id)
    if response_dict.get('status') == 'processing':
        if number_of_try >= 38: # типа много уже
            receipt = Receipt.objects.get(ticket_id=ticket_id)
            receipt.save_error_data('Слишком много попыток запроса чека')
            return
        get_receipt_status.apply_async(
            args=[ticket_id],
            kwargs={'number_of_try': number_of_try + 1},
            countdown=10*60
        )
    elif response_dict.get('status') == 'success':
        receipt = Receipt.objects.get(ticket_id=ticket_id)
        receipt.save_payload_data(response_dict)


@periodic_task(run_every=timedelta(minutes=30))
def get_token():
    schetmash.get_token()
