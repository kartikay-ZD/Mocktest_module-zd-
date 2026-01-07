import { useState } from 'react';
import CreateMock from './components/CreateMock';
import TakeMockTest from './TakeMockTest';
import './App.css'

function App() {
  const [currentMockId, setCurrentMockId] = useState(null);

  const handleMockCreated = (mockId) => {
    setCurrentMockId(mockId);
  };

  return (
    <div className="App">
      <h1>Mock Test Module</h1>
      {currentMockId ? (
        <TakeMockTest mockId={currentMockId} />
      ) : (
        <CreateMock onMockCreated={handleMockCreated} />
      )}
    </div>
  )
}

export default App
