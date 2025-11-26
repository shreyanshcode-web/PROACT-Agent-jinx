#!/usr/bin/env python
"""A simple AI agent that actually works"""

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

class SimpleAgent:
    def __init__(self):
        """Initialize the agent with Gemini API"""
        # Configure the API
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.conversation_history = []
        
    def add_system_prompt(self):
        """Add system instructions to guide the agent"""
        system_prompt = """You are Jinx, an autonomous AI engineering agent. You help with:
- Writing and debugging code
- Answering technical questions
- Creating programs and scripts
- Explaining concepts clearly

Be helpful, concise, and provide working code examples when relevant.
If you write code, format it in proper code blocks with language indicators."""
        
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
            return error_msg
    
    def display_welcome(self):
        """Display welcome message"""
        print("\n" + "="*60)
        print("🤖 JINX - Simple AI Agent")
        print("="*60)
        print("I'm here to help with coding and technical questions!")
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

async def main():
    """Main entry point"""
    agent = SimpleAgent()
    await agent.run()

if __name__ == "__main__":
    print("Starting Simple Agent...")
    asyncio.run(main())
