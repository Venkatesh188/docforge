#!/usr/bin/env python3
"""
DocForge Startup Script - Open Source Edition

Easy startup script that checks requirements and launches DocForge with
helpful guidance for first-time users.
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ DocForge requires Python 3.8 or higher")
        print(f"   You have Python {sys.version_info.major}.{sys.version_info.minor}")
        print("   Please upgrade Python and try again")
        return False
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'crewai',
        'openai', 
        'pydantic',
        'dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required dependencies:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n🛠️  To install dependencies, run:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def check_openai_key():
    """Check if OpenAI API key is configured"""
    # Check environment variable
    if os.getenv('OPENAI_API_KEY'):
        return True
    
    # Check .env file
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
            if 'OPENAI_API_KEY=' in content and 'your_openai_api_key_here' not in content:
                return True
    
    return False

def show_welcome():
    """Show welcome message and basic usage"""
    print("""
🚀 DocForge - Open Source AI Documentation Generator
═══════════════════════════════════════════════════════

Generate professional software documentation from simple ideas!

📋 Quick Commands:
   Generate docs:     python docforge.py generate "Your project idea"
   List projects:     python docforge.py list-projects  
   Check status:      python docforge.py status project-name
   Available docs:    python docforge.py list-docs

📁 Your documents will be saved to: ./generated-docs/

═══════════════════════════════════════════════════════
""")

def main():
    """Main startup routine"""
    print("🔍 DocForge Startup Check...")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    print("✅ Python version compatible")
    
    # Check if we're in the right directory
    if not Path('docforge.py').exists():
        print("❌ docforge.py not found in current directory")
        print("   Make sure you're in the DocForge root directory")
        sys.exit(1)
    print("✅ DocForge files found")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    print("✅ Dependencies installed")
    
    # Check OpenAI configuration
    if not check_openai_key():
        print("⚠️  OpenAI API key not configured")
        print("\n🛠️  Setup steps:")
        print("1. Run: python docforge.py init")
        print("2. Edit .env file with your OpenAI API key")
        print("3. Get your key from: https://platform.openai.com/api-keys")
        print("\nThen run this script again!")
        sys.exit(1)
    print("✅ OpenAI API key configured")
    
    print("\n🎉 DocForge is ready!")
    show_welcome()
    
    # Ask user what they want to do
    while True:
        print("What would you like to do?")
        print("1. Generate documentation from an idea")
        print("2. List existing projects")
        print("3. View available document types")
        print("4. Exit")
        
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                idea = input("\n💡 Enter your project idea: ").strip()
                if idea:
                    print(f"\n🚀 Generating documentation for: {idea}")
                    subprocess.run([sys.executable, 'docforge.py', 'generate', idea])
                else:
                    print("❌ Please enter a valid project idea")
                continue
                
            elif choice == '2':
                print("\n📁 Listing projects...")
                subprocess.run([sys.executable, 'docforge.py', 'list-projects'])
                continue
                
            elif choice == '3':
                print("\n📋 Available document types...")
                subprocess.run([sys.executable, 'docforge.py', 'list-docs'])
                continue
                
            elif choice == '4':
                print("\n👋 Thanks for using DocForge!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4")
                continue
                
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for using DocForge!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            continue

if __name__ == "__main__":
    main()