from discord.ext import commands
from db import db, mydb
import setup_db
from decouple import config
import discord

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
token = config('token')


@bot.event
async def on_ready():
    setup_db.initialize()
    guilds = ", ".join(bot.guilds) if len(bot.guilds) > 1 else bot.guilds[0]
    Users = []
    Bots = []
    for user in bot.users:
        if user.bot:
            Bots.append(user.name)
        else:
            db.execute(f"select * from users where id={user.id}")
            user_id = db.fetchall()
            if len(user_id) == 0:
                db.execute(
                    f"insert into users values({user.id}, '{user.name}')")
                mydb.commit()
            Users.append(user.name)

    users = ", ".join(Users)
    bots = ", ".join(Bots) if len(Bots) > 1 else Bots[0]

    status = f'''
    
============================================================
Discord.py Version : {discord.__version__}

...Successfully Connected...

+- Connected to ({bot.user}): {guilds}

+- Bots  ({len(Bots)}): 
            {bots}
+- Users ({len(Users)}): 
            {users}
============================================================

'''
    print(status)


@bot.event
async def on_member_join(ctx, member: discord.Member):
    print(f"New Member! -- {member.name}")
    welcome_chan = bot.get_channel(950546370861875222)

    embed = discord.Embed(
        title=f"Welcome {member.name}",
        color=0xd4af37,
        description=f"{member.name} has joined the Lolol Crew! :tada: Welcome and enjoy your stay!"
    )
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(
        text="Lolol Official",
        icon_url=
        "https://raw.githubusercontent.com/v8ive/LololBot/master/img/lolol_pfp.png"
    )

    db.execute(f"insert into users values({member.id}, '{member.name}')")
    mydb.commit()

    await welcome_chan.send(embed=embed)


if __name__ == "__main__":
    cogs = []
    for cog in cogs:
        bot.load_extension(cog)

bot.run(token)
