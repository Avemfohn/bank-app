from django.db import models
import uuid

class Account(models.Model):
    # We use UUIDs so attackers can't just guess "user 1, user 2"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, null=True, default="No notes")
    def __str__(self):
        return f"{self.owner} - ${self.balance}"