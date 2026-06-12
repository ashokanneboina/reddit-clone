import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.models import models
from app.core.security import get_password_hash

def seed_db():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(models.User).first():
        print("Database already seeded.")
        return

    # Create user
    user1 = models.User(username="demo_user", email="demo@example.com", hashed_password=get_password_hash("password"))
    user2 = models.User(username="another_user", email="another@example.com", hashed_password=get_password_hash("password"))
    db.add(user1)
    db.add(user2)
    db.commit()

    # Create subreddits
    sub1 = models.Subreddit(name="programming", description="Programming stuff", owner_id=user1.id)
    sub2 = models.Subreddit(name="reactjs", description="React stuff", owner_id=user2.id)
    db.add(sub1)
    db.add(sub2)
    db.commit()

    # Create posts
    post1 = models.Post(title="Why FastAPI is awesome", content="FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python type hints.", type="text", subreddit_id=sub1.id, author_id=user1.id)
    post2 = models.Post(title="React Server Components vs Client Components", content="Understanding the difference between the two is crucial for Next.js App Router.", type="text", subreddit_id=sub2.id, author_id=user2.id)
    post3 = models.Post(title="Hello World", content="Just testing the new Reddit clone!", type="text", subreddit_id=sub1.id, author_id=user2.id)
    
    db.add(post1)
    db.add(post2)
    db.add(post3)
    db.commit()

    print("Database seeded successfully.")

if __name__ == "__main__":
    seed_db()
