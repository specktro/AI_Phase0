from Library import *

if __name__ == '__main__':
    book1 = Book("Ready Player One", "Ernest Cline", 2010, 300, "Sci-Fi")
    book2 = Book("1984", "George Orwell", 1984, 500, "Sci-Fi")
    book3 = Book("Fahrenheit 451", "Ray Bradbury", 1953, 350, "Sci-Fi")
    article1 = Article("Can Science Fiction Wake Us Up to Our Climate Reality?", "The New Yorker", 2020, "The New Yorker")
    article2 = Article("Sample Article", "specktro", 1990, "The New Yorker")
    pubs = [book1, book2, book3, article1, article2]
    print(sorted(pubs))

    books = [pub for pub in pubs if isinstance(pub, Book)]
    print("=== Just Books ===")
    print(books)

    author_index = {}
    for pub in pubs:
        author_index.setdefault(pub.author, []).append(pub.title)
    print("\n=== Autor → Publications ===")
    print(dict(author_index))

    print("\n=== Sci-Fi ===")
    for pub in genre_generator(pubs, "Sci-Fi"):
        print(pub)

    library = Library(pubs)
    print("\n=== Library (just valid publications) ===")
    for pub in library:
        print(pub)

    book4 = Book("Sample Title", "specktro", 2024, 500, "Sci-Fi")

    lib1 = Library([book1, book2])   # "Library created"
    lib2 = Library([book3])          # gets the same Library

    print(lib1 is lib2)              # True — they're the same object
    print(len(list(lib1)))