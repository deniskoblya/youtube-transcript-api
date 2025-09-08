# YouTube Transcript API

A Python Flask API for retrieving YouTube video transcripts.

## Features

- Get transcripts from YouTube videos
- Support for multiple languages
- Automatic language fallback
- CORS enabled for web applications
- Health check endpoint
- Easy deployment to Railway/Heroku

## Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/youtube-transcript-api.git
cd youtube-transcript-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### GET /
Returns API information and available endpoints.

**Response:**
```json
{
  "name": "YouTube Transcript API",
  "version": "1.0.0",
  "endpoints": {
    "/health": "Health check",
    "/transcript": "Get video transcript (params: video_id, lang)"
  },
  "example": "/transcript?video_id=dQw4w9WgXcQ&lang=ru"
}
```

### GET /health
Health check endpoint to verify API status.

**Response:**
```json
{
  "status": "ok"
}
```

### GET /transcript
Get transcript for a YouTube video.

**Parameters:**
- `video_id` (required): YouTube video ID (e.g., `dQw4w9WgXcQ`)
- `lang` (optional): Language code (default: `en`). Examples: `en`, `ru`, `es`, `fr`, `de`

**Example Request:**
```bash
curl "https://your-api.railway.app/transcript?video_id=dQw4w9WgXcQ&lang=en"
```

**Response Format:**
```json
[
  {
    "start": 0.0,
    "duration": 3.5,
    "text": "Hello and welcome to this video"
  },
  {
    "start": 3.5,
    "duration": 2.8,
    "text": "Today we're going to talk about..."
  }
]
```

**Error Response:**
```json
{
  "error": "video_id is required"
}
```

## Language Support

The API automatically tries multiple languages in the following order:
1. Requested language (via `lang` parameter)
2. English (`en`)
3. Russian (`ru`)
4. Spanish (`es`)
5. French (`fr`)
6. German (`de`)
7. Any available language (automatic selection)

If no transcript is available in any language, it returns an empty array `[]`.

## Deployment

### Deploy to Railway

1. Fork this repository
2. Go to [Railway](https://railway.app)
3. Create a new project from your GitHub repository
4. Railway will automatically detect the configuration and deploy

### Deploy to Heroku

1. Install Heroku CLI
2. Create a new Heroku app:
```bash
heroku create your-app-name
```

3. Deploy:
```bash
git push heroku main
```

### Environment Variables

No environment variables are required for basic functionality. The app uses the `PORT` environment variable if provided (automatically set by Railway/Heroku).

## Usage Examples

### JavaScript (Fetch API)
```javascript
async function getTranscript(videoId, lang = 'en') {
  const response = await fetch(`https://your-api.railway.app/transcript?video_id=${videoId}&lang=${lang}`);
  const transcript = await response.json();
  return transcript;
}

// Usage
getTranscript('dQw4w9WgXcQ', 'en')
  .then(transcript => console.log(transcript));
```

### Python (requests)
```python
import requests

def get_transcript(video_id, lang='en'):
    url = f"https://your-api.railway.app/transcript"
    params = {'video_id': video_id, 'lang': lang}
    response = requests.get(url, params=params)
    return response.json()

# Usage
transcript = get_transcript('dQw4w9WgXcQ', 'en')
print(transcript)
```

### cURL
```bash
# Get English transcript
curl "https://your-api.railway.app/transcript?video_id=dQw4w9WgXcQ&lang=en"

# Get Russian transcript
curl "https://your-api.railway.app/transcript?video_id=dQw4w9WgXcQ&lang=ru"

# Health check
curl "https://your-api.railway.app/health"
```

## Error Handling

The API handles various error scenarios:

- **Missing video_id**: Returns 400 with error message
- **Video not found**: Returns empty array `[]`
- **No transcript available**: Returns empty array `[]`
- **Server errors**: Returns 500 with error details

## Dependencies

- `youtube-transcript-api==1.2.2` - Core transcript fetching
- `flask==3.0.0` - Web framework
- `flask-cors==4.0.0` - CORS support
- `gunicorn==21.2.0` - Production WSGI server

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Limitations

- Rate limiting depends on YouTube's policies
- Some videos may not have transcripts available
- Transcript accuracy depends on YouTube's automatic captioning quality