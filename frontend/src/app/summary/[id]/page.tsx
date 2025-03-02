'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import Header from '../../components/Header';

// Mock data for demonstration
const mockSummary = {
  id: '1',
  title: 'Marketing Team Weekly Sync',
  status: 'completed',
  source_type: 'upload',
  created_at: 'March 17, 2025',
  minutes_charged: 45,
  transcription: "John: Let's review our marketing efforts from Q1 and plan for Q2.\n\nSarah: We saw a 20% increase in social media engagement last quarter.\n\nTom: That's great! I think we should double down on that strategy.\n\nJohn: Agreed. Let's also consider the new product launch in June.\n\nSarah: I'll prepare some mockups for the campaign by Friday.\n\nTom: Perfect, and I'll schedule some user testing sessions.",
  summary_text: "The team discussed Q1 marketing results and planning for Q2. There was a 20% increase in social media engagement, which the team plans to build upon. They also discussed strategy for the upcoming product launch in June.",
  key_points: [
    "Q2 roadmap finalized with focus on user engagement features",
    "Mobile app redesign to launch in June",
    "Customer feedback shows need for improved onboarding"
  ],
  action_items: [
    "Sarah to finalize design mockups by Friday",
    "John to schedule user testing session"
  ],
  processed_on: 'March 17, 2025 at 2:35 PM'
};

export default function SummaryDetailPage() {
  const params = useParams();
  const summaryId = params.id;
  const [summary, setSummary] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // In a real app, this would fetch from your API
    setTimeout(() => {
      setSummary(mockSummary);
      setIsLoading(false);
    }, 1000);
  }, [summaryId]);

  return (
    <div className="min-h-screen bg-gray-50">
      <Header user={{ name: 'John Doe', email: 'john@example.com' }} />
      
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {isLoading ? (
            <div className="flex justify-center">
              <p className="text-gray-500">Loading summary...</p>
            </div>
          ) : (
            <div>
              <div className="flex items-center justify-between mb-6">
                <div>
                  <Link href="/dashboard" className="text-indigo-600 hover:text-indigo-900">
                    ← Back to Dashboard
                  </Link>
                  <h1 className="mt-2 text-2xl font-bold text-gray-900">{summary.title}</h1>
                  <div className="mt-1 flex items-center">
                    <p className="text-sm text-gray-500">
                      Created on {summary.created_at} • {summary.minutes_charged} minutes
                    </p>
                    {summary.status === 'completed' && (
                      <span className="ml-4 px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                        Completed
                      </span>
                    )}
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

              <div className="bg-white shadow overflow-hidden sm:rounded-lg mb-6">
                <div className="px-4 py-5 sm:px-6">
                  <h2 className="text-lg font-medium text-gray-900">Summary</h2>
                  <p className="mt-1 max-w-2xl text-sm text-gray-500">
                    Processed on {summary.processed_on}
                  </p>
                </div>
                <div className="border-t border-gray-200 px-4 py-5 sm:px-6">
                  <p className="text-gray-800">{summary.summary_text}</p>
                  
                  <h3 className="text-lg font-medium text-gray-900 mt-6 mb-3">Key Points</h3>
                  <ul className="list-disc pl-6 text-gray-800">
                    {summary.key_points.map((point, index) => (
                      <li key={index} className="mb-1">{point}</li>
                    ))}
                  </ul>
                  
                  <h3 className="text-lg font-medium text-gray-900 mt-6 mb-3">Action Items</h3>
                  <ul className="list-disc pl-6 text-gray-800">
                    {summary.action_items.map((item, index) => (
                      <li key={index} className="mb-1">{item}</li>
                    ))}
                  </ul>
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
            </div>
          )}
        </div>
      </main>
    </div>
  );
} 