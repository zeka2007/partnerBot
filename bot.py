import discord
from discord.ext import commands
from config import setting

client = commands.Bot(command_prefix = setting['PREFIX'],  intents = discord.Intents.all())
reactionchannel = [777962327357653022,
    778141789500080148,
    778142046954455041,
    778142261476458516,
    778142496856866817]
client.remove_command('help')


@client.event
async def on_ready():
    print('ready')
@client.event
async def on_member_join(member):
    channel = client.get_channel(779329178285506590)
    info_channel = client.get_channel(761648095234621462)
    rules_channel = client.get_channel(778136828204679199)
    emb = discord.Embed(description = f"{member}, тебя приветствует сервер {member.guild.name}.\nОбязательно ознакомься с {info_channel.mention} и {rules_channel.mention}", color = discord.Color.green())
    await channel.send(embed = emb)
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
    member = payload.member
    # if not payload.channel_id in reactionchannel:  # ID сообщения на которое нужно ставить реакции
    #     return
    if member == client.user:
        return
    if payload.emoji.name == '⚠️':  # или payload.emoji.name == "✔" для unicode-эмодзей
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
        emb.add_field(name = 'Команды для Администраторов:', value = 'appealAccept, appealNotAccepted')
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
client.run(setting['TOKEN'])
