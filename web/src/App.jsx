import React, { useState } from 'react';
import { Slider } from '@/components/ui/slider';

const App = () => {
  const [input, setInput] = useState('');
  const [domain, setDomain] = useState('general');
  const [specialization, setSpecialization] = useState('');
  const [complexity, setComplexity] = useState(5);
  const [response, setResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    
    try {
      const res = await fetch('http://localhost:8001/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text: input, 
          domain,
          specialization,
          complexity
        }),
      });
      
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      
      const data = await res.json();
      setResponse(data.response);
    } catch (error) {
      console.error('Error:', error);
      if (error.message === 'Failed to fetch') {
        setError('Unable to connect to the API server. Please make sure the backend is running at http://localhost:8001');
      } else {
        setError(`An error occurred: ${error.message}`);
      }
      setResponse('');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="w-full max-w-3xl bg-white rounded-lg shadow-lg p-6">
        <h1 className="text-2xl font-bold text-center text-gray-900 mb-4">
          Brain Project Interface
        </h1>
        <p className="text-center text-gray-600 mb-6">
          Enter your text and customize processing parameters
        </p>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Enter your text here..."
              className="w-full h-32 px-3 py-2 text-gray-700 border rounded-lg focus:outline-none focus:border-blue-500 resize-none"
              required
            />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Domain
              </label>
              <select
                value={domain}
                onChange={(e) => setDomain(e.target.value)}
                className="w-full px-3 py-2 text-gray-700 border rounded-lg focus:outline-none focus:border-blue-500"
              >
                <option value="general">General</option>
                <option value="scientific">Scientific</option>
                <option value="creative">Creative</option>
                <option value="analytical">Analytical</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Specialization
              </label>
              <input
                type="text"
                value={specialization}
                onChange={(e) => setSpecialization(e.target.value)}
                placeholder="E.g., neuroscience, poetry, data analysis"
                className="w-full px-3 py-2 text-gray-700 border rounded-lg focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Response Complexity: {complexity}/10
            </label>
            <Slider
              value={[complexity]}
              onValueChange={(value) => setComplexity(value[0])}
              min={1}
              max={10}
              step={1}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>Concise</span>
              <span>Complex</span>
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
          >
            {isLoading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing...
              </span>
            ) : 'Process Text'}
          </button>
        </form>

        {error && (
          <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        )}

        {response && (
          <div className="mt-6 pt-6 border-t">
            <h3 className="font-medium text-gray-900 mb-2">Response:</h3>
            <div className="bg-gray-50 p-4 rounded-lg">
              <pre className="whitespace-pre-wrap break-words text-sm text-gray-700">
                {response}
              </pre>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;