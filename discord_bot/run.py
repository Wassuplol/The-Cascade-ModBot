#!/usr/bin/env python3
"""
Simple startup script for the Discord bot
"""
import os
import sys
import subprocess

def install_requirements():
    """Install required packages from requirements.txt"""
    print("Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully!")
    except subprocess.CalledProcessError:
        print("Failed to install requirements!")
        sys.exit(1)

def check_env_file():
    """Check if .env file exists and has proper values"""
    if not os.path.exists('.env'):
        print("Creating .env file...")
        with open('.env', 'w') as f:
            f.write("DISCORD_TOKEN=your_discord_bot_token_here\nBOT_PREFIX=!\n")
        print("Please edit the .env file with your bot token!")
        return False
    return True

def main():
    print("Discord Bot Startup Script")
    print("=" * 30)
    
    # Check if requirements are installed
    install_requirements()
    
    # Check if .env file exists
    env_exists = check_env_file()
    
    if not env_exists:
        print("Setup complete! Please edit the .env file with your bot token and then run 'python main.py'")
        return
    
    # Run the bot
    print("Starting the bot...")
    try:
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()