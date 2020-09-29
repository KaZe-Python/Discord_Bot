import discord
from discord.utils import get
from discord.abc import Messageable

def getter(instance, iterator):
    data = get(instance, id = iterator)
    return data

def get_message(id):
    data = Messageable.fetch_message(id)
    return data
