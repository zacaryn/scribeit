'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

type HeaderProps = {
  user?: {
    name: string;
    email: string;
  };
};

export default function Header({ user }: HeaderProps) {
  const pathname = usePathname();
  
  const isActive = (path: string) => {
    return pathname === path;
  };
  
  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
        <div className="flex items-center">
          <Link href="/" className="text-3xl font-bold text-indigo-600">ScribeIt</Link>
          <div className="mx-4 h-6 border-l border-gray-300"></div>
        </div>
        <nav className="flex space-x-8 items-center">
          <Link 
            href="/dashboard" 
            className={`${isActive('/dashboard') ? 'text-gray-900 font-medium' : 'text-gray-600 hover:text-gray-900'}`}
          >
            Dashboard
          </Link>
          <Link 
            href="/upload" 
            className="text-gray-600 hover:text-gray-900"
          >
            Upload
          </Link>
          <Link 
            href="/youtube" 
            className="text-gray-600 hover:text-gray-900"
          >
            YouTube
          </Link>
          
          {user ? (
            <div className="relative">
              <button className="flex items-center text-gray-600 hover:text-gray-900">
                <span className="mr-2">{user.name}</span>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
            </div>
          ) : (
            <Link 
              href="/login" 
              className="bg-indigo-600 text-white px-4 py-2 rounded-md font-medium hover:bg-indigo-700"
            >
              Login
            </Link>
          )}
        </nav>
      </div>
    </header>
  );
} 