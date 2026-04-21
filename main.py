```python
import os
import time
import json
import google.generativeai as genai
from datetime import datetime

# --- CONFIGURATION ---
# The environment provides the key, but we ensure we check for it.
API_KEY = os.environ.get("GOOGLE_API_KEY", "")
genai.configure(api_key=API_KEY)

class ViralYTArchitect:
    def __init__(self):
        self.model_name = "gemini-2.5-flash-preview-09-2025"
        self.output_dir = "data"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def call_gemini_with_backoff(self, prompt, system_instruction):
        """Implements exponential backoff for API reliability."""
        retries = 5
        for i in range(retries):
            try:
                model = genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=system_instruction
                )
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                if i == retries - 1:
                    print(f"\n[Error] Final retry failed: {e}")
                    return None
                wait_time = 2**i
                print(f"[Warning] API busy. Retrying in {wait_time}s...")
                time.sleep(wait_time)
        return None

    def generate_strategy(self, topic):
        print(f"\n🚀 Architecting viral strategy for: '{topic}'...")
        
        system_prompt = (
            "You are a World-Class YouTube Strategist. Your goal is to maximize CTR and retention. "
            "Output your response in a clear, professional format."
        )
        
        user_prompt = f"""
        Create a comprehensive YouTube production plan for the topic: "{topic}".
        
        Requirements:
        1. THREE HIGH-CTR TITLES: Use psychological triggers (curiosity, fear of missing out, or extreme value).
        2. VIRAL SCRIPT STRUCTURE:
           - Hook (First 30 seconds to stop the scroll)
           - Body (Key points with high pacing)
           - Outro/CTA (Strong reason to subscribe)
        3. FIVE AI IMAGE PROMPTS: Detailed prompts for Midjourney/DALL-E to create thumbnails or cinematic B-roll.
        
        Format the output clearly with headers.
        """

        content = self.call_gemini_with_backoff(user_prompt, system_prompt)
        return content

    def save_to_file(self, topic, content):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"strategy_{timestamp}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"YOUTUBE STRATEGY: {topic.upper()}\n")
            f.write("="*40 + "\n\n")
            f.write(content)
        
        return filepath

def main():
    print("========================================")
    print("   🎬 VIRAL-YT-ARCHITECT by Hammad Virk")
    print("========================================")
    
    if not API_KEY:
        print("[!] Error: GOOGLE_API_KEY not found in environment.")
        return

    architect = ViralYTArchitect()
    
    topic = input("\nEnter your Video Topic/Idea: ").strip()
    if not topic:
        print("Topic cannot be empty!")
        return

    result = architect.generate_strategy(topic)
    
    if result:
        print("\n" + "="*20 + " GENERATED CONTENT " + "="*20)
        print(result)
        print("="*59)
        
        path = architect.save_to_file(topic, result)
        print(f"\n✅ Strategy saved successfully to: {path}")
    else:
        print("\n[!] Failed to generate content. Please check your connection or API limits.")

if __name__ == "__main__":
    main()

```
      
