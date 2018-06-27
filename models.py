from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Receipt(models.Model):
    RECEIPT_STATUS_NEW = 'new'
    RECEIPT_STATUS_PROCESSING = 'processing'
    RECEIPT_STATUS_SUCCESS = 'success'
    RECEIPT_STATUS_ERROR = 'error'
    RECEIPT_STATUS_CHOICES = (
        (RECEIPT_STATUS_NEW, _('новый')),
        (RECEIPT_STATUS_PROCESSING, _('в процессе')),
        (RECEIPT_STATUS_SUCCESS, _('успешно')),
        (RECEIPT_STATUS_ERROR, _('ошибка')),
    )

    ticket_id = models.IntegerField(
        verbose_name=_('id заявки'),
        blank=True,
        null=True,
    )
    status = models.CharField(
        verbose_name=_('Статус чека'),
        choices=RECEIPT_STATUS_CHOICES,
        max_length=16,
        default=RECEIPT_STATUS_NEW
    )
    order = models.OneToOneField(
        to=settings.ONLINEKASSA_ORDER_MODEL,
        verbose_name=_('Заказ'),
        related_name='receipt',
    )

    total = models.DecimalField(
        verbose_name=_('Финальная сумма'),
        blank=True,
        null=True,
        max_digits=12,
        decimal_places=2,
    )
    fns_site = models.CharField(
        verbose_name=_('Сайт'),
        max_length=256,
        blank=True,
        null=True,
    )
    fn_number = models.CharField(
        verbose_name=_('Номер чека?'),
        max_length=256,
        blank=True,
        null=True,
    )
    shift_number = models.IntegerField(
        verbose_name=_('shift_number'),
        blank=True,
        null=True,
    )
    receipt_datetime = models.DateTimeField(
        verbose_name=_('receipt_datetime'),
        blank=True,
        null=True,
    )
    fiscal_receipt_number = models.IntegerField(
        verbose_name=_('fiscal_receipt_number'),
        blank=True,
        null=True,
    )
    fiscal_document_number = models.IntegerField(
        verbose_name=_('fiscal_document_number'),
        blank=True,
        null=True,
    )
    ecr_registration_number = models.CharField(
        verbose_name=_('ecr_registration_number'),
        max_length=32,
        blank=True,
        null=True,
    )
    fiscal_document_attribute = models.CharField(
        verbose_name=_('fiscal_document_attribute'),
        max_length=32,
        blank=True,
        null=True,
    )
    error_message = models.CharField(
        verbose_name=_('Сообщение об ошибке'),
        max_length=512,
        blank=True,
        null=True,
    )

    create_date = models.DateTimeField(
        verbose_name=_('Дата создания'),
        auto_now_add=True
    )
    edit_date = models.DateTimeField(
        verbose_name=_('Дата изменения'),
        auto_now=True
    )

    class Meta():
        verbose_name_plural = _('Чеки в Онлайн-кассе Счетмаш')
        verbose_name = _('Чек в Онлайн-кассе Счетмаш')
        ordering = ['-create_date']

    def __str__(self):
        return str(self.pk)

    def save_payload_data(self, data_dict):
        self.total = data_dict['payload']['total']
        self.fns_site = data_dict['payload']['fns_site']
        self.fn_number = data_dict['payload']['fn_number']
        self.shift_number = data_dict['payload']['shift_number']
        self.fiscal_receipt_number = data_dict['payload']['fiscal_receipt_number']
        self.fiscal_document_number = data_dict['payload']['fiscal_document_number']
        self.ecr_registration_number = data_dict['payload']['ecr_registration_number']
        self.fiscal_document_attribute = data_dict['payload']['fiscal_document_attribute']
        self.status = self.RECEIPT_STATUS_SUCCESS
        self.save()

    def save_error_data(self, error_message):
        self.status = Receipt.RECEIPT_STATUS_ERROR
        self.error_message = error_message
        self.save()