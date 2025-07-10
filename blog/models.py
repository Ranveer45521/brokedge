from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Broker(models.Model):
    name = models.CharField(max_length=100)
    brokerage_charge = models.DecimalField(max_digits=6, decimal_places=2)
    hidden_charges = models.TextField(blank=True)
    features = models.TextField(blank=True)

    def __str__(self):
        return self.name

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"
    
from django.db import models

class BrokerSuggestion(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (from {self.email or 'anonymous'})"
