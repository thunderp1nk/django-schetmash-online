# django-schetmash-online
Пример приложения для интеграции проекта на django с https://online.schetmash.com/

В настройках проекта необходимо добавить значения:
ONLINEKASSA_LOGIN = 'your_login'
ONLINEKASSA_PASSWORD = 'your_password'
ONLINEKASSA_SHOPID = 123 # ваш номер магазина
ONLINEKASSA_ORDER_MODEL = 'orders.Order' # Путь к модели заказа

В модели заказа необходимо реализовать метод to_schetmash_receipt_dict(), который маппит данные заказа в валидный для онлайн-кассы вид

После поступления оплаты заказа должен вызываться такс register_receipt.apply_async(args=[instance.pk]), который начинает процесс регистрации чека в онлайн-кассе

Зависимости тестового проекта:
Django==1.11
celery==4.0.2
django-redis==4.8.0
requests==2.14.2
