import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

const TakeMockTest = ({ mockId }) => {
  const [mock, setMock] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // 1. Fetch Mock Details
    axios.get(`${API_URL}/mocks/${mockId}`)
      .then(res => {
        setMock(res.data);
        // 2. Start Session (assuming candidate_id=1 for demo)
        return axios.post(`${API_URL}/sessions/`, {
          candidate_id: 1,
          mock_id: mockId
    const initSession = async () => {
      try {
        // 1. Fetch Mock Details
        const mockRes = await axios.get(`${API_URL}/mocks/${mockId}`);
        setMock(mockRes.data);

        // 2. Create Session (using candidate_id 1 from seed data)
        const sessionRes = await axios.post(`${API_URL}/sessions/`, { 
          candidate_id: 1, 
          mock_id: mockId 
        });
      })
      .then(res => {
        setSessionId(res.data.id);
      })
      .catch(err => console.error("Error initializing test:", err));
        setSessionId(sessionRes.data.id);
        setLoading(false);
      } catch (err) {
        console.error("Error initializing test:", err);
        setLoading(false);
      }
    };

    if (mockId) initSession();
  }, [mockId]);

  const handleAnswerChange = (questionId, value) => {
    setAnswers(prev => ({ ...prev, [questionId]: value }));
  const handleAnswerChange = (questionId, text) => {
    setAnswers(prev => ({ ...prev, [questionId]: text }));
  };

  const handleSubmit = () => {
    if (!sessionId) return;
    
    const payload = Object.entries(answers).map(([qId, ans]) => ({
      question_id: parseInt(qId),
      candidate_answer: ans
    }));

    axios.post(`${API_URL}/sessions/${sessionId}/submit`, payload)
      .then(() => {
        setSubmitted(true);
      })
      .catch(err => console.error("Error submitting test:", err));
      .then(() => setSubmitted(true))
      .catch(err => console.error(err));
  };

  if (!mock || !sessionId) return <div>Loading Test...</div>;
  if (submitted) return <div style={{padding: 20}}><h2>Test Submitted Successfully!</h2><p>Thank you for taking the test.</p></div>;
  if (loading) return <div>Loading test environment...</div>;
  if (submitted) return <div style={{textAlign: 'center', marginTop: '50px'}}><h2>Test Submitted Successfully!</h2><p>Your responses have been recorded.</p></div>;
  if (!mock) return <div>Error loading mock test.</div>;

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto', textAlign: 'left' }}>
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px', textAlign: 'left' }}>
      <h2>{mock.name}</h2>
      <p>{mock.description}</p>
      <hr />
      {mock.questions.map((q, index) => (
        <div key={q.id} style={{ marginBottom: '20px', padding: '15px', border: '1px solid #eee', borderRadius: '5px' }}>
          <p><strong>Q{index + 1}: {q.question_text}</strong></p>
          <textarea 
            rows="4" 
            style={{ width: '100%', padding: '8px' }}
        <div key={q.id} style={{ marginBottom: '20px', padding: '15px', border: '1px solid #ddd', borderRadius: '8px' }}>
          <p><strong>Question {index + 1}:</strong> {q.question_text}</p>
          <textarea
            rows="4"
            style={{ width: '100%', padding: '8px', marginTop: '10px' }}
            placeholder="Type your answer here..."
            value={answers[q.id] || ''}
            onChange={(e) => handleAnswerChange(q.id, e.target.value)}
            onChange={e => handleAnswerChange(q.id, e.target.value)}
          />
        </div>
      ))}
      <button 
        onClick={handleSubmit}
        style={{ padding: '10px 20px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer', fontSize: '16px' }}
      >
        Submit Test
      </button>
    </div>
  );
};

export default TakeMockTest;