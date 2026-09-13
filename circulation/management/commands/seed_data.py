from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from catalog.models import Book, Music, Toy
from circulation.models import Borrower, Loan, Fine


class Command(BaseCommand):
    help = "Loads dummy books, music, toys, borrowers, and loans for testing"

    def handle(self, *args, **options):
        # --------------------------------------------------
        # Books
        # --------------------------------------------------

        books = [
            Book.objects.create(
                library_code='BK001',
                name='The Hobbit',
                description='Fantasy novel',
                author='J.R.R. Tolkien',
                genre='Fantasy',
            ),
            Book.objects.create(
                library_code='BK002',
                name='Dune',
                description='Sci-fi classic',
                author='Frank Herbert',
                genre='Science Fiction',
            ),
            Book.objects.create(
                library_code='BK003',
                name='1984',
                description='Dystopian novel',
                author='George Orwell',
                genre='Dystopian',
            ),
            Book.objects.create(
                library_code='BK004',
                name='Pride and Prejudice',
                description='Classic romance novel',
                author='Jane Austen',
                genre='Romance',
            ),
            Book.objects.create(
                library_code='BK005',
                name='To Kill a Mockingbird',
                description='Classic American novel',
                author='Harper Lee',
                genre='Drama',
            ),
            Book.objects.create(
                library_code='BK006',
                name='The Great Gatsby',
                description='American classic',
                author='F. Scott Fitzgerald',
                genre='Classic',
            ),
            Book.objects.create(
                library_code='BK007',
                name='Harry Potter and the Sorcerer Stone',
                description='Fantasy adventure',
                author='J.K. Rowling',
                genre='Fantasy',
            ),
            Book.objects.create(
                library_code='BK008',
                name='The Alchemist',
                description='Philosophical novel',
                author='Paulo Coelho',
                genre='Adventure',
            ),
            Book.objects.create(
                library_code='BK009',
                name='Atomic Habits',
                description='Self improvement book',
                author='James Clear',
                genre='Self Help',
            ),
            Book.objects.create(
                library_code='BK010',
                name='The Martian',
                description='Science fiction survival novel',
                author='Andy Weir',
                genre='Science Fiction',
            ),
            Book.objects.create(
                library_code='BK011',
                name='The Catcher in the Rye',
                description='Coming of age novel',
                author='J.D. Salinger',
                genre='Classic',
            ),
            Book.objects.create(
                library_code='BK012',
                name='The Kite Runner',
                description='Historical drama novel',
                author='Khaled Hosseini',
                genre='Drama',
            ),
            Book.objects.create(
                library_code='BK013',
                name='The Book Thief',
                description='Historical fiction novel',
                author='Markus Zusak',
                genre='Historical Fiction',
            ),
            Book.objects.create(
                library_code='BK014',
                name='The Da Vinci Code',
                description='Mystery thriller novel',
                author='Dan Brown',
                genre='Mystery',
            ),
            Book.objects.create(
                library_code='BK015',
                name='The Silent Patient',
                description='Psychological thriller',
                author='Alex Michaelides',
                genre='Thriller',
            ),
            Book.objects.create(
                library_code='BK016',
                name='Sapiens',
                description='History and anthropology book',
                author='Yuval Noah Harari',
                genre='History',
            ),
        ]

        # --------------------------------------------------
        # Music
        # --------------------------------------------------

        music = [
            Music.objects.create(
                library_code='MU001',
                name='Abbey Road',
                description='Studio album',
                artist='The Beatles',
                year=1969,
            ),
            Music.objects.create(
                library_code='MU002',
                name='Thriller',
                description='Studio album',
                artist='Michael Jackson',
                year=1982,
            ),
            Music.objects.create(
                library_code='MU003',
                name='Back in Black',
                description='Rock studio album',
                artist='AC/DC',
                year=1980,
            ),
            Music.objects.create(
                library_code='MU004',
                name='Random Access Memories',
                description='Electronic studio album',
                artist='Daft Punk',
                year=2013,
            ),
            Music.objects.create(
                library_code='MU005',
                name='Divide',
                description='Pop studio album',
                artist='Ed Sheeran',
                year=2017,
            ),
            Music.objects.create(
                library_code='MU006',
                name='25',
                description='Pop studio album',
                artist='Adele',
                year=2015,
            ),
            Music.objects.create(
                library_code='MU007',
                name='Nevermind',
                description='Grunge rock album',
                artist='Nirvana',
                year=1991,
            ),
            Music.objects.create(
                library_code='MU008',
                name='Discovery',
                description='Electronic music album',
                artist='Daft Punk',
                year=2001,
            ),
            Music.objects.create(
                library_code='MU009',
                name='Rumours',
                description='Rock studio album',
                artist='Fleetwood Mac',
                year=1977,
            ),
            Music.objects.create(
                library_code='MU010',
                name='Good Kid, M.A.A.D City',
                description='Hip hop studio album',
                artist='Kendrick Lamar',
                year=2012,
            ),
            Music.objects.create(
                library_code='MU011',
                name='Born to Die',
                description='Alternative pop album',
                artist='Lana Del Rey',
                year=2012,
            ),
            Music.objects.create(
                library_code='MU012',
                name='Hotel California',
                description='Rock studio album',
                artist='Eagles',
                year=1976,
            ),
            Music.objects.create(
                library_code='MU013',
                name='The Dark Side of the Moon',
                description='Progressive rock album',
                artist='Pink Floyd',
                year=1973,
            ),
            Music.objects.create(
                library_code='MU014',
                name='Random Access Memories 2',
                description='Electronic music collection',
                artist='Daft Punk',
                year=2014,
            ),
        ]

        # --------------------------------------------------
        # Toys
        # --------------------------------------------------

        toys = [
            Toy.objects.create(
                library_code='TY001',
                name='Jenga',
                description='Stacking block game',
                type='Board Game',
                age='6+',
            ),
            Toy.objects.create(
                library_code='TY002',
                name='Lego Castle',
                description='Building set',
                type='Building Set',
                age='8+',
            ),
            Toy.objects.create(
                library_code='TY003',
                name='Monopoly',
                description='Classic board game',
                type='Board Game',
                age='8+',
            ),
            Toy.objects.create(
                library_code='TY004',
                name='Rubik Cube',
                description='3D combination puzzle',
                type='Puzzle',
                age='8+',
            ),
            Toy.objects.create(
                library_code='TY005',
                name='Hot Wheels Car',
                description='Toy racing car',
                type='Vehicle',
                age='5+',
            ),
            Toy.objects.create(
                library_code='TY006',
                name='Lego City',
                description='City building set',
                type='Building Set',
                age='7+',
            ),
            Toy.objects.create(
                library_code='TY007',
                name='Chess Set',
                description='Classic strategy board game',
                type='Board Game',
                age='6+',
            ),
            Toy.objects.create(
                library_code='TY008',
                name='Remote Control Car',
                description='Battery powered toy car',
                type='Vehicle',
                age='10+',
            ),
            Toy.objects.create(
                library_code='TY009',
                name='Uno',
                description='Classic card game',
                type='Card Game',
                age='7+',
            ),
            Toy.objects.create(
                library_code='TY010',
                name='Scrabble',
                description='Word board game',
                type='Board Game',
                age='8+',
            ),
            Toy.objects.create(
                library_code='TY011',
                name='Play-Doh Set',
                description='Creative modeling clay set',
                type='Creative Toy',
                age='4+',
            ),
            Toy.objects.create(
                library_code='TY012',
                name='Toy Train',
                description='Electric toy train set',
                type='Vehicle',
                age='6+',
            ),
            Toy.objects.create(
                library_code='TY013',
                name='Jigsaw Puzzle',
                description='500 piece puzzle',
                type='Puzzle',
                age='10+',
            ),
            Toy.objects.create(
                library_code='TY014',
                name='Lego Technic',
                description='Advanced mechanical building set',
                type='Building Set',
                age='9+',
            ),
        ]

        # --------------------------------------------------
        # Borrowers
        # --------------------------------------------------

        borrowers = [
            Borrower.objects.create(
                name='Alice Rahman',
                email='alice@example.com',
                phone='0170000001',
            ),
            Borrower.objects.create(
                name='Bob Islam',
                email='bob@example.com',
                phone='0170000002',
            ),
            Borrower.objects.create(
                name='Charlie Hasan',
                email='charlie@example.com',
                phone='0170000003',
            ),
            Borrower.objects.create(
                name='David Ahmed',
                email='david@example.com',
                phone='0170000004',
            ),
            Borrower.objects.create(
                name='Eva Karim',
                email='eva@example.com',
                phone='0170000005',
            ),
            Borrower.objects.create(
                name='Farhan Hossain',
                email='farhan@example.com',
                phone='0170000006',
            ),
            Borrower.objects.create(
                name='Grace Chowdhury',
                email='grace@example.com',
                phone='0170000007',
            ),
            Borrower.objects.create(
                name='Hasan Mahmud',
                email='hasan@example.com',
                phone='0170000008',
            ),
            Borrower.objects.create(
                name='Imran Kabir',
                email='imran@example.com',
                phone='0170000011',
            ),
            Borrower.objects.create(
                name='Jannatul Ferdous',
                email='jannatul@example.com',
                phone='0170000012',
            ),
            Borrower.objects.create(
                name='Kamrul Hasan',
                email='kamrul@example.com',
                phone='0170000013',
            ),
            Borrower.objects.create(
                name='Lamia Akter',
                email='lamia@example.com',
                phone='0170000014',
            ),
            Borrower.objects.create(
                name='Nabil Hossain',
                email='nabil@example.com',
                phone='0170000015',
            ),
            Borrower.objects.create(
                name='Orin Sultana',
                email='orin@example.com',
                phone='0170000016',
            ),
        ]

        alice = borrowers[0]
        bob = borrowers[1]
        charlie = borrowers[2]
        david = borrowers[3]
        eva = borrowers[4]
        farhan = borrowers[5]
        grace = borrowers[6]
        hasan = borrowers[7]
        imran = borrowers[8]
        jannatul = borrowers[9]
        kamrul = borrowers[10]
        lamia = borrowers[11]
        nabil = borrowers[12]
        orin = borrowers[13]

        now = timezone.now()

        # --------------------------------------------------
        # Active Loans
        # --------------------------------------------------

        books[0].borrow()
        Loan.objects.create(
            item=books[0],
            borrower=alice,
            due_at=now + timedelta(days=14),
        )

        books[3].borrow()
        Loan.objects.create(
            item=books[3],
            borrower=charlie,
            due_at=now + timedelta(days=7),
        )

        music[2].borrow()
        Loan.objects.create(
            item=music[2],
            borrower=david,
            due_at=now + timedelta(days=10),
        )

        toys[3].borrow()
        Loan.objects.create(
            item=toys[3],
            borrower=eva,
            due_at=now + timedelta(days=5),
        )

        books[6].borrow()
        Loan.objects.create(
            item=books[6],
            borrower=farhan,
            due_at=now + timedelta(days=12),
        )

        music[4].borrow()
        Loan.objects.create(
            item=music[4],
            borrower=grace,
            due_at=now + timedelta(days=3),
        )

        # Additional active loans

        books[10].borrow()
        Loan.objects.create(
            item=books[10],
            borrower=imran,
            due_at=now + timedelta(days=9),
        )

        books[11].borrow()
        Loan.objects.create(
            item=books[11],
            borrower=jannatul,
            due_at=now + timedelta(days=6),
        )

        music[8].borrow()
        Loan.objects.create(
            item=music[8],
            borrower=kamrul,
            due_at=now + timedelta(days=11),
        )

        toys[8].borrow()
        Loan.objects.create(
            item=toys[8],
            borrower=lamia,
            due_at=now + timedelta(days=4),
        )

        books[12].borrow()
        Loan.objects.create(
            item=books[12],
            borrower=nabil,
            due_at=now + timedelta(days=8),
        )

        toys[12].borrow()
        Loan.objects.create(
            item=toys[12],
            borrower=orin,
            due_at=now + timedelta(days=13),
        )

        # --------------------------------------------------
        # Returned Loans - No Fine
        # --------------------------------------------------

        books[2].borrow()
        loan = Loan.objects.create(
            item=books[2],
            borrower=hasan,
            due_at=now - timedelta(days=2),
        )
        loan.returned_at = now - timedelta(days=3)
        loan.status = 'RETURNED'
        loan.save()
        books[2].return_item()

        toys[0].borrow()
        loan = Loan.objects.create(
            item=toys[0],
            borrower=alice,
            due_at=now + timedelta(days=2),
        )
        loan.returned_at = now - timedelta(days=1)
        loan.status = 'RETURNED'
        loan.save()
        toys[0].return_item()

        # Additional returned loans without fines

        music[9].borrow()
        loan = Loan.objects.create(
            item=music[9],
            borrower=imran,
            due_at=now + timedelta(days=2),
        )
        loan.returned_at = now - timedelta(days=1)
        loan.status = 'RETURNED'
        loan.save()
        music[9].return_item()

        toys[9].borrow()
        loan = Loan.objects.create(
            item=toys[9],
            borrower=jannatul,
            due_at=now + timedelta(days=3),
        )
        loan.returned_at = now - timedelta(days=2)
        loan.status = 'RETURNED'
        loan.save()
        toys[9].return_item()

        # --------------------------------------------------
        # Returned Loans - With Fines
        # --------------------------------------------------

        books[1].borrow()
        loan = Loan.objects.create(
            item=books[1],
            borrower=bob,
            due_at=now - timedelta(days=5),
        )
        loan.returned_at = now
        loan.status = 'RETURNED'
        loan.save()
        books[1].return_item()

        Fine.objects.create(
            loan=loan,
            amount=5 * 0.50,
        )

        music[0].borrow()
        loan = Loan.objects.create(
            item=music[0],
            borrower=charlie,
            due_at=now - timedelta(days=10),
        )
        loan.returned_at = now
        loan.status = 'RETURNED'
        loan.save()
        music[0].return_item()

        Fine.objects.create(
            loan=loan,
            amount=10 * 0.50,
        )

        toys[1].borrow()
        loan = Loan.objects.create(
            item=toys[1],
            borrower=david,
            due_at=now - timedelta(days=3),
        )
        loan.returned_at = now
        loan.status = 'RETURNED'
        loan.save()
        toys[1].return_item()

        Fine.objects.create(
            loan=loan,
            amount=3 * 0.50,
        )

        books[5].borrow()
        loan = Loan.objects.create(
            item=books[5],
            borrower=eva,
            due_at=now - timedelta(days=15),
        )
        loan.returned_at = now
        loan.status = 'RETURNED'
        loan.save()
        books[5].return_item()

        Fine.objects.create(
            loan=loan,
            amount=15 * 0.50,
        )

        # Additional returned loans with fines

        books[13].borrow()
        loan = Loan.objects.create(
            item=books[13],
            borrower=kamrul,
            due_at=now - timedelta(days=4),
        )
        loan.returned_at = now
        loan.status = 'RETURNED'
        loan.save()
        books[13].return_item()

        Fine.objects.create(
            loan=loan,
            amount=4 * 0.50,
        )

        music[10].borrow()
        loan = Loan.objects.create(
            item=music[10],
            borrower=lamia,
            due_at=now - timedelta(days=7),
        )
        loan.returned_at = now
        loan.status = 'RETURNED'
        loan.save()
        music[10].return_item()

        Fine.objects.create(
            loan=loan,
            amount=7 * 0.50,
        )

        toys[10].borrow()
        loan = Loan.objects.create(
            item=toys[10],
            borrower=nabil,
            due_at=now - timedelta(days=12),
        )
        loan.returned_at = now
        loan.status = 'RETURNED'
        loan.save()
        toys[10].return_item()

        Fine.objects.create(
            loan=loan,
            amount=12 * 0.50,
        )

        books[14].borrow()
        loan = Loan.objects.create(
            item=books[14],
            borrower=orin,
            due_at=now - timedelta(days=2),
        )
        loan.returned_at = now
        loan.status = 'RETURNED'
        loan.save()
        books[14].return_item()

        Fine.objects.create(
            loan=loan,
            amount=2 * 0.50,
        )

        # --------------------------------------------------
        # More Returned Loans
        # --------------------------------------------------

        music[1].borrow()
        loan = Loan.objects.create(
            item=music[1],
            borrower=farhan,
            due_at=now - timedelta(days=1),
        )
        loan.returned_at = now
        loan.status = 'RETURNED'
        loan.save()
        music[1].return_item()

        Fine.objects.create(
            loan=loan,
            amount=1 * 0.50,
        )

        toys[2].borrow()
        loan = Loan.objects.create(
            item=toys[2],
            borrower=grace,
            due_at=now + timedelta(days=5),
        )
        loan.returned_at = now - timedelta(days=2)
        loan.status = 'RETURNED'
        loan.save()
        toys[2].return_item()

        self.stdout.write(
            self.style.SUCCESS('Dummy data loaded successfully.')
        )
