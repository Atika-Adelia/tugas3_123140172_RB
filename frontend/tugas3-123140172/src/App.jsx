import { useState, useEffect } from 'react'
import './App.css' 

function App() {
  const [review, setReview] = useState('')
  const [result, setResult] = useState(null)
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const fetchHistory = async () => {

    try {
      const response = await fetch('http://localhost:5000/api/reviews');
      if (!response.ok) throw new Error('Gagal mengambil riwayat');
      const data = await response.json();
      setHistory(data);
    } catch (err) {
      console.error("Error fetching history:", err);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleAnalyze = async () => {
    if (!review.trim()) {
        setError("Mohon masukkan teks ulasan.");
        return;
    }
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:5000/api/analyze-review', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ review }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Terjadi kesalahan saat analisis');
      }

      setResult(data.result);
      setReview(''); 
      fetchHistory(); 
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  const ResultCard = ({ data, title }) => (
    <div className="result-card">
        {title && <h3>{title}</h3>}
        <div className="result-item">
            <span className="label">Sentimen</span>
            <div className="value">{data.sentiment}</div>
        </div>
        <div className="result-item">
            <span className="label">Poin Kunci</span>
            <div className="value">{data.key_points}</div>
        </div>
        <div className="result-item">
            <span className="label">Ulasan Asli</span>
            <div className="value original-review">"{data.original_review}"</div>
        </div>
        {data.timestamp && (
            <small style={{ color: 'var(--text-muted)' }}>
                Disimpan: {new Date(data.timestamp).toLocaleString()}
            </small>
        )}
    </div>
  );

  return (
    <div className="app-container">
      <h1>Product Review Analyzer 🤖</h1>

      <div className="input-section">
        <textarea
          value={review}
          onChange={(e) => setReview(e.target.value)}
          placeholder="Masukkan ulasan produk di sini... Contoh: Barangnya bagus banget, pengiriman cepat!"
          disabled={loading}
        />
        <button 
            className="analyze-button" 
            onClick={handleAnalyze} 
            disabled={loading || !review.trim()}
        >
          {loading ? 'Menganalisis...' : 'Analisis Ulasan'}
        </button>
      </div>

      {error && <div className="error-message">Error: {error}</div>}

      {result && <ResultCard data={result} title="Hasil Analisis Terbaru" />}

      <h2>Riwayat Analisis ({history.length})</h2>
      {history.length === 0 ? (
        <p style={{ color: 'var(--text-muted)', marginTop: '2rem' }}>Belum ada riwayat analisis.</p>
      ) : (
        <ul className="history-list">
          {history.map((item) => (
            <li key={item.id}>
              <ResultCard data={item} />
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default App