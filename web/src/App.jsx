import React, { useState } from 'react';

const App = () => {
  const [input, setInput] = useState('');
  const [domain, setDomain] = useState('general');
  const [response, setResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const res = await fetch('http://localhost:8000/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: input, domain }),
      });
      const data = await res.json();
      setResponse(data.response);
    } catch (error) {
      console.error('Error:', error);
      setResponse('An error occurred while processing your request.');
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
          Enter your text and select a domain for processing
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
          
          <div>
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

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Processing...' : 'Process Text'}
          </button>
        </form>

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