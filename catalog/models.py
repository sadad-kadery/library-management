from django.db import models


class Item(models.Model):
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('BORROWED', 'Borrowed'),
        ('DAMAGED', 'Damaged'),
        ('DESTROY', 'Destroy'),
    ]

    library_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='AVAILABLE')

    @property
    def item_type(self):
        if hasattr(self, 'book'):
            return 'Book'
        if hasattr(self, 'music'):
            return 'Music'
        if hasattr(self, 'toy'):
            return 'Toy'
        return 'Unknown'

    def borrow(self):
        # don't let someone check out something that's already gone / broken
        if self.status != 'AVAILABLE':
            raise ValueError(f"{self.name} is not available (status: {self.status})")
        self.status = 'BORROWED'
        self.save()

    def return_item(self):
        if self.status != 'BORROWED':
            raise ValueError(f"{self.name} wasn't marked as borrowed")
        self.status = 'AVAILABLE'
        self.save()

    def __str__(self):
        return f"{self.name} ({self.library_code})"


class Book(Item):
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100, blank=True)


class Music(Item):
    artist = models.CharField(max_length=255)
    year = models.IntegerField(null=True, blank=True)


class Toy(Item):
    type = models.CharField(max_length=100, blank=True)
    age = models.CharField(max_length=20, blank=True)