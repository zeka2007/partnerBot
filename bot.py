import discord
from discord.ext import commands
from config import setting

client = commands.Bot(command_prefix = setting['PREFIX'],  intents = discord.Intents.all())
reactionchannel = setting['channels']
guild = client.get_guild(761648095234621460)

client.remove_command('help')


@client.event
async def on_ready():
    activity = discord.Activity(name='.partner в ЛС | .help', type=discord.ActivityType.listening)
    await client.change_presence(activity = activity)
    print('ready')
# @client.event
# async def on_member_join(member):
    # channel = client.get_channel(779329178285506590)
    # info_channel = client.get_channel(761648095234621462)
    # rules_channel = client.get_channel(778136828204679199)
    # emb = discord.Embed(description = f"{member}, тебя приветствует сервер {member.guild.name}.\nОбязательно ознакомься с {info_channel.mention} и {rules_channel.mention}", color = discord.Color.green())
    # await channel.send(embed = emb)
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


    check_channel = guild.get_channel(812370126388592680)
    emoji = payload.emoji
    if pchannel == check_channel:
        if emoji.name == '❌':
            partner_channel = guild.get_channel(812045258572955748)
            message = await pchannel.fetch_message(payload.message_id)
            ids = []
            async for message in pchannel.history(limit = None):
                ids.append(message.id)


            message_p = await pchannel.fetch_message(ids[ids.index(message.id)-1])

            m = await partner_channel.fetch_message(int(message.content))
            # print(message_p.content)
            # print(message.content)
            # print(m.content)
            await message_p.delete()
            await message.delete()
            await m.delete()
        elif emoji.name == '✅':
            partner_channel = guild.get_channel(812045258572955748)
            message = await pchannel.fetch_message(payload.message_id)
            ids = []
            async for message in pchannel.history(limit = None):
                ids.append(message.id)


            message_p = await pchannel.fetch_message(ids[ids.index(message.id)-1])

            m = await partner_channel.fetch_message(int(message.content))
            # print(message_p.content)
            # print(message.content)
            # print(m.content)
            await message_p.delete()
            await message.delete()
@client.event
async def on_raw_reaction_remove(payload):
    member = await (await client.fetch_guild(payload.guild_id)).fetch_member(payload.user_id)
    if not payload.emoji.name == '⚠️':
        return
    if 778610047575654420 in [y.id for y in member.roles]:
        role = member.guild.get_role(778610047575654420)
        await member.remove_roles(role)
@client.command()
@commands.has_role(772122310244040755)
async def appealAccept(ctx, member: discord.Member):
    await ctx.message.delete()
    if 778610047575654420 in [y.id for y in member.roles]:
        await ctx.send('Жалоба участника {} была одобрена!'.format(member))
        role = discord.utils.get(member.guild.roles, id = 778610047575654420)
        await member.remove_roles(role)
    else:
        await ctx.send('Участник {} не подавал жалобу.'.format(member))
@client.command()
@commands.has_role(772122310244040755)
async def appealNotAccepted(ctx, member: discord.Member):
    await ctx.message.delete()
    if 778610047575654420 in [y.id for y in ctx.message.author.roles]:
        await ctx.send('Жалоба участника {} была отклонена!'.format(member))
        role = discord.utils.get(member.guild.roles, id = 778610047575654420)
        await member.remove_roles()
    else:
        await ctx.send('Участник {} не подавал жалобу.'.format(member))

@client.command()
@commands.dm_only()
async def partner(ctx):
    await ctx.send('Отправьте в канал для партнёров на вашем сервере вот это объявление:')
    await ctx.send("""‧₊˚✧ *·˚ ・゜+.  ✦ . ⁺  . ‧˖˚ ‧₊˚✧ . ⁺ ₊ ・+.  ✦ . ⁺ . ₊ ‧₊˚✧ *·˚
**⠀⠀⠀⠀Отзывы о серверах и партнёрствах⠀⠀⠀⠀**
‧₊˚✧ *·˚ ・゜+.  ✦ . ⁺  . ‧˖˚ ‧₊˚✧ . ⁺ ₊ ・+.  ✦ . ⁺ . ₊ ‧₊˚✧ *·˚

**Ищите себе партнёров? Наша дипломатичная площадка предоставляет огромный ассортимент партнёров!**

๑✅꒱・система "галочек"
๑\🎗️꒱・администрация 24/7
๑\🤝꒱・партнёрская программа
๑\🍡꒱・приятный дизайн
๑\☄️꒱・постоянные обновления

**Чего же вы ждёте переходите на новый уровень партнёрства прямо сейчас!**

๑\📌꒱・Гифка: https://cdn.discordapp.com/attachments/758679835647541251/812053288148140032/ezgif-4-5cb50d59a33c.gif
๑\🛎・Пинг:  @everyone @here
๑\📎・Ссылка: https://discord.gg/Q8h4VESMu3""")
    guild = client.get_guild(761648095234621460)


    channel = ctx.channel
    partner_channel = guild.get_channel(812045258572955748)
    check_img_channel = guild.get_channel(812370126388592680)
    await channel.send('После этого отправьте "готово".')

    def check(m):
        return m.content == 'готово' and m.channel == channel
    def check_img(m):
        return m.attachments != [] and m.channel == channel
    def check_desc(m):
        if not m.content.find('https://discord.gg/') == -1:
            return m.channel == channel
        else:
            return False
    msg = await client.wait_for('message', check=check)
    await ctx.send(f'теперь отправьте описание вашего сервера ')
    msg = await client.wait_for('message', check = check_desc)
    await ctx.send('Отправьте скриншот с нашим объявлением. Обратите внимание, что все фотографии проверяются модераторами.')
    message = await client.wait_for('message', check = check_img)
    partner_message = await partner_channel.send(msg.content)
    await check_img_channel.send(partner_message.id)
    check_message = await check_img_channel.send(message.attachments[0].url)
    await check_message.add_reaction('✅')
    await check_message.add_reaction('❌')

    await ctx.send('Ваше объявление было отправлено!')

    member = discord.utils.get(guild.members, id = msg.author.id)
    role = guild.get_role(812349807070412832)
    await member.add_roles(role)

@client.command()
async def help(ctx):
    member = ctx.author
    channel = ctx.channel

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
    await channel.send('Я отправил инструкцию Вам в ЛС.')
client.run(setting['TOKEN'])
