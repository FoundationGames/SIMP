import discord
from discord.ext import commands

# requires "opencv-python", "natsort", "tdqm"
from pyCAIR import user_input, cropByColumn

from PIL import Image

import json
import math

bot_config = {"bot_token": "","cmd_prefix":"s#"}

with open("bot_config.json") as f:
    bot_config = json.load(f)

intents = discord.Intents.default()

bot = commands.Bot(command_prefix=bot_config["cmd_prefix"], intents=intents)

token = bot_config["bot_token"]

@bot.event
async def on_ready():
    print("SIMP is online")

def optimize_image():
    img = Image.open("processing/in.png")
    w, h = img.size
    optimize = False
    if w > 256:
        h = int((256 / w) * h)
        w = 256
        optimize = True
    if h > 256:
        w = int((256 / h) * w)
        h = 256
        optimize = True
    if optimize:
        img = img.resize((w, h))
        img.save("processing/in.png")

async def save_image(ctx, user) -> bool:
    attachments = ctx.message.attachments
    if not user is None:
        await user.avatar_url_as(format="png", size=256).save("processing/in.png")
        return True
    if len(attachments) > 0:
        if attachments[0].filename.lower().endswith(".png"):
            await attachments[0].save("processing/in.png")
        else:
            await ctx.send("Must be a .png file")
            return False
    else:
        await ctx.author.avatar_url_as(format="png", size=256).save("processing/in.png")
    return True

# COMMANDS ---------------------------------------------------------

busy = False

@bot.command()
async def about(ctx):
    embed = discord.Embed()
    embed.title = "Specialized Image Manipulation Program"
    embed.description = "A Discord bot for performing simple, specialized image manipulation tasks."
    await ctx.send(embed=embed)

@bot.command(aliases=["cas", "cair"])
async def contentawarescale(ctx, amount: float, axis: str = "", user: discord.Member = None):
    global busy

    if busy:
        await ctx.send("**Busy at the moment.**")
        return
    
    busy = True

    saved = await save_image(ctx, user)

    if not saved:
        return

    if amount > 1: amount = 1
    if amount < 0: amount = 0

    axis = axis.lower()

    naxis = 0
    out_file_name = "results/in/column_cropped.png"
    if axis == "y":
        naxis = 1
        out_file_name = "results/in/row_cropped.png"

    await ctx.send("**Processing has started.** This will take a few minutes.")
    try:
        optimize_image()
        with open(out_file_name, "w") as h:
            pass
        user_input(alignment = naxis, scale = amount, display_seam = 1, image = "processing/in.png", generate = 0)
    except Exception as e:
        await ctx.send("An error occurred while processing.")
        print(e)
        return

    embed = discord.Embed()
    embed.title = "Content-Aware Scaled Image"
    with open(out_file_name, "rb") as img:
        await ctx.send(embed=embed,file=discord.File(img, "result.png"))
    
    busy = False

# ------------------------------------------------------------------

bot.run(token)