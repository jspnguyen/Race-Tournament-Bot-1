import discord, random, json, datetime, numpy
from discord.ext import commands
from discord.utils import get

with open('data/config.json', 'r') as f: 
  data = json.load(f)
with open('data/actions.json', 'r') as f2:
  actions_list = json.load(f2)
with open('data/trophies.json', 'r') as f3:
  trophies_list = json.load(f3)
with open('data/cooldowns.json', 'r') as f4:
  cooldowns_list = json.load(f4)
with open('data/targets.json', 'r') as f5:
  targets_list = json.load(f5)
with open('data/misactions.json', 'r') as f6:
  misactions_list = json.load(f6)

discord_token = data["token"]
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command=None)

# Bot startup and status
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="Sprints"))
    print("Sprint Bot Online")

# Sends cooldown on bot command
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.reply(f"{error.retry_after:.2f} seconds to try again", delete_after=3)  

# Command for joining the sprinting event
@bot.command(pass_context=True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def joinsprint(ctx):
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        member = ctx.author
        string_member = str(member)
        role = ctx.guild.get_role(1130325065985167420)
        if string_member in actions_list:
            embed = discord.Embed(title="You are already in the tournament!", color=discord.Colour.dark_red())
            await ctx.reply(embed=embed)
        else:
            actions_list[string_member] = 6
            misactions_list[string_member] = 3
            trophies_list[string_member] = 0
            presentDate = datetime.datetime.now()
            cooldowns_list[string_member] = datetime.datetime.timestamp(presentDate)*1000
            targets_list[string_member] = []
            with open("data/actions.json", "w") as outfile:
                json.dump(actions_list, outfile)
            with open("data/trophies.json", "w") as outfile2:
                json.dump(trophies_list, outfile2)
            with open("data/cooldowns.json", "w") as outfile3:
                json.dump(cooldowns_list, outfile3)
            with open("data/targets.json", "w") as outfile4:
                json.dump(targets_list, outfile4)
            with open("data/misactions.json", "w") as outfile5:
                json.dump(misactions_list, outfile5)
            embed = discord.Embed(title="You have joined the tournament, good luck!", color=discord.Colour.dark_green())
            await ctx.reply(embed=embed)
            await member.add_roles(role)

# Command for challenging someone to a sprint
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def sprint(ctx, member:discord.Member = None):
    string_member, string_author = str(member), str(ctx.author)
    name, pfp = ctx.author.display_name, ctx.author.display_avatar
    presentDate = datetime.datetime.now()
    unix_timestamp = datetime.datetime.timestamp(presentDate)*1000
    if cooldowns_list[string_author] <= unix_timestamp:
        actions_list[string_author] = 6
        misactions_list[string_member] = 3
        targets_list[string_author] = []
        with open("data/targets.json", "w") as outfile9:
            json.dump(targets_list, outfile9)
        with open("data/misactions.json", "w") as outfile5:
            json.dump(misactions_list, outfile5)
        with open("data/actions.json", "w") as outfile6:
            json.dump(actions_list, outfile6)
    elif actions_list[string_author] == 0:
        await ctx.reply(f"You can sprint again at <t:{round(cooldowns_list[string_author] / 1000)}>")
        return
    if string_member not in targets_list[string_author]:
        if (string_member in actions_list) and (string_member != string_author) and (string_author in actions_list):
            winner = random.randint(1, 101)
            if winner <= 50:
                trophies_list[string_author] += 1
            elif winner > 50:
                trophies_list[string_member] += 1
            actions_list[string_author] -= 1
            targets_list[string_author].append(string_member)
            if actions_list[string_author] == 5:
                presentDate = datetime.datetime.now()
                cooldowns_list[string_author] = ((datetime.datetime.timestamp(presentDate)*1000) + 82800000)
                with open("data/cooldowns.json", "w") as outfile3:
                    json.dump(cooldowns_list, outfile3)
            with open("data/targets.json", "w") as outfile4:
                json.dump(targets_list, outfile4)
            with open("data/actions.json", "w") as outfile:
                json.dump(actions_list, outfile)
            with open("data/trophies.json", "w") as outfile2:
                json.dump(trophies_list, outfile2)
            if winner <= 50:
                embed = discord.Embed(title=f"{string_author} won!", color=discord.Colour.brand_green())
                embed.set_author(name=f"{name}", icon_url=f"{pfp}")
                embed.set_image(url="https://cdn.discordapp.com/attachments/1123094071930531911/1130350543571779694/sprint.png")
                await ctx.reply(embed=embed)
            elif winner > 50:
                embed = discord.Embed(title=f"{string_member} won!", color=discord.Colour.brand_red())
                embed.set_author(name=f"{name}", icon_url=f"{pfp}")
                embed.set_image(url="https://cdn.discordapp.com/attachments/1123094071930531911/1130350543571779694/sprint.png")
                await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title="Invalid opponent", color=discord.Colour.dark_red())
            await ctx.reply(embed=embed)
            ctx.command.reset_cooldown(ctx)
    else: 
        embed = discord.Embed(title="You already interacted with this user today", color=discord.Colour.dark_red())
        await ctx.reply(embed=embed)
        ctx.command.reset_cooldown(ctx)

# Command for attempting to cast a spell
@bot.command(aliases=['mischief', 'sabotage'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def mischievous(ctx, member:discord.Member = None):
    string_member, string_author = str(member), str(ctx.author)
    name, pfp = ctx.author.display_name, ctx.author.display_avatar
    presentDate = datetime.datetime.now()
    unix_timestamp = datetime.datetime.timestamp(presentDate)*1000
    if cooldowns_list[string_author] <= unix_timestamp:
        actions_list[string_author] = 6
        misactions_list[string_member] = 3
        targets_list[string_author] = []
        with open("data/targets.json", "w") as outfile9:
            json.dump(targets_list, outfile9)
        with open("data/misactions.json", "w") as outfile5:
            json.dump(misactions_list, outfile5)
        with open("data/actions.json", "w") as outfile6:
            json.dump(actions_list, outfile6)
    elif actions_list[string_author] == 0:
        await ctx.reply(f"You can take action again at <t:{round(cooldowns_list[string_author] / 1000)}>")
        return
    if misactions_list[string_author] <= 0:
        embed = discord.Embed(title="You used all mischief actions for the day", color=discord.Colour.dark_red())
        await ctx.reply(embed=embed)
        return
    if actions_list[string_author] <= 1:
        embed = discord.Embed(title="You don't have enough actions left to use !mischief, please use !sprint instead", color=discord.Colour.dark_red())
        await ctx.reply(embed=embed)
        return
    if string_member not in targets_list[string_author]:
        if actions_list[string_member] > 0:
            if (string_member in actions_list) and (string_member != string_author) and (string_author in actions_list):
                winner = random.randint(1, 101)
                if winner <= 50:
                    actions_list[string_member] -= 1
                elif winner > 50:
                    actions_list[string_author] -= 1
                    if actions_list[string_author] == 5:
                        presentDate = datetime.datetime.now()
                        cooldowns_list[string_author] = ((datetime.datetime.timestamp(presentDate)*1000) + 82800000)
                        with open("data/cooldowns.json", "w") as outfile3:
                            json.dump(cooldowns_list, outfile3)
                actions_list[string_author] -= 1
                misactions_list[string_author] -= 1
                targets_list[string_author].append(string_member)
                if actions_list[string_author] == 5:
                    presentDate = datetime.datetime.now()
                    cooldowns_list[string_author] = ((datetime.datetime.timestamp(presentDate)*1000) + 82800000)
                    with open("data/cooldowns.json", "w") as outfile3:
                        json.dump(cooldowns_list, outfile3)
                with open("data/actions.json", "w") as outfile:
                    json.dump(actions_list, outfile)
                with open("data/targets.json", "w") as outfile4:
                    json.dump(targets_list, outfile4)
                with open("data/misactions.json", "w") as outfile5:
                    json.dump(misactions_list, outfile5)
                if winner <= 50:
                    embed = discord.Embed(title=f"Alas! {string_member} has not been able to avoid your naughty scheme and stepped on the banana peel :banana: and fell, losing 1 action point :heart: along the way!", color=discord.Colour.brand_green())
                    embed.set_author(name=f"{name}", icon_url=f"{pfp}")
                    embed.set_image(url="https://cdn.discordapp.com/attachments/1123094071930531911/1129301382973882378/buster_run_track_360.gif")
                    await ctx.reply(embed=embed)
                elif winner > 50:
                    embed = discord.Embed(title=f"What goes around comes around! You've stepped on your own banana peel :banana: and fell, losing 1 action point :heart: along the way! How fun! LOL! :stuck_out_tongue_winking_eye:", color=discord.Colour.brand_red())
                    embed.set_author(name=f"{name}", icon_url=f"{pfp}")
                    embed.set_image(url="https://cdn.discordapp.com/attachments/1123094071930531911/1129301382973882378/buster_run_track_360.gif")
                    await ctx.reply(embed=embed)
            else:
                embed = discord.Embed(title="Invalid target", color=discord.Colour.dark_red())
                await ctx.reply(embed=embed)
                ctx.command.reset_cooldown(ctx)
        else:
            embed = discord.Embed(title=f"Ahemm... {string_member} has already used up all actions. Please pick another one.", color=discord.Colour.dark_red())
            await ctx.reply(embed=embed)
            ctx.command.reset_cooldown(ctx)
    else: 
        embed = discord.Embed(title="You already interacted with this user today", color=discord.Colour.dark_red())
        await ctx.reply(embed=embed)
        ctx.command.reset_cooldown(ctx)

# Command for displaying sprint leaderboard
@bot.command(aliases=["sprintleaderboard", "lb", "slb"])
@commands.cooldown(1, 20, commands.BucketType.user)
async def leaderboard(ctx):
    rank1, rank2, rank3, rank4, rank5 = '', '', '', '', ''
    rank1score, rank2score, rank3score, rank4score, rank5score = 0, 0, 0, 0, 0
    rank6, rank7, rank8, rank9, rank10 = '', '', '', '', ''
    rank6score, rank7score, rank8score, rank9score, rank10score = 0, 0, 0, 0, 0
    rank11, rank12, rank13, rank14, rank15 = '', '', '', '', ''
    rank11score, rank12score, rank13score, rank14score, rank15score = 0, 0, 0, 0, 0
    rank16, rank17, rank18, rank19, rank20, rank21 = '', '', '', '', '', ''
    rank16score, rank17score, rank18score, rank19score, rank20score, rank21score = 0, 0, 0, 0, 0, 0

    keys, values = list(trophies_list.keys()), list(trophies_list.values())
    sorted_value_index = numpy.argsort(values)
    sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
    key_list = list(sorted_dict.keys())
    key_list = list(reversed(key_list))
    value_list = list(sorted_dict.values())
    value_list = list(reversed(value_list))

    if len(sorted_dict) >= 1:
        rank1, rank1score = key_list[0], value_list[0]
        if len(sorted_dict) >= 2:
            rank2, rank2score = key_list[1], value_list[1]
            if len(sorted_dict) >= 3:
                rank3, rank3score = key_list[2], value_list[2]
                if len(sorted_dict) >= 4:
                    rank4, rank4score = key_list[3], value_list[3]
                    if len(sorted_dict) >= 5:
                        rank5, rank5score = key_list[4], value_list[4]
                        if len(sorted_dict) >= 6:
                            rank6, rank6score = key_list[5], value_list[5]
                            if len(sorted_dict) >= 7:
                                rank7, rank7score = key_list[6], value_list[6]
                                if len(sorted_dict) >= 8:
                                    rank8, rank8score = key_list[7], value_list[7]
                                    if len(sorted_dict) >= 9:
                                        rank9, rank9score = key_list[8], value_list[8]
                                        if len(sorted_dict) >= 10:
                                            rank10, rank10score = key_list[9], value_list[9]
                                            if len(sorted_dict) >= 11:
                                                rank11, rank11score = key_list[10], value_list[10]
                                                if len(sorted_dict) >= 12:
                                                    rank12, rank12score = key_list[11], value_list[11]
                                                    if len(sorted_dict) >= 13:
                                                        rank13, rank13score = key_list[12], value_list[12]
                                                        if len(sorted_dict) >= 14:
                                                            rank14, rank14score = key_list[13], value_list[13]
                                                            if len(sorted_dict) >= 15:
                                                                rank15, rank15score = key_list[14], value_list[14]
                                                                if len(sorted_dict) >= 16:
                                                                    rank16, rank16score = key_list[15], value_list[15]
                                                                    if len(sorted_dict) >= 17:
                                                                        rank17, rank17score = key_list[16], value_list[16]
                                                                        if len(sorted_dict) >= 18:
                                                                            rank18, rank18score = key_list[17], value_list[17]
                                                                            if len(sorted_dict) >= 19:
                                                                                rank19, rank19score = key_list[18], value_list[18]
                                                                                if len(sorted_dict) >= 20:
                                                                                    rank20, rank20score = key_list[19], value_list[19]
                                                                                    if len(sorted_dict) >= 21:
                                                                                        rank21, rank21score = key_list[20], value_list[20]

                            
    embed = discord.Embed(title="Sprint Leaderboard", description="*Top 21 Trophies*", color=discord.Colour.dark_gold())
    embed.add_field(name=f"**1st. **{rank1}", value=f"{rank1score} trophies", inline='true')
    embed.add_field(name=f"**2nd. **{rank2}", value=f"{rank2score} trophies", inline='true')
    embed.add_field(name=f"**3rd. **{rank3}", value=f"{rank3score} trophies", inline='true')
    embed.add_field(name=f"**4th. **{rank4}", value=f"{rank4score} trophies", inline='true')
    embed.add_field(name=f"**5th. **{rank5}", value=f"{rank5score} trophies", inline='true')
    embed.add_field(name=f"**6th. **{rank6}", value=f"{rank6score} trophies", inline='true')
    embed.add_field(name=f"**7th. **{rank7}", value=f"{rank7score} trophies", inline='true')
    embed.add_field(name=f"**8th. **{rank8}", value=f"{rank8score} trophies", inline='true')
    embed.add_field(name=f"**9th. **{rank9}", value=f"{rank9score} trophies", inline='true')
    embed.add_field(name=f"**10th. **{rank10}", value=f"{rank10score} trophies", inline='true')
    embed.add_field(name=f"**11th. **{rank11}", value=f"{rank11score} trophies", inline='true')
    embed.add_field(name=f"**12th. **{rank12}", value=f"{rank12score} trophies", inline='true')
    embed.add_field(name=f"**13th. **{rank13}", value=f"{rank13score} trophies", inline='true')
    embed.add_field(name=f"**14th. **{rank14}", value=f"{rank14score} trophies", inline='true')
    embed.add_field(name=f"**15th. **{rank15}", value=f"{rank15score} trophies", inline='true')
    embed.add_field(name=f"**16th. **{rank16}", value=f"{rank16score} trophies", inline='true')
    embed.add_field(name=f"**17th. **{rank17}", value=f"{rank17score} trophies", inline='true')
    embed.add_field(name=f"**18th. **{rank18}", value=f"{rank18score} trophies", inline='true')
    embed.add_field(name=f"**19th. **{rank19}", value=f"{rank19score} trophies", inline='true')
    embed.add_field(name=f"**20th. **{rank20}", value=f"{rank20score} trophies", inline='true')
    embed.add_field(name=f"**21st. **{rank21}", value=f"{rank21score} trophies", inline='true')
    await ctx.send(embed=embed)

# Check your rank
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def rank(ctx, member:discord.Member = None):
    if member is None:
        member = ctx.author
    string_member = str(member)
    name, pfp = member.display_name, member.display_avatar
    keys, values = list(trophies_list.keys()), list(trophies_list.values())
    sorted_value_index = numpy.argsort(values)
    sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
    key_list = list(sorted_dict.keys())
    key_list = list(reversed(key_list))
    rank_number = key_list.index(string_member) + 1
    embed = discord.Embed(title="Rank", description=f"#{rank_number}", color=discord.Colour.dark_gold())
    embed.set_author(name=f"{name}", icon_url=f"{pfp}")
    await ctx.reply(embed=embed)

# Command for displaying your remaining actions
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def actions(ctx, member:discord.Member = None):
    if member is None:
        string_member = str(ctx.author)
        name, pfp = ctx.author.display_name, ctx.author.display_avatar
    else: 
        string_member = str(member)
        name, pfp = member.display_name, member.display_avatar
    if string_member in actions_list:
        total_lives = actions_list[string_member]
        if total_lives == 0:
            embed = discord.Embed(title=":broken_heart::broken_heart::broken_heart::broken_heart::broken_heart::broken_heart:", color=discord.Colour.dark_gray())
            embed.set_author(name=f"{name}", icon_url=f"{pfp}")
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title=(":heart:"*total_lives) + (":broken_heart:"*(6-total_lives)), color=discord.Colour.brand_red())
            embed.set_author(name=f"{name}", icon_url=f"{pfp}")
            await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(title="Invalid member", color=discord.Colour.dark_red())
        embed.set_author(name=f"{name}", icon_url=f"{pfp}")
        await ctx.reply(embed=embed)

# Command for displaying your remaining mischief
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def misactions(ctx, member:discord.Member = None):
    if member is None:
        string_member = str(ctx.author)
        name, pfp = ctx.author.display_name, ctx.author.display_avatar
    else: 
        string_member = str(member)
        name, pfp = member.display_name, member.display_avatar
    if string_member in actions_list:
        total_lives = misactions_list[string_member]
        if total_lives == 0:
            embed = discord.Embed(title=":stuck_out_tongue_winking_eye::stuck_out_tongue_winking_eye::stuck_out_tongue_winking_eye:", color=discord.Colour.dark_gray())
            embed.set_author(name=f"{name}", icon_url=f"{pfp}")
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title=(":banana:"*total_lives) + (":stuck_out_tongue_winking_eye:"*(3-total_lives)), color=discord.Colour.brand_red())
            embed.set_author(name=f"{name}", icon_url=f"{pfp}")
            await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(title="Invalid member", color=discord.Colour.dark_red())
        embed.set_author(name=f"{name}", icon_url=f"{pfp}")
        await ctx.reply(embed=embed)

# Command for displaying your total boxing wins
@bot.command(aliases=["wins", "trophy", "awards"])
@commands.cooldown(1, 5, commands.BucketType.user)
async def trophies(ctx, member:discord.Member = None):
    if member is None:
        string_member = str(ctx.author)
        name, pfp = ctx.author.display_name, ctx.author.display_avatar
    else: 
        string_member = str(member)
        name, pfp = member.display_name, member.display_avatar
    if string_member in trophies_list:
        total_wins = trophies_list[string_member]
        if total_wins == 0:
            embed = discord.Embed(title=":wastebasket:", color=discord.Colour.dark_gray())
            embed.set_author(name=f"{name}", icon_url=f"{pfp}")
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title=":trophy:"*total_wins, color=discord.Colour.dark_gold())
            embed.set_author(name=f"{name}", icon_url=f"{pfp}")
            await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(title="You are not in the event", color=discord.Colour.dark_red())
        embed.set_author(name=f"{name}", icon_url=f"{pfp}")
        await ctx.reply(embed=embed)

# Command for displaying other command information
@bot.command(aliases=['sprinthelp', 'sphelp'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def shelp(ctx):
    embed = discord.Embed(title="Help Menu", description="*To participate in the sprint event you must first use !joinsprint to be able to use the commands. Then, you can sprint up to 6 other members a day using the !sprint command. Don't tell anyone, but you can also use !mischief up to 3 times a day.*", color=discord.Colour.dark_green())
    embed.add_field(name="> !joinsprint", value="Joins the tournament", inline='false')
    embed.add_field(name="> !sprint <target>", value="Challenges another discord member to a sprint", inline='false')
    embed.add_field(name="> !mischief <target>", value="Attempts to reduce 1 action point from a player. Yours will be reduced instead if attempt fails. You can only use !sprint with your last action point of the day.", inline='false')
    embed.add_field(name="> !actions", value="Displays your remaining actions for the day, can mention a member to check their remaining actions", inline='false')
    embed.add_field(name="> !misactions", value="Displays your remaining !mischievous for the day, can mention a member to check their remaining mischief actions", inline='false')
    embed.add_field(name="> !trophies <target>", value="Displays your trophies or mention someone to check their trophies", inline='false')
    embed.add_field(name="> !leaderboard", value="Displays the top 21 members for trophies", inline='false')
    embed.add_field(name="> !rank <target>", value="Displays your rank or mention someone to check their rank", inline='false')
    await ctx.reply(embed=embed)

if __name__ == '__main__':
    bot.run(discord_token)