'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import Header from '../../components/Header';
import { useAuth } from '../../context/AuthContext';
import ProtectedRoute from '../../components/ProtectedRoute';

export default function SummaryDetailPage() {
  const params = useParams();
  const summaryId = params.id;
  const { user, token } = useAuth();
  const [summary, setSummary] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchSummary = async () => {
      if (!token) return;
      
      try {
        setIsLoading(true);
        setError('');
        
        // Fetch the summary from the API
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/process/result/${summaryId}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        if (!response.ok) {
          throw new Error('Failed to fetch summary data');
        }
        
        const data = await response.json();
        setSummary(data);
      } catch (err) {
        console.error('Error fetching summary:', err);
        setError('Failed to load summary. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchSummary();
  }, [summaryId, token]);

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50">
        <Header />
        
        <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0">
            {isLoading ? (
              <div className="flex justify-center">
                <p className="text-gray-500">Loading summary...</p>
              </div>
            ) : error ? (
              <div className="text-center py-10">
                <p className="text-red-500">{error}</p>
                <Link href="/dashboard" className="mt-4 inline-block text-indigo-600 hover:text-indigo-900">
                  Return to Dashboard
                </Link>
              </div>
            ) : summary ? (
              <div>
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <Link href="/dashboard" className="text-indigo-600 hover:text-indigo-900">
                      ← Back to Dashboard
                    </Link>
                    <h1 className="mt-2 text-2xl font-bold text-gray-900">{summary.title}</h1>
                    <div className="mt-1 flex items-center">
                      <p className="text-sm text-gray-500">
                        Created on {new Date(summary.created_at).toLocaleDateString()} • {summary.minutes_charged ? `${Math.ceil(summary.minutes_charged)} minutes` : 'Processing'}
                      </p>
                      <span className={`ml-4 px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        summary.status === 'completed' ? 'bg-green-100 text-green-800' : 
                        summary.status === 'failed' ? 'bg-red-100 text-red-800' : 
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {summary.status === 'completed' ? 'Completed' : 
                         summary.status === 'failed' ? 'Failed' : 
                         summary.status === 'processing' ? 'Processing' : 'Pending'}
                      </span>
                    </div>
                  </div>
                  <div className="flex space-x-3">
                    <button
                      type="button"
                      className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                    >
                      Export
                    </button>
                    <button
                      type="button"
                      className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                    >
                      Share
                    </button>
                  </div>
                </div>

                {summary.status === 'completed' ? (
                  <>
                    <div className="bg-white shadow overflow-hidden sm:rounded-lg mb-6">
                      <div className="px-4 py-5 sm:px-6">
                        <h2 className="text-lg font-medium text-gray-900">Summary</h2>
                        <p className="mt-1 max-w-2xl text-sm text-gray-500">
                          Processed on {new Date(summary.updated_at || summary.created_at).toLocaleString()}
                        </p>
                      </div>
                      <div className="border-t border-gray-200 px-4 py-5 sm:px-6">
                        <p className="text-gray-800">{summary.summary}</p>
                        
                        <h3 className="text-lg font-medium text-gray-900 mt-6 mb-3">Key Points</h3>
                        <ul className="list-disc pl-6 text-gray-800">
                          {summary.key_points && summary.key_points.map((point, index) => (
                            <li key={index} className="mb-1">{point}</li>
                          ))}
                        </ul>
                        
                        <h3 className="text-lg font-medium text-gray-900 mt-6 mb-3">Action Items</h3>
                        <ul className="list-disc pl-6 text-gray-800">
                          {summary.action_items && summary.action_items.map((item, index) => (
                            <li key={index} className="mb-1">{item}</li>
                          ))}
                        </ul>
                        
                        {summary.notable_quotes && summary.notable_quotes.length > 0 && (
                          <>
                            <h3 className="text-lg font-medium text-gray-900 mt-6 mb-3">Notable Quotes</h3>
                            <ul className="pl-6 text-gray-800">
                              {summary.notable_quotes.map((quote, index) => (
                                <li key={index} className="mb-3 border-l-4 border-indigo-300 pl-4 py-1 italic">
                                  "{quote}"
                                </li>
                              ))}
                            </ul>
                          </>
                        )}
                      </div>
                    </div>

                    <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                      <div className="px-4 py-5 sm:px-6 flex justify-between items-center">
                        <div>
                          <h2 className="text-lg font-medium text-gray-900">Transcript</h2>
                          <p className="mt-1 max-w-2xl text-sm text-gray-500">
                            Full meeting transcript
                          </p>
                        </div>
                        <button
                          type="button"
                          className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                        >
                          Copy
                        </button>
                      </div>
                      <div className="border-t border-gray-200 px-4 py-5 sm:px-6">
                        <pre className="whitespace-pre-wrap text-gray-800 font-mono text-sm">{summary.transcription}</pre>
                      </div>
                    </div>
                  </>
                ) : summary.status === 'failed' ? (
                  <div className="bg-white shadow overflow-hidden sm:rounded-lg p-6">
                    <h3 className="text-lg font-medium text-red-600 mb-2">Processing Failed</h3>
                    <p className="text-gray-700">{summary.error_message || 'An unknown error occurred while processing your file.'}</p>
                    <p className="mt-4 text-gray-600">Please try uploading the file again or contact support if the issue persists.</p>
                  </div>
                ) : (
                  <div className="bg-white shadow overflow-hidden sm:rounded-lg p-6">
                    <h3 className="text-lg font-medium text-yellow-600 mb-2">Processing in Progress</h3>
                    <p className="text-gray-700">Your file is currently being processed. This may take a few minutes depending on the file size.</p>
                    <p className="mt-4 text-gray-600">You can check back later or refresh the page to see the status.</p>
                  </div>
                )}
              </div>
            ) : (
              <div className="text-center py-10">
                <p className="text-gray-500">Summary not found.</p>
                <Link href="/dashboard" className="mt-4 inline-block text-indigo-600 hover:text-indigo-900">
                  Return to Dashboard
                </Link>
              </div>
            )}
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
} 