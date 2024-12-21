# Brain Project Setup Guide

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

## Installation

### 1. Backend Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: .\venv\Scripts\activate
```

2. Install the backend dependencies:
```bash
pip install -r api_requirements.txt
```

3. Set up your environment variables:
Create a `.env` file in the project root with:
```env
OPENAI_API_KEY=your_api_key_here
VERBOSE=True
```

### 2. Frontend Setup

1. Navigate to the web directory:
```bash
cd web
```

2. Install frontend dependencies:
```bash
npm install
# or if using yarn:
yarn install
```

3. Install shadcn/ui components:
```bash
npx shadcn-ui@latest init

# Install required components
npx shadcn-ui@latest add card
npx shadcn-ui@latest add button
npx shadcn-ui@latest add input
npx shadcn-ui@latest add textarea
npx shadcn-ui@latest add alert
```

## Running the Application

### 1. Start the Backend Server

1. Activate the virtual environment if not already active:
```bash
source venv/bin/activate  # On Windows, use: .\venv\Scripts\activate
```

2. Start the FastAPI server:
```bash
cd api
python main.py
```

The backend server will start at http://localhost:8000

### 2. Start the Frontend Development Server

1. In a new terminal, navigate to the web directory:
```bash
cd web
```

2. Start the Vite development server:
```bash
npm run dev
# or if using yarn:
yarn dev
```

The frontend will be available at http://localhost:5173

## Development Notes

- The backend server runs on port 8000 and provides the REST API
- The frontend development server runs on port 5173 with hot-reload enabled
- API requests from the frontend are automatically proxied to the backend
- Both servers support auto-reload during development

## Deployment

For production deployment:

1. Build the frontend:
```bash
cd web
npm run build
# or if using yarn:
yarn build
```

2. Configure the backend:
- Update CORS settings in `api/main.py` to match your production domain
- Set up proper security measures and environment variables
- Use a production-grade ASGI server like Gunicorn with Uvicorn workers

## Troubleshooting

1. If you see CORS errors:
   - Ensure both servers are running
   - Check that the backend CORS settings match your frontend URL
   - Clear browser cache and reload

2. If components are missing:
   - Ensure all shadcn/ui components are installed
   - Check the component import paths

3. If the API is unreachable:
   - Verify the backend server is running
   - Check the proxy settings in `vite.config.js`
   - Ensure the API endpoint URLs are correct