from discord.ext import commands as cm
from random import randrange, choice
from settings import *

class DbDm(cm.Cog):
	def __init__(self, bot):
		self.bot = bot

	@cm.command()
	async def random(self, ctx, arg=None):
		if ctx.channel.id == bot_channel_id:
		    if arg == "killer":
		        await ctx.send(choice(killers_list))
		        return 0

		    if arg == "survivor":
		        await ctx.send(choice(survivors_list))
		        return 0

		    elif arg == "choice":
		        if ctx.author.voice and ctx.author.voice.channel:
		            members = ctx.author.voice.channel.voice_states
		            if len(members) > 1:
		                user = await bot.fetch_user(choice(list(members.keys())))
		                await ctx.send(user.mention)
		            else:
		                await ctx.send("Нужно больше чем 1 человек для использования этой команды")
		        else:
		            await ctx.send("Тебе нужно быть в голосовом канале для использования этой команды")
		        return 0

		    try:
		        arg = int(arg)
		    except:
		        await ctx.send(f"{ctx.author.mention} нужно число, или одно из слов: survivor, killer, choice")
		        return 0
		    if arg > 0:
		        await ctx.send(randrange(0, arg))
		    else:
		        await ctx.send(f"{ctx.author.mention} нужно целое не отрицательное число")

	@cm.command()
	async def kill(self, ctx):
		if ctx.channel.id == bot_channel_id:
		    if ctx.author.id == admin_id:
		        await ctx.send("F")
		        await exit()
		    else:
		        await ctx.send("Это команда тебе не доступна!")

	@cm.Cog.listener()
	async def on_raw_reaction_add(self, payload):
	    emoji = payload.emoji.name
	    member = payload.member
	    guild = await self.bot.fetch_guild(payload.guild_id)
	    roles = guild.roles
	    message = payload.message_id

	    for obj in characters:
	        if characters[obj] == message:
	            for role in roles:
	                if role.name == obj:
	                    await member.add_roles(role)

	@cm.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
	    emoji = payload.emoji.name
	    guild = await self.bot.fetch_guild(payload.guild_id)
	    member = await guild.fetch_member(payload.user_id)
	    message = payload.message_id
	    roles = guild.roles

	    for obj in characters:
	        if characters[obj] == message:
	            for role in roles:
	                if role.name == obj:
	                    await member.remove_roles(role)

	@cm.Cog.listener()
	async def on_member_join(self, member):
		for role in member.guild.roles:
			if role.name == "Player":
				await member.add_roles(role)

def setup(bot):
    bot.add_cog(DbDm(bot))
