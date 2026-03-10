from collections.abc import Iterable
from typing import Optional
from abc import ABC, abstractmethod
from Decorators import timer, validate_year, log_access, singleton


class Catalogable(ABC):
    """Abstract base class for items that can be catalogued in a library system."""

    @abstractmethod
    def catalogue(self) -> str:
        """Return a formatted citation string for this item."""
        ...

    @abstractmethod
    def is_valid(self) -> bool:
        """Return True if the item has all required fields populated."""
        ...

class Publication:
    """Base class representing a published work with a title, author, and year."""

    @validate_year
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

    @log_access
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

    @log_access
    def catalogue(self) -> str:
        """Return a formatted article citation string, including DOI if available."""
        doi_str = f" DOI: {self.doi}" if self.doi else ""
        return f"[ARTICLE] {self.author} ({self.year}). {self.title}. {self.magazine}.{doi_str}"

    def is_valid(self) -> bool:
        """Return True if title, author, and magazine are all non-empty."""
        return bool(self.title and self.author and self.magazine)

    def __repr__(self) -> str:
        return f"Article(title='{self.title}', author='{self.author}', year={self.year})"

@timer
def genre_generator(pubs: Iterable[Publication], genre: str):
    """A generator that returns pubs from specific genre"""
    for pub in pubs:
        if isinstance(pub, Book) and pub.genre == genre:
            yield pub
@singleton
class Library:
    def __init__(self, pubs: Iterable[Publication]):
        self.pubs = pubs

    @timer
    def catalogue_all(self) -> list[str]:
        """Returns catalogue strings for all valid publications."""
        return [pub.catalogue() for pub in self if isinstance(pub, Catalogable)]

    def __iter__(self):
        for pub in self.pubs:
            if isinstance(pub, Catalogable) and pub.is_valid():
                yield pub