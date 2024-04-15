import settings
import discord
from discord.ext import commands

privileged_roles = {1172643890646483087, 1172648096967172186}
weiterleitung_role = 1172658831092875295
weiterleitung_id = 1223335631216971796
abstimmung_id = 1226528532583288953

def run():
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="?", intents=intents)


    @bot.event
    async def on_message(message):

        if message.content.startswith('?acheating'):
            await message.delete()
            channel = message.channel
            user_ids = set()


            async for msg in channel.history(limit=None):
                user_ids.add(msg.author.id)

            for user_id in user_ids:
                member = await channel.guild.fetch_member(user_id)
                member_role_ids = {role.id for role in member.roles}

                if privileged_roles.isdisjoint(member_role_ids):
                    await message.channel.send(f"""
Hallo <@{user_id}>,

Deine Aufnahme wurde überprüft und du erhältst hiermit einen permanenten Bann für Cheating.
Wenn du weiterhin auf unserem Gameserver spielen möchtest kannst du dich mit einer Donation freikaufen.

MfG,
Utopia Gangwar AC-Team

                                    """)

                    weiterleitung_target = bot.get_channel(weiterleitung_id)
                    await weiterleitung_target.send(f"""
<@&{weiterleitung_role}>
User `{user_id}` **bannen**.
Grund: Cheating
                                    """)


    @bot.event
    async def on_reaction_add(reaction, user):
        if reaction.message.channel.id == weiterleitung_id and str(reaction.emoji) == '✅':
            if reaction.message.channel.permissions_for(reaction.message.guild.me).manage_messages:
                await reaction.message.delete()
        elif str(reaction.emoji) == '📷':
            message_content = reaction.message.content
            original_channel = reaction.message.channel.id
            thread_name = f"({reaction.message.channel} Abstimmung)"
            abstimmung_target = bot.get_channel(abstimmung_id)

            abstimmung_message = await abstimmung_target.send(f"""{message_content} | <#{original_channel}>""")

            await abstimmung_message.add_reaction('✅')
            await abstimmung_message.add_reaction('❌')
            await abstimmung_message.create_thread(name=thread_name)

            channel = reaction.message.channel
            user_ids = set()

            async for msg in channel.history(limit=None):
                user_ids.add(msg.author.id)

            for user_id in user_ids:
                member = await channel.guild.fetch_member(user_id)
                member_role_ids = {role.id for role in member.roles}

                if privileged_roles.isdisjoint(member_role_ids):
                    await reaction.message.channel.send(f"""
Hallo <@{user_id}>,

Deine Aufnahme wird sofort geprüft. Du kannst in der Zwischenzeit wieder auf unseren Server connecten.

MfG Utopia Gangwar Anticheat Team
                            """)

                    weiterleitung_target = bot.get_channel(weiterleitung_id)
                    await weiterleitung_target.send(f"""
<@&{weiterleitung_role}>
User `{user_id}` **entbannen**.
Grund: Aufnahme eingereicht
                            """)


    bot.run(settings.DISCORD_API_SECRET)

if __name__ == "__main__":
    run()
