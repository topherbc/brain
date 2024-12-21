import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Loader2 } from "lucide-react";

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
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle className="text-2xl font-bold text-center text-gray-900">Brain Project Interface</CardTitle>
            <CardDescription className="text-center text-gray-600">
              Enter your text and select a domain for processing
            </CardDescription>
          </CardHeader>
          
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <Textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Enter your text here..."
                  className="h-32 resize-none"
                  required
                />
              </div>
              
              <div className="space-y-2">
                <Select value={domain} onValueChange={setDomain}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select a domain" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="general">General</SelectItem>
                    <SelectItem value="scientific">Scientific</SelectItem>
                    <SelectItem value="creative">Creative</SelectItem>
                    <SelectItem value="analytical">Analytical</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Button 
                type="submit" 
                className="w-full"
                disabled={isLoading}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Processing...
                  </>
                ) : (
                  'Process Text'
                )}
              </Button>
            </form>
          </CardContent>

          {response && (
            <CardFooter className="border-t">
              <div className="w-full space-y-2">
                <h3 className="font-medium text-gray-900">Response:</h3>
                <div className="bg-white p-4 rounded-md border">
                  <pre className="whitespace-pre-wrap break-words text-sm">
                    {response}
                  </pre>
                </div>
              </div>
            </CardFooter>
          )}
        </Card>
      </div>
    </div>
  );
};

export default App;