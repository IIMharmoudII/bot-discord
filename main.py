import discord
from discord.ext import commands
from discord.ui import View, Button
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
            await ctx.send(f"Cette commande n'existe pas. Peut-être vouliez-vous dire !{matches[0]} ?")
        else:
            await ctx.send("Cette commande n'existe pas. Tapez !commandes pour voir les commandes disponibles.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions nécessaires pour exécuter cette commande.")
    else:
        await ctx.send("Une erreur inattendue s'est produite.")
        raise error

# === Nouvelles données ===
citations = [
    "La vie, c'est comme une bicyclette, il faut avancer pour ne pas perdre l'équilibre. - Albert Einstein",
    "Le succès, c'est tomber sept fois et se relever huit. - Proverbe japonais",
    "Ne crains pas d’avancer lentement, crains seulement de t’arrêter. - Proverbe chinois",
    "Si tu veux que la vie te sourie, apporte-lui d’abord ta bonne humeur. - Spinoza",
    "L'imagination est plus importante que le savoir. - Albert Einstein",
    "Il n'y a qu'une façon d'échouer, c'est d'abandonner avant d'avoir réussi. - Proverbe américain",
    "L'humour est une chose trop sérieuse pour être laissée aux comiques. - Guy Bedos",
    "Les hommes construisent trop de murs et pas assez de ponts. - Isaac Newton"
]

blagues = [
    "Pourquoi les plongeurs plongent-ils toujours en arrière ? Parce que sinon ils tombent dans le bateau.",
    "Que dit une imprimante dans l'eau ? J'ai papier !",
    "Pourquoi les éoliennes sont-elles toujours contentes ? Parce qu'elles sont pleines d'énergie.",
    "Quel est le comble pour un électricien ? De ne pas être au courant.",
    "Pourquoi les canards sont-ils toujours à l'heure ? Parce qu'ils sont dans l'étang !",
    "C'est l'histoire d'un clown triste. Mais elle fait pas rire.",
    "Pourquoi les Belges emmènent-ils une échelle dans le supermarché ? Pour atteindre les prix bas !",
    "Quelle est la différence entre un banquier et un voleur ? Le voleur, lui, te laisse au moins ton sourire."
]

compliments = [
    "Tu es brillant(e) comme une étoile dans la nuit.",
    "Tu illumines la pièce dès que tu entres.",
    "Tu es un véritable rayon de soleil pour ceux qui t'entourent.",
    "Tu es tellement talentueux(se), c’est impressionnant !",
    "Tu rends tout meilleur juste par ta présence.",
    "Tu as un sourire contagieux, merci de l'apporter au monde !",
    "Tu as une énergie positive incroyable, c’est inspirant !",
    "Tu fais une différence dans la vie des gens autour de toi."
]

insultes = [
    "Tu es aussi utile qu'un tournevis dans un potage.",
    "Même un escargot va plus vite que toi dans la réflexion.",
    "Si la bêtise était une discipline olympique, tu serais médaillé d'or.",
    "Je pense que Google a renoncé à te comprendre.",
    "Ton QI est tellement bas qu'il est en négatif.",
    "Tu es comme un nuage : quand tu pars, c'est une belle journée.",
    "Tu es un vrai mystère... même pour les sciences modernes."
]

# === Commandes du bot ===
@bot.command()
async def pub(ctx):
    message = (
        "𓂃⊤ 🎀  Sydney 🭸 #ɡя  est un Nouveau serveur  🎀\n\n"
        "🎓   Avec une communauté safe\n"
        "🏰   Où faire de nouvelles rencontres\n"
        "🏆   Gagne des rôles en étant Actif sur le serveur\n"
        "🎮   Du Gambling et pleins d'autres jeux\n"
        "🎉   Pleins d'évènements qui arrive\n"
        "✨   Un rôle OG pour le début du serveur !\n\n"
        "ן   🎗️ Qu'attends-tu pour rejoindre !\n\n"
        "🏡   https://discord.gg/sydneyfr"
    )
    await ctx.send(message)

@bot.command()
async def citation(ctx):
    await ctx.send(random.choice(citations))

@bot.command()
async def compliment(ctx, member: discord.Member = None):
    target = member.mention if member else ctx.author.mention
    await ctx.send(f"{target}, {random.choice(compliments)}")

@bot.command()
async def insulte(ctx, member: discord.Member = None):
    target = member.mention if member else ctx.author.mention
    await ctx.send(f"{target}, {random.choice(insultes)}")

@bot.command()
async def blague(ctx):
    message = await ctx.send(random.choice(blagues))
    await message.add_reaction("😂")

class CommandesView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.page = 0
        self.pages = [
            "**Commandes Page 1**:\n!insulte\n!compliment\n!citation\n!blague\n!qi",
            "**Commandes Page 2**:\n!pileouface\n!lancerdé\n!ping\n!pub\n!shutdown"
        ]

    @discord.ui.button(label="◀️", style=discord.ButtonStyle.blurple)
    async def prev_page(self, interaction: discord.Interaction, button: Button):
        self.page = max(self.page - 1, 0)
        await interaction.response.edit_message(content=self.pages[self.page], view=self)

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.blurple)
    async def next_page(self, interaction: discord.Interaction, button: Button):
        self.page = min(self.page + 1, len(self.pages) - 1)
        await interaction.response.edit_message(content=self.pages[self.page], view=self)

@bot.command()
async def commandes(ctx):
    await ctx.send(content="Voici les commandes disponibles :", view=CommandesView())

# === Autres commandes ===
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
