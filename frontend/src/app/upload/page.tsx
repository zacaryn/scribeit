'use client';

import { useState, useRef, ChangeEvent, FormEvent } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

export default function UploadPage() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [title, setTitle] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const allowedFileTypes = [
    'audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/x-wav',
    'video/mp4', 'video/webm', 'audio/m4a', 'audio/x-m4a'
  ];

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const selectedFile = e.target.files[0];
      
      if (!allowedFileTypes.includes(selectedFile.type)) {
        setError('Please upload a valid audio or video file (MP3, WAV, MP4, WEBM, M4A)');
        setFile(null);
        return;
      }
      
      if (selectedFile.size > 500 * 1024 * 1024) { // 500MB limit
        setError('File size exceeds 500MB limit');
        setFile(null);
        return;
      }
      
      setError('');
      setFile(selectedFile);
      
      // Auto-fill title from filename if empty
      if (!title) {
        const fileName = selectedFile.name.replace(/\.[^/.]+$/, ""); // Remove extension
        setTitle(fileName);
      }
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const droppedFile = e.dataTransfer.files[0];
      
      if (!allowedFileTypes.includes(droppedFile.type)) {
        setError('Please upload a valid audio or video file (MP3, WAV, MP4, WEBM, M4A)');
        return;
      }
      
      if (droppedFile.size > 500 * 1024 * 1024) { // 500MB limit
        setError('File size exceeds 500MB limit');
        return;
      }
      
      setError('');
      setFile(droppedFile);
      
      // Auto-fill title from filename if empty
      if (!title) {
        const fileName = droppedFile.name.replace(/\.[^/.]+$/, ""); // Remove extension
        setTitle(fileName);
      }
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please select a file to upload');
      return;
    }
    
    if (!title.trim()) {
      setError('Please enter a title for your summary');
      return;
    }
    
    setIsUploading(true);
    setError('');
    
    // Simulate upload progress
    const progressInterval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 95) {
          clearInterval(progressInterval);
          return prev;
        }
        return prev + 5;
      });
    }, 300);
    
    try {
      // In a real application, you would upload the file to your API
      // const formData = new FormData();
      // formData.append('file', file);
      // formData.append('title', title);
      // const response = await fetch('/api/upload', {
      //   method: 'POST',
      //   body: formData,
      // });
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      clearInterval(progressInterval);
      setUploadProgress(100);
      
      // Simulate successful upload and redirect
      setTimeout(() => {
        // In a real app, you would get the summary ID from the API response
        const mockSummaryId = '123456';
        router.push(`/summary/${mockSummaryId}`);
      }, 500);
      
    } catch (error) {
      clearInterval(progressInterval);
      setIsUploading(false);
      setError('An error occurred while uploading your file. Please try again.');
      console.error('Upload error:', error);
    }
  };

  const triggerFileInput = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
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
            <h1 className="text-2xl font-bold text-gray-900">Upload Media</h1>
          </div>
          <p className="mt-2 text-gray-600">Upload an audio or video file to generate a summary</p>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          {isUploading ? (
            <div className="text-center py-8">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Uploading and Processing</h2>
              <div className="w-full bg-gray-200 rounded-full h-2.5 mb-4">
                <div 
                  className="bg-indigo-600 h-2.5 rounded-full transition-all duration-300" 
                  style={{ width: `${uploadProgress}%` }}
                ></div>
              </div>
              <p className="text-gray-600">
                {uploadProgress < 100 
                  ? 'Uploading your file...' 
                  : 'Upload complete! Redirecting to summary...'}
              </p>
            </div>
          ) : (
            <form onSubmit={handleSubmit}>
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

              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  File
                </label>
                <div
                  className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer ${
                    file ? 'border-indigo-300 bg-indigo-50' : 'border-gray-300 hover:border-indigo-300'
                  }`}
                  onDragOver={handleDragOver}
                  onDrop={handleDrop}
                  onClick={triggerFileInput}
                >
                  <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileChange}
                    className="hidden"
                    accept=".mp3,.wav,.mp4,.webm,.m4a"
                  />
                  
                  {file ? (
                    <div>
                      <svg className="w-10 h-10 mx-auto text-indigo-500 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <p className="text-sm text-gray-700 font-medium">{file.name}</p>
                      <p className="text-xs text-gray-500 mt-1">{(file.size / (1024 * 1024)).toFixed(2)} MB</p>
                      <button
                        type="button"
                        className="mt-3 text-sm text-indigo-600 hover:text-indigo-800"
                        onClick={(e) => {
                          e.stopPropagation();
                          setFile(null);
                        }}
                      >
                        Change file
                      </button>
                    </div>
                  ) : (
                    <div>
                      <svg className="w-10 h-10 mx-auto text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                      </svg>
                      <p className="text-sm text-gray-700 font-medium">Drag and drop your file here, or click to browse</p>
                      <p className="text-xs text-gray-500 mt-1">MP3, WAV, MP4, WEBM, M4A (max 500MB)</p>
                    </div>
                  )}
                </div>
              </div>

              {error && (
                <div className="mb-6 p-3 bg-red-50 text-red-700 rounded-md text-sm">
                  {error}
                </div>
              )}

              <div className="flex justify-between items-center">
                <p className="text-sm text-gray-500">
                  This will use approximately {file ? Math.ceil((file.size / (1024 * 1024 * 10)) * 5) : '0'} minutes of your quota
                </p>
                <button
                  type="submit"
                  className="bg-indigo-600 text-white px-6 py-2 rounded-md font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                  disabled={!file || isUploading}
                >
                  Upload and Process
                </button>
              </div>
            </form>
          )}
        </div>
      </main>
    </div>
  );
} 