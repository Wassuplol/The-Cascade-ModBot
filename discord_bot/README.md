# Discord Bot

A comprehensive Discord bot with moderation, fun, economy, utility, and music commands.

## Features

- **Moderation Commands**: Ban, kick, mute, warn, purge messages, lock/unlock channels, and more
- **Economy System**: Daily rewards, work, balance checking, transfers, and leaderboards
- **Fun Commands**: Games, memes, jokes, riddles, and more
- **Utility Commands**: Server info, user info, bot stats, and more
- **Music Commands**: Play music from YouTube in voice channels

## Commands

### Moderation
- `!ban @user [reason]` - Ban a user
- `!unban [user_id]` - Unban a user by ID
- `!kick @user [reason]` - Kick a user
- `!mute @user [duration] [reason]` - Mute a user (duration in minutes)
- `!unmute @user` - Unmute a user
- `!purge [amount]` - Delete messages
- `!warn @user [reason]` - Warn a user
- `!lock [channel]` - Lock a channel
- `!unlock [channel]` - Unlock a channel
- `!slowmode [seconds] [channel]` - Set slowmode in a channel

### Economy
- `!balance [@user]` - Check balance
- `!daily` - Claim daily coins
- `!work` - Work to earn coins
- `!deposit [amount]` - Deposit coins to bank
- `!withdraw [amount]` - Withdraw coins from bank
- `!transfer @user [amount]` - Transfer coins to another user
- `!leaderboard` - Show richest users
- `!rob @user` - Try to rob another user

### Fun
- `!ping` - Check bot latency
- `!roll [dice]` - Roll dice (default 1d6)
- `!flip` - Flip a coin
- `!rps [choice]` - Play rock paper scissors
- `!meme` - Get a random meme
- `!joke` - Get a random joke
- `!cat` - Get a random cat image
- `!dog` - Get a random dog image
- `!8ball [question]` - Ask the magic 8-ball
- `!riddle` - Get a random riddle
- `!trivia` - Get a random trivia question
- `!ascii [text]` - Convert text to ASCII art
- `!fact` - Get a random fact
- `!insult [@user]` - Generate an insult
- `!compliment [@user]` - Generate a compliment

### Utility
- `!serverinfo` - Get server information
- `!userinfo [@user]` - Get user information
- `!avatar [@user]` - Get user's avatar
- `!botinfo` - Get bot information
- `!invite` - Get bot invite link
- `!uptime` - Get bot uptime
- `!stats` - Get bot statistics
- `!suggest [suggestion]` - Make a suggestion
- `!vote [option1, option2, ...]` - Create a vote
- `!poll [question]` - Create a yes/no poll
- `!remind [time] [reminder]` - Set a reminder

### Music
- `!join` - Join voice channel
- `!leave` - Leave voice channel
- `!play [query]` - Play a song from YouTube
- `!pause` - Pause current song
- `!resume` - Resume current song
- `!stop` - Stop current song
- `!skip` - Skip current song
- `!queue` - Show current queue

### General
- `!help` - Show all commands
- `!help [command]` - Show specific command help

## Setup

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a Discord bot at the [Discord Developer Portal](https://discord.com/developers/applications)
4. Copy your bot token and add it to the `.env` file
5. Run the bot: `python main.py`

### Environment Variables

Create a `.env` file with the following variables:

```
DISCORD_TOKEN=your_discord_bot_token_here
BOT_PREFIX=!
```

## Requirements

- Python 3.8+
- Discord.py
- yt-dlp (for music)
- PyNaCl (for voice)

## Contributing

Feel free to fork this repository and submit pull requests for improvements or new features.

## License

This project is licensed under the MIT License.