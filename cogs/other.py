import discord
from discord.ext import commands
import datetime
import json
import os
import asyncio
intents = discord.Intents.default()
intents.members = True

class Other(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.log(guild.id f"Joined new guild - {guild.name}")
        os.system(f'touch configs/{guild.id}.json')
        with open(f'configs/{guild.id}.json', 'r') as f:
            config = json.load(f)

        config['General'] = {}
        config['Invites'] = {}

        config['General']['DeleteInvocations'] = 0
        config['General']['AdminRoles'] = []
        config['General']['ServerLog'] = 0

        for invite in await guild.invites():
            config['Invites'][f'{invite.code}'] = {}
            config['Invites'][f'{invite.code}']['roles'] = []
            config['Invites'][f'{invite.code}']['uses'] = invite.uses

        with open(f'configs/{guild.id}', 'w') as f:
            json.dump(config, f, indent = 4)

    @commands.command()
    async def addmod(self, ctx, role: discord.Role):
        if checkInvos(ctx.guild.id) = 1:
            await ctx.message.delete(delay=3)

        if ctx.author.id == ctx.guild.owner_id:
            with open(f'configs/{ctx.guild.id}.json', 'r') as f:
                config = json.load(f)

            admin_roles = config['General']['AdminRoles']

            if role.id in admin_roles:
                admin_roles.append(role.id)
                config['General']['AdminRoles'] = admin_roles
                with open(f'configs/{ctx.guild.id}', 'w') as f:
                    json.dump(config, f, indent = 4)

            else:
                embed = self.constructResponseEmbedBase("This role wasn't an admin role")
                await ctx.send(embed = embed)
        else:
            embed = self.constructResponseEmbedBase("You are not the server owner")
            await ctx.send(embed = embed)

    @commands.command()
    async def delmod(self, ctx, role: discord.Role):
        if checkInvos(ctx.guild.id) = 1:
            await ctx.message.delete(delay=3)

        if ctx.author.id == ctx.guild.owner_id:
            with open(f'configs/{ctx.guild.id}.json', 'r') as f:
                config = json.load(f)

            admin_roles = config['General']['AdminRoles']

            if role.id in admin_roles:
                admin_roles.remove(role.id)
                config['General']['AdminRoles'] = admin_roles
                with open(f'configs/{ctx.guild.id}', 'w') as f:
                    json.dump(config, f, indent = 4)
            else:
                embed = self.constructResponseEmbedBase("This role wasn't an admin role")
                await ctx.send(embed = embed)
        else:
            embed = self.constructResponseEmbedBase("You are not the server owner")
            await ctx.send(embed = embed)

    @commands.command(aliases = ['elog'])
    async def enablelog(self, ctx, channel: discord.TextChannel):
        if checkInvos(ctx.guild.id) = 1:
            await ctx.message.delete(delay=3)

        if ctx.author.id == ctx.guild.owner_id:
            with open(f'configs/{ctx.guild.id}.json', 'r') as f:
                config = json.load(f)

            config['General']['ServerLog'] = channel.id
            await ctx.send(f"Enabled log on channel {channel}")
            with open(f'configs/{ctx.guild.id}', 'w') as f:
                json.dump(config, f, indent = 4)

        else:
            embed = self.constructResponseEmbedBase("You are not the server owner")
            await ctx.send(embed = embed)

    @commands.command(aliases = ['dlog'])
    async def disablelog(self, ctx):
        if checkInvos(ctx.guild.id) = 1:
            await ctx.message.delete(delay=3)

        if ctx.author.id == ctx.guild.owner_id:
            with open(f'configs/{ctx.guild.id}.json', 'r') as f:
                config = json.load(f)

            config['General']['ServerLog'] = 0
            await ctx.send(f"Disabled log")
            with open(f'configs/{ctx.guild.id}', 'w') as f:
                json.dump(config, f, indent = 4)

        else:
            embed = self.constructResponseEmbedBase("You are not the server owner")
            await ctx.send(embed = embed)

    @commands.command()
    async def delinvos(self, ctx, choice):
        if checkInvos(ctx.guild.id) = 1:
            await ctx.message.delete(delay=3)

        if checkPerms(ctx.author.id, ctx.guild.id) == False:
            await ctx.send("You are not permitted to run this command")
            return

        if choice == 'true' or choice == 'yes' or choice == 'y' or choice == 'allow' or choice == 'enable':
            choice = 1
        if choice == 'false' or choice == 'no' or choice == 'n' or choice == 'deny' or choice == 'disable':
            choice = 0
        if choice not in [0,1]:
            embed = self.constructResponseEmbedBase("This is not a valid input")
            await ctx.send(embed = embed)
            return

        with open(f'configs/{ctx.guild.id}.json', 'r') as f:
            config = json.load(f)

        config['General']['DeleteInvocations'] = choice
        if choice == 1:
            embed = self.constructResponseEmbedBase("You've successfully enabled Invocation Deletion")
            await ctx.send(embed = embed)
        if choice == 0:
            embed = self.constructResponseEmbedBase("You've successfully disabled Invocation Deletion")
            await ctx.send(embed = embed)

        with open(f'configs/{ctx.guild.id}', 'w') as f:
            json.dump(config, f, indent = 4)

    @commands.command()
    async def help(self, ctx):
        if checkInvos(ctx.guild.id) = 1:
            await ctx.message.delete(delay=3)

        embed = discord.Embed(title = f"**InviteBot Help**", color = discord.Colour.from_rgb(119, 137, 218))
        embed.set_thumbnail(url="https://nevalicjus.github.io/docs/invitebot.png")
        now = datetime.datetime.now()
        embed.set_footer(text = f"{now.strftime('%H:%M')} / {now.strftime('%d/%m/%y')} | InviteBot made with \u2764\ufe0f by Nevalicjus")

        embed.add_field(name = "inv!**addmod @role**", value = "*Only for Server Owner*\nAdds @role to Admin Roles", inline = False)
        embed.add_field(name = "inv!**delmod @role**", value = "*Only for Server Owner*\nRemoves @role from Admin Roles", inline = False)
        embed.add_field(name = "inv!**delinvos y/n**", value = "Enables or disables Invocation Deletion.\nAcceptable input:\nyes/no, y/n, true/false, allow/deny, enable/disable, 1/0", inline = False)
        embed.add_field(name = "inv!**invadd <invite> @role**", value = "Aliases - inva\nAdds a link between <invite> and @role", inline = False)
        embed.add_field(name = "inv!**invremove <invite> (@role)**", value = "Aliases - invdel, invrem, invr\nRemoves a link between <invite> and @role or removes all invite-roles links on the invite if no role is specified", inline = False)
        embed.add_field(name = "inv!**listinvs**", value = "Aliases - invlist, invls\nLists all invite-role links for the current server", inline = False)
        embed.add_field(name = "inv!**invmake #channel @role (<max_uses>) (<max_age>)**", value = "Aliases - invm\nCreates an invite for #channel and instantly adds a link to @role for it. If <max_uses> and <max_age> are specified, the invite will be created with them in mind", inline = False)
        embed.add_field(name = "inv!**invite**", value = "Sends you the bot invite", inline = False)
        embed.add_field(name = "inv!**enablelog #channel**", value = "*Only for Server Owner\n*Aliases - elog\nEnables log on #channel", inline = False)
        embed.add_field(name = "inv!**disablelog**", value = "*Only for Server Owner*\nAliases - dlog\nDisables log", inline = False)

        await ctx.send(embed = embed)

    @commands.command()
    @commands.check_any(commands.has_any_role(*owner_roles), commands.is_owner())
    async def invite(self, ctx):
        if checkInvos(ctx.guild.id) = 1:
            await ctx.message.delete(delay=3)

        self.log(ctx.guild.id, f"Invite to the bot requested by {ctx.message.author}[{ctx.message.author.id}] on {ctx.message.channel}")
        await ctx.send('**Invite the bot here ->** https://discord.com/api/oauth2/authorize?client_id=788044126242603070&permissions=268487921&scope=bot')


    def log(self, guild_id, log_msg: str):
        print(f"[{datetime.datetime.now()}] [{guild_id}] [\033[34mOTHER\033[0m]: " + log_msg)
        with open('log.txt', 'a') as f:
            f.write(f"[{datetime.datetime.now()}] : " + log_msg + "\n")

    def checkPerms(self, user_id, guild_id):
        with open(f'configs/{ctx.guild.id}.json', 'r') as f:
            config = json.load(f)
            admin_roles = config['General']['AdminRoles']
        with open(f'config.json', 'r') as f:
            main_config = json.load(f)
            owners = main_config['OwnerUsers']

        isAble = 0

        guild = self.client.get_guild(guild_id)
        member = guild.get_member(user_id)

        if user_id in owners:
            isAble += 1
        if user_id == guild.owner_id:
            isAble += 1
        for role in cmember.roles:
            if role.id in admin_roles:
                isAble += 1

        if isAble >= 1:
            return True
        else:
            return False

    def checkInvos(self, guild_id):
        with open(f'configs/{ctx.guild.id}.json', 'r') as f:
            config = json.load(f)
            delinvos = config['General']['DeleteInvocations']

        if delinvos == 1:
            return True
        else:
            return False

    def constructResponseEmbedBase(self, desc):
        embed = discord.Embed(title = f"**InviteBot**", description = desc, color = discord.Colour.from_rgb(119, 137, 218))
        embed.set_thumbnail(url="https://nevalicjus.github.io/docs/invitebot.png")
        now = datetime.datetime.now()
        embed.set_footer(text = f"{now.strftime('%H:%M')} / {now.strftime('%d/%m/%y')} | InviteBot made with \u2764\ufe0f by Nevalicjus")

        return embed


def setup(client):
    client.add_cog(Other(client))
