
from discord.ext import commands
import discord, random, db
import db as DB

db, mydb = DB.get_main()

class levelling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mediaChan = [954657087449890816]

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return

        elif ctx.content.startswith('$'):
            return

        def generateXP():
                messBonus = int((len(ctx.clean_content)/100)*5)
                rand = random.randint(1, 10)
                XP = rand + messBonus
                return XP

        xp = generateXP()

        db.execute(f"SELECT xp FROM users where id = {ctx.author.id}")
        userXP = db.fetchall()
        userXP = int(userXP[0][0])
        db.execute(f"SELECT lun FROM users where id = {ctx.author.id}")
        userLun = db.fetchall()
        userLun = int(userLun[0][0])

        newXP = userXP + xp
        pXP = "{:,}".format(newXP)

        def check_tier():
            if newXP < 100 and userXP < 100:
                tier = '7'
            if 100 <= newXP < 500:
                tier = '6'
            if 500 <= newXP < 1000:
                tier = '5'
            if 1000 <= newXP < 5000:
                tier = '4'
            if 5000 <= newXP < 10000:
                tier = '3'
            if 10000 <= newXP < 20000:
                tier = '2'
            if 20000 <= newXP:
                tier = '1'
            if 25000 <= newXP:
                tier = '0'
            if 50000 <= newXP:
                tier = 'Lolol Fanatic'
            if 100000 <= newXP:
                tier = 'Lolol Lord'
            return tier
        tier = check_tier()

        lounge = self.bot.get_channel(945829687878357072)

        if newXP > 100:
            if userXP < 100:
                await lounge.send(f":tada: Congrats {ctx.author.mention}! You're now Tier {tier}!\nCurrent XP: {pXP}xp.")
            if newXP > 500 and userXP < 500:
                await lounge.send(f":tada: Congrats {ctx.author.mention}! You're now Tier {tier}!\nCurrent XP: {pXP}xp.")
            if newXP > 1000 and userXP < 1000:
                await lounge.send(f":tada: Congrats {ctx.author.mention}! You're now Tier {tier}!\nCurrent XP: {pXP}xp.")
            if newXP > 5000 and userXP < 5000:
                await lounge.send(f":tada: Congrats {ctx.author.mention}! You're now Tier {tier}!\nCurrent XP: {pXP}xp.")
            if newXP > 10000 and userXP < 10000:
                await lounge.send(f":tada: Congrats {ctx.author.mention}! You're now Tier {tier}!\nCurrent XP: {pXP}xp.")
            if newXP > 20000 and userXP < 20000:
                await lounge.send(f":tada: Congrats {ctx.author.mention}! You're now Tier {tier}!\nCurrent XP: {pXP}xp.")
            if newXP > 25000 and userXP < 25000:
                await lounge.send(f":tada: Congrats {ctx.author.mention}, you're over 25,000xp! Thank you for being such an active member of the Lolol Community!\nCurrent: {pXP}xp.")

        db.execute(f'UPDATE users SET xp = {newXP} WHERE id = {ctx.author.id}')
        mydb.commit()
        db.execute(f'UPDATE users SET tier = {tier} WHERE id = {ctx.author.id}')
        mydb.commit()

        if len(ctx.attachments)>0:
            if ctx.channel.id in self.mediaChan:
                pics =  f' [{len(ctx.attachments)} pics] '
                if len(ctx.attachments)>1:
                    s = 's'
                else:
                    s = ''
                lunEarn = 10000*len(ctx.attachments)
                prettyEarn = "{:,}".format(lunEarn)
                await ctx.channel.send(f"🔥 Sent {prettyEarn} Lun to {ctx.author.name} for {len(ctx.attachments)} picture{s}")
            else:
                lunEarn = 100
                pics = ' '
        else:
                lunEarn = 100
                pics = ' '

        newUserLun = userLun + lunEarn
        pNewUserLun = "{:,}".format(newUserLun) 

        db.execute(f"UPDATE users SET lun={newUserLun} WHERE id={ctx.author.id}")
        mydb.commit()

        if isinstance(ctx.channel, discord.channel.DMChannel):
            channelname = 'DM Channel'
        else:
            channelname = ctx.channel.name

        print(f'Message - {ctx.author.name} -- {channelname} -- "{ctx.content}" --- Total Lun: {pNewUserLun} Lun (+{lunEarn} Lun){pics}-- XP: {pXP}xp (+{xp}xp) -- Tier: {tier}')

    @commands.command()
    async def xp(self, ctx, user:discord.User=None):

        if not user:
            user = ctx.author
            
        db.execute(f"SELECT xp, tier FROM users where id = {user.id}")
        XP = db.fetchall()
        tier = XP[0][1]
        XP = XP[0][0]
        pXP = "{:,}".format(XP)
    
        await ctx.channel.send(f'{user.name} has {pXP}xp!\nTier : {tier}', delete_after=10)
        await ctx.message.delete(delay=10)

    @xp.error
    async def xp_error(self, ctx, error: commands.CommandError):
        if isinstance(error, commands.UserNotFound):
            await ctx.channel.send(f"{error} Please use their @", delete_after=10)
            await ctx.message.delete(delay=10)
            return

        else:
            await ctx.channel.send("Sorry, an unknown error occured, this has been reported to @v8ive and will be addressed ASAP :)\nPlease try again, or try another command.")
            server = ctx.channel.guild
            botOwner = server.get_member(692106881644101723)
            await botOwner.send(f"XP Error! - {error}")
            return

async def setup(bot):
    await bot.add_cog(levelling(bot))