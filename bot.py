import discord
from discord.ext import commands
from config import setting

client = commands.Bot(command_prefix = setting['PREFIX'],  intents = discord.Intents.all())
reactionchannel = setting['channels']
guild = client.get_guild(761648095234621460)

client.remove_command('help')


@client.event
async def on_ready():
    activity = discord.Activity(name='.help', type=discord.ActivityType.listening)
    await client.change_presence(activity = activity)
    print('ready')

@client.event
async def on_command_error(ctx, error):
    guild = client.get_guild(761648095234621460)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'**{ctx.author}**, команда использует обязательный аргумент `{error.param.name}`.')
    elif isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.TooManyArguments):
        await ctx.send(f'**{ctx.author}**, вы отправили слишком много аргументов.')
    elif isinstance(error, commands.MissingRole):
        await ctx.send(f'**{ctx.author}**, у вас нет роли `{guild.get_role(error.missing_role).name}` для использования этой команды')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f'**{ctx.author}**, у вас нет прав {i for i in error.missing_perms} для использования это команды.')
    else:
        await ctx.send(f'Во время выполнения команды произошла ошибка:\n||**{error}**||')
@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.channel.id in reactionchannel:
        t = message.content
        if t.find('https://discord.gg') == -1:
            await message.delete()
            emb = discord.Embed(title = '{0.author}, ваше сообщение было удалено по причине отсутствия и/или недействительности ссылки!'.format(message),
            color = discord.Color.red())
            await message.author.send(embed = emb)
        else:
            guild_user_role = discord.utils.get(message.author.guild.roles, id = 772121588769226762)
            await message.add_reaction('👍')
            await message.add_reaction('👎')
            await message.add_reaction('⚠️')
            await message.author.add_roles(guild_user_role)


@client.event
async def on_raw_reaction_add(payload):
    guild = client.get_guild(761648095234621460)

    member = payload.member
    pchannel = guild.get_channel(payload.channel_id)
    # if not payload.channel_id in reactionchannel:  # ID сообщения на которое нужно ставить реакции
    #     return
    if member == client.user:
        return
    if payload.emoji.name == '⚠️':
        alarm_channel = client.get_channel(777962537631088720)
        channel = client.get_channel(payload.channel_id)
        async for message in channel.history(limit = None):
            if message.id == payload.message_id:
                user = client.get_user(payload.user_id)
                emb = discord.Embed(title = "Отправлена жалоба!", color = discord.Color.red())
                emb.add_field(name = "Текст сообщения:", value = message.content)
                emb.set_footer(text = f"Жалобу подал: {user}", icon_url = user.avatar_url)
                await alarm_channel.send( embed = emb)

        role = discord.utils.get(member.guild.roles, id = 778610047575654420)
        emb = discord.Embed(title = '{0.member}, вы отправили жалобу на один из серверов. Для её составления обратитесь к инструкции на сервере.\nid канала: {0.channel_id}'.format(payload),
        color = discord.Color.green())
        await member.add_roles(role)
        await member.send(embed = emb)

    if payload.message_id == 779676453431279626:
        dev1 = client.get_user(551810310747717633)
        dev2 = client.get_user(615595496525791295)

        emb = discord.Embed(title = f'{client.user.name} - бот для сервера {member.guild.name}', color = discord.Color.green())
        emb.set_thumbnail(url = client.user.avatar_url)
        emb.add_field(name = 'В чём смысл этого бота?', value = 'Этот бот помогает автоматизировать процессы на сервере и помочь новым пользователем сделать первые шаги на нём.')
        emb.add_field(name = 'Преминение:', value = 'Для создателей серверов данный бот поможет опубликовать объявление, а для пользователей Discord - возможность оценить чей-нибудь проект.')
        emb.add_field(name = 'Команды для Администраторов:', value = '.appealAccept, .appealNotAccepted')
        emb.add_field(name = 'Команды для Пользователей:', value = '.help, .partner')
        emb.set_footer(text = f'Разработчики: {dev1.name} и {dev2.name}', icon_url = client.user.avatar_url)
        await member.send(embed = emb)



@client.event
async def on_raw_reaction_remove(payload):
    member = await (await client.fetch_guild(payload.guild_id)).fetch_member(payload.user_id)
    if not payload.emoji.name == '⚠️':
        return
    if 778610047575654420 in [y.id for y in member.roles]:
        role = member.guild.get_role(778610047575654420)
        await member.remove_roles(role)
@client.command(neme = 'appealAccept', aliases = ['appealAccepted','жалоба_принята', 'фззуфдФссузев'])
@commands.has_role(772122310244040755)
async def appealAccept(ctx, member: discord.Member):
    await ctx.message.delete()
    if 778610047575654420 in [y.id for y in member.roles]:
        await ctx.send('Жалоба участника {} была одобрена!'.format(member))
        role = discord.utils.get(member.guild.roles, id = 778610047575654420)
        await member.remove_roles(role)
    else:
        await ctx.send('Участник {} не подавал жалобу.'.format(member))
@client.command(name = 'appealNotAccepted', aliases = ['appealNotAccept', 'отклонить_жалобу', 'фззуфдТщеФссузев'])
@commands.has_role(772122310244040755)
async def appealNotAccepted_(ctx, member: discord.Member):
    await ctx.message.delete()
    if 778610047575654420 in [y.id for y in ctx.message.author.roles]:
        await ctx.send('Жалоба участника {} была отклонена!'.format(member))
        role = discord.utils.get(member.guild.roles, id = 778610047575654420)
        await member.remove_roles()
    else:
        await ctx.send('Участник {} не подавал жалобу.'.format(member))

@client.command(name = 'help', aliases = ['помощь', 'рудз'])
async def help_(ctx, arg = None):
    member = ctx.author
    channel = ctx.channel
    if arg == None:
        dev1 = client.get_user(551810310747717633)
        dev2 = client.get_user(615595496525791295)

        emb = discord.Embed(title = f'{client.user.name} - бот для сервера {member.guild.name}', color = discord.Color.green())
        emb.set_thumbnail(url = client.user.avatar_url)
        emb.add_field(name = 'В чём смысл этого бота?', value = 'Этот бот помогает автоматизировать процессы на сервере и помочь новым пользователем сделать первые шаги на нём.')
        emb.add_field(name = 'Преминение:', value = 'Для создателей серверов данный бот поможет опубликовать объявление, а для пользователей Discord - возможность оценить чей-нибудь проект.')
        emb.add_field(name = 'Команды для Администраторов:', value = '.appealAccept, .appealNotAccepted')
        emb.add_field(name = 'Команды для Пользователей:', value = '.help')
        emb.set_footer(text = f'Разработчики: {dev1.name} и {dev2.name}', icon_url = client.user.avatar_url)
        await member.send(embed = emb)
        await channel.send('Я отправил инструкцию Вам в ЛС.')
    elif arg.lower() == 'commands' or arg.lower() == 'команды':
        emb = discord.Embed(title = 'Команды:', color = discord.Color.green())
        emb.set_thumbnail(url = 'https://raw.githubusercontent.com/DevItsMB/DevItsMB/master/verified_developer_badge.png')
        emb.add_field(name = 'Команды для Администраторов:',
        value = '**.appealAccept <member>** - принять жалобу участника, **.appealNotAccepted <member>** - отклонить жолобу участника', inline = False)
        emb.add_field(name = 'Команды для Пользователей:',
        value = '**.help [category]** - помощь', inline = False)
        await member.send(embed = emb)
        await channel.send('Я отправил инструкцию Вам в ЛС.')
client.run(setting['TOKEN'])
