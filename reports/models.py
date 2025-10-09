from django.db import models
from user.models import User

class Lost_reports(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    item_description = models.TextField()
    item_image = models.ImageField(upload_to='lost_items/', blank=True, null=True)
    location = models.CharField(max_length=255)
    lost_date = models.DateField()
    contact = models.CharField(max_length=100)
    reported_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, default='others')


    def __str__(self):
        return self.item_name
    


class Found_reports(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    item_description = models.TextField()
    item_image = models.ImageField(upload_to='Found_items/', blank=True, null=True)
    location = models.CharField(max_length=255)
    found_date = models.DateField()
    contact = models.CharField(max_length=100)
    reported_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, default='others')


    def __str__(self):
        return self.item_name
    

class Claimed_items(models.Model):
    found_report= models.ForeignKey(Found_reports, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    description = models.TextField()
    claimed_at = models.DateTimeField(auto_now_add=True)
    claim_status = models.BooleanField(default=False)  # False = Pending, True = Approved
    status = models.CharField(max_length=50, default='Pending')  # e.g., Pending, Approved, Rejected

    def __str__(self):
        return f"Claim by {self.name} for {self.found_report.item_name}"