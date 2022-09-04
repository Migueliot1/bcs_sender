from django.db import models
import uuid

# Create your models here.
class Transaction(models.Model):
    '''
    The model for each sent transaction.

    Consists of ID (primary key), sent BCS amount, 
    sender's address, recipient's address, description, 
    and date of transaction.

    Only ID is necessary to create an instance.
    '''
    id = models.CharField(max_length=200, unique=True, primary_key=True, editable=True)

    amount = models.IntegerField(null=True, blank=True)
    sender = models.CharField(max_length=200, null=True, blank=True)
    recipient = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=2000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
