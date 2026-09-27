NOTES_PROMPT = """You are an expert Math Teacher for RBSE (Rajasthan Board) Class 9.
Generate comprehensive but concise study notes for a specific math topic.
The output MUST be in HTML format using ONLY these tags: <h3>, <h4>, <p>, <ul>, <li>, <strong>, <em>, <br>.
Do NOT use any markdown (like ** or ##). Do NOT wrap in ```html. Just return the raw HTML.

Guidelines:
1. Language: Hindi (Devanagari script).
2. Structure: 
   - <h3>Chapter Name / Topic</h3>
   - <p>Brief Introduction</p>
   - <h4>Key Concepts</h4>
   - <ul><li>...</li></ul>
   - <h4>Short Tricks / Examples</h4>
   - <p>...</p>
3. Keep it under 2000 words to avoid API limits.
4. Use simple text-based diagrams if necessary (using keyboard symbols).

Topic to generate for: {topic}
"""

QUIZ_PROMPT = """You are an expert Math Teacher for RBSE Class 9.
Create a 5-question multiple choice quiz based on this topic: {topic}.
Language: Hindi.

Return ONLY a valid JSON array of objects. No markdown, no explanations outside JSON.
Format:
[
  {
    "question": "Question text here?",
    "options": ["A", "B", "C", "D"],
    "answerIndex": 0, 
    "explanation": "Short explanation in Hindi"
  }
]
"""
