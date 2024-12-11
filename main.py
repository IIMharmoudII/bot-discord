import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import random
import os
import json
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

# Charger les variables d'environnement
load_dotenv()
TOKEN = os.getenv('TOKEN_BOT_DISCORD')

# Configurer les intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Initialisation du bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Variables globales
user_qi = {}
user_aura = {}
data_file = "user_data.json"
command_list = [
    "insulte", "compliment", "citation", "blague", "qi", "commandes",
    "pileouface", "lancerdé", "ping", "pub", "aura", "classement", "pfc"
]

# === Données pour insultes, compliments et autres ===
insultes = [
    ("glope saucisse", 500),
    ("sac à foutre", 1000),
    ("ramassis de fond d'capote", 1500),
    ("t'es un gluant", 300),
    ("t qu'un bouffeur de niglo", 700),
    ("bouffe mes couilles et étouffe-toi avec", 2000)
]

compliments = [
    ("t'es une étoile dans l'univers", 500),
    ("tu es un pilier pour tes amis", 1000),
    ("tu illumines la pièce en entrant", 700),
    ("tu as un sourire contagieux", 300),
    ("on devrait te cloner pour rendre le monde meilleur", 1500)
]

# Charger les données depuis un fichier JSON
def load_data():
    global user_qi, user_aura
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            data = json.load(f)
            user_qi = data.get("user_qi", {})
            user_aura = data.get("user_aura", {})

# Sauvegarder les données dans un fichier JSON
def save_data():
    with open(data_file, "w") as f:
        json.dump({"user_qi": user_qi, "user_aura": user_aura}, f)

load_data()

# === Serveur Web pour garder le bot actif ===
app = Flask('')

@app.route('/')
def home():
    return "Le bot est en ligne !"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
@bot.command()
@cooldown(1, 30, BucketType.user)
async def insulte(ctx, member: discord.Member = None):
    if member is None:
        member = random.choice(ctx.guild.members)
    if member.bot:
        await ctx.send("Je ne peux pas insulter un bot.")
        return
    if member == ctx.author:
        await ctx.send("Tu ne peux pas t'insulter toi-même.")
        return

    insulte, aura_perdue = random.choice(insultes)
    user_aura[member.id] = user_aura.get(member.id, 0) - aura_perdue
    save_data()
    await ctx.send(f"{member.mention}, {insulte} (-{aura_perdue} aura)")

@bot.command()
@cooldown(1, 30, BucketType.user)
async def compliment(ctx, member: discord.Member = None):
    if member is None:
        member = random.choice(ctx.guild.members)
    if member.bot:
        await ctx.send("Je ne peux pas complimenter un bot.")
        return
    if member == ctx.author:
        await ctx.send("Tu ne peux pas te complimenter toi-même.")
        return

    compliment, aura_gagnee = random.choice(compliments)
    user_aura[member.id] = user_aura.get(member.id, 0) + aura_gagnee
    save_data()
    await ctx.send(f"{member.mention}, {compliment} (+{aura_gagnee} aura)")

@bot.command()
async def aura(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    aura = user_aura.get(member.id, 0)
    await ctx.send(f"{member.mention} a {aura} points d'aura.")

@bot.command()
async def classement(ctx):
    sorted_users = sorted(user_aura.items(), key=lambda x: x[1], reverse=True)
    leaderboard = "\n".join(
        f"{i + 1}. <@{user_id}> : {aura} aura"
        for i, (user_id, aura) in enumerate(sorted_users[:10])
    )
    await ctx.send(f"**Classement des 10 meilleurs auras :**\n{leaderboard}")
@bot.command()
@cooldown(1, 30, BucketType.user)
async def insulte(ctx, member: discord.Member = None):
    if member is None:
        member = random.choice(ctx.guild.members)
    if member.bot:
        await ctx.send("Je ne peux pas insulter un bot.")
        return
    if member == ctx.author:
        await ctx.send("Tu ne peux pas t'insulter toi-même.")
        return

    insulte, aura_perdue = random.choice(insultes)
    user_aura[member.id] = user_aura.get(member.id, 0) - aura_perdue
    save_data()
    await ctx.send(f"{member.mention}, {insulte} (-{aura_perdue} aura)")

@bot.command()
@cooldown(1, 30, BucketType.user)
async def compliment(ctx, member: discord.Member = None):
    if member is None:
        member = random.choice(ctx.guild.members)
    if member.bot:
        await ctx.send("Je ne peux pas complimenter un bot.")
        return
    if member == ctx.author:
        await ctx.send("Tu ne peux pas te complimenter toi-même.")
        return

    compliment, aura_gagnee = random.choice(compliments)
    user_aura[member.id] = user_aura.get(member.id, 0) + aura_gagnee
    save_data()
    await ctx.send(f"{member.mention}, {compliment} (+{aura_gagnee} aura)")

@bot.command()
async def aura(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    aura = user_aura.get(member.id, 0)
    await ctx.send(f"{member.mention} a {aura} points d'aura.")

@bot.command()
async def classement(ctx):
    sorted_users = sorted(user_aura.items(), key=lambda x: x[1], reverse=True)
    leaderboard = "\n".join(
        f"{i + 1}. <@{user_id}> : {aura} aura"
        for i, (user_id, aura) in enumerate(sorted_users[:10])
    )
    await ctx.send(f"**Classement des 10 meilleurs auras :**\n{leaderboard}")
