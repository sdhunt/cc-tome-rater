## TomeRater Project
#
# Simon Hunt
# sdhunt@gmail.com
#
# For the "Creative" part, I added the more sophisticated error testing

## User class

class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print('User email has been updated to <{}>'.format(address))

    def __repr__(self):
        return '{} <{}> Books read: {}'.format(
            self.name, self.email, len(self.books)
        )

    def __eq__(self, other_user):
        return self.name == other_user.name and self.email == other_user.email

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        total = 0
        count = 0
        for rating in self.books.values():
            if rating is not None:
                total += rating
                count += 1
        return total / count

## Book class

class Book:
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def __eq__(self, other):
        return self.title == other.title and self.isbn == other.isbn

    def __hash__(self):
        return hash((self.title, self.isbn))

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, isbn):
        self.isbn = isbn
        print('Book ISBN has been updated to <{}>'.format(isbn))

    def add_rating(self, rating):
        if not rating is None:
            if rating >= 0 and rating <= 4:
                self.ratings.append(rating)
            else:
                print("Invalid Rating")

    def get_average_rating(self):
        total = 0
        for rating in self.ratings:
            total += rating
        return total / len(self.ratings)


## Fiction subclass

class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)


## Non-Fiction subclass

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return '{}, a {} manual on {}'.format(
            self.title, self.level, self.subject
        )

## TomeRater class

class DuplicateIsbnException(Exception):
    pass

class TomeRater:
    def __init__(self):
        self.users = {}
        self.books = {}
        self.isbns = {}

    def validate_isbn(self, isbn):
        for existing in self.isbns:
            if isbn == existing:
                raise DuplicateIsbnException
        self.isbns[isbn] = True

    def create_book(self, title, isbn):
        self.validate_isbn(isbn)
        return Book(title, isbn)

    def create_novel(self, title, author, isbn):
        self.validate_isbn(isbn)
        return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        self.validate_isbn(isbn)
        return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating=None):
        user = self.users.get(email, None)
        if not user:
            print("No user with email {}".format(email))
        else:
            user.read_book(book, rating)
            book.add_rating(rating)
            if not book in self.books:
                self.books[book] = 1
            else:
                self.books[book] += 1

    def valid_email(self, email):
        domains = ['.com', '.edu', '.org']
        domain = email[-4:] if len(email) > 4 else None
        return '@' in email and domain in domains

    def add_user(self, name, email, user_books=None):
        if not self.valid_email(email):
            print("Invalid email format: {}".format(email))
            return

        if email in self.users:
            print("User with that email already exists: {}".format(email))
            return

        self.users[email] = User(name, email)
        if user_books:
            for book in user_books:
                self.add_book_to_user(book, email)

    def print_catalog(self):
        for book in self.books:
            print('  ', book)

    def print_users(self):
        for user in self.users.values():
            print('  ', user)

    def most_read_book(self):
        most_book = None
        most_reads = 0
        for book, count in self.books.items():
            if not count is None and count > most_reads:
                most_reads = count
                most_book = book
        return most_book

    def highest_rated_book(self):
        high_book = None
        highest = -1
        for book in self.books:
            if book.get_average_rating() > highest:
                highest = book.get_average_rating()
                high_book = book
        return high_book

    def most_positive_user(self):
        high_user = None
        highest = -1
        for user in self.users.values():
            if user.get_average_rating() > highest:
                highest = user.get_average_rating()
                high_user = user
        return high_user

#### ------------- For Local Testing -----------------------
if False:
    test_emails = [
        'simon@arc',
        'simon@foo.edh',
        'simon@foo.edu',
        '.edu',
        'xxx',
        'kris.computation',
        'kris@gmail.edu',
        'kris@gmail.org',
        'simon@yoohoo@com',
        'simon@yoohoo.com',
        '',
    ]
    tome = TomeRater()
    for email in test_emails:
        print('{:>20}: {}'.format(email, tome.valid_email(email)))

if False:
    art = Fiction('Artemis', 'Andy Weir', 9876)
    print(art)

    ppr = Non_Fiction('Pocket Python Reference', 'Python Programming', 'advanced', 12345)
    print(ppr)

    tome = TomeRater()
    tome.add_user('Simon', 'simon@yoohoo.com', [art, ppr])
    tome.add_user('Kris', 'kriso@yoohoo.com')

    tome.print_catalog()
    tome.print_users()
