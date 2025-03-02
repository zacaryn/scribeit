'use client';

import { useState, FormEvent } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

export default function YouTubePage() {
  const router = useRouter();
  const [url, setUrl] = useState('');
  const [title, setTitle] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    
    // Validate the URL
    if (!url.trim()) {
      setError('Please enter a YouTube URL');
      return;
    }
    
    // Simple YouTube URL validation
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$/;
    if (!youtubeRegex.test(url)) {
      setError('Please enter a valid YouTube URL');
      return;
    }
    
    if (!title.trim()) {
      setError('Please enter a title for your summary');
      return;
    }
    
    setIsProcessing(true);
    setError('');
    
    try {
      // In a real application, you would call your API
      // const response = await fetch('/api/youtube/process', {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json',
      //   },
      //   body: JSON.stringify({ url, title }),
      // });
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Simulate successful processing and redirect
      // In a real app, you would get the summary ID from the API response
      const mockSummaryId = '789012';
      router.push(`/summary/${mockSummaryId}`);
      
    } catch (error) {
      setIsProcessing(false);
      setError('An error occurred while processing your YouTube video. Please try again.');
      console.error('Processing error:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center">
            <Link href="/" className="text-2xl font-bold text-indigo-600">Meeting.AI</Link>
          </div>
          <nav className="flex space-x-8 items-center">
            <Link href="/dashboard" className="text-gray-600 hover:text-gray-900">Dashboard</Link>
            <Link href="/account" className="text-gray-600 hover:text-gray-900">Account</Link>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="mb-8">
          <div className="flex items-center">
            <Link href="/dashboard" className="text-indigo-600 hover:text-indigo-800 mr-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
            </Link>
            <h1 className="text-2xl font-bold text-gray-900">Process YouTube Video</h1>
          </div>
          <p className="mt-2 text-gray-600">Enter a YouTube URL to generate a summary</p>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          {isProcessing ? (
            <div className="text-center py-8">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Processing YouTube Video</h2>
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
              <p className="text-gray-600">
                This may take a few minutes depending on the video length...
              </p>
            </div>
          ) : (
            <form onSubmit={handleSubmit}>
              <div className="mb-6">
                <label htmlFor="youtube-url" className="block text-sm font-medium text-gray-700 mb-1">
                  YouTube URL
                </label>
                <input
                  type="text"
                  id="youtube-url"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="https://www.youtube.com/watch?v=..."
                />
              </div>

              <div className="mb-6">
                <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
                  Title
                </label>
                <input
                  type="text"
                  id="title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="Enter a title for your summary"
                />
              </div>

              {error && (
                <div className="mb-6 p-3 bg-red-50 text-red-700 rounded-md text-sm">
                  {error}
                </div>
              )}

              <div className="mb-6">
                <div className="bg-gray-50 p-4 rounded-md border border-gray-200">
                  <h3 className="text-sm font-medium text-gray-700 mb-2">Note:</h3>
                  <p className="text-sm text-gray-600">
                    This will process approximately 5 minutes of your quota per 10 minutes of video.
                    Only the audio portion will be processed for summaries.
                  </p>
                </div>
              </div>

              <div className="flex justify-end">
                <button
                  type="submit"
                  className="bg-indigo-600 text-white px-6 py-2 rounded-md font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                  disabled={isProcessing}
                >
                  Process Video
                </button>
              </div>
            </form>
          )}
        </div>
      </main>
    </div>
  );
} 