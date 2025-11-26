#!/usr/bin/env python
"""Fast AI Agent - Optimized for Quick Code Generation"""

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

class FastAgent:
    def __init__(self):
        """Initialize the agent with Gemini API"""
        # Configure the API
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ Error: GEMINI_API_KEY not found")
            print("Please set GEMINI_API_KEY in your .env file")
            sys.exit(1)
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
    def get_system_prompt(self, task_type):
        """Get optimized system prompt based on task type"""
        prompts = {
            "portfolio": """You are a web development expert. Create a complete, professional portfolio website with:
- Modern, responsive design
- Hero section with call-to-action
- About section
- Projects showcase
- Skills section
- Contact form
- Smooth animations
- Professional styling

Provide complete HTML with embedded CSS and JavaScript. Make it visually impressive.""",
            
            "ecommerce": """You are an e-commerce web development expert. Create a complete e-commerce landing page with:
- Hero section with product showcase
- Features/benefits section
- Product categories
- Customer testimonials
- Pricing section
- Call-to-action buttons
- Professional, conversion-focused design

Provide complete HTML with embedded CSS and JavaScript.""",
            
            "landing": """You are a landing page specialist. Create a high-converting landing page with:
- Compelling hero section
- Value proposition
- Features/benefits
- Social proof/testimonials
- Clear call-to-action
- Modern, professional design

Provide complete HTML with embedded CSS and JavaScript.""",
            
            "default": """You are a full-stack web developer. Create high-quality, modern web applications with:
- Clean, semantic HTML5
- Responsive CSS3 styling
- Interactive JavaScript
- Best practices and accessibility
- Professional appearance

Provide complete, working code with explanations when needed."""
        }
        
        return prompts.get(task_type.lower(), prompts["default"])
    
    async def generate_code(self, user_input):
        """Generate code quickly without conversation history"""
        # Determine task type
        task_type = "default"
        if "portfolio" in user_input.lower():
            task_type = "portfolio"
        elif "ecommerce" in user_input.lower() or "e-commerce" in user_input.lower():
            task_type = "ecommerce"
        elif "landing" in user_input.lower():
            task_type = "landing"
        
        # Build prompt
        system_prompt = self.get_system_prompt(task_type)
        full_prompt = f"{system_prompt}\n\nUser Request: {user_input}\n\nGenerate the complete code:"
        
        try:
            # Generate response with shorter timeout
            response = self.model.generate_content(
                full_prompt,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 4000,
                }
            )
            
            return response.text
            
        except Exception as e:
            if "429" in str(e):
                return "⚠️ Rate limit exceeded. Please wait a moment and try again."
            elif "403" in str(e) or "401" in str(e):
                return "❌ API key issue. Please check your GEMINI_API_KEY."
            else:
                return f"❌ Error: {str(e)}"
    
    def display_welcome(self):
        """Display welcome message"""
        print("\n" + "="*60)
        print("⚡ FAST AI AGENT - Quick Code Generation")
        print("="*60)
        print("I generate complete websites and code instantly!")
        print("Specializes in: Portfolio sites, E-commerce, Landing pages")
        print("Type 'quit' to exit. No waiting, just results!")
        print("-"*60)
    
    async def run(self):
        """Run the fast agent"""
        self.display_welcome()
        
        while True:
            try:
                # Get user input
                user_input = input("\n💬 What would you like to create? ").strip()
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                # Show working indicator
                print("\n⚡ Generating...", end="", flush=True)
                
                # Generate response
                response = await self.generate_code(user_input)
                
                # Clear line and show response
                print("\r" + " " * 20 + "\r", end="")
                print("\n🤖 Here's your code:")
                print("="*50)
                print(response)
                print("="*50)
                
                # Ask if user wants to save
                save = input("\n💾 Save to file? (y/n): ").strip().lower()
                if save == 'y':
                    filename = input("📁 Filename (e.g., index.html): ").strip()
                    if not filename:
                        filename = "index.html"
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(response)
                    print(f"✅ Saved to {filename}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

def main():
    """Main entry point"""
    agent = FastAgent()
    asyncio.run(agent.run())

if __name__ == "__main__":
    main()
