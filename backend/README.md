## Gemini API Integration

1. Install new dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file in the `backend/` directory with the following content:
   ```env
   GEMINI_API_KEY=your-gemini-api-key-here
   ```
   Replace `your-gemini-api-key-here` with your actual Gemini API key.

3. The backend exposes a new endpoint `/gemini-answer` that accepts a POST request with a JSON body `{ "prompt": "your question" }` and returns the Gemini model's answer. 