#!/usr/bin/env python
"""Jinx Agent - Gemini API Version"""

from __future__ import annotations

import os
import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
from datetime import datetime

class GeminiJinxAgent:
    def __init__(self):
        """Initialize the agent with Gemini API"""
        # Configure the API
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ Error: GEMINI_API_KEY not found in environment variables")
            print("Please set GEMINI_API_KEY in your .env file")
            sys.exit(1)
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.conversation_history = []
        
    def add_system_prompt(self):
        """Add system instructions to guide the agent"""
        system_prompt = """You are Jinx, an autonomous AI engineering agent specialized in web development and programming.

Your capabilities include:
- Creating HTML, CSS, and JavaScript files
- Building landing pages and e-commerce sites
- Writing clean, production-ready code
- Debugging and fixing code issues
- Providing technical explanations

When creating code:
1. Always provide complete, working code
2. Use proper HTML5 structure
3. Include responsive design with CSS
4. Add comments for clarity
5. Make it visually appealing and professional

Be helpful, concise, and provide practical solutions."""
        
        self.conversation_history.append({"role": "system", "content": system_prompt})
    
    async def chat(self, user_input):
        """Process user input and generate response"""
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Build conversation context
        context = ""
        for msg in self.conversation_history:
            if msg["role"] == "system":
                context += f"System: {msg['content']}\n\n"
            elif msg["role"] == "user":
                context += f"User: {msg['content']}\n\n"
            elif msg["role"] == "assistant":
                context += f"Assistant: {msg['content']}\n\n"
        
        try:
            # Generate response
            response = self.model.generate_content(context)
            assistant_response = response.text
            
            # Add to history
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            # Keep only last 10 messages to avoid context limit
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return assistant_response
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            if "429" in str(e):
                error_msg = "Rate limit exceeded. Please wait a moment before trying again."
            elif "403" in str(e) or "401" in str(e):
                error_msg = "API key issue. Please check your GEMINI_API_KEY."
            return error_msg
    
    def display_welcome(self):
        """Display welcome message"""
        print("\n" + "="*60)
        print("🤖 JINX - Gemini-Powered AI Agent")
        print("="*60)
        print("I'm here to help with web development, coding, and technical questions!")
        print("Type 'quit' or 'exit' to end the conversation.")
        print("-"*60)
    
    async def run(self):
        """Run the interactive agent"""
        self.display_welcome()
        self.add_system_prompt()
        
        while True:
            try:
                # Get user input
                user_input = input("\n💬 You: ").strip()
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                # Show typing indicator
                print("\n🤖 Jinx: ", end="", flush=True)
                
                # Generate and display response
                response = await self.chat(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

def _run() -> int:
    """Execute the agent runtime.

    Returns
    -------
    int
        Process exit code. ``0`` on success, non-zero on handled errors.
    """
    try:
        agent = GeminiJinxAgent()
        asyncio.run(agent.run())
        return 0
    except KeyboardInterrupt:
        # Graceful shutdown on Ctrl+C
        return 130  # Conventional exit code for SIGINT
    except Exception as exc:  # pragma: no cover - safety net
        # Last-resort guard to avoid silent crashes.
        print(f"Fatal error: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(_run())
