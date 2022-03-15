from discord.ext import commands
from db_connect import db, mydb
from decouple import config
import discord

intents = discord.Intents().all()
bot = commands.Bot(command_prefix = "!", intents=intents, help_command=None)
token = config('token')

@bot.event
async def on_ready():
    db.execute(f"create table if not exists users(id bigint not null primary key, name varchar(100) not null)")
    mydb.commit()
    guilds = ", ".join(bot.guilds) if len(bot.guilds) > 1 else bot.guilds[0]
    users = []
    bots = []
    for user in bot.users:        
        if user.bot:
            bots.append(user.name)
        else:
            db.execute(f"select * from users where id={user.id}")
            user_id = db.fetchall()
            if len(user_id) == 0:
                db.execute(f"insert into users values({user.id}, '{user.name}')")
                mydb.commit()
            users.append(user.name)
            
    users = ", ".join(users)
    bots = ", ".join(bots) if len(bots) > 1 else bots[0]
    
    status = f'''
Discord.py Version : {discord.__version__}

Successfully Connected...

Connected to ({bot.user}): {guilds}

Bots  ({len(bots)}): {bots}
Users ({len(users)}): {users}

'''
    print(status)

@bot.event
async def on_member_join(ctx, member:discord.Member):
    welcome_chan = bot.get_channel(950546370861875222)
    
    embed = discord.Embed(title=f"Welcome {member.name}", color=0xd4af37, description=f"{member.name} has joined the Lolol Crew! :tada: Welcome!")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text="Lolol Official", icon_url="https://raw.githubusercontent.com/v8ive/LololBot/master/img/lolol_pfp.png")
    
    db.execute(f"insert into users values({member.id}, '{member.name}')")
    mydb.commit()
            
    await welcome_chan.send(embed=embed)

if __name__ == "__main__":
    cogs = []
    for cog in cogs:
        bot.load_extension(cog)

bot.run(token)