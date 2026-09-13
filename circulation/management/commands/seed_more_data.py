from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from catalog.models import Book, Music, Toy
from circulation.models import Borrower, Loan, Fine


class Command(BaseCommand):
    help = "Loads additional dummy books, music, toys, borrowers, loans, and fines"

    def handle(self, *args, **options):

        # =========================
        # BOOKS
        # =========================

        books = [
            Book.objects.create(
                library_code='BK004',
                name='Harry Potter and the Philosopher\'s Stone',
                description='Fantasy adventure novel',
                author='J.K. Rowling',
                genre='Fantasy',
            ),
            Book.objects.create(
                library_code='BK005',
                name='The Alchemist',
                description='Inspirational adventure novel',
                author='Paulo Coelho',
                genre='Adventure',
            ),
            Book.objects.create(
                library_code='BK006',
                name='To Kill a Mockingbird',
                description='Classic American novel',
                author='Harper Lee',
                genre='Drama',
            ),
            Book.objects.create(
                library_code='BK007',
                name='The Great Gatsby',
                description='Classic American novel',
                author='F. Scott Fitzgerald',
                genre='Classic',
            ),
            Book.objects.create(
                library_code='BK008',
                name='The Martian',
                description='Science fiction survival story',
                author='Andy Weir',
                genre='Science Fiction',
            ),
            Book.objects.create(
                library_code='BK009',
                name='Pride and Prejudice',
                description='Classic romance novel',
                author='Jane Austen',
                genre='Romance',
            ),
            Book.objects.create(
                library_code='BK010',
                name='The Kite Runner',
                description='Historical drama novel',
                author='Khaled Hosseini',
                genre='Drama',
            ),
        ]

        # =========================
        # MUSIC
        # =========================

        music = [
            Music.objects.create(
                library_code='MU003',
                name='Back to Black',
                description='Studio album',
                artist='Amy Winehouse',
                year=2006,
            ),
            Music.objects.create(
                library_code='MU004',
                name='Random Access Memories',
                description='Electronic music album',
                artist='Daft Punk',
                year=2013,
            ),
            Music.objects.create(
                library_code='MU005',
                name='25',
                description='Studio album',
                artist='Adele',
                year=2015,
            ),
            Music.objects.create(
                library_code='MU006',
                name='Divide',
                description='Pop music album',
                artist='Ed Sheeran',
                year=2017,
            ),
            Music.objects.create(
                library_code='MU007',
                name='After Hours',
                description='R&B and pop album',
                artist='The Weeknd',
                year=2020,
            ),
        ]

        # =========================
        # TOYS
        # =========================

        toys = [
            Toy.objects.create(
                library_code='TY003',
                name='Monopoly',
                description='Classic property trading board game',
                type='Board Game',
                age='8+',
            ),
            Toy.objects.create(
                library_code='TY004',
                name='Rubik\'s Cube',
                description='3D combination puzzle',
                type='Puzzle',
                age='8+',
            ),
            Toy.objects.create(
                library_code='TY005',
                name='Chess Set',
                description='Classic strategy board game',
                type='Board Game',
                age='6+',
            ),
            Toy.objects.create(
                library_code='TY006',
                name='Remote Control Car',
                description='Battery powered toy car',
                type='Vehicle',
                age='10+',
            ),
            Toy.objects.create(
                library_code='TY007',
                name='Lego City',
                description='City building construction set',
                type='Building Set',
                age='7+',
            ),
        ]

        # =========================
        # BORROWERS
        # =========================

        borrowers = [
            Borrower.objects.create(
                name='Charlie Ahmed',
                email='charlie@example.com',
                phone='0170000003',
            ),
            Borrower.objects.create(
                name='David Hasan',
                email='david@example.com',
                phone='0170000004',
            ),
            Borrower.objects.create(
                name='Emma Karim',
                email='emma@example.com',
                phone='0170000005',
            ),
            Borrower.objects.create(
                name='Farhan Hossain',
                email='farhan@example.com',
                phone='0170000006',
            ),
            Borrower.objects.create(
                name='Grace Akter',
                email='grace@example.com',
                phone='0170000007',
            ),
            Borrower.objects.create(
                name='Hasan Rahman',
                email='hasan@example.com',
                phone='0170000008',
            ),
            Borrower.objects.create(
                name='Ibrahim Khan',
                email='ibrahim@example.com',
                phone='0170000009',
            ),
            Borrower.objects.create(
                name='Nadia Islam',
                email='nadia@example.com',
                phone='0170000010',
            ),
        ]

        # =========================
        # ACTIVE LOANS
        # =========================

        # Book 4 - Charlie - due in 7 days
        books[0].borrow()
        Loan.objects.create(
            item=books[0],
            borrower=borrowers[0],
            due_at=timezone.now() + timedelta(days=7),
        )

        # Book 5 - David - due in 10 days
        books[1].borrow()
        Loan.objects.create(
            item=books[1],
            borrower=borrowers[1],
            due_at=timezone.now() + timedelta(days=10),
        )

        # Music 3 - Emma - due in 5 days
        music[0].borrow()
        Loan.objects.create(
            item=music[0],
            borrower=borrowers[2],
            due_at=timezone.now() + timedelta(days=5),
        )

        # Toy 3 - Farhan - due in 3 days
        toys[0].borrow()
        Loan.objects.create(
            item=toys[0],
            borrower=borrowers[3],
            due_at=timezone.now() + timedelta(days=3),
        )

        # Toy 4 - Grace - due in 12 days
        toys[1].borrow()
        Loan.objects.create(
            item=toys[1],
            borrower=borrowers[4],
            due_at=timezone.now() + timedelta(days=12),
        )

        # =========================
        # OVERDUE RETURNED LOANS
        # =========================

        # Book 6 - returned 8 days late
        books[2].borrow()
        loan1 = Loan.objects.create(
            item=books[2],
            borrower=borrowers[5],
            due_at=timezone.now() - timedelta(days=8),
        )

        loan1.returned_at = timezone.now()
        loan1.status = 'RETURNED'
        loan1.save()

        books[2].return_item()

        Fine.objects.create(
            loan=loan1,
            amount=8 * 0.50,
        )

        # Music 4 - returned 3 days late
        music[1].borrow()
        loan2 = Loan.objects.create(
            item=music[1],
            borrower=borrowers[6],
            due_at=timezone.now() - timedelta(days=3),
        )

        loan2.returned_at = timezone.now()
        loan2.status = 'RETURNED'
        loan2.save()

        music[1].return_item()

        Fine.objects.create(
            loan=loan2,
            amount=3 * 0.50,
        )

        # Toy 5 - returned 12 days late
        toys[2].borrow()
        loan3 = Loan.objects.create(
            item=toys[2],
            borrower=borrowers[7],
            due_at=timezone.now() - timedelta(days=12),
        )

        loan3.returned_at = timezone.now()
        loan3.status = 'RETURNED'
        loan3.save()

        toys[2].return_item()

        Fine.objects.create(
            loan=loan3,
            amount=12 * 0.50,
        )

        # =========================
        # MORE RETURNED ON-TIME LOANS
        # =========================

        # Book 7 - returned on time
        books[3].borrow()
        loan4 = Loan.objects.create(
            item=books[3],
            borrower=borrowers[0],
            due_at=timezone.now() + timedelta(days=5),
        )

        loan4.returned_at = timezone.now()
        loan4.status = 'RETURNED'
        loan4.save()

        books[3].return_item()

        # Music 5 - returned on time
        music[2].borrow()
        loan5 = Loan.objects.create(
            item=music[2],
            borrower=borrowers[1],
            due_at=timezone.now() + timedelta(days=7),
        )

        loan5.returned_at = timezone.now()
        loan5.status = 'RETURNED'
        loan5.save()

        music[2].return_item()

        # =========================
        # SUCCESS MESSAGE
        # =========================

        self.stdout.write(
            self.style.SUCCESS(
                'Additional dummy data loaded successfully.'
            )
        )