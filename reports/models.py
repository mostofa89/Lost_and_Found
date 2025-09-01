from django.db import models
from user import models as user_models
# Create your models here.
class Lost_reports(models.Model):
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    item_description = models.TextField(max_length=30)
    item_image = models.ImageField(upload_to='lost_items/', blank=True, null=True)
    location = models.CharField(max_length=255)
    date_lost = models.DateField()
    contact = models.CharField(max_length=100)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_name