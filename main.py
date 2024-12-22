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
command_list = ["insulte", "compliment", "citation", "blague", "qi", "commandes", "pileouface", "lancerdé", "ping", "shutdown", "pub", "annonce"]

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
    message = """

𓂃ꕤ 🎀  Sydney 🧸 #ғя  est un Nouveau serveur  🎀

  🎓   Avec une communauté safe
  🏰   Où faire de nouvelles rencontres
  🏆   Gagne des rôles en étant Actif sur le serveur
  🎲   Du Gambling et pleins d'autres jeux
  🎉   Pleins d'évènements qui arrive
  💎   Serveur boosté !
  🤖   Plein de bots pour te divertir ! 

彡   🎗️ Qu'attend tu pour rejoindre !
  🏯   https://discord.gg/sydneyfr 
||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|||||||||​||||​||||​||||||​||||​||||​||||​||||​||||​|||
 https://media.discordapp.net/attachments/1183871422049820758/1312024330812526662/IMG_3324.gif?ex=674afd60&is=6749abe0&hm=a8a69e96c61c2d6cadbb1dc5b63bc269da5d6df6f65adffb4fd772d83e9f4a7e&
"""
    await ctx.send(message)

@bot.command()
async def annonce(ctx, *, message: str):
    # Création de l'embed
    embed = discord.Embed(
        description=message,  # Le message d'annonce
        color=discord.Color.purple()  # Couleur du texte (rose/violet)
    )
    
    # Ajouter un footer avec le nom de l'auteur
    embed.set_footer(text=f"Annonce de {ctx.author.name}", icon_url=ctx.author.avatar.url)
    
    # Envoi du message
    await ctx.send(embed=embed)

@bot.command()
async def insulte(ctx, member: discord.Member = None):
    insultes = [
        "moulin à bite",
        "je te pisse dessus, cordialement.",
        "tu es moche, sacré glope.",
        "tu n'es qu'un mange canette.",
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
    embed.add_field(name="!pub", value="Affiche notre pub. ^^ ", inline=False)
    embed.add_field(name="!annonce", value="Affiche une annonce si vous êtes administrateur.", inline=False)
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

# === Smash or Pass ===
TARGET_CHANNEL_ID = 1312570416665071797
VALID_REACTIONS = ["👍", "👎"]  # Réactions pour validé/pas validé
message_threads = {}

@bot.event
async def on_message(message):
    # Ne pas répondre aux messages du bot
    if message.author.bot:
        return

    # Gérer les tickets
    await handle_tickets(message)

    # Gérer Smash or Pass
    await handle_smash_or_pass(message)

    # Toujours traiter les commandes
    await bot.process_commands(message)


async def handle_tickets(message):
    """Gérer les tickets, comme les demandes de partenariat."""
    # IDs des catégories et salons
    support_category_id = 1312414647386640424
    conditions_channel_id = 1312830314653155479
    pub_channel_id = 1312850532293017631

    # Vérifier si le message est dans un salon de la catégorie support
    if message.channel and message.channel.category_id == support_category_id:
        if "Demande de partenariat" in message.content:
            await send_partnership_response(message.channel, conditions_channel_id, pub_channel_id)


async def handle_smash_or_pass(message):
    """Gérer les messages du canal Smash or Pass."""
    if message.channel.id == TARGET_CHANNEL_ID:
        # Supprimer les messages sans pièce jointe
        if not message.attachments:
            await message.delete()
            return

        # Ajouter les réactions spécifiées
        for reaction in VALID_REACTIONS:
            await message.add_reaction(reaction)

        # Créer un fil de discussion
        thread_name = f"Fil de {message.author.display_name}"
        thread = await message.create_thread(name=thread_name)
        message_threads[message.id] = thread.id

        # Envoyer un message d'introduction dans le thread
        await thread.send(
            f"Bienvenue dans le fil de discussion pour l'image postée par {message.author.mention}.\n"
            f"Merci de respecter la personne et de rester courtois. Tout propos méprisant, dévalorisant, insultant ou méchant est interdit et sera sanctionné !"
        )


async def send_partnership_response(channel, conditions_channel_id, pub_channel_id):
    """Envoie la réponse standard pour une demande de partenariat."""
    conditions_channel = bot.get_channel(conditions_channel_id)
    pub_channel = bot.get_channel(pub_channel_id)

    # Vérifier si les salons sont valides
    if conditions_channel and pub_channel:
        response = (
            f"Bonjour, merci d'avoir ouvert un ticket de partenariat !\n"
            f"Veuillez lire le salon {conditions_channel.mention}. Une fois que vous avez lu et respecté les conditions, "
            f"envoyez votre pub dans ce salon (attention : il faut s'attribuer le rôle partenariat pour pouvoir envoyer des liens). "
            f"Notre pub est disponible dans le salon {pub_channel.mention}.\n"
            f"Copiez-la avec les 3 petits points pour qu’elle s'affiche correctement et ajoutez les captures d'écran comme preuve de la pub dans le ticket.\n"
            f"Un administrateur enverra votre pub dès que possible et vous identifiera dans ce ticket dès que ce sera fait pour le clôturer."
        )
        await channel.send(response)
    else:
        print("Erreur : Les salons mentionnés n'existent pas ou ne sont pas accessibles.")

# Lancement du bot
keep_alive()
bot.run(TOKEN)
