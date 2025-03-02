'use client';

import Link from 'next/link';
import Image from 'next/image';

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Header navigation with fixed alignment */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center">
              <Link href="/" className="flex-shrink-0">
                <h1 className="text-3xl font-bold text-indigo-600">ScribeIt</h1>
              </Link>
              <div className="mx-4 h-6 border-l border-gray-300"></div>
              <nav className="hidden md:ml-2 md:flex md:space-x-8">
                <Link href="/pricing" className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900">
                  Pricing
                </Link>
                <Link href="/blog" className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-700 hover:text-gray-900">
                  Blog
                </Link>
                <Link href="/about" className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-700 hover:text-gray-900">
                  About
                </Link>
              </nav>
            </div>
            
            {/* Fixed alignment for auth buttons */}
            <div className="flex items-center space-x-4">
              <Link 
                href="/login" 
                className="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-indigo-600 bg-white hover:bg-gray-50"
              >
                Login
              </Link>
              <Link 
                href="/register" 
                className="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
              >
                Sign up
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero section */}
      <section className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 flex flex-col md:flex-row items-center">
          <div className="md:w-1/2 mb-8 md:mb-0">
            <h2 className="text-4xl font-bold mb-4">Transform Your Meetings with AI</h2>
            <p className="text-xl mb-6">
              Automatically transcribe, summarize, and extract action items from your meetings.
              Save time and never miss important details again.
            </p>
            <div className="flex space-x-4">
              <Link 
                href="/register" 
                className="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-indigo-700 bg-white hover:bg-gray-50"
              >
                Get Started Free
              </Link>
              <Link 
                href="/dashboard/demo" 
                className="inline-flex items-center justify-center px-5 py-3 border border-white text-base font-medium rounded-md text-white hover:bg-indigo-500"
              >
                See Demo
              </Link>
            </div>
          </div>
          <div className="md:w-1/2 flex justify-center">
            <div className="w-full max-w-md bg-white rounded-xl shadow-2xl overflow-hidden transform transition-all duration-300 hover:scale-[1.02] text-sm">
              {/* Card header with more details - condensed */}
              <div className="p-3 bg-gradient-to-r from-indigo-600 to-indigo-700 text-white">
                <div className="flex justify-between items-center">
                  <h3 className="font-semibold">Weekly Team Sync - Summary</h3>
                  <span className="text-xs bg-indigo-500 px-2 py-0.5 rounded-full">45 min</span>
                </div>
                <div className="flex items-center text-xs space-x-2 text-indigo-100 mt-1">
                  <span>March 15, 2025</span>
                  <span>•</span>
                  <span>8 participants</span>
                  <span>•</span>
                  <span className="flex items-center">
                    <svg className="w-3 h-3 mr-0.5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                    </svg>
                    Processed in 2m
                  </span>
                </div>
              </div>
              
              {/* Card body with improved styling - condensed */}
              <div className="p-4 bg-white text-gray-800">
                <div className="grid grid-cols-12 gap-3">
                  {/* Summary section - condensed */}
                  <div className="col-span-12 mb-3 pb-3 border-b border-gray-100">
                    <div className="flex items-start">
                      <div className="p-1 rounded-md bg-blue-50 mr-2 mt-0.5 flex-shrink-0">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4 text-blue-500">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" />
                        </svg>
                      </div>
                      <div>
                        <h4 className="font-medium text-gray-900 mb-0.5 text-xs">SUMMARY</h4>
                        <p className="text-gray-600 text-xs">Team discussed Q2 marketing strategy with focus on social media campaigns and budget allocation for upcoming launch.</p>
                      </div>
                    </div>
                  </div>
                  
                  {/* Key points section - condensed */}
                  <div className="col-span-6 pr-2">
                    <div className="flex items-start mb-1">
                      <div className="p-1 rounded-md bg-amber-50 mr-2 flex-shrink-0">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4 text-amber-500">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M12 18v-5.25m0 0a6.01 6.01 0 001.5-.189m-1.5.189a6.01 6.01 0 01-1.5-.189m3.75 7.478a12.06 12.06 0 01-4.5 0m3.75 2.383a14.406 14.406 0 01-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 10-7.517 0c.85.493 1.509 1.333 1.509 2.316V18" />
                        </svg>
                      </div>
                      <h4 className="font-medium text-gray-900 text-xs">KEY POINTS</h4>
                    </div>
                    <ul className="list-disc pl-6 text-gray-600 space-y-0.5 text-xs">
                      <li>Q2 roadmap finalized</li>
                      <li>Mobile app redesign - June</li>
                      <li>Improved onboarding needed</li>
                    </ul>
                  </div>
                  
                  {/* Action items section - condensed */}
                  <div className="col-span-6 pl-2 border-l border-gray-100">
                    <div className="flex items-start mb-1">
                      <div className="p-1 rounded-md bg-green-50 mr-2 flex-shrink-0">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4 text-green-500">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                      <h4 className="font-medium text-gray-900 text-xs">ACTION ITEMS</h4>
                    </div>
                    <ul className="text-gray-600 space-y-1 text-xs pl-2">
                      {["S", "J", "M"].map((initial, index) => (
                        <li key={index} className="flex items-center">
                          <div className="w-5 h-5 rounded-full bg-gradient-to-r from-indigo-400 to-purple-400 flex items-center justify-center text-white text-xs mr-1.5 flex-shrink-0">
                            {initial}
                          </div>
                          <span>{index === 0 ? "Design mockups by Fri" : 
                                 index === 1 ? "Schedule user testing" :
                                 "Create content calendar"}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
              
              {/* Card footer - condensed */}
              <div className="px-4 py-2 bg-gray-50 border-t border-gray-100 flex justify-between items-center text-xs">
                <span className="text-gray-500">Generated by ScribeIt</span>
                <div className="flex space-x-1">
                  <button className="px-1.5 py-0.5 bg-white rounded border border-gray-200 text-gray-600 hover:bg-gray-50">Share</button>
                  <button className="px-1.5 py-0.5 bg-indigo-50 rounded border border-indigo-100 text-indigo-600 hover:bg-indigo-100">Transcript</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How it works section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-900">How It Works</h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2 text-gray-900">1. Upload Recording</h3>
              <p className="text-gray-800">
                Upload your meeting recording or provide a YouTube link. We support various audio and video formats.
              </p>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2 text-gray-900">2. AI Processing</h3>
              <p className="text-gray-800">
                Our AI transcribes the audio and analyzes the content to identify key points and action items.
              </p>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25zM6.75 12h.008v.008H6.75V12zm0 3h.008v.008H6.75V15zm0 3h.008v.008H6.75V18z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2 text-gray-900">3. Get Summary</h3>
              <p className="text-gray-800">
                Receive a concise summary with key discussion points and a list of action items within minutes.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing section with improved styling */}
      <section className="py-20 bg-gradient-to-b from-white to-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 sm:text-4xl">Simple, Transparent Pricing</h2>
            <p className="mt-4 text-xl text-gray-600 max-w-3xl mx-auto">
              Choose the plan that's right for you and start saving time with AI-powered meeting summaries.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {/* Free tier */}
            <div className="bg-white rounded-xl shadow-lg p-8 border border-gray-100 hover:border-gray-200 hover:shadow-xl transition-all duration-300">
              <h3 className="text-xl font-bold text-gray-900">Free</h3>
              <p className="mt-2 text-3xl font-extrabold text-gray-900">$0</p>
              <p className="text-gray-700 mt-1">For occasional use</p>
              
              <ul className="mt-8 space-y-4">
                <li className="flex items-start">
                  <span className="flex-shrink-0 text-green-500">
                    <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </span>
                  <span className="ml-3 text-gray-700">100 minutes per month</span>
                </li>
                <li className="flex items-start">
                  <span className="flex-shrink-0 text-green-500">
                    <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </span>
                  <span className="ml-3 text-gray-700">Basic summaries</span>
                </li>
                <li className="flex items-start">
                  <span className="flex-shrink-0 text-green-500">
                    <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </span>
                  <span className="ml-3 text-gray-700">Text export</span>
                </li>
              </ul>
              
              <div className="mt-8">
                <Link 
                  href="/register" 
                  className="block w-full px-4 py-3 bg-white border border-indigo-600 rounded-lg text-indigo-600 text-center font-medium hover:bg-indigo-50 transition-colors duration-200"
                >
                  Sign up
                </Link>
              </div>
            </div>
            
            {/* Pro tier */}
            <div className="bg-white rounded-xl shadow-xl p-8 border-2 border-indigo-500 relative transform hover:scale-105 transition-all duration-300">
              <div className="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-indigo-600 text-white px-6 py-1 rounded-full text-sm font-bold">
                MOST POPULAR
              </div>
              <h3 className="text-xl font-bold text-gray-900">Pro</h3>
              <p className="mt-2 text-3xl font-extrabold text-gray-900">$9.99</p>
              <p className="text-gray-700 mt-1">Per month</p>
              
              <ul className="mt-8 space-y-4">
                <li className="flex items-start">
                  <span className="flex-shrink-0 text-green-500">
                    <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </span>
                  <span className="ml-3 text-gray-700">400 minutes per month</span>
                </li>
                <li className="flex items-start">
                  <span className="flex-shrink-0 text-green-500">
                    <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </span>
                  <span className="ml-3 text-gray-700">Advanced summaries</span>
                </li>
                <li className="flex items-start">
                  <span className="flex-shrink-0 text-green-500">
                    <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </span>
                  <span className="ml-3 text-gray-700">All export options</span>
                </li>
                <li className="flex items-start">
                  <span className="flex-shrink-0 text-green-500">
                    <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </span>
                  <span className="ml-3 text-gray-700">Priority processing</span>
                </li>
              </ul>
              
              <div className="mt-8">
                <Link 
                  href="/register" 
                  className="block w-full px-4 py-3 bg-indigo-600 rounded-lg text-white text-center font-medium hover:bg-indigo-700 transition-colors duration-200"
                >
                  Get started
                </Link>
              </div>
            </div>
            
            {/* Enterprise tier */}
            <div className="bg-white rounded-xl shadow-lg p-8 border border-gray-100 hover:border-gray-200 hover:shadow-xl transition-all duration-300">
              <h3 className="text-xl font-bold text-gray-900">Enterprise</h3>
              <p className="mt-2 text-3xl font-extrabold text-gray-900">$99</p>
              <p className="text-gray-700 mt-1">Per month</p>
              
              <ul className="mt-8 space-y-4">
                <li className="flex items-start">
                  <span className="flex-shrink-0 text-green-500">
                    <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </span>
                  <span className="ml-3 text-gray-700">1,500 minutes per month</span>
                </li>
                <li className="flex items-start">
                  <span className="flex-shrink-0 text-green-500">
                    <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </span>
                  <span className="ml-3 text-gray-700">Premium summaries</span>
                </li>
                <li className="flex items-start">
                  <span className="flex-shrink-0 text-green-500">
                    <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </span>
                  <span className="ml-3 text-gray-700">All export options</span>
                </li>
                <li className="flex items-start">
                  <span className="flex-shrink-0 text-green-500">
                    <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </span>
                  <span className="ml-3 text-gray-700">Team sharing</span>
                </li>
                <li className="flex items-start">
                  <span className="flex-shrink-0 text-green-500">
                    <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </span>
                  <span className="ml-3 text-gray-700">API access</span>
                </li>
              </ul>
              
              <div className="mt-8">
                <Link 
                  href="/register" 
                  className="block w-full px-4 py-3 bg-white border border-indigo-600 rounded-lg text-indigo-600 text-center font-medium hover:bg-indigo-50 transition-colors duration-200"
                >
                  Contact sales
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer section */}
      <footer className="bg-gray-800 text-gray-300 py-12 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <h3 className="text-3xl font-bold mb-4">ScribeIt</h3>
              <p className="text-gray-400">
                Transform your meetings with AI-powered transcription and summarization.
              </p>
            </div>
            <div>
              <h3 className="text-xl font-bold mb-4">Quick Links</h3>
              <ul className="space-y-2">
                <li><Link href="/dashboard" className="hover:text-white transition-colors">Dashboard</Link></li>
                <li><Link href="/login" className="hover:text-white transition-colors">Login</Link></li>
                <li><Link href="/register" className="hover:text-white transition-colors">Register</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="text-xl font-bold mb-4">Contact</h3>
              <p className="text-gray-400">
                Have questions? Contact our support team.
              </p>
              <a href="mailto:contact@scribeit.pro" className="text-indigo-400 hover:text-indigo-300 transition-colors">
                contact@scribeit.pro
              </a>
            </div>
          </div>
          <div className="border-t border-gray-700 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p>© 2025 ScribeIt. All rights reserved.</p>
            <p className="mt-4 md:mt-0">
              Created by <a href="https://hh6influential.com/" target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:text-indigo-300 transition-colors">HH6 Influential</a>
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
