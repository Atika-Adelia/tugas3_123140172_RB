import os
from dotenv import load_dotenv  
from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, ReviewResult
from analyzer import analyze_review

load_dotenv()

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise ValueError("DATABASE_URL tidak ditemukan! Pastikan file .env sudah benar.")

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

@app.route('/api/analyze-review', methods=['POST'])
def analyze_new_review():
    try:
        data = request.get_json()
        review = data.get('review')
        if not review:
            return jsonify({"error": "Review text is required"}), 400

        # Panggil fungsi analisis
        sentiment, key_points = analyze_review(review)
        
        # Simpan ke Database
        session = Session()
        new_result = ReviewResult(
            original_review=review,
            sentiment=sentiment,
            key_points=key_points 
        )
        session.add(new_result)
        session.commit()

        return jsonify({
            "message": "Analysis successful and saved",
            "result": new_result.to_dict()
        }), 201

    except Exception as e:
        # Error handling
        print(f"Error during analysis or save: {e}")
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

@app.route('/api/reviews', methods=['GET'])
def get_all_reviews():
    session = Session()
    try:
        reviews = session.query(ReviewResult).order_by(ReviewResult.id.desc()).all()
        results = [review.to_dict() for review in reviews]
        return jsonify(results), 200
    except Exception as e:
        print(f"Error fetching reviews: {e}")
        return jsonify({"error": "Failed to fetch reviews"}), 500
    finally:
        session.close()


if __name__ == '__main__':
    app.run(debug=True, port=5000)