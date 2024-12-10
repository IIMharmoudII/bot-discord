import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
from flask import Flask
from threading import Thread
from difflib import get_close_matches

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
command_list = ["insulte", "compliment", "citation", "blague", "qi", "commandes", "pileouface", "lancerdé", "ping", "shutdown", "pub"]

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

# === Gestion des erreurs globales ===
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il manque un argument requis pour cette commande.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("L'argument fourni n'est pas valide.")
    elif isinstance(error, commands.CommandNotFound):
        # Suggérer une commande similaire
        command = ctx.invoked_with
        matches = get_close_matches(command, command_list, n=1, cutoff=0.6)
        if matches:
            await ctx.send(f"Cette commande n'existe pas. Peut-être vouliez-vous dire `!{matches[0]}` ?")
        else:
            await ctx.send("Cette commande n'existe pas. Tapez `!commandes` pour voir les commandes disponibles.")
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
        " Tu es un vrai mystère... même pour les sciences modernes."
        
        
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

@bot.command()
async def qi(ctx, member: discord.Member = None):
    user_id = member.id if member else ctx.author.id
    if user_id not in user_qi:
        user_qi[user_id] = random.randint(50, 150)
    await ctx.send(f"Le QI de {member.mention if member else ctx.author.mention} est de {user_qi[user_id]}.")

@bot.command()
async def commandes(ctx):
    embed = discord.Embed(
        title="Liste des commandes disponibles",
        description="Voici les commandes que vous pouvez utiliser avec ce bot :",
        color=discord.Color.blue()
    )
    embed.add_field(name="!insulte", value="Insulte un utilisateur.", inline=False)
    embed.add_field(name="!compliment", value="Complimente un utilisateur.", inline=False)
    embed.add_field(name="!citation", value="Affiche une citation aléatoire.", inline=False)
    embed.add_field(name="!blague", value="Raconte une blague aléatoire.", inline=False)
    embed.add_field(name="!qi", value="Affiche le QI d'un utilisateur.", inline=False)
    embed.add_field(name="!pileouface", value="Lance une pièce.", inline=False)
    embed.add_field(name="!lancerdé", value="Lance un dé.", inline=False)
    embed.add_field(name="!ping", value="Affiche la latence du bot.", inline=False)
    embed.add_field(name="!pub", value="Affiche un message promotionnel.", inline=False)
    embed.set_footer(text="Tapez une commande pour l'utiliser.")
    await ctx.send(embed=embed)

@bot.command()
async def pileouface(ctx):
    await ctx.send(f"C'est... {random.choice(['Pile', 'Face'])} !")

@bot.command()
async def lancerdé(ctx):
    await ctx.send(f"Tu as lancé le dé... et c'est un **{random.randint(1, 6)}**!")

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong ! 🏓 Latence : {latency}ms")

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Arrêt du bot... 🛑")
    await bot.close()

# Lancement du bot
keep_alive()
bot.run(TOKEN)
