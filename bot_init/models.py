from django.contrib.auth import get_user_model

User = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(User)
    surname_client = models.TextField()
    name_client = models.TextField()
    atronymic_client.TextField()
    phone_client = models.TextField()
    info = models.TextField()
    info_from_measurer = models.TextField()
    deliveryman_datetime = models.Datetime()
    installer_datetime = models.Datetime()