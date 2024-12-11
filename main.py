import discord
from discord.ext import commands, tasks
import random
import os
from dotenv import load_dotenv
from flask import Flask
from threading import Thread
from difflib import get_close_matches
from datetime import datetime, timedelta

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
user_coins = {}
user_last_claim = {}  # Pour vérifier si l'utilisateur a réclamé ses coins journaliers
command_list = ["insulte", "compliment", "citation", "blague", "qi", "commandes", "pileouface", "lancerdé", "ping", "shutdown", "pub", "coins", "donnercoins", "journalier", "classement", "boutique"]

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

# === Commandes du bot ===

@bot.command()
async def pub(ctx):
    message = (
        "𓂃ꕤ 🎀  Sydney 🧸 #ғя  est un Nouveau serveur  🎀\n\n"
        "🎓   Avec une communauté safe\n"
        "🏰   Où faire de nouvelles rencontres\n"
        "🏆   Gagne des rôles en étant Actif sur le serveur\n"
        "🎲   Du Gambling et pleins d'autres jeux\n"
        "🎉   Pleins d'évènements qui arrive\n"
        "✨   Un rôle OG pour le début du serveur !\n\n"
        "彡   🎗️ Qu'attends-tu pour rejoindre !\n\n"
        "🏯   https://discord.gg/sydneyfr"
    )
    await ctx.send(message)

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong ! Latence: {round(bot.latency * 1000)}ms")

@bot.command()
async def pileouface(ctx):
    result = random.choice(["Face", "Pile"])
    await ctx.send(f"Résultat: {result}")

@bot.command()
async def lancerdé(ctx):
    roll = random.randint(1, 6)
    await ctx.send(f"Tu as lancé un {roll}.")

@bot.command()
async def citation(ctx):
    citations = [
        "L'avenir appartient à ceux qui croient en la beauté de leurs rêves. - Eleanor Roosevelt",
        "Ce n'est pas la taille du chien dans la lutte, mais la taille de la lutte dans le chien. - Mark Twain",
        "Ne pleure pas parce que c'est fini, souris parce que ça a eu lieu. - Dr. Seuss",
        "La vie est ce qui arrive quand on est occupé à faire d'autres projets. - John Lennon"
    ]
    await ctx.send(random.choice(citations))

@bot.command()
async def commandes(ctx):
    embed = discord.Embed(
        title="Liste des Commandes",
        description="Voici les commandes disponibles sur ce serveur !",
        color=discord.Color.blue()
    )
    for command in command_list:
        embed.add_field(name=f"!{command}", value=f"Exécuter la commande `{command}`.", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def insulte(ctx, member: discord.Member = None):
    insultes = [
        "moulin à bite",
        "je te pisse dessus, cordialement.",
        "tu es moche, sacré glope.",
        "tu n'es qu'un manche canette.",
        "glope saucisse",
        "espece de sac a foutre",
        "t'es qu'un rammasi de fond d'capote",
        "t'es un gluant",
        "t'es qu'un bouffeur de niglo",
        "Ton QI est tellement bas qu'il est en négatif.",
        "Tu es un vrai mystère... même pour les sciences modernes."
    ]

    if member is None:
        if ctx.guild:
            human_members = [m for m in ctx.guild.members if not m.bot]
            if not human_members:
                await ctx.send("Il n'y a pas de membres humains à insulter.")
                return
            member = random.choice(human_members)
        else:
            await ctx.send("Cette commande doit être utilisée dans un serveur.")
            return

    if member.bot:
        await ctx.send("Je ne peux pas insulter un bot.")
        return

    await ctx.send(f"{member.mention}, {random.choice(insultes)}")

@bot.command()
async def compliment(ctx, member: discord.Member = None):
    compliments = [
        "Tu es brillant(e) comme une étoile dans la nuit.",
        "Tu illumines la pièce dès que tu entres.",
        "Tu es un véritable rayon de soleil pour ceux qui t'entourent.",
        "Tu es tellement talentueux(se), c’est impressionnant !"
    ]

    if member is None:
        if ctx.guild:
            human_members = [m for m in ctx.guild.members if not m.bot]
            if not human_members:
                await ctx.send("Il n'y a pas de membres humains à complimenter.")
                return
            member = random.choice(human_members)
        else:
            await ctx.send("Cette commande doit être utilisée dans un serveur.")
            return

    if member.bot:
        await ctx.send("Je ne peux pas complimenter un bot.")
        return

    await ctx.send(f"{member.mention}, {random.choice(compliments)}")

@bot.command()
async def journalier(ctx):
    user_id = ctx.author.id
    current_time = datetime.now()

    if user_id in user_last_claim:
        time_diff = current_time - user_last_claim[user_id]
        if time_diff < timedelta(days=1):
            remaining_time = timedelta(days=1) - time_diff
            await ctx.send(f"Tu as déjà réclamé tes coins aujourd'hui. Tu peux recommencer dans {remaining_time.seconds // 3600} heures et {(remaining_time.seconds % 3600) // 60} minutes.")
            return
    
    # Récompense journalière
    user_coins[user_id] = user_coins.get(user_id, 0) + 500
    user_last_claim[user_id] = current_time
    await ctx.send(f"Félicitations {ctx.author.mention}, tu as reçu 500 coins pour ta réclamation journalière !")

@bot.command()
async def classement(ctx):
    sorted_users = sorted(user_coins.items(), key=lambda x: x[1], reverse=True)
    leaderboard = "\n".join([f"{ctx.guild.get_member(user_id).name}: {coins} coins" for user_id, coins in sorted_users])
    await ctx.send(f"Classement des utilisateurs :\n{leaderboard}")

@bot.command()
async def coins(ctx):
    user_id = ctx.author.id
    coins = user_coins.get(user_id, 0)
    await ctx.send(f"{ctx.author.mention}, tu as actuellement {coins} coins.")

role_shop = {
    "Thalix": 15000,
    "Ragnar": 25000,
    "Lynther": 35000,
    "Orakaï": 45000
}

@bot.command()
async def boutique(ctx):
    embed = discord.Embed(title="Boutique des Rôles", description="Achetez des rôles en utilisant vos coins !", color=discord.Color.green())
    for role, price in role_shop.items():
        embed.add_field(name=role, value=f"{price} coins", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def acheter(ctx, role_name: str):
    if role_name not in role_shop:
        await ctx.send("Ce rôle n'existe pas dans la boutique.")
        return

    price = role_shop[role_name]
    user_id = ctx.author.id
    user_coins_count = user_coins.get(user_id, 0)

    if user_coins_count < price:
        await ctx.send(f"Tu n'as pas assez de coins pour acheter ce rôle. Il te manque {price - user_coins_count} coins.")
        return

    # Deduction des coins et attribution du rôle
    user_coins[user_id] -= price
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    await ctx.author.add_roles(role)
    await ctx.send(f"Félicitations {ctx.author.mention}, tu as acheté le rôle {role_name} !")

# Garder le bot actif
keep_alive()

# Lancer le bot
bot.run(TOKEN)

