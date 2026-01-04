import discord
import subprocess
import shlex
from discord.ext import commands, tasks
from discord import app_commands
# from discord import ui
import logging
import os
import json
import asyncio
import aiohttp
import random as rand
import folder
import datetime
import shutil
import downloader
from ffprobe import FFprobe
import humanize
import sqlite3
from urlextract import URLExtract
import parse
from catboxpy.catbox import CatboxClient
from dpy_paginator import paginate
from yt_dlp import YoutubeDL
import re
youguessedit = input('Run IHTX Bot? (Y/N)')
if youguessedit.upper() == 'Y':
  print('Sent message to run.')
else:
  print('Ok.')
  exit()
global conn, c
conn = sqlite3.connect('templates.db')
c = conn.cursor()
c.execute('''
        CREATE TABLE IF NOT EXISTS templates (
            guild_id INTEGER,
            name TEXT,
            content TEXT,
            user_id INTEGER,
            PRIMARY KEY (guild_id, name)
        )
    ''')
conn.commit()

prefix = ':'
theme = 0x6100FF
invitelink = "https://discord.com/oauth2/authorize?client_id=1456584616533299343&permissions=8&integration_type=0&scope=bot"
bottoken = "MTQ1NjU4NDYxNjUzMzI5OTM0Mw.GR5jpt.FIqU611jOq_Gf-bwTZNlP1w9LGkZzjFiVqgAQI" # place your bot token here
UPLOAD_DIR = "./uploads"
folder.makeDir(UPLOAD_DIR)
folder.clear(UPLOAD_DIR,True)
folder.makeDir(f"{UPLOAD_DIR}/ihtx")
# os.makedirs(UPLOAD_DIR, exist_ok=True)
FILE_EXTENSION = ".ts"
ADDITIONAL_COMPATIBILITY = ""
handler = logging.FileHandler(filename='discord.log',encoding='utf-8',mode='w')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)
statuses = ["for AMTVE","everyone","NotSoBot","TADC","Robot 64","SMG4","Numberblocks"]
@bot.event
async def on_ready():
  print(f'Logged in as {bot.user}!')
  await bot.tree.sync() # Syncs all global commands
        # For guild-specific commands, use: await bot.tree.sync(guild=discord.Object(id=YOUR_GUILD_ID))
  print("Commands synced!")
  change_status.start()
  print('Status changed.')

@bot.event
async def on_guild_join(guild):
  print(f"Joined new guild: {guild.name} (ID: {guild.id})")
  icon = discord.File("icon.png", filename="icon.png")
  embeder = discord.Embed(title=f"Thank you for inviting {bot.user.name} to {guild.name}.",description=f"{bot.user.name} is a I hate the X video editing bot. I hate the X is where a effect gets repeated by a amount of times. Say {prefix}help for all commands. It uses FFmpeg, so you have to have some FFmpeg knowledge to use this bot properly.",color=theme,timestamp=datetime.datetime.now())
  embeder.set_footer(text=bot.user.name, icon_url="attachment://icon.png")
  if guild.system_channel:
    await guild.system_channel.send(embed=embeder,file=icon) 
  else:
        # If no system channel is found, try to send to the first available text channel
    for channel in guild.text_channels:
      try:
        await channel.send(embed=embeder,file=icon) 
        break  # Send to the first available channel and break the loop
      except discord.Forbidden:
        continue  # Bot doesn't have permission to send messages in this channel

@tasks.loop(seconds=10.0)
async def change_status():
    await bot.change_presence(activity=discord.Activity(name=rand.choice(statuses),type=discord.ActivityType.watching),status=discord.Status.online)

# start of commands

bot.remove_command('help') # removes default help

class MyHelpCommand(commands.HelpCommand):
  async def send_bot_help(self, mapping):
    icon = discord.File("icon.png", filename="icon.png")
    embed = discord.Embed(title=f"{bot.user.name} Help", description="Here are my commands:",color=theme)
    for cog, commands in mapping.items():
      if cog:
        name = cog.qualified_name
      else:
        name = "No Category"
      command_signatures = [self.get_command_signature(c) for c in commands]
      for i, v in enumerate(commands):
        if v.brief:
          command_signatures[i] = command_signatures[i]+f" - {v.brief}"
      if command_signatures:
        embed.add_field(name=name, value="\n".join(command_signatures), inline=False)
    embed.set_footer(text=f"{len(commands)} commands | "+bot.user.name, icon_url="attachment://icon.png")
    await self.get_destination().send(embed=embed,file=icon)
  async def send_cog_help(self, cog):
    icon = discord.File("icon.png", filename="icon.png")
    embed = discord.Embed(title=cog.qualified_name,color=theme)
    if cog.description:
      desc = cog.description
    else:
      desc = "-# _No description provided._"
    commands = ""
    for i, v in enumerate(cog.get_commands()):
      commands += f"- {self.get_command_signature(v)}\n"
    embed.add_field(name="Description",value=desc)
    embed.add_field(name="Commands",value=commands)
    embed.set_footer(text=bot.user.name, icon_url="attachment://icon.png")
    await self.get_destination().send(embed=embed,file=icon)
  async def send_command_help(self, command):
    icon = discord.File("icon.png", filename="icon.png")
    embed = discord.Embed(title=self.get_command_signature(command),color=theme)
    if command.cog:
      cogname = command.cog.qualified_name
    else:
      cogname = "No Category"
    if command.help:
      commandhelp = command.help
    else:
      commandhelp = "No help provided."
    embed.add_field(name="Help",value=commandhelp,inline=False)
    embed.add_field(name="Category",value=cogname,inline=True)
    embed.add_field(name="Usage",value=command.usage,inline=True)
    embed.set_footer(text=bot.user.name, icon_url="attachment://icon.png")
    await self.get_destination().send(embed=embed,file=icon)
  async def send_command_help(self, command):
    icon = discord.File(f"icon.png", filename="icon.png")
    embed = discord.Embed(title=self.get_command_signature(command),color=theme)
    if command.cog:
      cogname = command.cog.qualified_name
    else:
      cogname = "No Category"
    if command.help:
      commandhelp = command.help
    else:
      commandhelp = "No help provided."
    embed.add_field(name="Help",value=commandhelp,inline=False)
    embed.add_field(name="Category",value=cogname,inline=True)
    embed.add_field(name="Usage",value=command.usage,inline=True)
    embed.set_footer(text=bot.user.name, icon_url="attachment://icon.png")
    await self.get_destination().send(embed=embed,file=icon)
      
bot.help_command = MyHelpCommand()
class FileLayout(discord.ui.LayoutView):
  def __init__(self, file:discord.File, filename:str, timeout=60):
    super().__init__()
    self.file = file
    self.filename = filename
    container = discord.ui.Container(discord.ui.MediaGallery(discord.MediaGalleryItem(self.file)),accent_color=theme)
    container.add_item(discord.ui.Separator())
    probed = FFprobe(self.filename)
    container.add_item(discord.ui.TextDisplay(f'-# {probed["streams"][0]["width"]}x{probed["streams"][0]["height"]}, {probed["streams"][0]["nb_frames"]} frames, {humanize.naturalsize(int(probed["format"]["size"]))}'))
    self.container = container
  def make(self):
    t = discord.ui.LayoutView()
    t.add_item(item=self.container)
    return t
class FileLayoutURL(discord.ui.LayoutView):
  def __init__(self, url:str, filename:str, timeout=60):
    super().__init__()
    self.url = url
    self.filename = filename
    container = discord.ui.Container(discord.ui.MediaGallery(discord.MediaGalleryItem(self.url)),accent_color=theme)
    container.add_item(discord.ui.Separator())
    probed = FFprobe(self.filename)
    container.add_item(discord.ui.TextDisplay(f'-# {probed["streams"][0]["width"]}x{probed["streams"][0]["height"]}, {probed["streams"][0]["nb_frames"]} frames, {humanize.naturalsize(int(probed["format"]["size"]))}'))
    self.container = container
  def make(self):
    t = discord.ui.LayoutView()
    t.add_item(item=self.container)
    return t
class FileLayout2(discord.ui.LayoutView):
  def __init__(self, file:discord.File, filename:str, thing:dict, timeout=60):
    super().__init__()
    self.file = file
    self.filename = filename
    self.thing = thing
    container = discord.ui.Container(discord.ui.MediaGallery(discord.MediaGalleryItem(self.file)),accent_color=theme)
    container.add_item(discord.ui.Separator())
    probed = FFprobe(self.filename)
    container.add_item(discord.ui.TextDisplay(f'-# {probed["streams"][0]["width"]}x{probed["streams"][0]["height"]}, {probed["streams"][0]["nb_frames"]} frames, {humanize.naturalsize(int(probed["format"]["size"]))}'))
    container.add_item(discord.ui.Separator())
    stat = "-# "
    for k, v in thing.items():
      stat += f"{k}: {v}, "
    stat = stat[:len(stat)-2]
    container.add_item(discord.ui.TextDisplay(stat))
    self.container = container
  def make(self):
    t = discord.ui.LayoutView()
    t.add_item(item=self.container)
    return t
def FileBiggerThan(mb:float,filename:str):
    filesize_bytes = os.path.getsize(filename)
    mb = mb * 1024 * 1024  # 8 MB converted to bytes
    return filesize_bytes > mb
def catbox_upload(filename:str):
  client = CatboxClient()
  upload = client.upload(filename)
  return upload
def getyoutubeid(url: str) -> str | None:
    """Extracts the YouTube video ID from a URL using regex."""
    pattern = r'(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None
@bot.command()
async def suggest(ctx):
  await ctx.send("[Suggest any ideas here.](https://amtve.straw.page/suggestihtxbot)")
@bot.command()
async def command(ctx,*,command):
    """
      Execute a FFmpeg command on a video file, works on reply.

      Example usage:
        :command -vf "scale=320:240"
    """
    loadMessage = await ctx.reply("> <a:load:1417523157824442599> Loading Video (1/3)", mention_author=False)
    file_names = [os.path.join(UPLOAD_DIR, f"output_{ctx.author.id}.mp4"),os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"input_{ctx.author.id}.mp4")]
    for i, v in enumerate(file_names):
      if os.path.exists(v):
        await loadMessage.edit(content="> :warning: You still have a process still running. Please wait.")
        return
    attachment_url = None
    # Check for attachments or replied media
    if ctx.message.reference:
        referenced_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if referenced_message.attachments:
            attachment_url = referenced_message.attachments[0].url
        else:
            extractor = URLExtract()
            urls = extractor.find_urls(referenced_message.content)
            if urls:
              attachment_url = urls[0]
        if not referenced_message.components == []:
          attachment_url = referenced_message.components[0].children[0].items[0].media.url
    if not attachment_url and ctx.message.attachments:
        attachment_url = ctx.message.attachments[0].url

    if not attachment_url:
        await loadMessage.edit(content="> :x: Please provide a video attachment or link.")
        return
    else:
        await loadMessage.edit(content="> <a:load:1417523157824442599> Downloading Video (2/3)",allowed_mentions=discord.AllowedMentions(replied_user=False))
    try:
        # Download the file
        file_name = os.path.join(UPLOAD_DIR, f"input_{ctx.author.id}.mp4")
        await downloader.from_url(attachment_url,file_name)
        probet = FFprobe(file_name)
        w = probet["streams"][0]["width"]
        h = probet["streams"][0]["height"]
        fc = probet["streams"][0]["nb_frames"]
        await loadMessage.edit(content="> <a:load:1417523157824442599> Processing Video (3/3)",allowed_mentions=discord.AllowedMentions(replied_user=False))
          
        command = command.replace("$w",str(w))
        command = command.replace("$h",str(h))
        command = command.replace("$fc",str(fc))
        sanitized_command = shlex.split(command)

        # Prepare output file
        output_file = os.path.join(UPLOAD_DIR, f"output_{ctx.author.id}.mp4")
        if not any(arg.endswith(".mp4") for arg in sanitized_command):
            sanitized_command.append(output_file)

        # Run FFmpeg command asynchronously
        process = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-i", file_name,
            *sanitized_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if os.path.exists(output_file):
            file = discord.File(output_file)
            view = FileLayout(file, output_file)
            # "Command executed successfully."
            await loadMessage.delete()
            await asyncio.sleep(0.5)
            await ctx.reply(file=file,view=view.make())
            os.remove(output_file)
        else:
            await loadMessage.edit(content=f"> :x: Error executing command:\n```{stderr.decode()}```")

        if os.path.exists(file_name):
            os.remove(file_name)

    except Exception as e:
        if os.path.exists(file_name):
          os.remove(file_name)
        await loadMessage.edit(content=f"> :x: An error occurred: {str(e)}")
@bot.command()
async def sync(ctx):
    """
      Execute a FFmpeg command on a video file, works on reply.

      Usage: :sync
    """
    loadMessage = await ctx.reply("> <a:load:1417523157824442599> Loading Video (1/3)", mention_author=False)
    file_names = [os.path.join(UPLOAD_DIR, f"output_{ctx.author.id}.mp4"),os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"input_{ctx.author.id}.mp4")]
    for i, v in enumerate(file_names):
      if os.path.exists(v):
        await loadMessage.edit(content="> :warning: You still have a process still running. Please wait.")
        return
    attachment_url = None
    # Check for attachments or replied media
    if ctx.message.reference:
        referenced_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if referenced_message.attachments:
            attachment_url = referenced_message.attachments[0].url
        else:
            extractor = URLExtract()
            urls = extractor.find_urls(referenced_message.content)
            if urls:
              attachment_url = urls[0]
        if not referenced_message.components == []:
          attachment_url = referenced_message.components[0].children[0].items[0].media.url
    if not attachment_url and ctx.message.attachments:
        attachment_url = ctx.message.attachments[0].url

    if not attachment_url:
        await loadMessage.edit(content="> :x: Please provide a video attachment or link.")
        return
    else:
        await loadMessage.edit(content="> <a:load:1417523157824442599> Downloading Video (2/3)",allowed_mentions=discord.AllowedMentions(replied_user=False))
    try:
        # Download the file
        file_name = os.path.join(UPLOAD_DIR, f"input_{ctx.author.id}.mp4")
        await downloader.from_url(attachment_url,file_name)
        probet = FFprobe(file_name)
        vdur = float(probet["streams"][0]["duration"])
        adur = float(probet["streams"][1]["duration"])
        fps = probet["streams"][0]["r_frame_rate"]
        speed = str(vdur/adur)
        diff = str(vdur-adur)
        await loadMessage.edit(content="> <a:load:1417523157824442599> Processing Video (3/3)",allowed_mentions=discord.AllowedMentions(replied_user=False))
        sanitized_command = shlex.split(f"-vf setpts=1/{speed}*PTS,fps={fps}")
        # Prepare output file
        output_file = os.path.join(UPLOAD_DIR, f"output_{ctx.author.id}.mp4")
        if not any(arg.endswith(".mp4") for arg in sanitized_command):
            sanitized_command.append(output_file)

        # Run FFmpeg command asynchronously
        process = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-i", file_name,
            *sanitized_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if os.path.exists(output_file):
            file = discord.File(output_file)
            huhg = {}
            huhg["Video"] = adur
            huhg["Audio"] = vdur
            huhg["Speed used"] = speed
            huhg["Difference"] = diff
            view = FileLayout2(file, output_file, huhg)
            # "Command executed successfully."
            await loadMessage.delete()
            await asyncio.sleep(0.5)
            await ctx.reply(file=file,view=view.make())
            os.remove(output_file)
        else:
            await loadMessage.edit(content=f"> :x: Error executing command:\n```{stderr.decode()}```")

        if os.path.exists(file_name):
            os.remove(file_name)

    except Exception as e:
        if os.path.exists(file_name):
          os.remove(file_name)
        await loadMessage.edit(content=f"> :x: An error occurred: {str(e)}")
@bot.command(aliases=["fix","fixvideo"])
async def reencode(ctx):
    """
      Re-encodes a video. So it can work with bot commands properly.

      Usage: :reencode, :fix
    """
    loadMessage = await ctx.reply("> <a:load:1417523157824442599> Loading Video (1/3)", mention_author=False)
    file_names = [os.path.join(UPLOAD_DIR, f"output_{ctx.author.id}.mp4"),os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"input_{ctx.author.id}.mp4")]
    for i, v in enumerate(file_names):
      if os.path.exists(v):
        await loadMessage.edit(content="> :warning: You still have a process still running. Please wait.")
        return
    attachment_url = None
    # Check for attachments or replied media
    if ctx.message.reference:
        referenced_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if referenced_message.attachments:
            attachment_url = referenced_message.attachments[0].url
        else:
            extractor = URLExtract()
            urls = extractor.find_urls(referenced_message.content)
            if urls:
              attachment_url = urls[0]
        if not referenced_message.components == []:
          attachment_url = referenced_message.components[0].children[0].items[0].media.url
    if not attachment_url and ctx.message.attachments:
        attachment_url = ctx.message.attachments[0].url
    if not attachment_url:
      async for message in ctx.channel.history(limit=50):
        if message.attachments:
          attachment_url = message.attachments[0].url
          break
    if not attachment_url:
        await loadMessage.edit(content="> :x: Please provide a video attachment or link.")
        return
    else:
        await loadMessage.edit(content="> <a:load:1417523157824442599> Downloading Video (2/3)",allowed_mentions=discord.AllowedMentions(replied_user=False))
    try:
        # Download the file
        file_name = os.path.join(UPLOAD_DIR, f"input_{ctx.author.id}.mp4")
        await downloader.from_url(attachment_url,file_name)
        await loadMessage.edit(content="> <a:load:1417523157824442599> Reencoding Video (3/3)",allowed_mentions=discord.AllowedMentions(replied_user=False))
        sanitized_command = shlex.split("-c:v libx264 -crf 23 -preset medium -c:a aac -b:a 192k")
        # Prepare output file
        output_file = os.path.join(UPLOAD_DIR, f"output_{ctx.author.id}.mp4")
        if not any(arg.endswith(".mp4") for arg in sanitized_command):
            sanitized_command.append(output_file)

        # Run FFmpeg command asynchronously
        process = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-i", file_name,
            *sanitized_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if os.path.exists(output_file):
            file = discord.File(output_file)
            view = FileLayout(file, output_file)
            await loadMessage.delete()
            await asyncio.sleep(0.5)
            await ctx.reply(file=file,view=view.make())
            os.remove(output_file)
        else:
            await loadMessage.edit(content=f"> :x: Error executing command:\n```{stderr.decode()}```")

        if os.path.exists(file_name):
            os.remove(file_name)

    except Exception as e:
        if os.path.exists(file_name):
          os.remove(file_name)
        await loadMessage.edit(content=f"> :x: An error occurred: {str(e)}")
async def FFrun(i,co,o,time):
  try:
    # subprocess.run(shlex.split(f"ffmpeg -i {i} {co} -t {time} {o}"),check=True,capture_output=True)
    splitter = shlex.split(co)
    proc = await asyncio.create_subprocess_exec("ffmpeg","-i",i,*splitter,"-t",str(time),"-b:v","5000k",o,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
      print(f"Subprocess failed with exit code {proc.returncode}")
      print(f"Stderr: {stderr.decode().strip()}")
    # else:
      # print(f"Subprocess completed successfully.")
      # print(f"Stdout: {stdout.decode().strip()}")
  except Exception as e:
    print(str(e))
async def FFconcat(items,out):
  conc = "|".join(items)
  try:
    # subprocess.run(shlex.split(f'ffmpeg -i "concat:{conc}" {out}'),check=True,capture_output=True)
    proc = await asyncio.create_subprocess_exec("ffmpeg","-i",f"concat:{conc}",out,"-b:v","5000k","-c","copy",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
      print(f"Subprocess failed with exit code {proc.returncode}")
      print(f"Stderr: {stderr.decode().strip()}")
    # else:
      # print(f"Subprocess completed successfully.")
      # print(f"Stdout: {stdout.decode().strip()}")
  except Exception as e:
    print(str(e))
@bot.command()
async def ihtx(ctx,powers,time,usetemplate:bool,*,command):
    loadMessage = await ctx.reply("> <a:load:1417523157824442599> Loading Video (1/3)", mention_author=False)
    file_names = [os.path.join(UPLOAD_DIR, f"output_{ctx.author.id}.mp4"),os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"input_{ctx.author.id}.mp4")]
    for i, v in enumerate(file_names):
      if os.path.exists(v):
        await loadMessage.edit(content="> :warning: You still have a process still running. Please wait.")
        return
    attachment_url = None
    # Check for attachments or replied media
    if ctx.message.reference:
        referenced_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if referenced_message.attachments:
            attachment_url = referenced_message.attachments[0].url
        else:
            extractor = URLExtract()
            urls = extractor.find_urls(referenced_message.content)
            if urls:
              attachment_url = urls[0]
        if not referenced_message.components == []:
          attachment_url = referenced_message.components[0].children[0].items[0].media.url
    if not attachment_url and ctx.message.attachments:
        attachment_url = ctx.message.attachments[0].url
    if not attachment_url:
      async for message in ctx.channel.history(limit=50):
        if message.attachments:
          attachment_url = message.attachments[0].url
          break

    if not attachment_url:
        await loadMessage.edit(content="> :x: Please provide a video attachment or link.")
        return
    else:
        await loadMessage.edit(content="> <a:load:1417523157824442599> Downloading Video (2/3)",allowed_mentions=discord.AllowedMentions(replied_user=False))
    try:
        # Download the file
        file_name = os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"input_{ctx.author.id}.mp4")
        await downloader.from_url(attachment_url,file_name)
        await loadMessage.edit(content="> <a:load:1417523157824442599> Processing Video (3/3)",allowed_mentions=discord.AllowedMentions(replied_user=False))
        if usetemplate == False:
          sanitized_command = shlex.split(command)
          probet = FFprobe(file_name)
          w = probet["streams"][0]["width"]
          h = probet["streams"][0]["height"]
          fc = probet["streams"][0]["nb_frames"]
          vidlen = probet["streams"][0]["duration"]
          com = command.replace("$w",str(w))
          com = com.replace("$h",str(h))
          com = com.replace("$fc",str(fc))
          com = com.replace("$d",str(vidlen))
          time = str(vidlen) if time == "vidlen" else time
        # Prepare output file
          output_file = os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"ihtx_custom_{ctx.author.id}.mp4")
          powers = int(powers)
          await FFrun(file_name,com,os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"{ctx.author.id}_1{FILE_EXTENSION}"),time)
          files = []
          for i in range(powers):
            files.append(os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"{ctx.author.id}_{i+1}{FILE_EXTENSION}"))
          for i, v in enumerate(files):
            await FFrun(v,com,os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"{ctx.author.id}_{i+2}{FILE_EXTENSION}"),time)
          await FFconcat(files,output_file)
          for i in range(powers+1):
            if os.path.exists(os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"{ctx.author.id}_{i+1}{FILE_EXTENSION}")):
                os.remove(os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"{ctx.author.id}_{i+1}{FILE_EXTENSION}"))
          # if os.path.exists(output_file):
            # file = discord.File(output_file)
            # view = FileLayout(file, output_file)
            # "Command executed successfully."
            # await loadMessage.delete()
            # await asyncio.sleep(0.5)
            # await ctx.reply(file=file,view=view.make())
            # os.remove(output_file)
            # os.remove(file_name)
          # else:
          #   os.remove(file_name)
          #   await loadMessage.edit(content="> :x: Error executing command")
        else:
          c.execute('SELECT content FROM templates WHERE guild_id = ? AND name = ?', (ctx.guild.id, command))
          result = c.fetchone()
          if result:
            probet = FFprobe(file_name)
            w = probet["streams"][0]["width"]
            h = probet["streams"][0]["height"]
            fc = probet["streams"][0]["nb_frames"]
            vidlen = probet["streams"][0]["duration"]
            com = result[0].replace("$w",str(w))
            com = com.replace("$h",str(h))
            com = com.replace("$fc",str(fc))
            com = com.replace("$d",str(vidlen))
            time = str(vidlen) if time == "vidlen" else time
            # Prepare output file
            output_file = os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"ihtx_custom_{ctx.author.id}.mp4")
            powers = int(powers)
            await FFrun(file_name,com,os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"{ctx.author.id}_1{FILE_EXTENSION}"),time)
            files = []
            for i in range(powers):
              files.append(os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"{ctx.author.id}_{i+1}{FILE_EXTENSION}"))
            for i, v in enumerate(files):
              await FFrun(v,com,os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"{ctx.author.id}_{i+2}{FILE_EXTENSION}"),time)
            await FFconcat(files,output_file)
            for i in range(powers+1):
              if os.path.exists(os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"{ctx.author.id}_{i+1}{FILE_EXTENSION}")):
                os.remove(os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"{ctx.author.id}_{i+1}{FILE_EXTENSION}"))
          else:
            os.remove(file_name)
            await loadMessage.edit(content="> :x: Template does not exist.")
        if os.path.exists(output_file):
          if not FileBiggerThan(10.0,output_file):
            file = discord.File(output_file)
            view = FileLayout(file, output_file)
            await loadMessage.delete()
            await asyncio.sleep(0.5)
            await ctx.reply(file=file,view=view.make())
            os.remove(output_file)
            os.remove(file_name)
          else:
            catbox_url = catbox_upload(output_file)
            await loadMessage.delete()
            await asyncio.sleep(0.5)
            await ctx.reply(f"> Since the video was over 10MB it got uploaded over to Catbox.\n{catbox_url}")
            os.remove(output_file)
            os.remove(file_name)
        else:
          os.remove(file_name)
          await loadMessage.edit(content="> :x: Error executing command")
    except Exception as e:
        if os.path.exists(file_name):
          os.remove(file_name)
        await loadMessage.edit(content=f"> :x: An error occurred: {str(e)}")
@bot.command(aliases=["fe,fec,first,first_export_custom"])
async def first_export(ctx,time):
    """
      Trims the video to the first export by a specified duration.
    """
    loadMessage = await ctx.reply("> <a:load:1417523157824442599> Loading Video (1/3)", mention_author=False)
    file_names = [os.path.join(UPLOAD_DIR, f"output_{ctx.author.id}.mp4"),os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"input_{ctx.author.id}.mp4")]
    for i, v in enumerate(file_names):
      if os.path.exists(v):
        await loadMessage.edit(content="> :warning: You still have a process still running. Please wait.")
        return
    attachment_url = None
    # Check for attachments or replied media
    if ctx.message.reference:
        referenced_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if referenced_message.attachments:
            attachment_url = referenced_message.attachments[0].url
        if not referenced_message.components == []:
          attachment_url = referenced_message.components[0].children[0].items[0].media.url
    if not attachment_url and ctx.message.attachments:
        attachment_url = ctx.message.attachments[0].url

    if not attachment_url:
        await loadMessage.edit(content="> :x: Please provide a video attachment or link.")
        return
    else:
        await loadMessage.edit(content="> <a:load:1417523157824442599> Downloading Video (2/3)",allowed_mentions=discord.AllowedMentions(replied_user=False))
    try:
        # Download the file
        file_name = os.path.join(UPLOAD_DIR, f"input_{ctx.author.id}.mp4")
        await downloader.from_url(attachment_url,file_name)
        await loadMessage.edit(content="> <a:load:1417523157824442599> Processing Video (3/3)",allowed_mentions=discord.AllowedMentions(replied_user=False))
        output_file = os.path.join(UPLOAD_DIR, f"output_{ctx.author.id}.mp4")
        subprocess.run(shlex.split(f"ffmpeg -i {file_name} -t {time} {output_file}"),check=True,capture_output=True)
        if os.path.exists(output_file):
            file = discord.File(output_file)
            view = FileLayout(file, output_file)
            await loadMessage.delete()
            await asyncio.sleep(0.5)
            await ctx.reply(file=file,view=view.make())
            os.remove(output_file)
            os.remove(file_name)
        else:
            os.remove(file_name)
            await loadMessage.edit(content="> :x: Error executing command")
    except Exception as e:
        await loadMessage.edit(content=f"> :x: An error occurred: {str(e)}")
@bot.command(aliases=["le","lec","last","last_export_custom"])
async def last_export(ctx,time):
    """
      Trims the video to the last export by a specified duration.
    """
    loadMessage = await ctx.reply("> <a:load:1417523157824442599> Loading Video (1/3)", mention_author=False)
    file_names = [os.path.join(UPLOAD_DIR, f"output_{ctx.author.id}.mp4"),os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"input_{ctx.author.id}.mp4")]
    for i, v in enumerate(file_names):
      if os.path.exists(v):
        await loadMessage.edit(content="> :warning: You still have a process still running. Please wait.")
        return
    attachment_url = None
    # Check for attachments or replied media
    if ctx.message.reference:
        referenced_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if referenced_message.attachments:
            attachment_url = referenced_message.attachments[0].url
        if not referenced_message.components == []:
          attachment_url = referenced_message.components[0].children[0].items[0].media.url
    if not attachment_url and ctx.message.attachments:
        attachment_url = ctx.message.attachments[0].url

    if not attachment_url:
        await loadMessage.edit(content="> :x: Please provide a video attachment or link.")
        return
    else:
        await loadMessage.edit(content="> <a:load:1417523157824442599> Downloading Video (2/3)",allowed_mentions=discord.AllowedMentions(replied_user=False))
    try:
        # Download the file
        file_name = os.path.join(UPLOAD_DIR, f"input_{ctx.author.id}.mp4")
        await downloader.from_url(attachment_url,file_name)
        await loadMessage.edit(content="> <a:load:1417523157824442599> Processing Video (3/3)",allowed_mentions=discord.AllowedMentions(replied_user=False))
        output_file = os.path.join(UPLOAD_DIR, f"output_{ctx.author.id}.mp4")
        subprocess.run(shlex.split(f"ffmpeg -i {file_name} -vf reverse,trim=0:{time},reverse -af areverse,atrim=0:{time},areverse {output_file}"),check=True,capture_output=True)
        if os.path.exists(output_file):
            file = discord.File(output_file)
            view = FileLayout(file, output_file)
            await loadMessage.delete()
            await asyncio.sleep(0.5)
            await ctx.reply(file=file,view=view.make())
            os.remove(output_file)
            os.remove(file_name)
        else:
            os.remove(file_name)
            await loadMessage.edit(content="> :x: Error executing command")
    except Exception as e:
        await loadMessage.edit(content=f"> :x: An error occurred: {str(e)}")
@bot.command()
async def invite(ctx):
  """
    Invite the bot to your server or use anywhere!
  """
  await ctx.reply(f"[Click here to invite the bot anywhere!]({invitelink})",mention_author=False)
@bot.command()
async def interpolate(ctx):
    """
      Interpolates a video to 60 FPS.
    """
    loadMessage = await ctx.reply("> <a:load:1417523157824442599> Loading Video (1/3)", mention_author=False)
    file_names = [os.path.join(UPLOAD_DIR, f"output_{ctx.author.id}.mp4"),os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"input_{ctx.author.id}.mp4")]
    for i, v in enumerate(file_names):
      if os.path.exists(v):
        await loadMessage.edit(content="> :warning: You still have a process still running. Please wait.")
        return
    attachment_url = None
    # Check for attachments or replied media
    if ctx.message.reference:
        referenced_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if referenced_message.attachments:
            attachment_url = referenced_message.attachments[0].url
        if not referenced_message.components == []:
          attachment_url = referenced_message.components[0].children[0].items[0].media.url
    if not attachment_url and ctx.message.attachments:
        attachment_url = ctx.message.attachments[0].url

    if not attachment_url:
        await loadMessage.edit(content="> :x: Please provide a video attachment or link.")
        return
    else:
        await loadMessage.edit(content="> <a:load:1417523157824442599> Downloading Video (2/3)",allowed_mentions=discord.AllowedMentions(replied_user=False))
    try:
        # Download the file
        file_name = os.path.join(UPLOAD_DIR, f"input_{ctx.author.id}.mp4")
        await downloader.from_url(attachment_url,file_name)
        await loadMessage.edit(content="> <a:load:1417523157824442599> Processing Video (3/3)",allowed_mentions=discord.AllowedMentions(replied_user=False))
        output_file = os.path.join(UPLOAD_DIR, f"output_{ctx.author.id}.mp4")
        subprocess.run(shlex.split(f'ffmpeg -i {file_name} -vf "fps=30,minterpolate=mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=60" {output_file}'),check=True,capture_output=True)
        if os.path.exists(output_file):
            file = discord.File(output_file)
            view = FileLayout(file, output_file)
            await loadMessage.delete()
            await asyncio.sleep(0.5)
            await ctx.reply(file=file,view=view.make())
            os.remove(output_file)
            os.remove(file_name)
        else:
            os.remove(file_name)
            await loadMessage.edit(content="> :x: Error executing command")
    except Exception as e:
        await loadMessage.edit(content=f"> :x: An error occurred: {str(e)}")
@bot.command(name='createtemplate',aliases=["addtemplate"])
async def create_template(ctx, name: str, *, content: str):
    try:
        # Store the user's ID
        c.execute('INSERT INTO templates (guild_id, name, content, user_id) VALUES (?, ?, ?, ?)', (ctx.guild.id, name, content, ctx.author.id))
        conn.commit()
        await ctx.send(f'> Successfully created template `{name}`')
    except sqlite3.IntegrityError:
        await ctx.send(f'> A template with the name `{name}` already exists.')
@bot.command()
async def template(ctx, name: str, *, args: str=""):
    c.execute('SELECT content FROM templates WHERE guild_id = ? AND name = ?', (ctx.guild.id, name))
    result = c.fetchone()
    if result:
        processed_content = parse.TemplateParse(result[0],args)
        await ctx.send(processed_content)
    else:
        await ctx.send(f'Template `{name}` not found.')
@bot.command()
async def viewtemplate(ctx, name: str):
    c.execute('SELECT content FROM templates WHERE guild_id = ? AND name = ?', (ctx.guild.id, name))
    result = c.fetchone()
    if result:
        embed = discord.Embed(title=name,description=f"```{result[0]}```",color=theme)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f'Template `{name}` not found.')
@bot.command(name='edittemplate')
async def edit_template(ctx, name: str, *, new_content: str):
    # The WHERE clause now includes user_id
    c.execute('UPDATE templates SET content = ? WHERE guild_id = ? AND name = ? AND user_id = ?', (new_content, ctx.guild.id, name, ctx.author.id))
    conn.commit()
    if c.rowcount > 0:
        await ctx.send(f'Template `{name}` updated successfully!')
    else:
        # Check if the template exists at all to provide better feedback
        c.execute('SELECT user_id FROM templates WHERE guild_id = ? AND name = ?', (ctx.guild.id, name))
        result = c.fetchone()
        if result:
            await ctx.send(f'You are not the owner of the template `{name}`.')
        else:
            await ctx.send(f'Could not find a template named `{name}` to update.')
@bot.command(name='removetemplate')
async def remove_template(ctx, name: str):
    # The DELETE statement now includes the user_id for an ownership check
    c.execute('DELETE FROM templates WHERE guild_id = ? AND name = ? AND user_id = ?', (ctx.guild.id, name, ctx.author.id))
    conn.commit()
    
    if c.rowcount > 0:
        await ctx.send(f'Template `{name}` removed successfully!')
    else:
        # Check if the template exists at all to provide better feedback
        c.execute('SELECT user_id FROM templates WHERE guild_id = ? AND name = ?', (ctx.guild.id, name))
        result = c.fetchone()
        if result:
            await ctx.send(f'You are not the owner of the template `{name}`.')
        else:
            await ctx.send(f'Could not find a template named `{name}` to remove.')
@bot.command(name='templatelist')
async def template_list(ctx, user: discord.Member = None):
    """Lists templates for the current server or a specific user."""
    embed = discord.Embed(title="Server Templates", color=theme)
    
    if user:
        # Fetch templates for a specific user
        c.execute('SELECT name FROM templates WHERE guild_id = ? AND user_id = ?', (ctx.guild.id, user.id))
        user_templates = c.fetchall()
        
        if user_templates:
            # Format the user's templates into a readable string
            template_names = [f"`{t[0]}`" for t in user_templates]
            embed.add_field(name=f"Templates by {user.display_name}", value=", ".join(template_names), inline=False)
        else:
            embed.add_field(name=f"Templates by {user.display_name}", value="No templates found for this user.", inline=False)
    else:
        # Fetch all templates for the server
        c.execute('SELECT name, user_id FROM templates WHERE guild_id = ?', (ctx.guild.id,))
        all_templates = c.fetchall()
        
        if all_templates:
            user_templates_map = {}
            for name, user_id in all_templates:
                if user_id not in user_templates_map:
                    user_templates_map[user_id] = []
                user_templates_map[user_id].append(f"`{name}`")
            
            # Add fields for each user's templates
            for user_id, templates in user_templates_map.items():
                member = ctx.guild.get_member(user_id)
                user_name = member.display_name if member else f"User ID: {user_id}"
                embed.add_field(name=f"Templates by {user_name}", value=", ".join(templates), inline=False)
        else:
            embed.description = "No templates found for this server."
    await ctx.reply(embed=embed,mention_author=False)
@bot.command(aliases=["dl","ytdl"])
async def download(ctx, url:str):
    """
      Downloads YouTube videos.

      Usage:
        :download https://youtu.be/8gklmIIyOVQ
        :download https://youtube.com/watch?v=90U0dYQDft0
    """
    loadMessage = await ctx.reply("> <a:load:1417523157824442599> Loading Video (1/2)", mention_author=False)
    file_names = [os.path.join(UPLOAD_DIR, f"output_{ctx.author.id}.mp4"),os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"input_{ctx.author.id}.mp4")]
    for i, v in enumerate(file_names):
      if os.path.exists(v):
        await loadMessage.edit(content="> :warning: You still have a process still running. Please wait.")
        return
    attachment_url = None
    # Check for attachments or replied media
    if ctx.message.reference:
        referenced_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        extractor = URLExtract()
        urls = extractor.find_urls(referenced_message.content)
        if urls:
            attachment_url = urls[0]
    if not attachment_url:
        attachment_url = url

    if not attachment_url:
        await loadMessage.edit(content="> :x: Please provide a YouTube link.")
        return
    else:
        await loadMessage.edit(content="> <a:load:1417523157824442599> Downloading Video (2/2)",allowed_mentions=discord.AllowedMentions(replied_user=False))
    opts = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best','outtmpl': 'downloads/youtube-%(id)s.%(ext)s'}
    try:
      with YoutubeDL(opts) as ydl:
        await asyncio.to_thread(ydl.download,[url])
      if (yid := getyoutubeid(url)):
        print(yid)
        formatted = f"./downloads/youtube-{yid}.mp4"
      if os.path.exists(formatted):
        file = discord.File(formatted)
        view = FileLayout(file, formatted)
        await loadMessage.delete()
        await asyncio.sleep(0.5)
        await ctx.reply(file=file,view=view.make())
        os.remove(formatted)
      else:
        await loadMessage.edit(content="> :x: Error locating file.")
        if os.path.exists(formatted):
          os.remove(formatted)
    except Exception as e:
      await loadMessage.edit(content=f"Error: {e}")
    

# end of commands
# start of slash commands

@bot.tree.command(name="invite",description="sends a invite to the current channel to invite the bot.")
async def invite(interaction: discord.Interaction, hide:bool=False):
  await interaction.response.send_message(f"[Click here to invite the bot anywhere!]({invitelink})",ephemeral=hide)

@bot.tree.command(name="command",description="burps")
async def ffmpeg(i:discord.Interaction,video:discord.Attachment,command:str):
    """
    Execute an FFmpeg command on a Discord video link, uploaded file, or reply.
    Example usage: !ffmpeg -vf "scale=320:240"
    """
    await i.response.defer()
    attachment_url = video.url
    # Check for attachments or replied media

    try:
        # Download the file
        file_name = os.path.join(UPLOAD_DIR, f"input_{i.user.id}.mp4")
        async with aiohttp.ClientSession() as session:
            async with session.get(attachment_url) as response:
                if response.status == 200:
                    with open(file_name, "wb") as f:
                        f.write(await response.read())
                else:
                    await i.followup.send("Failed to download the video.")
                    return

        sanitized_command = shlex.split(command)

        # Prepare output file
        output_file = os.path.join(UPLOAD_DIR, f"output_{i.user.id}.mp4")
        if not any(arg.endswith(".mp4") for arg in sanitized_command):
            sanitized_command.append(output_file)

        # Run FFmpeg command asynchronously
        process = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-i", file_name,
            *sanitized_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if os.path.exists(output_file):
            file = discord.File(output_file)
            view = FileLayout(file, output_file)
            await i.followup.send(file=file,view=view.make())
            os.remove(output_file)
        else:
            await i.followup.send(f"Error executing command:\n```{stderr.decode()}```")

        if os.path.exists(file_name):
            os.remove(file_name)

    except Exception as e:
        await i.followup.send(f"An error occurred: {str(e)}")
@bot.tree.command(name="ihtx",description="does an ihtx on a video with a command and time and powers.")
async def ihtx(interaction:discord.Interaction,video:discord.Attachment,command:str,powers:app_commands.Range[int,1,100],time:float=0.5):
    await interaction.response.defer()
    attachment_url = video.url
    file_names = [os.path.join(UPLOAD_DIR, f"output_{interaction.user.id}.mp4"),os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"input_{interaction.user.id}.mp4")]
    for i, v in enumerate(file_names):
      if os.path.exists(v):
        await interaction.followup.send("> :warning: You still have a process still running. Please wait.")
        return
    try:
        # Download the file
        file_name = os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"input_{interaction.user.id}.mp4")
        await downloader.from_url(attachment_url,file_name)
        probet = FFprobe(file_name)
        w = probet["streams"][0]["width"]
        h = probet["streams"][0]["height"]
        fc = probet["streams"][0]["nb_frames"]
        command = command.replace("$w",str(w))
        command = command.replace("$h",str(h))
        command = command.replace("$fc",str(fc))
        sanitized_command = shlex.split(command)
        # Prepare output file
        output_file = os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"ihtx_custom_{interaction.user.id}.mp4")
        # powers = int(powers)
        await FFrun(file_name,command,os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"{interaction.user.id}_1{FILE_EXTENSION}"),time)
        files = []
        for i in range(powers):
            files.append(os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"{interaction.user.id}_{i+1}{FILE_EXTENSION}"))
        for i, v in enumerate(files):
            await FFrun(v,command,os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"{interaction.user.id}_{i+2}{FILE_EXTENSION}"),time)
        await FFconcat(files,output_file)
        for i in range(powers+1):
            if os.path.exists(os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"{interaction.user.id}_{i+1}{FILE_EXTENSION}")):
                os.remove(os.path.join(os.path.join(UPLOAD_DIR,"ihtx"), f"{interaction.user.id}_{i+1}{FILE_EXTENSION}"))
        if os.path.exists(output_file):
            file = discord.File(output_file)
            view = FileLayout(file, output_file)
            # "Command executed successfully."
            await interaction.followup.send(file=file,view=view.make())
            os.remove(output_file)
            os.remove(file_name)
        else:
            os.remove(file_name)
            await interaction.followup.send("> :x: Error executing command")
    except Exception as e:
        await interaction.followup.send(content=f"> :x: An error occurred: {str(e)}")
# end of slash commands
bot.run(bottoken, log_handler=handler, log_level=logging.WARNING)
