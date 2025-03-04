# ScribeIt

ScribeIt is a SaaS platform that uses AI to transcribe and summarize audio/video content from meetings, lectures, and videos. It provides structured notes, key takeaways, and action items to help users save time and extract valuable insights.

## Features

- **AI Transcription**: Convert audio/video to text using OpenAI Whisper
- **Smart Summarization**: Generate concise summaries, key points, and action items
- **File Upload Support**: Process MP3, MP4, WAV, M4A, and WEBM files
- **YouTube Integration**: Process videos directly from YouTube URLs
- **Speaker Differentiation**: Identify different speakers in the conversation
- **User Dashboard**: Track past summaries and usage limits
- **Export Options**: Save as PDF or Google Docs
- **Mobile Responsive**: Access from any device

## Subscription Tiers

- **Free Tier**: 30 minutes of processing per month
- **Basic Plan**: 300 minutes per month ($9.99)
- **Pro Plan**: 1,000 minutes per month ($19.99)
- **One-Time Credits**: Purchase additional minutes as needed

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Next.js (React)
- **Database**: PostgreSQL
- **Storage**: AWS S3
- **AI APIs**: OpenAI (Whisper for transcription, GPT for summarization)
- **Payments**: Stripe
- **Deployment**: Vercel (frontend), Render or DigitalOcean (backend)

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL
- AWS Account (for S3)
- OpenAI API Key
- Stripe Account (for payments)

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables by copying `.env.example` to `.env` and filling in your values:
   ```
   cp .env.example .env
   ```

4. Run database migrations:
   ```
   alembic upgrade head
   ```

5. Start the backend server:
   ```
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Set up environment variables by copying `.env.local.example` to `.env.local` and filling in your values:
   ```
   cp .env.local.example .env.local
   ```

4. Start the development server:
   ```
   npm run dev
   ```

## API Documentation

Once the backend is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

This project is licensed under the GPL License - see the LICENSE file for details. 
