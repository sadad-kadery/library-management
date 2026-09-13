from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from catalog.models import Book, Music, Toy
from circulation.models import Borrower, Loan, Fine


class Command(BaseCommand):
    help = "Loads some dummy books, music, toys, borrowers, and loans for testing"

    def handle(self, *args, **options):
        # already seeded on an earlier deploy? don't try again, just exit quietly
        if Book.objects.filter(library_code='BK001').exists():
            self.stdout.write(self.style.WARNING('Dummy data already present — skipping.'))
            return

        # books
        b1 = Book.objects.create(
            library_code='BK001', name='The Hobbit', description='Fantasy novel',
            author='J.R.R. Tolkien', genre='Fantasy',
        )
        b2 = Book.objects.create(
            library_code='BK002', name='Dune', description='Sci-fi classic',
            author='Frank Herbert', genre='Science Fiction',
        )
        Book.objects.create(
            library_code='BK003', name='1984', description='Dystopian novel',
            author='George Orwell', genre='Dystopian',
        )

        # music
        Music.objects.create(
            library_code='MU001', name='Abbey Road', description='Studio album',
            artist='The Beatles', year=1969,
        )
        Music.objects.create(
            library_code='MU002', name='Thriller', description='Studio album',
            artist='Michael Jackson', year=1982,
        )

        # toys
        Toy.objects.create(
            library_code='TY001', name='Jenga', description='Stacking block game',
            type='Board Game', age='6+',
        )
        Toy.objects.create(
            library_code='TY002', name='Lego Castle', description='Building set',
            type='Building Set', age='8+',
        )

        # borrowers
        alice = Borrower.objects.create(name='Alice Rahman', email='alice@example.com', phone='0170000001')
        bob = Borrower.objects.create(name='Bob Islam', email='bob@example.com', phone='0170000002')

        # an active loan, still within the due date
        b1.borrow()
        Loan.objects.create(item=b1, borrower=alice, due_at=timezone.now() + timedelta(days=14))

        # an overdue loan that's already been returned late, so there's a fine to look at
        b2.borrow()
        loan2 = Loan.objects.create(
            item=b2, borrower=bob,
            due_at=timezone.now() - timedelta(days=5),
        )
        loan2.returned_at = timezone.now()
        loan2.status = 'RETURNED'
        loan2.save()
        b2.return_item()
        Fine.objects.create(loan=loan2, amount=5 * 0.50)

        self.stdout.write(self.style.SUCCESS('Dummy data loaded.'))