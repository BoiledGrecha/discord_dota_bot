import discord
from discord.ext import commands
import sys
import sqlite3
from rank import get_rank
from config import token


try:
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
except:
    print("Something wrong with database")
    sys.exit()

bot = commands.Bot(command_prefix="!")
channel_name = "авторизация"

@bot.event
async def on_ready():
    print("STARTED!")

@bot.command()
async def show_id(ctx, *args):
    if not channel_name == ctx.channel.name:
        return
    
    if len(args) > 0:
        await ctx.channel.send("<@{}> this command have to be empty".format(ctx.message.author.id))
        return
    
    user_id = cur.execute("SELECT dota_id FROM users WHERE user_id = ?;", (ctx.message.author.id, ) ).fetchone()
    
    if not user_id or user_id[0] == None:
        await ctx.channel.send("<@{}> you dont have linked id YET!".format(ctx.message.author.id))
        return

    await ctx.channel.send("<@{}> your DotaID is {}".format(ctx.message.author.id, user_id[0]))    
    
@bot.command()
async def delete_id(ctx, *args):
    
    if not channel_name == ctx.channel.name:
        return
    
    if len(args) > 0:
        await ctx.channel.send("<@{}> this command have to be empty".format(ctx.message.author.id))
        return

    user_id = cur.execute("SELECT dota_id FROM users WHERE user_id = ?;", (ctx.message.author.id,) ).fetchone()

    if not user_id or user_id[0] == None:
        await ctx.channel.send("<@{}> you dont have linked id YET!".format(ctx.message.author.id))
        return

    cur.execute("DELETE FROM users WHERE user_id = ?;", (ctx.message.author.id, ))
    conn.commit()

    await ctx.channel.send("<@{}> Your DotaID was deleted".format(ctx.message.author.id))

@bot.command()
async def link_id(ctx, *args):
    
    if not channel_name == ctx.channel.name:
        return
    
    if len(args) != 1:
        await ctx.channel.send("<@{}> this command needs only your DotaID".format(ctx.message.author.id))
        return

    user_id = cur.execute("SELECT dota_id FROM users WHERE user_id = ?;", (ctx.message.author.id,) ).fetchone()

    if not user_id or user_id[0] == None:
        cur.execute("INSERT INTO users VALUES(?, ?)", (ctx.message.author.id, args[0]))
        await ctx.channel.send("<@{}> your DotaID was linked".format(ctx.message.author.id))
    else:
        cur.execute("UPDATE users SET dota_id = ? WHERE user_id = ?", (args[0], ctx.message.author.id))
        await ctx.channel.send("<@{}> your DotaID was updated".format(ctx.message.author.id))
    conn.commit()

@bot.command()
async def test(ctx, *args):
    # if ctx.author == bot.user:
    #     print(" here ")
    #     return
    # if len(args) > 0:
    #     await ctx.channel.send("no words after \'test\' required")
    # else:
    #     await ctx.channel.send("Check check")
    
    # print(dir(ctx))
    await ctx.channel.send("<@{}>, hi".format(ctx.message.author.id))
    print("_______________")
    print("Channel")
    print(dir(ctx.message.channel.name))
    print("_______________")
    print("---------------Author---------------")
    print("Bot")
    print(ctx.message.author.bot)
    print("ID")
    print(ctx.message.author.id)
    print("_______________")
    print(args)

bot.run(token)