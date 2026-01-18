import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List

import models, schemas, ai_service
from database import engine, get_db, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Intelligent Book Manager")


# 1. POST /books: Add a new book
@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    # Generate initial summary based on title/author
    summary_text = ai_service.summarize_book_details(book.title, book.author)
    book.summary = summary_text
    # Note: Using 'summary' to match models.py (corrected from 'content_summary')
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


# 2. GET /books: Retrieve all books
@app.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Book).offset(skip).limit(limit).all()


# 3. GET /books/<id>: Retrieve a specific book by its ID
@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


# 4. PUT /books/<id>: Update a book's information by its ID
@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book_update: schemas.BookUpdate, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Update only fields that are provided
    update_data = book_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


# 5. DELETE /books/<id>: Delete a book by its ID
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}


# 6. POST /books/<id>/reviews: Add a review for a book
@app.post("/books/{book_id}/reviews", response_model=schemas.Review)
def create_review(book_id: int, review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db_review = models.Review(**review.dict(), book_id=book_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


# 7. GET /books/<id>/reviews: Retrieve all reviews for a book
@app.get("/books/{book_id}/reviews", response_model=List[schemas.Review])
def read_book_reviews(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.reviews


# 8. GET /books/<id>/summary: Get a summary and aggregated rating for a book
@app.get("/books/{book_id}/summary", response_model=schemas.BookSummaryResponse)
def get_book_summary_stats(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Calculate aggregated rating
    reviews = book.reviews
    avg_rating = 0.0
    if reviews:
        total_score = sum(r.rating for r in reviews)
        avg_rating = total_score / len(reviews)

    return {
        "id": book.id,
        "title": book.title,
        # Corrected: database field is 'summary', not 'content_summary'
        "summary": book.summary,
        "aggregated_rating": avg_rating,
        "review_count": len(reviews)
    }


# 9. GET /recommendations: Get book recommendations based on user preferences
@app.get("/recommendations")
def get_recommendations(preferences: str):
    # Using GET with query param usually requires URL encoding on client side
    recommendations = ai_service.recommend_books(preferences)
    return {"recommendations": recommendations}


# 10. POST /generate-summary: Generate a summary for a given book content
@app.post("/generate-summary")
def generate_summary_from_content(payload: schemas.TextContent):
    """
    Accepts raw text content and uses AI to generate a summary.
    This is useful if you are uploading the text of a book not yet in the DB.
    """
    summary = ai_service.summarize_text(payload.content)
    return {"summary": summary}


if __name__ == "__main__":
    # Allows running the server directly via Python script
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)