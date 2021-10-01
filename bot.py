import discord
from discord.ext import commands
from discord.utils import get
import sys
import sqlite3
from rank import get_rank
from config import token

ALLOWED_TO_DELETE = [
    "Empty",
    "Herald",
    "Guardian",
    "Crusader",
    "Archon",
    "Legend",
    "Ancient",
    "Divine",
    "Immortal",
    "Immortal,",
    "Unranked",
    ]

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
    
    # add deleting role function
    
    await ctx.channel.send("<@{}> Your DotaID was deleted".format(ctx.message.author.id))

@bot.command()
@commands.has_permissions(manage_roles=True)
async def link_id(ctx, *args):
    
    user = ctx.message.author
    
    if not channel_name == ctx.channel.name:
        return
    
    if len(args) != 1:
        await ctx.channel.send("<@{}> this command needs only your DotaID".format(user.id))
        return

    user_id = cur.execute("SELECT dota_id FROM users WHERE user_id = ?;", (user.id,) ).fetchone()

    if not user_id or user_id[0] == None:
        cur.execute("INSERT INTO users VALUES(?, ?)", (user.id, args[0]))
        user_id = (args[0], )
        await ctx.channel.send("<@{}> your DotaID was linked".format(user.id))
    else:
        cur.execute("UPDATE users SET dota_id = ? WHERE user_id = ?", (args[0], user.id))
        await ctx.channel.send("<@{}> your DotaID was updated".format(user.id))
    conn.commit()
    
    needed_rank = get_rank(user_id[0])
    for i in user.roles:
        # print("\n___________________\n", i.name, "\n___________________\n")
        if i.name not in ALLOWED_TO_DELETE:
            continue
        role = get(user.guild.roles, id = i.id)
        await user.remove_roles(role)
    
    role = get(user.guild.roles, name = needed_rank)
    if role == None:
        await user.guild.create_role(name = needed_rank)
        role = get(user.guild.roles, name = needed_rank)
    await user.add_roles(role)

@bot.command()
async def update_rank(ctx, *args):
    
    user = ctx.message.author
    
    if not channel_name == ctx.channel.name:
        return
    
    if len(args) > 0:
        await ctx.channel.send("<@{}> this command have to be empty".format(ctx.message.author.id))
        return

    user_id = cur.execute("SELECT dota_id FROM users WHERE user_id = ?;", (ctx.message.author.id,) ).fetchone()

    if not user_id or user_id[0] == None:
        await ctx.channel.send("<@{}> you dont have linked id YET!".format(ctx.message.author.id))
        return

    needed_rank = get_rank(user_id[0])
    
    for i in user.roles:
        if i.name not in ALLOWED_TO_DELETE:
            continue
        role = get(user.guild.roles, id = i.id)
        await user.remove_roles(role)
    
    role = get(user.guild.roles, name = needed_rank)
    
    if role == None:
        await user.guild.create_role(name = needed_rank)
        role = get(user.guild.roles, name = needed_rank)
    
    await user.add_roles(role)
    await ctx.channel.send("<@{}> Your DotaID rank was updated".format(ctx.message.author.id))

# @bot.command()
# async def test(ctx, *args):
#     user = ctx.message.author
#     # role = get(user.guild.roles, name = "Test role")
#     # await user.guild.create_role(name = "Lol Kek")
#     # await user.remove_roles(role)
#     # await user.add_roles(role)
#     roles = user.guild.roles
#     for role in roles:
#         print("\n___________________\n", role.name, "\n___________________\n")
#     # print("\n________ROLES___________________\n")
#     # print(user.roles)
#     # print("\n_________________________\n")

bot.run(token)



