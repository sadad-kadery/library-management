from django.db import models
from catalog.models import Item


class Borrower(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name


class Loan(models.Model):
    STATUS_CHOICES = [
        ('BORROWED', 'Borrowed'),
        ('RETURNED', 'Returned'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_at = models.DateTimeField()
    returned_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='BORROWED')


class Fine(models.Model):
    STATUS_CHOICES = [
        ('UNPAID', 'Unpaid'),
        ('PAID', 'Paid'),
    ]

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='UNPAID')