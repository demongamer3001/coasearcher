#Made by Blank (PHG Moderator)

import discord, os, aiohttp, asyncio, json
from discord.ext import commands, tasks
try:
    from keep_alive import keep_alive
except Exception:
    pass

ownerid=904682505104396329
prefix=","


def page_url(method, page:int=0):
    if method=="main":
        return f"https://www.curseofaros.com/highscores.json?p={page}"
    else:
        if method in ['mining', 'smithing', 'fishing', 'crafting', 'cooking', 'woodcutting']:
            return f"https://www.curseofaros.com/highscores-{method}.json?p={page}"

async def stats(method, name):
    page=0
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.get(page_url(method, page)) as r:
                if not (await r.text()).strip()=='[]' and not (await r.text()).strip()=='Not Found':
                    for i in range(len(await r.json())):
                        if (await r.json())[i]['name'].lower()==name.lower():
                            stats=(await r.json())[i]
                            return stats
                    page+=1
                else:
                    raise Exception('Not Found')

def colour(color=None):
    if color is not None:
        return int(color, 16)
    else:
        return 16705372

def format(xp):
    return f"{xp:,}"

async def leaderb(method, name):
    page=0
    lb=[None]*9
    rank=1
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.get(page_url(method, page)) as r:
                if not (await r.text()).strip()=='[]' and not (await r.text()).strip()=='Not Found':
                    for i in range(len(await r.json())):
                        if len((await r.json())[i]['name'].lower().split(' '))==1:
                            rank+=1
                            continue
                        if (await r.json())[i]['name'].lower().split(' ')[0]==name.lower():
                            if lb[0] is None:
                                lb[0]=(await r.json())[i]['name']
                                lb[6]=(await r.json())[i]['xp']
                                lb[3]=rank
                            elif lb[0] is not None and lb[1] is None:
                                lb[1]=(await r.json())[i]['name']
                                lb[7]=(await r.json())[i]['xp']
                                lb[4]=rank
                            elif lb[1] is not None and lb[2] is None:
                                lb[2]=(await r.json())[i]['name']
                                lb[8]=(await r.json())[i]['xp']
                                lb[5]=rank
                                return lb
                        rank+=1
                    page+=1
                else:
                    raise Exception('Not Found')
            
def level(xp=None):
    if xp is None:
        raise Exception("XP is None")
    else:
        xps=[0, 46, 99, 159, 229, 309, 401, 507, 628, 768, 928, 1112, 1324, 1567, 1847, 2168, 2537, 2961, 3448, 4008, 4651, 5389, 6237, 7212, 8332, 9618, 11095, 12792, 14742, 16982, 19555, 22510, 25905, 29805, 34285, 39431, 45342, 52132, 59932, 68892, 79184, 91006, 104586, 120186, 138106, 158690, 182335, 209496, 240696, 276536, 317705, 364996, 419319, 481720, 553400, 635738, 730320, 838966, 963768, 1107128, 1271805, 1460969, 1678262, 1927866, 2214586, 2543940, 2922269, 3356855, 3856063, 4429503, 5088212, 5844870, 6714042, 7712459, 8859339, 10176758, 11690075, 13428420, 15425254, 17719014, 20353852, 23380486, 26857176, 30850844, 35438364, 40708040, 46761308, 53714688, 61702024, 70877064, 81416417, 93522954, 107429714, 123404386, 141754466, 162833172, 187046247, 214859767, 246809111, 283509271, 325666684, 374092835, 429719875, 493618564, 567018884, 651333710, 748186012, 859440093, 987237472, 1134038112, 1302667765, 1496372370, 1718880532, 1974475291, 2268076571, 2605335878, 2992745089, 3437761413, 3948950932, 4536153492, 5210672106]
        
        for i in range(len(xps)):
            if xps[-1]==xps[i]:
                return i+1
            elif xp>=xps[i] and xp<xps[i+1]:
                return i+1

intents=discord.Intents.default()
intents.members=True

client=commands.Bot(command_prefix=prefix, owner_id=ownerid, help_command=None, intents=intents)

@tasks.loop(minutes=10)
async def activity():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{prefix}help in {len(client.guilds)} servers!"))

@client.event
async def on_ready():
    try:
        keep_alive()
    except Exception:
        pass
    await asyncio.sleep(2)
    if os.name=="nt":
        os.system('cls')
    else:
        os.system('clear')
    print(f"Connected to {client.user}")
    activity.start()

@client.event
async def on_guild_join(guild):
    try:
        await guild.me.edit(nick=f"{client.user.display_name} ({prefix})")
    except Exception:
        pass

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    else:
        print(error)

@client.command()
async def about(ctx):
    owner=client.get_user(ownerid)
    if owner is None:
        embed=discord.Embed(title="About", description="Bot made by **Blank (PHG Moderator)**", colour=discord.Colour.random())
    else:
        embed=discord.Embed(title="About", description="Bot made by {owner.mention}", colour=discord.Colour.random())
    async with ctx.typing():
      await asyncio.sleep(1)
      await ctx.reply(embed=embed)



@client.command()
async def search(ctx, *, name=None):
        if name is None:
                await ctx.reply("You need to enter the name too!")
                return
            
        if type(name)==discord.Member:
            await ctx.reply(f'Invalid Name: `{name}`')
            return
        exp=0
        method_list=['main', 'mining', 'smithing', 'fishing', 'crafting', 'cooking', 'woodcutting']
        embed=discord.Embed(title=f"Info - {name}" ,colour=discord.Color.blue(), description="*Searching...*")
        m=await ctx.reply(embed=embed)
        for i in method_list:
            try:
                exp=await stats(i, name)
            except Exception as e:
                if e=="Not Found":
                    em=discord.Embed(title=f"Info - {name}" ,colour=discord.Color.red(), description="*Not Found*")
                    try:
                        await m.edit(embed=em)
                        return
                    except Exception:
                        return
                else:
                    print(e)
            lvl=level(exp['xp'])
            if i=='main':
                emoji="⚔️"
            elif i=="mining":
                emoji="⛏️"
            elif i=='smithing':
                emoji="🔨"
            elif i=='fishing':
                emoji='🎣'
            elif i=='crafting':
                emoji='🧵'
            elif i=='cooking':
                emoji="🍳"
            elif i=="woodcutting":
                emoji="🪓"
            await asyncio.sleep(1)
            embed.add_field(name=f"{emoji} {i.title()}", value=f"Level {lvl} (XP: {format(exp['xp'])})", inline=False)
            embed.color=colour(exp['name_color'])
            if i==method_list[-1]:
                embed.description=None
            try:
                await m.edit(embed=embed)
            except Exception:
                return
            
@client.command()
async def woodcutting(ctx, *, name=None):
        if name is None:
            
                await ctx.reply("You need to enter the name too!")
                return
            
        if type(name)==discord.Member:
            await ctx.reply(f'Invalid Name: `{name}`')
            return
        exp=0
        method_list=['woodcutting']
        embed=discord.Embed(title=f"Info - {name}" ,colour=discord.Color.blue(), description="*Searching...*")
        m=await ctx.reply(embed=embed)
        for i in method_list:
            try:
                exp=await stats(i, name)
            except Exception as e:
                if e=="Not Found":
                    em=discord.Embed(title=f"Info - {name}" ,colour=discord.Color.red(), description="*Not Found*")
                    try:
                        await m.edit(embed=em)
                        return
                    except Exception:
                        return
                else:
                    print(e)
            lvl=level(exp['xp'])
            if i=='main':
                emoji="⚔️"
            elif i=="mining":
                emoji="⛏️"
            elif i=='smithing':
                emoji="🔨"
            elif i=='fishing':
                emoji='🎣'
            elif i=='crafting':
                emoji='🧵'
            elif i=='cooking':
                emoji="🍳"
            elif i=="woodcutting":
                emoji="🪓"
            await asyncio.sleep(1)
            embed.add_field(name=f"{emoji} {i.title()}", value=f"Level {lvl} (XP: {format(exp['xp'])})", inline=False)
            embed.color=colour(exp['name_color'])
            if i==method_list[-1]:
                embed.description=None
            try:
                await m.edit(embed=embed)
            except Exception:
                return
            
@client.command()
async def mining(ctx, *, name=None):
        if name is None:
            
                await ctx.reply("You need to enter the name too!")
                return
            
        if type(name)==discord.Member:
            await ctx.reply(f'Invalid Name: `{name}`')
            return
        exp=0
        method_list=['mining']
        embed=discord.Embed(title=f"Info - {name}" ,colour=discord.Color.blue(), description="*Searching...*")
        m=await ctx.reply(embed=embed)
        for i in method_list:
            try:
                exp=await stats(i, name)
            except Exception as e:
                if e=="Not Found":
                    em=discord.Embed(title=f"Info - {name}" ,colour=discord.Color.red(), description="*Not Found*")
                    try:
                        await m.edit(embed=em)
                        return
                    except Exception:
                        return
                else:
                    print(e)
            lvl=level(exp['xp'])
            if i=='main':
                emoji="⚔️"
            elif i=="mining":
                emoji="⛏️"
            elif i=='smithing':
                emoji="🔨"
            elif i=='fishing':
                emoji='🎣'
            elif i=='crafting':
                emoji='🧵'
            elif i=='cooking':
                emoji="🍳"
            elif i=="woodcutting":
                emoji="🪓"
            await asyncio.sleep(1)
            embed.add_field(name=f"{emoji} {i.title()}", value=f"Level {lvl} (XP: {format(exp['xp'])})", inline=False)
            embed.color=colour(exp['name_color'])
            if i==method_list[-1]:
                embed.description=None
            try:
                await m.edit(embed=embed)
            except Exception:
                return
            
@client.command()
async def cooking(ctx, *, name=None):
        if name is None:
            
                await ctx.reply("You need to enter the name too!")
                return
            
        if type(name)==discord.Member:
            await ctx.reply(f'Invalid Name: `{name}`')
            return
        exp=0
        method_list=['cooking']
        embed=discord.Embed(title=f"Info - {name}" ,colour=discord.Color.blue(), description="*Searching...*")
        m=await ctx.reply(embed=embed)
        for i in method_list:
            try:
                exp=await stats(i, name)
            except Exception as e:
                if e=="Not Found":
                    em=discord.Embed(title=f"Info - {name}" ,colour=discord.Color.red(), description="*Not Found*")
                    try:
                        await m.edit(embed=em)
                        return
                    except Exception:
                        return
                else:
                    print(e)
            lvl=level(exp['xp'])
            if i=='main':
                emoji="⚔️"
            elif i=="mining":
                emoji="⛏️"
            elif i=='smithing':
                emoji="🔨"
            elif i=='fishing':
                emoji='🎣'
            elif i=='crafting':
                emoji='🧵'
            elif i=='cooking':
                emoji="🍳"
            elif i=="woodcutting":
                emoji="🪓"
            await asyncio.sleep(1)
            embed.add_field(name=f"{emoji} {i.title()}", value=f"Level {lvl} (XP: {format(exp['xp'])})", inline=False)
            embed.color=colour(exp['name_color'])
            if i==method_list[-1]:
                embed.description=None
            try:
                await m.edit(embed=embed)
            except Exception:
                return
            
@client.command()
async def fishing(ctx, *, name=None):
        if name is None:
            
                await ctx.reply("You need to enter the name too!")
                return
            
        if type(name)==discord.Member:
            await ctx.reply(f'Invalid Name: `{name}`')
            return
        exp=0
        method_list=['fishing']
        embed=discord.Embed(title=f"Info - {name}" ,colour=discord.Color.blue(), description="*Searching...*")
        m=await ctx.reply(embed=embed)
        for i in method_list:
            try:
                exp=await stats(i, name)
            except Exception as e:
                if e=="Not Found":
                    em=discord.Embed(title=f"Info - {name}" ,colour=discord.Color.red(), description="*Not Found*")
                    try:
                        await m.edit(embed=em)
                        return
                    except Exception:
                        return
                else:
                    print(e)
            lvl=level(exp['xp'])
            if i=='main':
                emoji="⚔️"
            elif i=="mining":
                emoji="⛏️"
            elif i=='smithing':
                emoji="🔨"
            elif i=='fishing':
                emoji='🎣'
            elif i=='crafting':
                emoji='🧵'
            elif i=='cooking':
                emoji="🍳"
            elif i=="woodcutting":
                emoji="🪓"
            await asyncio.sleep(1)
            embed.add_field(name=f"{emoji} {i.title()}", value=f"Level {lvl} (XP: {format(exp['xp'])})", inline=False)
            embed.color=colour(exp['name_color'])
            if i==method_list[-1]:
                embed.description=None
            try:
                await m.edit(embed=embed)
            except Exception:
                return
            
@client.command()
async def smithing(ctx, *, name=None):
        if name is None:
            
                await ctx.reply("You need to enter the name too!")
                return
            
        if type(name)==discord.Member:
            await ctx.reply(f'Invalid Name: `{name}`')
            return
        exp=0
        method_list=['smithing']
        embed=discord.Embed(title=f"Info - {name}" ,colour=discord.Color.blue(), description="*Searching...*")
        m=await ctx.reply(embed=embed)
        for i in method_list:
            try:
                exp=await stats(i, name)
            except Exception as e:
                if e=="Not Found":
                    em=discord.Embed(title=f"Info - {name}" ,colour=discord.Color.red(), description="*Not Found*")
                    try:
                        await m.edit(embed=em)
                        return
                    except Exception:
                        return
                else:
                    print(e)
            lvl=level(exp['xp'])
            if i=='main':
                emoji="⚔️"
            elif i=="mining":
                emoji="⛏️"
            elif i=='smithing':
                emoji="🔨"
            elif i=='fishing':
                emoji='🎣'
            elif i=='crafting':
                emoji='🧵'
            elif i=='cooking':
                emoji="🍳"
            elif i=="woodcutting":
                emoji="🪓"
            await asyncio.sleep(1)
            embed.add_field(name=f"{emoji} {i.title()}", value=f"Level {lvl} (XP: {format(exp['xp'])})", inline=False)
            embed.color=colour(exp['name_color'])
            if i==method_list[-1]:
                embed.description=None
            try:
                await m.edit(embed=embed)
            except Exception:
                return
            
@client.command()
async def crafting(ctx, *, name=None):
        if name is None:
            
                await ctx.reply("You need to enter the name too!")
                return
            
        if type(name)==discord.Member:
            await ctx.reply(f'Invalid Name: `{name}`')
            return
        exp=0
        method_list=['crafting']
        embed=discord.Embed(title=f"Info - {name}" ,colour=discord.Color.blue(), description="*Searching...*")
        m=await ctx.reply(embed=embed)
        for i in method_list:
            try:
                exp=await stats(i, name)
            except Exception as e:
                if e=="Not Found":
                    em=discord.Embed(title=f"Info - {name}" ,colour=discord.Color.red(), description="*Not Found*")
                    try:
                        await m.edit(embed=em)
                        return
                    except Exception:
                        return
                else:
                    print(e)
            lvl=level(exp['xp'])
            if i=='main':
                emoji="⚔️"
            elif i=="mining":
                emoji="⛏️"
            elif i=='smithing':
                emoji="🔨"
            elif i=='fishing':
                emoji='🎣'
            elif i=='crafting':
                emoji='🧵'
            elif i=='cooking':
                emoji="🍳"
            elif i=="woodcutting":
                emoji="🪓"
            await asyncio.sleep(1)
            embed.add_field(name=f"{emoji} {i.title()}", value=f"Level {lvl} (XP: {format(exp['xp'])})", inline=False)
            embed.color=colour(exp['name_color'])
            if i==method_list[-1]:
                embed.description=None
            try:
                await m.edit(embed=embed)
            except Exception:
                return
            
@client.command()
async def main(ctx, *, name=None):
        if name is None:
            
                await ctx.reply("You need to enter the name too!")
                return
            
        if type(name)==discord.Member:
            await ctx.reply(f'Invalid Name: `{name}`')
            return
        exp=0
        method_list=['main']
        embed=discord.Embed(title=f"Info - {name}" ,colour=discord.Color.blue(), description="*Searching...*")
        m=await ctx.reply(embed=embed)
        for i in method_list:
            try:
                exp=await stats(i, name)
            except Exception as e:
                if e=="Not Found":
                    em=discord.Embed(title=f"Info - {name}" ,colour=discord.Color.red(), description="*Not Found*")
                    try:
                        await m.edit(embed=em)
                        return
                    except Exception:
                        return
                else:
                    print(e)
            lvl=level(exp['xp'])
            if i=='main':
                emoji="⚔️"
            elif i=="mining":
                emoji="⛏️"
            elif i=='smithing':
                emoji="🔨"
            elif i=='fishing':
                emoji='🎣'
            elif i=='crafting':
                emoji='🧵'
            elif i=='cooking':
                emoji="🍳"
            elif i=="woodcutting":
                emoji="🪓"
            await asyncio.sleep(1)
            embed.add_field(name=f"{emoji} {i.title()}", value=f"Level {lvl} (XP: {format(exp['xp'])})", inline=False)
            embed.color=colour(exp['name_color'])
            if i==method_list[-1]:
                embed.description=None
            try:
                await m.edit(embed=embed)
            except Exception:
                return

@client.command()
async def save(ctx, *, name:str=None):
    if name is None:
        await ctx.reply('You need to enter the name too!')
        return
    if type(name)==discord.Member:
            await ctx.reply(f'Invalid Name: `{name}`')
            return
    with open('saved.json') as e:
        saved=json.load(e)
    saved[ctx.author.id]=name.strip()
    with open('saved.json', 'w') as e:
        json.dump(saved, e)
    await ctx.reply('Successfully saved `{name.strip()}` on your profile!')

@client.command(aliases=['lb'])
async def refresh(ctx, name="PHG"):
    ranks=""
    method_list=['main', 'mining', 'smithing', 'fishing', 'crafting', 'cooking', 'woodcutting']
    embed=discord.Embed(title=f"{name.upper()} leaderboards", description="*Searching...*", colour=discord.Colour.random())
    m=await ctx.send(embed=embed)
    for i in method_list:
        try:
            leaderboards=await leaderb(i, name)
        except Exception as e:
            if e=="Not Found":
                    em=discord.Embed(title=f"{name.upper()} leaderboards" ,colour=discord.Color.red(), description="*Not Found*")
                    try:
                        await m.edit(embed=em)
                        return
                    except Exception:
                        return
            else:
                print(e)
        for j in range(3):
            if j==0:
                ranks+=f"🥇 {leaderboards[0]}    #{leaderboards[3]} (Lvl: {level(leaderboards[6])})\n"
            elif j==1:
                ranks+=f"🥈 {leaderboards[1]}    #{leaderboards[4]} (Lvl: {level(leaderboards[7])})\n"
            elif j==2:
                ranks+=f"🥉 {leaderboards[2]}    #{leaderboards[5]} (Lvl: {level(leaderboards[8])})\n"
        if i=='main':
                emoji="⚔️"
        elif i=="mining":
                emoji="⛏️"
        elif i=='smithing':
                emoji="🔨"
        elif i=='fishing':
                emoji='🎣'
        elif i=='crafting':
                emoji='🧵'
        elif i=='cooking':
                emoji="🍳"
        elif i=="woodcutting":
                emoji="🪓"
        embed.add_field(name=f"{i.title()} leaders {emoji}", value=ranks, inline=False)
        if i==method_list[-1]:
            embed.description=None
        try:
            await asyncio.sleep(1)
            await m.edit(embed=embed)
        except Exception:
            return
        ranks=""


@client.command()
async def invite(ctx):
  async with ctx.typing():
    invite_url=f"https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=67161088"
    embed=discord.Embed(colour=discord.Colour.random(), title="Invite me?", description=f"Click [here]({invite_url}) to invite me to your server")
    await asyncio.sleep(1)
    await ctx.reply(embed=embed)

@client.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
        return
    if message.author.bot:
        return
    if message.author==client.user:
        return
    if message.content.strip()==f"<@{client.user.id}>" or message.content.strip()==f"<@!{client.user.id}>":
        await message.reply(f"My prefix is {prefix}")
    else:
        await client.process_commands(message)

@client.event
async def on_message_edit(before, after):
    if after.author.bot:
        return
    if after.author==client.user:
        return
    if not after=="":
        await client.process_commands(after)

@client.command()
async def help(ctx):
  async with ctx.typing():
    invite_url=f"https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=67161088"
    embed=discord.Embed(title="COA Searcher", colour=discord.Colour.random(), url=invite_url)
    embed.add_field(name=f"1) search <name>", value="```\nGets info about a CoA user```", inline=False)
    embed.add_field(name=f"2) main <name>", value="```\nGets info about the main level of a CoA user```", inline=False)
    embed.add_field(name=f"3) mining <name>", value="```\nGets info about the mining level of a CoA user```", inline=False)
    embed.add_field(name=f"4) woodcutting <name>", value="```\nGets info about the woodcutting level of a CoA user```", inline=False)
    embed.add_field(name=f"5) smithing <name>", value="```\nGets info about the smithing level of a CoA user```", inline=False)
    embed.add_field(name=f"6) crafting <name>", value="```\nGets info about the crafting level of a CoA user```", inline=False)
    embed.add_field(name=f"7) fishing <name>", value="```\nGets info about the fishing level of a CoA user```", inline=False)
    embed.add_field(name=f"8) cooking <name>", value="```\nGets info about the cooking level of a CoA user```", inline=False)
    embed.add_field(name=f"9) refresh <guild prefix>", value="```\nGets the leaderboards of a guild (e.g. PHG, GOD etc.)```", inline=False)
    embed.add_field(name=f"10) invite", value="```\nInvite the bot to your server```", inline=False)
    embed.add_field(name=f"11) about", value="```\nGets info about the bot```", inline=False)
    embed.set_footer(text=f"Requested by {ctx.author} | Prefix: {prefix}")
    await asyncio.sleep(1)
    await ctx.reply(embed=embed)
    
client.run(os.environ['token'])
