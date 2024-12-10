import discord
from discord.ext import commands
import random
import os
import asyncio
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
user_aura = {}  # Stockage de l'aura des utilisateurs
last_action_time = {}  # Stockage des derniers moments des actions
aura_change = 10  # Points d'aura modifiés par compliment ou insulte
command_cooldown = timedelta(minutes=30)  # Délai entre deux actions
command_list = [
    "insulte", "compliment", "citation", "blague", "qi", "commandes", 
    "pileouface", "lancerdé", "ping", "shutdown", "pub", "aura", "classement"
]

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

# === Fonction pour gérer les délais ===
def can_perform_action(user_id, action):
    now = datetime.now()
    if user_id not in last_action_time:
        last_action_time[user_id] = {}
    if action not in last_action_time[user_id]:
        last_action_time[user_id][action] = now - command_cooldown
    return now - last_action_time[user_id][action] >= command_cooldown

def update_last_action(user_id, action):
    if user_id not in last_action_time:
        last_action_time[user_id] = {}
    last_action_time[user_id][action] = datetime.now()

# === Gestion des erreurs globales ===
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il manque un argument requis pour cette commande.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("L'argument fourni n'est pas valide.")
    elif isinstance(error, commands.CommandNotFound):
        command = ctx.invoked_with
        matches = get_close_matches(command, command_list, n=1, cutoff=0.6)
        if matches:
            await ctx.send(f"Cette commande n'existe pas. Peut-être vouliez-vous dire !{matches[0]} ?")
        else:
            await ctx.send("Cette commande n'existe pas. Tapez !commandes pour voir les commandes disponibles.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions nécessaires pour exécuter cette commande.")
    else:
        await ctx.send("Une erreur inattendue s'est produite.")
        raise error

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
async def insulte(ctx, member: discord.Member = None):
    user_id = ctx.author.id
    if not can_perform_action(user_id, "insulte"):
        remaining = command_cooldown - (datetime.now() - last_action_time[user_id]["insulte"])
        minutes, seconds = divmod(remaining.seconds, 60)
        await ctx.send(f"Tu dois attendre encore {minutes} minutes et {seconds} secondes avant d'insulter à nouveau.")
        return

    insultes = [
        "moulin à bite",
        "je te pisse dessus, cordialement.",
        "tu es moche, sacré glope.",
        "tu n'es qu'un manche canette.",
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

    # Réduction d'aura
    user_aura[ctx.author.id] = user_aura.get(ctx.author.id, 1000) - aura_change
    await ctx.send(f"{member.mention}, {random.choice(insultes)} (Aura restante : {user_aura[ctx.author.id]})")
    update_last_action(user_id, "insulte")

@bot.command()
async def compliment(ctx, member: discord.Member = None):
    user_id = ctx.author.id
    if not can_perform_action(user_id, "compliment"):
        remaining = command_cooldown - (datetime.now() - last_action_time[user_id]["compliment"])
        minutes, seconds = divmod(remaining.seconds, 60)
        await ctx.send(f"Tu dois attendre encore {minutes} minutes et {seconds} secondes avant de complimenter à nouveau.")
        return

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

    # Augmentation d'aura
    user_aura[ctx.author.id] = user_aura.get(ctx.author.id, 1000) + aura_change
    await ctx.send(f"{member.mention}, {random.choice(compliments)} (Aura actuelle : {user_aura[ctx.author.id]})")
    update_last_action(user_id, "compliment")

@bot.command()
async def aura(ctx):
    aura = user_aura.get(ctx.author.id, 1000)
    await ctx.send(f"{ctx.author.mention}, votre aura est de {aura} points.")

@bot.command()
async def classement(ctx):
    if not user_aura:
        await ctx.send("Personne n'a encore modifié son aura.")
        return
    classement = sorted(user_aura.items(), key=lambda x: x[1], reverse=True)
    message = "**Classement des auras :**\n"
    for i, (user_id, aura) in enumerate(classement, start=1):
        user = await bot.fetch_user(user_id)
        message += f"{i}. {user.name} : {aura} points\n"
    await ctx.send(message)

@bot.command()
async def citation(ctx):
    citations = [
        "La vie, c'est comme une bicyclette, il faut avancer pour ne pas perdre l'équilibre. - Albert Einstein",
        "Le succès, c'est tomber sept fois et se relever huit. - Proverbe japonais",
        "Ne crains pas d’avancer lentement, crains seulement de t’arrêter. - Proverbe chinois",
        "Si tu veux que la vie te sourie, apporte-lui d’abord ta bonne humeur. - Spinoza"
    ]
    await ctx.send(random.choice(citations))

@bot.command()
async def blague(ctx):
    blagues = [
        "Pourquoi les plongeurs plongent-ils toujours en arrière ? Parce que sinon ils tombent dans le bateau.",
        "Que dit une imprimante dans l'eau ? J'ai papier !",
        "Pourquoi les éoliennes sont-elles toujours contentes ? Parce qu'elles sont pleines d'énergie.",
        "Quel est le comble pour un électricien ? De ne pas être au courant."
    ]
    message = await ctx.send(random.choice(blagues))
    await message.add_reaction("😂")

# === Lancer le bot ===
keep_alive()
bot.run
