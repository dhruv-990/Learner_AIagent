# API Keys Setup Guide

This application now supports multiple AI providers. You can choose between Google Gemini Pro and Perplexity Pro.

## Option 1: Google Gemini Pro (Recommended)

1. **Get Google API Key:**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy the generated API key

2. **Set Environment Variable:**
   ```bash
   # Windows (PowerShell)
   $env:GOOGLE_API_KEY="your_google_api_key_here"
   
   # Windows (Command Prompt)
   set GOOGLE_API_KEY=your_google_api_key_here
   
   # Linux/Mac
   export GOOGLE_API_KEY="your_google_api_key_here"
   ```

3. **Create .env file:**
   Create a `.env` file in the project root with:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Option 2: Perplexity Pro

1. **Get Perplexity API Key:**
   - Go to [Perplexity API](https://www.perplexity.ai/settings/api)
   - Sign in to your Perplexity Pro account
   - Generate a new API key
   - Copy the generated API key

2. **Set Environment Variable:**
   ```bash
   # Windows (PowerShell)
   $env:PERPLEXITY_API_KEY="your_perplexity_api_key_here"
   
   # Windows (Command Prompt)
   set PERPLEXITY_API_KEY=your_perplexity_api_key_here
   
   # Linux/Mac
   export PERPLEXITY_API_KEY="your_perplexity_api_key_here"
   ```

3. **Create .env file:**
   Create a `.env` file in the project root with:
   ```
   PERPLEXITY_API_KEY=your_perplexity_api_key_here
   ```

## Switching Between Providers

To switch between AI providers, modify the `main.py` file:

```python
# For Google Gemini Pro
ai_service = AIService(provider="gemini")

# For Perplexity Pro
ai_service = AIService(provider="perplexity")
```

## Additional API Keys (Optional)

### YouTube API (for enhanced video recommendations)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3
4. Create credentials (API Key)
5. Set environment variable: `YOUTUBE_API_KEY=your_youtube_api_key`

### Notion API (for storing learning paths)
1. Go to [Notion Developers](https://developers.notion.com/)
2. Create a new integration
3. Get the integration token
4. Set environment variable: `NOTION_TOKEN=your_notion_token`
5. Set environment variable: `NOTION_DATABASE_ID=your_database_id`

## Complete .env Example

```env
# AI Provider (choose one)
GOOGLE_API_KEY=your_google_api_key_here
# OR
PERPLEXITY_API_KEY=your_perplexity_api_key_here

# Optional APIs
YOUTUBE_API_KEY=your_youtube_api_key_here
NOTION_TOKEN=your_notion_token_here
NOTION_DATABASE_ID=your_notion_database_id_here
```

## Installation

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your API keys as described above

3. Run the application:
   ```bash
   python main.py
   ```

## Troubleshooting

- **"API key not found"**: Make sure you've set the correct environment variable for your chosen provider
- **"Invalid API key"**: Verify your API key is correct and has the necessary permissions
- **Rate limiting**: Both providers have rate limits. If you hit them, wait a moment and try again
- **JSON parsing errors**: The AI responses are parsed as JSON. If you get parsing errors, the AI might not be returning valid JSON format

## Cost Comparison

- **Google Gemini Pro**: Free tier available, then pay-per-use
- **Perplexity Pro**: Requires Perplexity Pro subscription ($20/month), then pay-per-use for API calls

Both providers offer competitive pricing compared to OpenAI's GPT-4. 