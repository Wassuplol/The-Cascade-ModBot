#!/usr/bin/env python3
"""
Accurate script to count the total number of commands in the bot
"""
import os

def count_commands_in_file(file_path):
    """Count the number of commands in a given file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    command_count = 0
    
    for i, line in enumerate(lines):
        if '@commands.command' in line:
            # Look for the next async def line within the next 10 lines
            for j in range(i+1, min(i+10, len(lines))):
                if 'async def' in lines[j]:
                    command_count += 1
                    break
    
    return command_count

def count_all_commands():
    """Count all commands in the bot"""
    total_commands = 0
    cogs_dir = os.path.join(os.path.dirname(__file__), 'cogs')
    
    print("Command counts by cog:")
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