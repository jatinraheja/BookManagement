from pydantic import BaseModel
from typing import List, Optional

# --- Review Schemas ---
class ReviewBase(BaseModel):
    user_id: int
    review_text: str
    rating: int

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    book_id: int
    class Config:
        orm_mode = True

# --- Book Schemas ---
class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    year_published: Optional[int] = None
    summary: Optional[str] = None

class Book(BookBase):
    id: int
    reviews: List[Review] = []
    class Config:
        orm_mode = True

# --- Utility / Extra Schemas ---

class BookSummaryResponse(BaseModel):
    id: int
    title: str
    summary: Optional[str]
    aggregated_rating: float
    review_count: int

class TextContent(BaseModel):
    content: str