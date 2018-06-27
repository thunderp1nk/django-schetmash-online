# django-schetmash-online
Пример приложения для интеграции проекта на django с https://online.schetmash.com/

В настройках проекта необходимо добавить значения:<br>
ONLINEKASSA_LOGIN = 'your_login'<br>
ONLINEKASSA_PASSWORD = 'your_password'<br>
ONLINEKASSA_SHOPID = 123 # ваш номер магазина<br>
ONLINEKASSA_ORDER_MODEL = 'orders.Order' # Путь к модели заказа<br>

В модели заказа необходимо реализовать метод to_schetmash_receipt_dict(), который маппит данные заказа в валидный для онлайн-кассы вид

После поступления оплаты заказа должен вызываться такс register_receipt.apply_async(args=[instance.pk]), который начинает процесс регистрации чека в онлайн-кассе

Зависимости тестового проекта:<br>
Django==1.11<br>
celery==4.0.2<br>
django-redis==4.8.0<br>
requests==2.14.2<br>
