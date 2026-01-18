import models
from database import engine, SessionLocal
print("Creating database tables...")
models.Base.metadata.create_all(bind=engine)
print("Tables created successfully.")


def init_data():
    db = SessionLocal()
    try:
        # Check if data already exists to avoid duplicates
        if db.query(models.Book).first():
            print("Database already contains data. Skipping initialization.")
            return

        print("Inserting sample data...")

        # Sample Books
        book1 = models.Book(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            genre="Classic",
            year_published=1925,
            summary="A novel set in the Jazz Age that tells the story of Jay Gatsby's unrequited love for Daisy Buchanan."
        )

        book2 = models.Book(
            title="1984",
            author="George Orwell",
            genre="Dystopian",
            year_published=1949,
            summary="A social science fiction novel and cautionary tale about the dangers of totalitarianism."
        )

        book3 = models.Book(
            title="To Kill a Mockingbird",
            author="Harper Lee",
            genre="Classic",
            year_published=1960,
            summary="A novel about the serious issues of rape and racial inequality told through the eyes of a child."
        )

        db.add_all([book1, book2, book3])
        db.commit()

        # Refresh to get IDs for foreign keys
        db.refresh(book1)
        db.refresh(book2)

        # Sample Reviews
        review1 = models.Review(
            book_id=book1.id,
            user_id=101,
            rating=5,
            review_text="A masterpiece of American literature. The symbolism is incredible."
        )

        review2 = models.Review(
            book_id=book1.id,
            user_id=102,
            rating=4,
            review_text="Great story, but a bit slow in the middle."
        )

        review3 = models.Review(
            book_id=book2.id,
            user_id=103,
            rating=5,
            review_text="Scary how accurate this prediction of the future feels."
        )

        db.add_all([review1, review2, review3])
        db.commit()
        print("Sample data inserted successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_data()