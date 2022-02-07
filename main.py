import discord, praw, random, re, subprocess, requests

# set global variables.
TOKEN = "" # Edit This
client = discord.Client()

# Login to the reddit account
# This will be changed to OAUTH in the future for better security.
reddit = praw.Reddit(client_id="", # Edit This
                     client_secret="", # Edit This
                     password="", # Edit This
                     user_agent="", # Edit This
                     username="") # Edit This

# take <subreddit> from "from_sub" and dump a random matching title and image from it.
def sub_random(from_sub):
    sub = reddit.subreddit(from_sub).hot(limit=200)
    listme = []
    for submission in sub:
        if submission.stickied is False:
            listme.append(submission)

    subid = random.choice(listme)
    ransub = reddit.submission(id=subid)
    if ransub.over_18 is True:
        return ('NSFW | {}\n{}'.format(ransub.title, ransub.url))
    elif ransub.is_self is True:
        return ('/r/{}\n\n{}'.format(submission.subreddit, submission.selftext))
    else:
        return ('{}\n{}'.format(ransub.title, ransub.url))

@client.event
# Initial print of logging information.
async def on_ready():
    print('\n')
    print(dash)
    print('Logged in as "{}"'.format(client.user.name))
    print('time: '+str(now))
    print(dash)

@client.event
async def on_message(message):
    # Don't want to have the bot respond to itself.
    if message.author == client.user:
        return

    if message.content.startswith("r/") or message.content.startswith("R/"):
        await message.channel.trigger_typing()
        NSFW = ("This post is NSFW and this is not and NSFW Channel.")
        msgstart = sub_random(message.content.lower()[2:])
        if msgstart.startswith('NSFW | ') and message.channel.nsfw is False:
            await message.channel.send(NSFW)

        else:
            await message.channel.send(msgstart)

# Other Server Utilities
    # Help Command
    if message.content.startswith("~help"):
        await message.channel.send('The commands on this bot are:\n'
                                   '~server member count\n'
                                   '~dp\n'
                                   '~tea\n'
                                   '~annoy\n'
                                   'r/<subreddit>\n')
    # Counter Server Members
    if message.content.startswith("~server member count"):
        await message.channel.trigger_typing()
        await message.channel.send("This server has {} members.".format(message.guild.member_count))

    # Dr. Pepper Image
    if message.content.startswith("~dp"):
        await message.channel.send("https://i.ibb.co/x8B4zxf/image0.jpg")

    # Tea Gif
    if message.content.startswith("~tea"):
        await message.channel.send("https://tenor.com/view/twisted-twisted-tea-tea-smack-karma-gif-19753004")

    # Just shows the bot typing
    if message.content.startswith("~annoy"):
        await message.channel.trigger_typing()

    #Randomly posts yelling meme when someone is typing in all caps.
    if message.content.isupper() and len(message.content) > 7:
        # 30% Chance it will happen
        if random.random() > .7:
            await message.channel.send(
                'https://cdn.discordapp.com/attachments/572599663157313538/869735303710138428/839648032642302032.png')

client.run(TOKEN)
