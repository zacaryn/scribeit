'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Header from '../components/Header';

export default function DashboardPage() {
  const [summaries, setSummaries] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [stats, setStats] = useState({
    tier: 'Pro',
    minutesUsed: 120,
    minutesTotal: 400
  });

  useEffect(() => {
    // In a real app, this would fetch from your API
    setTimeout(() => {
      setSummaries([
        {
          id: '1',
          title: 'Marketing Team Weekly Sync',
          status: 'completed',
          created_at: 'March 17, 2025',
          source_type: 'upload',
          minutes_charged: 45
        },
        {
          id: '2',
          title: 'Product Planning Session',
          status: 'completed',
          created_at: 'April 3, 2025',
          source_type: 'youtube',
          minutes_charged: 32
        },
        {
          id: '3',
          title: 'Quarterly Review Meeting',
          status: 'completed',
          created_at: 'May 12, 2025',
          source_type: 'upload',
          minutes_charged: 58
        },
        {
          id: '4',
          title: 'Customer Feedback Discussion',
          status: 'processing',
          created_at: 'June 1, 2025',
          source_type: 'upload',
          minutes_charged: null
        },
        {
          id: '5',
          title: 'Executive Team Standup',
          status: 'completed',
          created_at: 'June 5, 2025',
          source_type: 'youtube',
          minutes_charged: 15
        }
      ]);
      setIsLoading(false);
    }, 1000);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <Header user={{ name: 'John Doe', email: 'john@example.com' }} />
      
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="mb-8 bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Your Usage</h2>
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center">
              <div>
                <p className="text-gray-600">Current Plan: <span className="font-medium">{stats.tier}</span></p>
                <p className="text-gray-600">Minutes Used: <span className="font-medium">{stats.minutesUsed} / {stats.minutesTotal}</span></p>
              </div>
              <div className="mt-4 sm:mt-0">
                <span className="inline-flex rounded-md shadow-sm">
                  <button
                    type="button"
                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-500"
                  >
                    Upgrade Plan
                  </button>
                </span>
              </div>
            </div>
            <div className="mt-4 w-full h-2 bg-gray-200 rounded-full overflow-hidden">
              <div 
                className="h-full bg-indigo-600 rounded-full"
                style={{ width: `${(stats.minutesUsed / stats.minutesTotal) * 100}%` }}
              ></div>
            </div>
            <p className="mt-2 text-sm text-gray-500">Current billing period: June 1, 2025 - June 30, 2025</p>
          </div>
          
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <div className="flex justify-between items-center p-6 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900">Your Summaries</h2>
              <div className="flex space-x-4">
                <Link 
                  href="/upload"
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-500"
                >
                  Upload File
                </Link>
                <Link 
                  href="/youtube"
                  className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                >
                  YouTube Link
                </Link>
              </div>
            </div>
            
            {isLoading ? (
              <div className="p-6 flex justify-center">
                <p className="text-gray-500">Loading your summaries...</p>
              </div>
            ) : summaries.length === 0 ? (
              <div className="p-6 text-center">
                <p className="text-gray-500 mb-4">You don't have any summaries yet</p>
                <p className="text-gray-500">Upload a recording or provide a YouTube link to get started</p>
              </div>
            ) : (
              <div>
                <ul className="divide-y divide-gray-200">
                  {summaries.map((summary) => (
                    <li key={summary.id} className="hover:bg-gray-50">
                      <Link href={`/summary/${summary.id}`} className="block">
                        <div className="px-6 py-4">
                          <div className="flex items-center justify-between">
                            <p className="text-sm font-medium text-indigo-600 truncate">
                              {summary.title}
                            </p>
                            <div className="ml-2 flex-shrink-0 flex">
                              {summary.status === 'completed' ? (
                                <p className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                                  Completed
                                </p>
                              ) : summary.status === 'processing' ? (
                                <p className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">
                                  Processing
                                </p>
                              ) : (
                                <p className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                                  Failed
                                </p>
                              )}
                            </div>
                          </div>
                          <div className="mt-2 flex justify-between">
                            <div className="sm:flex">
                              <p className="flex items-center text-sm text-gray-500">
                                {summary.source_type === 'upload' ? (
                                  <svg className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                    <path fillRule="evenodd" d="M8 4a3 3 0 00-3 3v4a5 5 0 0010 0V7a1 1 0 112 0v4a7 7 0 11-14 0V7a5 5 0 0110 0v4a3 3 0 11-6 0V7a1 1 0 012 0v4a1 1 0 102 0V7a3 3 0 00-3-3z" clipRule="evenodd" />
                                  </svg>
                                ) : (
                                  <svg className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z" />
                                  </svg>
                                )}
                                {summary.source_type === 'upload' ? 'Uploaded File' : 'YouTube Video'}
                              </p>
                              <p className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0 sm:ml-6">
                                <svg className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                  <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd" />
                                </svg>
                                {summary.created_at}
                              </p>
                            </div>
                            {summary.minutes_charged && (
                              <p className="text-sm text-gray-500">{summary.minutes_charged} mins</p>
                            )}
                          </div>
                        </div>
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
} 