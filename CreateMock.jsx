import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

const CreateMock = ({ onMockCreated }) => {
  const [techStacks, setTechStacks] = useState([]);
  const [selectedStacks, setSelectedStacks] = useState(new Set());
  const [mockName, setMockName] = useState('');
  const [numQuestions, setNumQuestions] = useState(10);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    // Fetch available tech stacks from the backend
    axios.get(`${API_URL}/tech-stacks/`)
      .then(response => {
        setTechStacks(response.data);
      })
      .catch(err => {
        console.error("Error fetching tech stacks:", err);
        setError('Failed to load tech stacks. Please ensure the backend is running.');
      });
  }, []);

  const handleStackToggle = (stackId) => {
    const newSelection = new Set(selectedStacks);
    if (newSelection.has(stackId)) {
      newSelection.delete(stackId);
    } else {
      newSelection.add(stackId);
    }
    setSelectedStacks(newSelection);
  };

  const handleGenerateMock = () => {
    if (!mockName.trim()) {
      setError('Please provide a name for the mock test.');
      return;
    }
    if (selectedStacks.size === 0) {
      setError('Please select at least one tech stack.');
      return;
    }

    setIsLoading(true);
    setError('');

    const payload = {
      name: mockName,
      tech_stack_ids: Array.from(selectedStacks),
      num_questions: numQuestions,
    };

    axios.post(`${API_URL}/mocks/generate`, payload)
      .then(response => {
        console.log('Mock created:', response.data);
        // Pass the created mock's ID to the parent component
        if (onMockCreated) {
          onMockCreated(response.data.id);
        }
      })
      .catch(err => {
        console.error("Error generating mock:", err);
        setError('Failed to generate mock test. Please try again.');
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  return (
    <div className="create-mock-container" style={{ padding: '20px', maxWidth: '600px', margin: '0 auto', textAlign: 'left' }}>
      <h2>Create New Mock Test</h2>
      
      {error && <div style={{ color: 'red', marginBottom: '10px', padding: '10px', backgroundColor: '#ffe6e6', borderRadius: '4px' }}>{error}</div>}

      <div style={{ marginBottom: '20px' }}>
        <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>Mock Test Name:</label>
        <input
          type="text"
          value={mockName}
          onChange={(e) => setMockName(e.target.value)}
          placeholder="e.g., Full Stack Developer Assessment"
          style={{ width: '100%', padding: '10px', borderRadius: '4px', border: '1px solid #ccc' }}
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>Select Tech Stacks:</label>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
          {techStacks.length > 0 ? (
            techStacks.map(stack => (
              <button
                key={stack.id}
                onClick={() => handleStackToggle(stack.id)}
                style={{
                  padding: '8px 16px',
                  borderRadius: '20px',
                  border: selectedStacks.has(stack.id) ? '1px solid #007bff' : '1px solid #ccc',
                  backgroundColor: selectedStacks.has(stack.id) ? '#007bff' : '#f8f9fa',
                  color: selectedStacks.has(stack.id) ? 'white' : '#333',
                  cursor: 'pointer',
                  transition: 'all 0.2s'
                }}
              >
                {stack.name}
              </button>
            ))
          ) : (
            <p style={{ color: '#666' }}>Loading tech stacks...</p>
          )}
        </div>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>Number of Questions:</label>
        <input
          type="number"
          min="1"
          max="50"
          value={numQuestions}
          onChange={(e) => setNumQuestions(parseInt(e.target.value) || 10)}
          style={{ width: '100%', padding: '10px', borderRadius: '4px', border: '1px solid #ccc' }}
        />
      </div>

      <button
        onClick={handleGenerateMock}
        disabled={isLoading}
        style={{
          padding: '12px 24px',
          backgroundColor: isLoading ? '#6c757d' : '#28a745',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: isLoading ? 'not-allowed' : 'pointer',
          fontSize: '16px',
          fontWeight: 'bold',
          width: '100%'
        }}
      >
        {isLoading ? 'Generating...' : 'Generate Mock Test'}
      </button>
    </div>
  );
};

export default CreateMock;