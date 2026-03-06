from typing import Optional
from abc import ABC, abstractmethod

class Catalogable(ABC):
    """Abstract base class for items that can be catalogued in a library system."""

    @abstractmethod
    def catalogue(self) -> str:
        """Return a formatted citation string for this item."""
        ...

    def is_valid(self) -> bool:
        """Return True if the item has all required fields populated."""
        ...

class Publication:
    """Base class representing a published work with a title, author, and year."""

    def __init__(self, title: str, author: str, year: int):
        """
        Args:
            title: The title of the publication.
            author: The name of the author.
            year: The year the publication was released.
        """
        self.title = title
        self.author = author
        self.year = year

    @property
    def age(self) -> int:
        """Number of years since the publication was released (relative to 2025)."""
        return 2025 - self.year

    def __str__(self) -> str:
        return f"Title: {self.title}, author: {self.author}, year: {self.year}"

    def __repr__(self) -> str:
        return f"Publication(title='{self.title}', author='{self.author}', year={self.year})"

    def __eq__(self, o: object) -> bool:
        """Two publications are equal if they share the same title and author."""
        if not isinstance(o, Publication):
            return NotImplemented
        return self.title == o.title and self.author == o.author

    def __lt__(self, o: object) -> bool:
        """Publications are ordered by year, enabling sorting with sorted()."""
        if not isinstance(o, Publication):
            return NotImplemented
        return self.year < o.year

class Book(Publication, Catalogable):
    """A book publication with a page count and genre."""

    def __init__(self, title: str, author: str, year: int, pages: int, genre: str):
        """
        Args:
            title: The title of the book.
            author: The name of the author.
            year: The year the book was published.
            pages: Total number of pages.
            genre: The literary genre (e.g. "Sci-Fi", "Mystery").
        """
        super().__init__(title, author, year)
        self.pages = pages
        self.genre = genre

    def catalogue(self) -> str:
        """Return a formatted book citation string."""
        return f"[BOOK] {self.author} ({self.year}). {self.title}. {self.pages}p. Genre: {self.genre}"

    def is_valid(self) -> bool:
        """Return True if title, author, year, and page count are all valid."""
        return bool(self.title and self.author and self.year > 0 and self.pages > 0)

    def __str__(self) -> str:
        return f"{super().__str__()}, Pages: {self.pages}, Genre: {self.genre}"

    def __repr__(self) -> str:
        return f"Book(title='{self.title}', author='{self.author}', year={self.year}, pages={self.pages})"

class Article(Publication, Catalogable):
    """A magazine or journal article, optionally identified by a DOI."""

    def __init__(self, title: str, author: str, year: int, magazine: str, doi: Optional[str] = None):
        """
        Args:
            title: The title of the article.
            author: The name of the author.
            year: The year the article was published.
            magazine: The name of the magazine or journal.
            doi: Optional Digital Object Identifier for the article.
        """
        super().__init__(title, author, year)
        self.magazine = magazine
        self.doi = doi

    def catalogue(self) -> str:
        """Return a formatted article citation string, including DOI if available."""
        doi_str = f" DOI: {self.doi}" if self.doi else ""
        return f"[ARTICLE] {self.author} ({self.year}). {self.title}. {self.magazine}.{doi_str}"

    def is_valid(self) -> bool:
        """Return True if title, author, and magazine are all non-empty."""
        return bool(self.title and self.author and self.magazine)

    def __repr__(self) -> str:
        return f"Article(title='{self.title}', author='{self.author}', year={self.year})"

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    book1 = Book("Ready Player One", "Ernest Cline", 2010, 300, "Sci-Fi")
    book2 = Book("1984", "George Orwell", 1984, 500, "Sci-Fi")
    book3 = Book("Fahrenheit 451", "Ray Bradbury", 1953, 350, "Sci-Fi")
    article1 = Article("Can Science Fiction Wake Us Up to Our Climate Reality?", "The New Yorker", 2020, "The New Yorker")
    article2 = Article("Sample Article", "specktro", 1990, "The New Yorker")
    pubs = [book1, book2, book3, article1, article2]
    print(sorted(pubs))
