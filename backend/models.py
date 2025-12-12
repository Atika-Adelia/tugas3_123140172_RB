from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ReviewResult(Base):
    __tablename__ = 'review_results'

    id = Column(Integer, primary_key=True)
    original_review = Column(Text, nullable=False)
    sentiment = Column(String(50), nullable=False)
    key_points = Column(Text) 
    timestamp = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "original_review": self.original_review,
            "sentiment": self.sentiment,
            "key_points": self.key_points,
            "timestamp": self.timestamp.isoformat()
        }