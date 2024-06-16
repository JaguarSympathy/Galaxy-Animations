import discord
from discord.ext import tasks
import json
import feedparser

API_KEY = "AIzaSyBpQItiGAzCehn-gx0f7Sb-HPzJw39OF-c"
TOKEN = "MTE1MzQyMjI0NzY1OTMxNTI5MQ.GvUSCE.F8Stp_C2whvlO92w3MH4w0TyNDAAH52lpv4O_s"

client = discord.Client(intents=discord.Intents.all())
prefix = "£"

owner = [667755060163248138,610020302692417546]
suggestionsChannel = 1155606435619672255
testChannel = 1154915199065784370

operation = ""
data = ""
notificationChannel = ""


def embedInit(pName,pDescription):
    embed = discord.Embed(title="",colour=0xed0735)
    embed.set_author(name="Galaxy Animations")
    embed.set_footer(text="Galaxy Animations",icon_url="https://media.discordapp.net/attachments/1154915199065784370/1154920583394513037/Galaxy_Animations.png?width=1074&height=1186")
    embed.add_field(name=pName,value=pDescription)
    return embed

def embedInitOnly():
    embed = discord.Embed(title="",colour=0xed0735)
    embed.set_author(name="Galaxy Animations")
    embed.set_footer(text="Galaxy Animations",icon_url="https://media.discordapp.net/attachments/1154915199065784370/1154920583394513037/Galaxy_Animations.png?width=1074&height=1186")
    return embed


@tasks.loop(minutes=1)
async def videoCheck():
    print("Running video check...")
    with open("youtubeData.json") as f:
        data = json.load(f)
        print("Checked for videos.")

    

    for ytChannel in data:
        videos = f"https://www.youtube.com/feeds/videos.xml?channel_id={ytChannel}"
        videos = str(feedparser.parse(videos))
        startPos = int(videos.find("href"))+8
        endPos = videos.find("'",startPos)
        video = videos[startPos:endPos]

        latest_video_url = video

        if str(data[ytChannel]["latest_video_url"]) != latest_video_url:
            data[str(ytChannel)]["latest_video_url"] = latest_video_url
            with open("youtubeData.json","w") as f:
                json.dump(data,f)

            notificationChannel = data[str(ytChannel)]["notification_channel"]
            notificationChannel = await client.fetch_channel(notificationChannel)
            botlogs = await client.fetch_channel(1153431330743406592)

            await notificationChannel.send(f"@ping Galaxy Animations has uploaded a new video/is live! Check it out at {latest_video_url}")
            await botlogs.send("[YT] - New video uploaded by Galaxy Animations and posted in the notification channel!")

@client.event
async def on_ready():
    print("Online and ready.")
    await videoCheck.start()

@client.event
async def on_message(message):
    if message.content.startswith(prefix) and message.author.id != client.user.id and (message.author.id in owner or discord.Permissions.administrator.flag):
        botlogs = await client.fetch_channel(1153431330743406592)
        suggestions = await client.fetch_channel(suggestionsChannel)

        #rank
        if message.content.startswith(prefix+"rank"):
            content = message.content.replace(prefix+"rank ","").split(" ")
            if len(content) == 3:
                target,rank,reason = content[0],content[1],content[2]
                if rank.startswith("<@"):
                    rank = rank.replace("<@","").replace(">")

                try: 
                    target = await message.guild.fetch_member(int(target))
                except:
                    await message.channel.send("ERROR - User not found.")
                    await botlogs.send(f"[ERR] - User not found.")
                
                if target.get_role(int(rank)):        
                    operation = "Remove"
                else:
                    operation = "Add"
                rank = message.guild.get_role(int(rank))

                if operation == "Add":
                    await target.add_roles(rank,reason=reason)
                    await message.channel.send(f"Successfully ranked `{target}` to `{rank}` with reason `{reason}`.")
                    await botlogs.send(f"[CMD] - {message.author.name} has ranked `{target}` to `{rank}` with reason `{reason}`.")
                elif operation == "Remove":
                    await target.remove_roles(rank,reason=reason)
                    await message.channel.send(f"Successfully removed `{rank}` from `{target}` with reason `{reason}`.")
                    await botlogs.send(f"[CMD] - {message.author.name} has removed `{rank}` from `{target}` with reason `{reason}`.")
                else:
                    await message.channel.send("An unexpected error has occured. Please consult Apollo Systems staff team. We apologise for inconvenience.")
                    await botlogs.send(f"[ERR] - Unexpected error while executing `rank` by {message.author.name} with content `{message.content}`")
            else:
                await message.channel.send(f"Three parameters expected but {len(content)} given.")
                await botlogs.send(f"[ERR] - Three parameters expected but {len(content)} given.")
        #suggest
        elif message.content.startswith(prefix+"suggest"):
            content = message.content.replace(prefix+"suggest ","")
            await suggestions.send(embed=embedInit(f"{message.author.name}'s suggestion",str(content)))
            await botlogs.send(f"[CMD] - {message.author.name} has submitted a suggestion with content `{content}`.")


client.run(TOKEN)