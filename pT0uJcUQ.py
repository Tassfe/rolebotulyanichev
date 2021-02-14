import discord
from discord import utils

import config

TOKEN = 'ODEwMTc0NDY3NDYzOTcwODE2.YCfzxQ.RKcSc6LcPp4qW5CLWs3xlYBpm5U'

POST_ID = 810199131409743872

ROLES = {
    '😀' : 810177534637244446,
}

MAX_ROLES_PER_USER = 1000

EXCROLES = ()

intents = discord.Intents.all()

class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged on as {0}!'.format(self.user))

	async def on_raw_reaction_add(self, payload):
		if payload.message_id == POST_ID:
			channel = self.get_channel(payload.channel_id) # РїРѕР»СѓС‡Р°РµРј РѕР±СЉРµРєС‚ РєР°РЅР°Р»Р°
			message = await channel.fetch_message(payload.message_id) # РїРѕР»СѓС‡Р°РµРј РѕР±СЉРµРєС‚ СЃРѕРѕР±С‰РµРЅРёСЏ
			member = utils.get(message.guild.members, id=payload.user_id) # РїРѕР»СѓС‡Р°РµРј РѕР±СЉРµРєС‚ РїРѕР»СЊР·РѕРІР°С‚РµР»СЏ РєРѕС‚РѕСЂС‹Р№ РїРѕСЃС‚Р°РІРёР» СЂРµР°РєС†РёСЋ

			try:
				emoji = str(payload.emoji) # СЌРјРѕРґР¶РёРє РєРѕС‚РѕСЂС‹Р№ РІС‹Р±СЂР°Р» СЋР·РµСЂ
				role = utils.get(message.guild.roles, id=ROLES[emoji]) # РѕР±СЉРµРєС‚ РІС‹Р±СЂР°РЅРЅРѕР№ СЂРѕР»Рё (РµСЃР»Рё РµСЃС‚СЊ)

				if(len([i for i in member.roles if i.id not in EXCROLES]) <= MAX_ROLES_PER_USER):
					await member.add_roles(role)
					print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
				else:
					await message.remove_reaction(payload.emoji, member)
					print('[ERROR] Too many roles for user {0.display_name}'.format(member))

			except KeyError as e:
				print('[ERROR] KeyError, no role found for ' + emoji)
			except Exception as e:
				print(repr(e))

	async def on_raw_reaction_remove(self, payload):
		channel = self.get_channel(payload.channel_id) # получаем объект канала
		message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
		member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию

		try:
			emoji = str(payload.emoji) # эмоджик который выбрал юзер
			role = utils.get(message.guild.roles, id=ROLES[emoji]) # объект выбранной роли (если есть)

			await member.remove_roles(role)
			print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))

		except KeyError as e:
			print('[ERROR] KeyError, no role found for ' + emoji)
		except Exception as e:
			print(repr(e))

# RUN
client = MyClient(intents = discord.Intents.all())
client.run(TOKEN)