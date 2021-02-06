from discord.ext import commands
import discord
import random
import asyncio

"""
        description='\n**SupportRole**\n`.ticketconfig supportrole <roleid/mention>`'
                    '\n\n**Enabled**\n`.ticketconfig enabled <true/false>`'
                    '\n\n**Channel**\n`.ticketconfig channel <channel_id>`'
                    '\n\n**Clear**\n`.ticketconfig reset <module/all>`'
                    '\n\n**Info**\n `.ticketconfig info <all>`'
                    '\n\n**LogsChannel**\n `.ticketconfig logs <channel>`'
"""

def disconfig_embed(ctx):
    embed = discord.Embed(
        title=f'{ctx.guild.name}',
        description='\n**SupportRole**\n`.ticketconfig supportrole <roleid/mention>`'
                    '\n\n**Enabled**\n`.ticketconfig enabled <true/false>`'
                    '\n\n**Channel**\n`.ticketconfig channel <channel_id>`'
                    '\n\n**Clear**\n`.ticketconfig reset <module/all>`'
                    '\n\n**Info**\n `.ticketconfig info <all>`'
                    '\n\n**LogsChannel**\n `.ticketconfig logs <channel>`'
    )
    return embed

def random_char(y):
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') for _ in range(y))

async def abuse_check(ctx, role):
    role1 = ctx.guild.get_role(role)
    if role1 >= ctx.author.top_role:
        return True
    else:
        return False

async def can_message(ctx, channel):
    if not list(channel.permissions_for(ctx.guild.me))[11][1]:
        return None
    return True

class DisVerify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class BoolConv(commands.Converter):
        async def convert(self, ctx, argument):
            if argument.lower() == 'false' or argument.lower() == 'f':
                return False
            if argument.lower() == 'true' or argument.lower() == 't':
                return True
            else:
                return None

    @commands.group(name='ticketconfig', invoke_without_command=True)
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _helptic(self, ctx):
        await ctx.send(embed=disconfig_embed(ctx))

    @_helptic.command()
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.bot_has_guild_permissions(manage_channels=True,
                                        send_messages=True,
                                        manage_messages=True,
                                        add_reactions=True
                                        )
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def reset(self, ctx, arg):
        if arg.lower() == "supportrole":
            await self.bot.pool.execute(f'UPDATE tickets_on SET support_role=$1 WHERE guildid=$2;', None,
                                        ctx.guild.id)
            await ctx.send('Successfully have reseted the module(s)!')
        elif arg.lower() == "enabled":
            await self.bot.pool.execute(f'UPDATE tickets_on SET enabled=$1 WHERE guildid=$2;', None,
                                        ctx.guild.id)
            await ctx.send('Successfully have reseted the module(s)!')
        elif arg.lower() == "channel":
            await self.bot.pool.execute(f'UPDATE tickets_on SET channel=$1 WHERE guildid=$2;', None,
                                        ctx.guild.id)
            await ctx.send('Successfully have reseted the module(s)!')
        elif arg.lower() == "all":
            await self.bot.pool.execute(f'UPDATE tickets_on SET support_role=$1, enabled=$2, channel=$3, message_id=$4'
                                        f' WHERE guildid=$5;', None, None, None, None,
                                        ctx.guild.id)
            await ctx.send('Successfully have reseted the module(s)!')
        else:
            await ctx.send('I could not find that module!')

    @_helptic.command()
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.bot_has_guild_permissions(manage_channels=True,
                                        send_messages=True,
                                        manage_messages=True,
                                        add_reactions=True
                                        )
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def info(self, ctx):
        info = await self.bot.pool.fetch('SELECT * FROM tickets_on WHERE guildid=$1;', ctx.guild.id)
        sprt_rl = ctx.guild.get_role(info[0]["support_role"])
        chnl_obj = ctx.guild.get_channel(info[0]["channel"])
        chnl_obj2 = ctx.guild.get_channel(info[0]["logs"])
        esk = sprt_rl
        eskv2 = chnl_obj
        eskv3 = chnl_obj2

        if sprt_rl is None:
            esk = None
        elif esk is not None:
            esk = sprt_rl.name

        if chnl_obj2 is None:
            eskv3 = None
        elif esk is not None:
            eskv3 = chnl_obj2.name

        if chnl_obj is None:
            eskv2 = None
        elif chnl_obj is not None:
            eskv2 = chnl_obj.name

        em = discord.Embed(
            title=f'Configuration for {ctx.guild.name}',
            description=f'\n**SupportRole**\n`{esk}`'
                        f'\n\n**Enabled**\n`{info[0]["enabled"]}`'
                        f'\n\n**Channel**\n`{eskv2}`'
                        f'\n\n**Logs Channel**\n `{eskv3}`'
        )
        em.set_footer(text='None means that it isn\'t there or the bot couldn\'t find it!')
        await ctx.send(embed=em)

    @_helptic.command()
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.bot_has_guild_permissions(manage_channels=True,
                                        send_messages=True,
                                        manage_messages=True,
                                        add_reactions=True
                                        )
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def supportrole(self, ctx, role: discord.Role):
        abuse = await abuse_check(ctx, role.id)
        if abuse is False:
            await self.bot.pool.execute(f'UPDATE tickets_on SET support_role=$1 WHERE guildid=$2;', role.id,
                                        ctx.guild.id)
            await ctx.send(f'Successfully changed the config role to `{role.name}`!')
        else:
            return await ctx.send('You may not set a role that\'s higher or equal to your highest one.')

    @_helptic.command()
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.bot_has_guild_permissions(manage_channels=True,
                                        send_messages=True,
                                        manage_messages=True,
                                        add_reactions=True
                                        )
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def logs(self, ctx, role: discord.TextChannel):
        abuse = await can_message(ctx, role)
        if abuse is True:
            await self.bot.pool.execute(f'UPDATE tickets_on SET logs=$1 WHERE guildid=$2;', role.id,
                                        ctx.guild.id)
            await ctx.send(f'Successfully changed the config channel to `{role.name}`!')
        else:
            return await ctx.send('I can\'t message that channel. Please give me required permission to do so!')

    @_helptic.command()
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.bot_has_guild_permissions(manage_channels=True,
                                        send_messages=True,
                                        manage_messages=True,
                                        add_reactions=True
                                        )
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def channel(self, ctx, channel: discord.TextChannel):
        em = discord.Embed(
            title='Tickets',
            description='React with :tickets: to create a ticket!'
        )
        await self.bot.pool.execute(f'UPDATE tickets_on SET channel=$1 WHERE guildid=$2;', channel.id, ctx.guild.id)
        tic = await channel.send(embed=em)
        await tic.add_reaction('🎟️')
        await self.bot.pool.execute(f'UPDATE tickets_on SET message_id=$1 WHERE guildid=$2;', tic.id, ctx.guild.id)
        await ctx.send(f'Successfully set the channel to `{channel.name}`!')

    @supportrole.error
    async def supportrole_error(self, ctx, error):
        error = getattr(error, 'original', error)
        if isinstance(error, commands.RoleNotFound):
            return await ctx.send('Improper value has been passed!')

    @_helptic.command()
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.bot_has_guild_permissions(manage_channels=True,
                                        send_messages=True,
                                        manage_messages=True,
                                        add_reactions=True
                                        )
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def enabled(self, ctx, value: BoolConv):
        if value is None:
            return await ctx.send('Improper value has been passed!')
        await self.bot.pool.execute(f'UPDATE tickets_on SET enabled=$1 WHERE guildid=$2;', value, ctx.guild.id)
        if value is True:
            await ctx.send('Successfully enabled the module!')
        elif value is False:
            await ctx.send('Successfully disabled the module!')

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_guild_permissions(manage_channels=True,
                                        send_messages=True,
                                        manage_messages=True,
                                        add_reactions=True
                                        )
    @commands.cooldown(1, 500, commands.BucketType.user)
    async def cleartickets(self, ctx):
        await ctx.message.delete()
        v1 = await self.bot.pool.fetch('SELECT channelid FROM tickets WHERE guildid=$1 AND userid=$2', ctx.guild.id,
                                       ctx.author.id)
        if bool(v1) is False:
            return await ctx.author.send('You have no tickets for this guild.')
        for channel in v1:
            chnl = ctx.guild.get_channel(int(channel["channelid"]))
            await asyncio.sleep(5)
            try:
                await chnl.delete()
            except AttributeError:
                await ctx.author.send('Successfully reseted your tickets for this guild!')
                await self.bot.pool.execute('DELETE FROM tickets WHERE guildid=$1 AND userid=$2', ctx.guild.id,
                                            ctx.author.id)
        await ctx.author.send('Successfully reseted your tickets for this guild!')
        await self.bot.pool.execute('DELETE FROM tickets WHERE guildid=$1 AND userid=$2', ctx.guild.id, ctx.author.id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if str(payload.emoji) != '🎟️':
            return
        v1 = await self.bot.pool.fetchrow('SELECT message_id FROM tickets_on WHERE guildid=$1', payload.guild_id)
        if payload.member.id == 727910779696971868:
            return
        if payload.message_id != v1["message_id"]:
            return
        guild = self.bot.get_guild(payload.guild_id)
        log = await self.bot.pool.fetch('SELECT logs FROM tickets_on WHERE guildid=$1;', guild.id)
        bruh = await self.bot.pool.fetchrow('SELECT enabled FROM tickets_on WHERE guildid=$1', payload.guild_id)
        support_id = await self.bot.pool.fetchrow('SELECT support_role FROM tickets_on WHERE guildid=$1',
                                                  payload.guild_id)
        if bruh["enabled"] is False:
            return await payload.member.send('This server hasn\'t enabled tickets!')
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                bruhv2 = await connection.fetch('SELECT * FROM tickets WHERE guildid=$1 AND userid=$2',
                                                payload.guild_id, payload.member.id)
        if bruhv2:
            return await payload.member.send(
                'You already have a ticket opened! Incase, your ticket channel was deleted, please run `.cleartickets`!')
        role_obj = guild.get_role(support_id["support_role"])
        overwrites = {
                guild.default_role: discord.PermissionOverwrite(
                    read_messages=False,
                    send_messages=False,
                ),
                payload.member: discord.PermissionOverwrite(
                    read_messages=True,
                    send_messages=True,
                )
            }
        if role_obj is not None:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(
                    read_messages=False,
                    send_messages=False,
                ),
                payload.member: discord.PermissionOverwrite(
                    read_messages=True,
                    send_messages=True,
                ),
                role_obj: discord.PermissionOverwrite(
                    read_messages=True,
                    send_messages=True,
                )
            }
        channel = await guild.create_text_channel(
            f'ticket-{payload.member.name}',
            overwrites=overwrites,
            reason="Essentials Ticket System")
        id_tick = random_char(30)
        em = discord.Embed(
            title='Ticket',
            description=f'Welcome {payload.member.mention} to your ticket. Support will be with you soonly!'
        )
        await payload.member.send(embed=discord.Embed(
            title='Tickets',
            description=f'Your ticket with the id `{id_tick}` has been successfully opened!'
        ))
        em.set_footer(text=f'Ticket ID: {id_tick} | .faq')
        await channel.send(embed=em)
        await self.bot.pool.execute(
            'INSERT INTO tickets (guildid, userid, ticketid, channelid) VALUES ($1, $2, $3, $4)',
            payload.guild_id, payload.member.id, id_tick, channel.id)
        try:
            if log[0]["logs"] is not None:
                channel = guild.get_channel(log[0]["logs"])
                em = discord.Embed(
                    title='Ticket Oppened',
                    description=f'Ticket ID: `{id_tick}`\n'
                                f'Owner: `{payload.member.name}`\n'
                )
                return await channel.send(embed=em)
        except IndexError:
            pass

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_guild_permissions(manage_channels=True,
                                        send_messages=True,
                                        manage_messages=True,
                                        add_reactions=True
                                        )
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def faq(self, ctx):
        if 'ticket' in ctx.channel.name:
            em = discord.Embed(
                title='Tickets',
                description='Click **[here](https://docs.google.com/document/d/1zsOAPWc8uEaGbZl8SnUJebzEMl1yHTeBCVKwHpSKqP8/edit?usp=sharing)** for more information on the ticket system.'
            )
            await ctx.send(embed=em)
        else:
            await ctx.send('You may not run this command in non-ticket channels.')

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_guild_permissions(manage_channels=True,
                                        send_messages=True,
                                        manage_messages=True,
                                        add_reactions=True
                                        )
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def close(self, ctx, ticket=None, *, reason=None):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                v2 = await connection.fetch('SELECT channelid FROM tickets WHERE guildid=$1 AND ticketid=$2',
                                            ctx.guild.id,
                                            ticket)
                v1 = await connection.fetch('SELECT userid FROM tickets WHERE guildid=$1 AND ticketid=$2', ctx.guild.id,
                                            ticket)
                perm = await connection.fetch('SELECT support_role FROM tickets_on WHERE guildid=$1',
                                              ctx.guild.id)
        try:
            log = await self.bot.pool.fetch('SELECT logs FROM tickets_on WHERE guildid=$1;', ctx.guild.id)
            if ticket is None:
                v3owo = await self.bot.pool.fetch('SELECT * FROM tickets WHERE guildid=$1 AND channelid=$2',
                                            ctx.guild.id, ctx.channel.id)
                try:
                    if v3owo[0]["channelid"] is not None:
                        if perm[0]["support_role"] is not None:
                            role = ctx.guild.get_role(perm[0]["support_role"])
                            if role not in ctx.author.roles:
                                return await ctx.send('You may not use this command. 1')
                            channel = ctx.guild.get_channel(v3owo[0]["channelid"])
                            await ctx.send('The ticket will be closed in 5 seconds.')
                            await asyncio.sleep(5)
                            await channel.delete()
                            member = ctx.guild.get_member(v3owo[0]["userid"])
                            await member.send(embed=discord.Embed(
                                title='Tickets',
                                description=f'Your ticket with the id `{v3owo[0]["ticketid"]}` has been closed by `{ctx.author.name}` for:'
                                            f' `No reason provided`'
                            ))
                            await self.bot.pool.execute(f'DELETE FROM tickets WHERE ticketid=$1 AND guildid=$2;',
                                                        v3owo[0]["ticketid"],
                                                        ctx.guild.id)
                            try:
                                if log[0]["logs"] is not None:
                                    channel = ctx.guild.get_channel(log[0]["logs"])
                                    em = discord.Embed(
                                        title='Ticket Closed',
                                        description=f'Ticket ID: `{ticket}`\n'
                                                    f'Owner: `{member.name}`\n'
                                                    f'Closed by: `{ctx.author.name}`\n'
                                                    f'Reason: `{reason}`\n'
                                    )
                                    return await channel.send(embed=em)
                            except IndexError:
                                pass
                        else:
                            if ctx.author.guild_permissions.kick_members is True:
                                channel = ctx.guild.get_channel(v3owo[0]["channelid"])
                                await ctx.send('The ticket will be closed in 5 seconds.')
                                await asyncio.sleep(5)
                                await channel.delete()
                                member = ctx.guild.get_member(v3owo[0]["userid"])
                                await member.send(embed=discord.Embed(
                                    title='Tickets',
                                    description=f'Your ticket with the id `{v3owo[0]["ticketid"]}` has been closed by `{ctx.author.name}` for:'
                                                f' `No reason provided`'
                                ))
                                await self.bot.pool.execute(f'DELETE FROM tickets WHERE ticketid=$1 AND guildid=$2;',
                                                            v3owo[0]["ticketid"],
                                                            ctx.guild.id)
                                try:
                                    if log[0]["logs"] is not None:
                                        channel = ctx.guild.get_channel(log[0]["logs"])
                                        em = discord.Embed(
                                            title='Ticket Closed',
                                            description=f'Ticket ID: `{ticket}`\n'
                                                        f'Owner: `{member.name}`\n'
                                                        f'Closed by: `{ctx.author.name}`\n'
                                                        f'Reason: `{reason}`\n'
                                        )
                                        return await channel.send(embed=em)
                                except IndexError:
                                    pass
                            else:
                                await ctx.send('You may not use this command. 2')
                except IndexError:
                    return await ctx.send('I couldn\'t find that channel!')
            if perm[0]["support_role"] is not None:
                tck_close_res = reason
                if reason is None:
                    tck_close_res = "No reason provided"
                role = ctx.guild.get_role(perm[0]["support_role"])
                if role not in ctx.author.roles:
                    return await ctx.send('You may not use this command. 1')
                channel = ctx.guild.get_channel(v2[0]["channelid"])
                await ctx.send('The ticket will be closed in 5 seconds.')
                await asyncio.sleep(5)
                await channel.delete()
                member = ctx.guild.get_member(v1[0]["userid"])
                await member.send(embed=discord.Embed(
                    title='Tickets',
                    description=f'Your ticket with the id `{ticket}` has been closed by `{ctx.author.name}` for: `{tck_close_res}`'
                ))
                await self.bot.pool.execute(f'DELETE FROM tickets WHERE ticketid=$1 AND guildid=$2;', ticket,
                                            ctx.guild.id)
                try:
                    if log[0]["logs"] is not None:
                        channel = ctx.guild.get_channel(log[0]["logs"])
                        em = discord.Embed(
                            title='Ticket Closed',
                            description=f'Ticket ID: `{ticket}`\n'
                                        f'Owner: `{member.name}`\n'
                                        f'Closed by: `{ctx.author.name}`\n'
                                        f'Reason: `{reason}`\n'
                        )
                        await channel.send(embed=em)
                except IndexError:
                    pass
            else:
                if ctx.author.guild_permissions.kick_members is True:
                    channel = ctx.guild.get_channel(v2[0]["channelid"])
                    await ctx.send('The ticket will be closed in 5 seconds.')
                    await asyncio.sleep(5)
                    await channel.delete()
                    member = ctx.guild.get_member(v1[0]["userid"])
                    await member.send(embed=discord.Embed(
                        title='Tickets',
                        description=f'Your ticket with the id `{ticket}` has been closed by `{ctx.author.name}` for: `{reason}`'
                    ))
                    await self.bot.pool.execute(f'DELETE FROM tickets WHERE ticketid=$1 AND guildid=$2;', ticket,
                                                ctx.guild.id)
                    try:
                        if log[0]["logs"] is not None:
                            channel = ctx.guild.get_channel(log[0]["logs"])
                            em = discord.Embed(
                                title='Ticket Closed',
                                description=f'Ticket ID: `{ticket}`\n'
                                            f'Owner: `{member.name}`\n'
                                            f'Closed by: `{ctx.author.name}`\n'
                                            f'Reason: `{reason}`\n'
                            )
                            await channel.send(embed=em)
                    except IndexError:
                        pass
                else:
                    await ctx.send('You may not use this command. 2')
        except AttributeError:
            return await self.bot.pool.execute(f'DELETE FROM tickets WHERE ticketid=$1 AND guildid=$2;', ticket,
                                               ctx.guild.id)
        except IndexError:
            return await ctx.send('I couldn\'t find that ticket!')

def setup(bot):
    bot.add_cog(DisVerify(bot))
