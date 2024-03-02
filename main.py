from flask import Flask, redirect, request, session, url_for
from discord.ext import commands
import requests
import random
import discord
import asyncio
from flask import Flask, render_template
import json
import discord.ext
from discord import app_commands
import youtube_dl


app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secure secret key
client_id = "1210693713030946826"
client_secret = "151EmsslYy0G0HrCzqGLZc3yj8NZxMZL"
redirect_uri = "https://5b5af42a-a5d8-4f74-b2f9-509a2de7b9fe-00-1bxu3pv3nu2b1.picard.replit.dev/callback"
discord_api_url = "https://discord.com/api"
bot_token = "MTIxMDY5MzcxMzAzMDk0NjgyNg.GD9FV2.xtiuXDLPq7zTjgkHtz32yveR1WPui1U_ZYYEl8"
GIPHY_API_KEY = 'Hjyv2Vg3arAYJon9zthD5p85VMESBHxE'  # Replace with your Giphy API key

intents = discord.Intents.all()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

import socket

@bot.event
async def on_ready():
  guild_count = len(bot.guilds)
  member_count = sum([len(guild.members) for guild in bot.guilds])
  await bot.change_presence(activity=discord.Streaming(name=f"Streaming on {guild_count} guilds with {member_count} members", url='https://www.twitch.tv/your_channel_here'))

@bot.command(name='avatar', help='Displays the avatar of the mentioned user or your own avatar if no user is mentioned.')
async def display_avatar(ctx, user: discord.User = None):
    # If no user is mentioned, use the author's avatar
    if not user:
        user = ctx.author

    # Get the user's avatar URL
    avatar_url = user.avatar_url

    # Send the avatar to the Discord channel
    await ctx.send(f'{user.display_name}\'s Avatar:\n{avatar_url}')

@bot.command(name='8ball', help='Provides a magic 8-ball response to a yes/no question.')
async def magic_8ball(ctx, *, question):
    # Possible 8-ball responses
    responses = ["Yes", "No", "Ask again later", "Cannot predict now", "Don't count on it", "Most likely", "Maybe"]

    # Select a random response
    response = random.choice(responses)

    # Send the response to the Discord channel
    await ctx.send(f'Magic 8-Ball says: {response}')

@bot.command(name='quote', help='Shares an inspirational or funny quote.')
async def get_quote(ctx):
    # Make a request to the Quotable API
    response = requests.get('https://api.quotable.io/random')
    quote_data = response.json()

    # Check if a valid quote was found
    if 'content' in quote_data and 'author' in quote_data:
        quote_content = quote_data['content']
        quote_author = quote_data['author']
        await ctx.send(f'"{quote_content}" - {quote_author}')
    else:
        await ctx.send('Oops! I couldn\'t fetch a quote this time. Try again!')

@bot.command(name='catfact', help='Shares a random cat fact.')
async def get_cat_fact(ctx):
    # Make a request to the Cat Fact API
    response = requests.get('https://meowfacts.herokuapp.com/')
    cat_data = response.json()

    if 'data' in cat_data:
        cat_fact = cat_data['data'][0]
        await ctx.send(f'Did you know? {cat_fact}')
    else:
        await ctx.send('Oops! I couldn\'t fetch a cat fact this time. Try again!')

@bot.command(name='dogfact', help='Shares a random dog fact.')
async def get_dog_fact(ctx):
    # Make a request to the Dog CEO's Dog API
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    dog_data = response.json()

    if 'message' in dog_data and 'breeds' in dog_data['message']:
        dog_breed = dog_data['message']['breeds'][0]
        await ctx.send(f'Did you know? {dog_breed.capitalize()} is a fascinating dog breed!')
    else:
        await ctx.send('Oops! I couldn\'t fetch a dog fact this time. Try again!')

@bot.command(name='rps', help='Plays rock, paper, scissors with the bot.')
async def play_rps(ctx, user_choice: str):
    # List of valid choices
    valid_choices = ['rock', 'paper', 'scissors']

    # Convert user's choice to lowercase
    user_choice = user_choice.lower()

    # Check if user's choice is valid
    if user_choice not in valid_choices:
        await ctx.send('Invalid choice. Please choose rock, paper, or scissors.')
        return

    # Bot randomly selects a choice
    bot_choice = random.choice(valid_choices)

    # Determine the winner
    result = determine_winner(user_choice, bot_choice)

    # Send the result to the Discord channel
    await ctx.send(f'You chose {user_choice.capitalize()}.\nI chose {bot_choice.capitalize()}.\nResult: {result}')

def determine_winner(user_choice, bot_choice):
    if user_choice == bot_choice:
        return 'It\'s a tie!'
    elif (
        (user_choice == 'rock' and bot_choice == 'scissors') or
        (user_choice == 'paper' and bot_choice == 'rock') or
        (user_choice == 'scissors' and bot_choice == 'paper')
    ):
        return 'You win!'
    else:
        return 'I win!'

@bot.command(name='meme', help='Shares a random meme.')
async def share_meme(ctx):
    # Fetch a random meme template ID from Imgflip API
    template_response = requests.get('https://api.imgflip.com/get_memes')
    template_data = template_response.json()

    if 'data' in template_data and 'memes' in template_data['data']:
        memes = template_data['data']['memes']
        random_template_id = random.choice(memes)['id']

        # Generate a meme using the selected template
        meme_response = requests.post('https://api.imgflip.com/caption_image', data={
            'template_id': random_template_id,
            'username': 'Mxersion',  # Replace with your Imgflip username
            'password': 'Mxersion@gmail.com',  # Replace with your Imgflip password
        })

        meme_data = meme_response.json()

        if 'data' in meme_data and 'url' in meme_data['data']:
            meme_url = meme_data['data']['url']
            await ctx.send(meme_url)
        else:
            await ctx.send('Oops! I couldn\'t generate a meme this time. Try again!')
    else:
        await ctx.send('Oops! I couldn\'t fetch a meme template this time. Try again!')

@bot.command(name='telljoke', help='Tells a random joke.')
async def tell_joke(ctx):
    # Fetch a random joke from JokeAPI
    response = requests.get('https://v2.jokeapi.dev/joke/Any')
    joke_data = response.json()

    if 'joke' in joke_data:
        joke = joke_data['joke']
        await ctx.send(joke)
    elif 'setup' in joke_data and 'delivery' in joke_data:
        setup = joke_data['setup']
        delivery = joke_data['delivery']
        await ctx.send(f'{setup}\n{delivery}')
    else:
        await ctx.send('Oops! I couldn\'t fetch a joke this time. Try again!')

@bot.command(name='coinflip', help='Flips a coin and returns the result.')
async def coinflip(ctx):
    # Generate random result (heads or tails)
    result = random.choice(['Heads', 'Tails'])

    # Send the result to the Discord channel
    await ctx.send(f'Coin landed on: {result}')

@bot.command(name='rolldice', help='Rolls a standard six-sided dice.')
async def roll_dice(ctx):
    # Generate a random number between 1 and 6
    dice_result = random.randint(1, 6)

    # Send the result to the Discord channel
    await ctx.send(f'The dice rolled: {dice_result}')

@bot.command(name='gif', help='Displays a random gif based on the provided keyword.')
async def display_gif(ctx, keyword):
    # Make a request to the Giphy API
    url = f'https://api.giphy.com/v1/gifs/random?api_key={GIPHY_API_KEY}&tag={keyword}'
    response = requests.get(url)
    gif_data = response.json()

    # Check if a valid gif was found
    if 'data' in gif_data and 'image_original_url' in gif_data['data']:
        gif_url = gif_data['data']['image_original_url']
        await ctx.send(gif_url)
    else:
        await ctx.send('Sorry, no gif found for that keyword.')

@bot.command(name='randomuser', help='Mentions a random user from the server.')
async def random_user(ctx):
    # Get the list of members in the server
    members = ctx.guild.members

    # Exclude the bot itself from the list
    members = [member for member in members if not member.bot]

    if members:
        # Select a random member
        random_member = random.choice(members)

        # Mention the randomly selected user
        await ctx.send(f'Random User: {random_member.mention}')
    else:
        await ctx.send('No users found in the server.')




@app.route('/ban', methods=['POST'])
def ban_user():
    user_id = request.form['user_id']
    ban_user(user_id)
    return render_template('index.html', banlist=banlist)

@app.route('/unban', methods=['POST'])
def unban_user():
    user_id = request.form['user_id']
    unban_user(user_id)
    return render_template('index.html', banlist=banlist)

ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
}

@bot.command()
async def download(ctx, url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:

            info = ydl.extract_info(url, download=False)
            filename = info['title'] + '.mp4'
            ydl.download([url])
            await ctx.send(file=discord.File(filename))
            print(f'Sent {filename} to {ctx.channel.name}')
        except youtube_dl.DownloadError as e:
            await ctx.send(e)



# Load configuration from a JSON file
with open('config.json', 'r') as f:
    config = json.load(f)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    try:
        if config['anti_raid_enabled']:
            if message.author.id in message_timestamps:
                current_time = time.time()
                time_difference = current_time - message_timestamps[message.author.id]
                message_limit = 200  # Set the character limit for messages

                if len(message.content) > message_limit:
                    await message.delete()
                    await message.channel.send(f"{message.author.mention}, your message exceeds the character limit and has been deleted.")
                elif time_difference < 2:
                    await message.delete()
                    await message.channel.send(f"{message.author.mention}, please wait before sending another message.")

                message_timestamps[message.author.id] = time.time()
            else:
                message_timestamps[message.author.id] = time.time()
    except Exception as e:
        print(e)

    await bot.process_commands(message)

@bot.command()
async def toggle_antiraid(ctx):
    try:
        config['anti_raid_enabled'] = not config['anti_raid_enabled']

        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)

        status = "enabled" if config['anti_raid_enabled'] else "disabled"
        await ctx.send(f"Anti-raid feature is now {status}.")
    except Exception as e:
        print(e)
        await ctx.send("An error occurred while toggling the anti-raid feature.")

# Initialize the message timestamps dictionary
message_timestamps = {}

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason: str = None):
    if member.top_role >= ctx.author.top_role and member.id != ctx.bot.user.id:
        await ctx.send("I can't kick that user because they have a higher role than you.")
        return
    if member.id == ctx.bot.user.id:
        await ctx.send("I can't kick myself.")
        return
    await member.kick(reason=reason)
    await ctx.send(f"{member.display_name} has been kicked.")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.mention}, you don't have the necessary permissions to run this command. You need the `Kick Members` permission.")



@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 0):
    if amount > 100:
        await ctx.send("I can't delete more than 100 messages at once.")
        return
    deleted_messages = await ctx.channel.purge(limit=amount)
    embed = discord.Embed(title="Messages Cleared", description=f"{len(deleted_messages)} messages have been cleared.", color=0x00ff00)
    message = await ctx.send(embed=embed)
    await asyncio.sleep(5)
    await message.delete()

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permissions to do that")

config_file = 'config.json'

@bot.command()
async def setwelcome(ctx, *, message: str = "Welcome to our server!"):
    # Get the channel where the command was used
    welcome_channel = ctx.channel.id

    # Update or add the welcome channel to the config JSON
    with open(config_file, 'r') as f:
        config = json.load(f)
    config['welcome_channel'] = welcome_channel
    config['welcome_message'] = message
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)

    await ctx.send(f'Welcome channel and message set to {ctx.channel.mention} and {message}')

@bot.event
async def on_member_join(member):
    # Load welcome message from the config JSON
    with open(config_file, 'r') as f:
        config = json.load(f)
    welcome_message = config.get('welcome_message')

    # Get the welcome channel from the config JSON
    with open(config_file, 'r') as f:
        config = json.load(f)
    welcome_channel_id = config.get('welcome_channel')

    if welcome_channel_id:
        welcome_channel = member.guild.get_channel(welcome_channel_id)
        if welcome_channel:
            # Send a welcome message
            await welcome_channel.send(welcome_message.format(member=member))

@bot.command(name='helpe')
async def help_command(ctx):
    help_message = (
        "Welcome to the Bot!\n"
        "`!help`: Display this message.\n"
        "`!server_info <server_id>`: Display information about a specific server.\n"
        "`!manage_server <server_id>`: Manage a specific server.\n"
        "`!logout`: Log out and redirect to the home page."
    )
    await ctx.send(help_message)

@bot.command(name='ping')
async def ping_command(ctx):
    await ctx.send('Pong! Latency is {:.2f}ms'.format(bot.latency * 1000))

from discord import Embed
@bot.command(name='dashboard')
async def dashboard_command(ctx):
    embed = Embed(
        title='Dashboard Link',
        description='Click the button below to access the dashboard:',
        color=discord.Color.blue()
    )
    embed.add_field(name='Dashboard Link:', value='[Access Dashboard](https://your-dashboard-link-here)', inline=False)
    embed.set_footer(text='Enjoy managing your servers!')
    await ctx.send(embed=embed)

from discord.ext.commands import CommandOnCooldown
from discord.ext.commands import cooldown

@bot.event
@cooldown(1, 60)  # 1 message per 60 seconds (1 minute)
async def on_message(message):
    if message.author.bot:
        return  # Ignore messages from bots

    try:
        await bot.process_commands(message)  # Process the command

    except CommandOnCooldown as e:
        await message.channel.send(f"Please slow down your messages to prevent spam. Try again in {e.retry_after:.2f} seconds.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason: str = None):
    if member.top_role >= ctx.author.top_role and member.id != ctx.bot.user.id:
        await ctx.send("I can't ban that user because they have a higher role than you.")
        return
    if member.id == ctx.bot.user.id:
        await ctx.send("I can't ban myself.")
        return
    await member.ban(reason=reason, delete_message_days=7)
    await ctx.send(f"{member.display_name} has been banned.")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.mention}, you don't have the necessary permissions to run this command. You need the `Ban Members` permission.")


from discord.ext import commands
from discord.ext.commands import has_permissions
from discord import Permissions




@bot.command(name='members')
async def members_command(ctx):
    members = ctx.guild.members
    member_list = "\n".join([member.name for member in members])
    await ctx.send(f"Members in this server:\n{member_list}")

@bot.command(name='serverinfo')
async def serverinfo_command(ctx):
    server = ctx.guild
    total_members = server.member_count
    server_name = server.name
    server_owner = server.owner
    verification_level = server.verification_level

    info_message = f"Server Name: {server_name}\nOwner: {server_owner}\nVerification Level: {verification_level}\nTotal Members: {total_members}"

    await ctx.send(info_message)

@bot.event
async def on_command(ctx):
    server_id = ctx.guild.id
    user_id = ctx.author.id
    command_used = ctx.message.content

    data = {
        'server_id': server_id,
        'user_id': user_id,
        'command_used': command_used
    }

    with open('commands.json', 'a') as file:
        json.dump(data, file)
        file.write('\n')


@app.route("/")
def home():
    if "discord_token" in session:
        user_info = get_user_info(session["discord_token"])

        # Access the user's email from the session
        user_email = session.get("user_email", "Email not available")

        servers = get_user_servers(session["discord_token"])

        # Save server data to a JSON file (Replace with your own logic)
        server_data = [
            {"id": server["id"], "name": server["name"], "email": user_email} 
            for server in servers
        ]

        with open("server_data.json", "w") as json_file:
            json.dump(server_data, json_file)

        # Generate HTML cards for each server
        server_cards = ""
        for server in servers:
            server_cards += f"""
                <div class="server-card">
                    <h3>{server["name"]}</h3>
                    <p>ID: {server["id"]}</p>
                    {get_manage_server_button(server["id"])}
                </div>
            """

        return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard</title>
        <style>
            body {{
                background-color: #08081C;
                color: white;
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            h1, p {{
                text-align: center;
            }}

            .server-card {{
                border: 1px solid #080E2C;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                background-color: #080E2C;
            }}

            h3, p {{
                margin: 0;
            }}

            button {{
                background-color: #1B213D; /* Updated button color */
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 10px; /* Rounded corners for the button */
                cursor: pointer;
            }}

            button:hover {{
                background-color: #2B315D; /* Adjusted hover color */
            }}

            a {{
                color: #080E2C;
                text-decoration: none;
                display: block;
                margin-top: 20px;
                text-align: center;
            }}

            a:hover {{
                color: #0A0E3C;
            }}
        </style>
    </head>
    <body>
        <h1>Welcome, {user_info['username']}!</h1>
        <p>Your servers:</p>
        {server_cards}
        <a href="/logout"><button>Logout</button></a>
    </body>
    </html>
        """
    else:
        return render_template('index.html')

def get_manage_server_button(server_id):
    if bot_is_in_server(server_id):
        return f"""
            <button id="manageServerBtn" onclick="openManageServerPage('{server_id}')">Manage Server</button>
            <script>
                function openManageServerPage(server_id) {{
                    window.open('/manage_server/' + server_id, '_blank');
                }}
            </script>
        """
    else:
        invite_url = generate_invite_url()
        return f'<a href="{invite_url}"><button>Invite Bot</button></a>'

def bot_is_in_server(server_id):
    guild = bot.get_guild(int(server_id))
    return guild is not None

def generate_invite_url():
    # Replace 'YOUR_CLIENT_ID' with your bot's client ID
    return f"https://discord.com/oauth2/authorize?client_id=1210693713030946826&permissions=8&scope=bot"

@app.route("/login")
def login():
    return redirect(f"{discord_api_url}/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=identify%20guilds%20email")

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token = get_access_token(code)

    # Get user info, including email
    user_info = get_user_info(token)

    # Save email and token in the session
    session["discord_token"] = token
    session["user_email"] = user_info.get("email", None)

    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.pop("discord_token", None)
    return redirect(url_for("home"))

def get_access_token(code):
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "scope": "identify guilds"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(f"{discord_api_url}/oauth2/token", data=data, headers=headers)
    return response.json()["access_token"]

def get_user_info(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "scope": "identify email"
    }
    response = requests.get(f"{discord_api_url}/users/@me", headers=headers, params=params)
    return response.json()

def get_user_servers(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(f"{discord_api_url}/users/@me/guilds", headers=headers)
    servers = response.json()
    admin_servers = [server for server in servers if (server['permissions'] & 0x8) == 0x8]  # Check if the user has the Administrator permission
    return admin_servers

# ... (existing code)

from flask import render_template

from flask import render_template

@app.route("/manage_server/<server_id>")
def manage_server(server_id):
    server_info = get_server_info(server_id)
    return render_template('manage_server.html', server_info=server_info, server_id=server_id)

@app.route("/logs/<server_id>")
def logs_page(server_id):
    try:
        # Fetch logs from 'commands.json' based on the provided server_id
        with open('commands.json', 'r') as file:
            logs = [json.loads(line) for line in file if str(json.loads(line).get('server_id')).lstrip('$') == server_id]

        # Display logs
        logs_html = "<h2>Command Logs:</h2>"
        for log in logs:
            logs_html += f"<p>User {log['user_id']} used command: {log['command_used']}</p>"

        return logs_html

    except FileNotFoundError:
        return "Logs file not found."

import datetime
import json

# Function to get server information
def get_server_info(server_id):
    server_id = server_id.lstrip('$')  # Remove the '$' prefix

    try:
        guild = bot.get_guild(int(server_id))
    except ValueError:
        return {
            "name": "Invalid Server ID",
            "owner": "Owner not available",
            "user_count": "User count not available"
        }

    if not guild:
        return {
            "name": "Server not found",
            "owner": "Owner not available",
            "user_count": "User count not available"
        }

    server_info = {
        "name": guild.name,
        "owner": guild.owner.name if guild.owner else "Owner not available",
        "user_count": guild.member_count
    }

    if hasattr(guild, 'region'):
        server_info['region'] = guild.region
    else:
        server_info['region'] = "Region not available"

    return server_info

# Function to collect weekly analytics
async def collect_weekly_analytics(guild):
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=7)

    server_member_count = guild.member_count
    message_activity = await collect_message_activity(guild, start_date, end_date)

    return {
        "server_member_count": server_member_count,
        "message_activity": message_activity
    }

# Function to save analytics data to a JSON file
def save_analytics_to_json(server_id, analytics_data):
    file_path = f"analytics_{server_id}.json"
    with open(file_path, 'w') as json_file:
        json.dump(analytics_data, json_file)

    return server_info

async def collect_weekly_analytics(guild):
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=7)

    server_member_count = guild.member_count
    message_activity = await collect_message_activity(guild, start_date, end_date)

    return {
        "server_member_count": server_member_count,
        "message_activity": message_activity
    }

# Function to save analytics data to a JSON file
def save_analytics_to_json(server_id, analytics_data):
    file_path = f"analytics_{server_id}.json"
    with open(file_path, 'w') as json_file:
        json.dump(analytics_data, json_file)

@app.route("/toggle_antiraid")
def toggle_antiraid():
    with open('config.json', 'r') as f:
        config = json.load(f)

    config['anti_raid_enabled'] = not config['anti_raid_enabled']

    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

    return redirect(url_for("home"))

if __name__ == "__main__":
    from concurrent.futures import ThreadPoolExecutor
    import threading

    # Define a function to run the Flask app
    def run_flask():
        app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)

    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Wait for a moment to ensure Flask has started
    import time
    time.sleep(2)

    # Start the Discord bot
    bot.run(bot_token)
