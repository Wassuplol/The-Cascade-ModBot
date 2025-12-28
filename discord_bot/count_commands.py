#!/usr/bin/env python3
"""
Script to count the total number of commands in the bot
"""
import os
import re

def count_commands_in_file(file_path):
    """Count the number of commands in a given file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # For cogs, count functions that are decorated with @commands.command, @commands.command(name=...), etc.
    if 'cogs' in file_path:
        # Find all @commands.command decorators followed by async def function_name
        # This pattern matches @commands.command with optional parameters, possibly with intermediate decorators, followed by async def
        # Pattern: @commands.command(...) followed by any number of lines with decorators, then async def function_name
        cog_command_pattern = r'@commands\.command(?:\s*\(\s*[^\)]*\))?\s*\n(?:\s*@\w+(?:\.\w+)*\s*\n)*\s*async def (\w+)'
        cog_commands = re.findall(cog_command_pattern, content, re.MULTILINE)
        
        # Also look for patterns like @bot.command or other variations
        alt_command_pattern = r'@\w+\.command(?:\s*\(\s*[^\)]*\))?\s*\n(?:\s*@\w+(?:\.\w+)*\s*\n)*\s*async def (\w+)'
        alt_commands = re.findall(alt_command_pattern, content, re.MULTILINE)
        
        # Remove duplicates and return total
        all_commands = list(set(cog_commands + alt_commands))
        return len(all_commands)
    
    # For non-cog files, use the original method
    command_pattern = r'@commands\.command'
    commands = len(re.findall(command_pattern, content))
    
    bot_command_pattern = r'@.*?\.command'
    bot_commands = len(re.findall(bot_command_pattern, content, re.MULTILINE))
    
    return commands + bot_commands

def count_all_commands():
    """Count all commands in the bot"""
    total_commands = 0
    cogs_dir = os.path.join(os.path.dirname(__file__), 'cogs')
    
    for filename in os.listdir(cogs_dir):
        if filename.endswith('.py'):
            file_path = os.path.join(cogs_dir, filename)
            count = count_commands_in_file(file_path)
            print(f"{filename}: {count} commands")
            total_commands += count
    
    print(f"\nTotal commands: {total_commands}")
    return total_commands

if __name__ == "__main__":
    print("Counting commands in the Discord bot...")
    count_all_commands()