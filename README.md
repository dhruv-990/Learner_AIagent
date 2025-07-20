# Learning Path Mentor Bot

An AI-powered learning companion that creates personalized study plans with YouTube videos, GitHub projects, and adaptive recommendations based on your progress.

## 🚀 Features

### Core Functionality
- **Personalized Learning Paths**: Create customized study plans for any topic (Web3, DevOps, Machine Learning, etc.)
- **YouTube Integration**: Curated educational videos from top creators
- **GitHub Projects**: Hands-on coding projects and examples
- **Progress Tracking**: Monitor your learning journey with detailed progress updates
- **Adaptive Recommendations**: AI-powered suggestions based on your progress and challenges

### Tech Stack
- **Backend**: FastAPI (Python)
- **AI**: Google Gemini Pro or Perplexity Pro for learning path generation and recommendations
- **APIs**: YouTube API, GitHub API, Notion API
- **Frontend**: HTML/CSS/JavaScript with Tailwind CSS
- **Storage**: Notion database with local JSON fallback

### Unique Twist
The bot evaluates your weekly progress and adapts the learning plan accordingly, providing personalized recommendations and adjusting the curriculum based on your challenges and achievements.

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd learning-path-mentor-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory with your API keys:

```env
# AI Provider (choose one)
GOOGLE_API_KEY=your_google_api_key_here
# OR
PERPLEXITY_API_KEY=your_perplexity_api_key_here

# YouTube API Configuration (Optional)
YOUTUBE_API_KEY=your_youtube_api_key_here

# Notion API Configuration (Optional)
NOTION_API_KEY=your_notion_api_key_here
NOTION_DATABASE_ID=your_notion_database_id_here

# Application Configuration
APP_NAME=Learning Path Mentor Bot
DEBUG=True
```

### 4. API Key Setup

#### Google Gemini Pro (Recommended)
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key
5. Add it to your `.env` file

#### Perplexity Pro (Alternative)
1. Go to [Perplexity API](https://www.perplexity.ai/settings/api)
2. Sign in to your Perplexity Pro account
3. Generate a new API key
4. Add it to your `.env` file

#### YouTube API Key (Optional)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3
4. Create credentials (API Key)
5. Add it to your `.env` file

#### Notion API Key (Optional)
1. Visit [Notion Developers](https://developers.notion.com/)
2. Create a new integration
3. Get your API key
4. Create a database and share it with your integration
5. Add both API key and database ID to your `.env` file

### 5. Test Your Setup
```bash
python test_ai_service.py
```

### 6. Run the Application
```bash
python main.py
```

The application will be available at `http://localhost:8000`

## 📖 Usage Guide

### Creating a Learning Path

1. **Visit the Home Page**: Navigate to `http://localhost:8000`
2. **Enter Your Topic**: Choose what you want to learn (e.g., "Web3", "DevOps", "Machine Learning")
3. **Set Your Profile**:
   - Experience Level: Beginner, Intermediate, or Advanced
   - Time Commitment: How many hours per week you can dedicate
   - Learning Goals: Specific skills you want to acquire (optional)
4. **Generate Path**: Click "Create My Learning Path"
5. **Review Plan**: The AI will generate a personalized study plan with:
   - Weekly goals and objectives
   - YouTube video recommendations
   - GitHub project suggestions
   - Estimated time commitments
   - Deadlines for each week

### Tracking Progress

1. **Access Dashboard**: Click "Dashboard" in the header or visit `/progress-dashboard`
2. **Search Your Path**: Enter your learning topic to find your existing path
3. **Update Progress**: 
   - List completed items
   - Describe your current progress
   - Mention any challenges faced
4. **Get Recommendations**: Click "Get Recommendations" for AI-powered suggestions
5. **View History**: See your progress history and patterns

### Features Breakdown

#### YouTube Integration
- Automatically searches for educational videos related to your topic
- Filters for high-quality, relevant content
- Provides video duration, view count, and ratings
- Direct links to YouTube videos

#### GitHub Projects
- Finds relevant open-source projects
- Includes project descriptions and statistics
- Links to practical coding examples
- Sorted by popularity and relevance

#### Adaptive AI Recommendations
- Analyzes your progress patterns
- Provides personalized suggestions
- Addresses specific challenges
- Adjusts difficulty based on your level

#### Progress Tracking
- Weekly progress updates
- Completion tracking
- Challenge documentation
- Progress visualization

## 🏗️ Project Structure

```
learning-path-mentor-bot/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── API_KEYS_GUIDE.md      # Detailed API setup instructions
├── test_ai_service.py     # Test script for AI services
├── README.md              # This file
├── models/
│   └── learning_path.py   # Pydantic models for data structures
├── services/
│   ├── ai_service.py      # AI service (Gemini/Perplexity)
│   ├── youtube_service.py # YouTube API integration
│   ├── notion_service.py  # Notion API integration
│   └── learning_path_service.py # Main business logic
├── templates/
│   ├── index.html         # Home page template
│   └── dashboard.html     # Progress dashboard template
└── data/
    └── learning_paths/    # Local storage for learning paths
```

## 🔧 API Endpoints

### Core Endpoints
- `GET /` - Home page with learning path creation form
- `POST /create-learning-path` - Create a new learning path
- `GET /learning-path/{topic}` - Retrieve existing learning path
- `POST /update-progress` - Update progress and get recommendations
- `GET /progress-dashboard` - Progress tracking dashboard

### Resource Endpoints
- `GET /youtube-resources/{topic}` - Get YouTube videos for a topic
- `GET /github-projects/{topic}` - Get GitHub projects for a topic

## 🎯 Example Use Cases

### Web3 Learning Path
1. Enter "Web3" as your topic
2. Set experience level to "Beginner"
3. Choose "5-10 hours per week"
4. Add goal: "Build a simple dApp"
5. Get a 6-week plan with:
   - Week 1: Blockchain fundamentals
   - Week 2: Smart contracts basics
   - Week 3: Web3 development tools
   - Week 4: Building your first dApp
   - Week 5: DeFi concepts
   - Week 6: Advanced Web3 topics

### DevOps Learning Path
1. Enter "DevOps" as your topic
2. Set experience level to "Intermediate"
3. Choose "10-20 hours per week"
4. Add goal: "Master CI/CD pipelines"
5. Get an 8-week plan with practical projects and tools

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production Deployment
1. Set up a production server (AWS, Google Cloud, etc.)
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables
4. Use a production WSGI server like Gunicorn:
   ```bash
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:
1. Check that all API keys are properly configured
2. Ensure all dependencies are installed
3. Verify your internet connection for API calls
4. Check the console for error messages
5. Run `python test_ai_service.py` to test your AI service setup

## 🔮 Future Enhancements

- [ ] Mobile app version
- [ ] Integration with learning platforms (Coursera, Udemy)
- [ ] Social learning features
- [ ] Gamification elements
- [ ] Advanced analytics and insights
- [ ] Multi-language support
- [ ] Integration with calendar apps
- [ ] Email notifications and reminders 