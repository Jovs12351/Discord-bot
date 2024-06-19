import discord
from discord.ext import tasks
import requests

# Discord bot token
DISCORD_BOT_TOKEN = 'YOUR_DISCORD_BOT_TOKEN'

# GitHub repository details
GITHUB_API_URL = 'https://api.github.com/repos/{owner}/{repo}/releases/latest'
GITHUB_OWNER = 'Jovs12351'
GITHUB_REPO = 'Discord-bot'

# Bot setup
intents = discord.Intents.default()
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    check_latest_release.start()  # Start the task to check for the latest release

@tasks.loop(minute=1)  # Check every hour
async def check_latest_release():
    url = GITHUB_API_URL.format(owner=GITHUB_OWNER, repo=GITHUB_REPO)
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        latest_version = data['tag_name']
        release_url = data['html_url']
        release_name = data['name']
        release_body = data['body']

        print(f"New Release: {release_name}")
        print(f"Version: {latest_version}")
        print(f"URL: {release_url}")
        print(f"Description: {release_body}")
    else:
        print(f"Failed to fetch the latest release: {response.status_code}")

# Run the bot
bot.run(DISCORD_BOT_TOKEN)
