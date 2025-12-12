// src/App.jsx
import React, { useState, useEffect } from 'react';
import './App.css'; 

const API_BASE_URL = 'http://127.0.0.1:5000/api'; // Sesuaikan dengan port Flask Anda

function App() {
  const [reviewText, setReviewText] = useState('');
  const [currentResult, setCurrentResult] = useState(null);
  const [allReviews, setAllReviews] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // Fetch semua review saat komponen dimuat
  useEffect(() => {
    fetchReviews();
  }, []);

  const fetchReviews = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/reviews`);
      if (!response.ok) throw new Error('Failed to fetch reviews');
      const data = await response.json();
      setAllReviews(data.reverse()); // Tampilkan yang terbaru di atas
    } catch (err) {
      setError(`Error fetching: ${err.message}`);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setCurrentResult(null);
    if (!reviewText.trim()) return;

    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/analyze-review`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ review: reviewText }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Server responded with an error');
      }

      const data = await response.json();
      setCurrentResult(data.result);
      setReviewText('');
      fetchReviews(); // Refresh daftar setelah berhasil
    } catch (err) {
      setError(`Analysis Error: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Product Review Analyzer 🤖</h1>

      {/* Form Input */}
      <form onSubmit={handleSubmit} className="review-form">
        <textarea
          value={reviewText}
          onChange={(e) => setReviewText(e.target.value)}
          placeholder="Masukkan ulasan produk di sini..."
          rows="5"
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Menganalisis...' : 'Analisis Ulasan'}
        </button>
      </form>

      {/* Error & Loading States */}
      {error && <p className="error-message">Error: {error}</p>}

      {/* Hasil Analisis Terbaru */}
      {currentResult && (
        <div className="current-result">
          <h2>Hasil Analisis Terbaru</h2>
          <div className={`sentiment-badge ${currentResult.sentiment.toLowerCase()}`}>
            Sentimen: {currentResult.sentiment}
          </div>
          <p><strong>Poin Kunci:</strong> {currentResult.key_points}</p>
          <p>Ulasan Asli: <em>"{currentResult.original_review}"</em></p>
        </div>
      )}

      {/* Display Semua Hasil */}
      <div className="results-history">
        <h2>Riwayat Analisis ({allReviews.length})</h2>
        {allReviews.length === 0 && !isLoading && <p>Belum ada riwayat analisis.</p>}

        {allReviews.map((item) => (
          <div key={item.id} className="review-card">
            <div className={`sentiment-badge ${item.sentiment.toLowerCase()}`}>
              {item.sentiment}
            </div>
            <p><strong>Poin Kunci:</strong> {item.key_points}</p>
            <p className="original-text">Ulasan Asli: <em>"{item.original_review.substring(0, 100)}..."</em></p>
            <small>Disimpan: {new Date(item.timestamp).toLocaleString()}</small>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;