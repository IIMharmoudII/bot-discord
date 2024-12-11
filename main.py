import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import random
import os
from dotenv import load_dotenv
from flask import Flask
from threading import Thread
import asyncio

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
command_list = [
    "insulte", "compliment", "citation", "blague", "qi", "commandes",
    "pileouface", "lancerdé", "ping", "pub", "aura", "classement", "addaura", "pfc"
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

# === Gestion des erreurs globales ===
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il manque un argument requis pour cette commande.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("L'argument fourni n'est pas valide.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Cette commande n'existe pas. Tapez `!commandes` pour voir les commandes disponibles.")
    elif isinstance(error, commands.CommandOnCooldown):
        minutes = int(error.retry_after // 60)
        seconds = int(error.retry_after % 60)
        await ctx.send(f"Cette commande est en cooldown. Réessayez dans {minutes} minutes et {seconds} secondes.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions nécessaires pour exécuter cette commande.")
    else:
        await ctx.send("Une erreur inattendue s'est produite.")
        raise error

# === Commandes du bot ===
@bot.command()
async def commandes(ctx):
    embed = discord.Embed(title="Liste des commandes disponibles", color=discord.Color.blue())
    embed.description = "\n".join([f"`!{cmd}`" for cmd in command_list if cmd != "shutdown"])
    await ctx.send(embed=embed)

@bot.command()
@cooldown(1, 1800, BucketType.user)
async def insulte(ctx, member: discord.Member = None):
    if member is None or member == ctx.author:
        member = random.choice([m for m in ctx.guild.members if m != ctx.author and not m.bot])

    insultes = [
        "moulin à bite", "je te pisse dessus, cordialement.",
        "tu es moche, sacré glope.", "tu n'es qu'un manche canette.",
        "t'es qu'un bouffeur de niglo", "Ton QI est tellement bas qu'il est en négatif."
    ]

    user_aura[member.id] = user_aura.get(member.id, 1000) - 10
    await ctx.send(f"{member.mention}, {random.choice(insultes)} (Aura restante : {user_aura[member.id]})")

@bot.command()
@cooldown(1, 1800, BucketType.user)
async def compliment(ctx, member: discord.Member = None):
    if member is None or member == ctx.author:
        member = random.choice([m for m in ctx.guild.members if m != ctx.author and not m.bot])

    compliments = [
        "Tu es brillant(e) comme une étoile dans la nuit.",
        "Tu illumines la pièce dès que tu entres.",
        "Tu es un véritable rayon de soleil pour ceux qui t'entourent.",
        "Tu es tellement talentueux(se), c’est impressionnant !"
    ]

    user_aura[member.id] = user_aura.get(member.id, 1000) + 10
    await ctx.send(f"{member.mention}, {random.choice(compliments)} (Aura actuelle : {user_aura[member.id]})")

@bot.command()
async def aura(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    aura = user_aura.get(member.id, 1000)
    await ctx.send(f"{member.mention}, votre aura est de {aura} points.")

@bot.command()
async def classement(ctx):
    for member in ctx.guild.members:
        if member.id not in user_aura:
            user_aura[member.id] = 1000

    classement = sorted(user_aura.items(), key=lambda x: x[1], reverse=True)
    embed = discord.Embed(title="Classement des Auras", color=discord.Color.gold())
    for i, (user_id, aura) in enumerate(classement[:10], start=1):
        user = await bot.fetch_user(user_id)
        embed.add_field(name=f"{i}. {user.name}", value=f"{aura} points", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def pfc(ctx):
    players = {}

    embed = discord.Embed(
        title="Pierre-Feuille-Ciseaux",
        description="Cliquez sur un bouton pour faire votre choix !",
        color=discord.Color.green()
    )

    class PFCView(discord.ui.View):
        def __init__(self, timeout=15):
            super().__init__(timeout=timeout)

        async def on_timeout(self):
            if len(players) < 2:
                await ctx.send("Le jeu a été annulé faute de participants.")

        @discord.ui.button(label="Pierre", style=discord.ButtonStyle.primary)
        async def pierre(self, interaction: discord.Interaction, button: discord.ui.Button):
            players[interaction.user.id] = "Pierre"
            await self.process_game(interaction)

        @discord.ui.button(label="Feuille", style=discord.ButtonStyle.success)
        async def feuille(self, interaction: discord.Interaction, button: discord.ui.Button):
            players[interaction.user.id] = "Feuille"
            await self.process_game(interaction)

        @discord.ui.button(label="Ciseaux", style=discord.ButtonStyle.danger)
        async def ciseaux(self, interaction: discord.Interaction, button: discord.ui.Button):
            players[interaction.user.id] = "Ciseaux"
            await self.process_game(interaction)

        async def process_game(self, interaction):
            if len(players) == 2:
                player_ids = list(players.keys())
                player_choices = list(players.values())
                results = {"Pierre": "Ciseaux", "Ciseaux": "Feuille", "Feuille": "Pierre"}

                player1, player2 = player_ids
                choice1, choice2 = player_choices

                if choice1 == choice2:
                    result_message = "Égalité !"
                elif results[choice1] == choice2:
                    winner, loser = player1, player2
                    result_message = f"{(await bot.fetch_user(winner)).mention} a gagné contre {(await bot.fetch_user(loser)).mention} !"
                    user_aura[winner] = user_aura.get(winner, 1000) + 20
                    user_aura[loser] = user_aura.get(loser, 1000) - 20
                else:
                    winner, loser = player2, player1
                    result_message = f"{(await bot.fetch_user(winner)).mention} a gagné contre {(await bot.fetch_user(loser)).mention} !"
                    user_aura[winner] = user_aura.get(winner, 1000) + 20
                    user_aura[loser] = user_aura.get(loser, 1000) - 20

                result_message += f"\n\nChoix : \n- {(await bot.fetch_user(player1)).mention} : {choice1}\n- {(await bot.fetch_user(player2)).mention} : {choice2}"
                await interaction.message.edit(content=result_message, view=None)

    view = PFCView()
    await ctx.send(embed=embed, view=view)

@bot.command()
async def addaura(ctx, member: discord.Member, points: int):
    if ctx.author.id != 911189303625924631:
        await ctx.send("Vous n'avez pas la permission d'ajouter de l'aura.")
        return

    user_aura[member.id] = user_aura.get(member.id, 1000) + points
    await ctx.send(f"{member.mention} a maintenant {user_aura[member.id]} points d'aura.")

@bot.command()
async def qi(ctx):
    qi = random.randint(50, 150)
    user_qi[ctx.author.id] = qi
    await ctx.send(f"{ctx.author.mention}, votre QI est évalué à {qi}.")

@bot.command()
async def citation(ctx):
    citations = [
        "La vie est un mystère qu'il faut vivre, et non un problème à résoudre. - Gandhi",
        "Le seul vrai voyage, ce n’est pas d’aller vers d’autres paysages, mais d’avoir d’autres yeux. - Proust",
        "Celui qui déplace une montagne commence par déplacer de petites pierres. - Confucius",
        "Le bonheur n'est pas quelque chose de prêt à l'emploi. Il vient de vos propres actions. - Dalaï Lama"
    ]
    await ctx.send(random.choice(citations))

@bot.command()
async def blague(ctx):
    blagues = [
        "Pourquoi les éléphants ne bronzent-ils pas ? Parce qu’ils ont peur des coups de soleil !",
        "Que dit un électricien quand il est content ? Je suis au courant !",
        "Pourquoi est-ce que les plongeurs plongent toujours en arrière et jamais en avant ? Parce que sinon ils tombent dans le bateau !",
        "Qu’est-ce qui est jaune et qui attend ? Jonathan !"
    ]
    await ctx.send(random.choice(blagues))

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong ! 🏓 Latence : {latency}ms")

# Lancement du bot
keep_alive()
bot.run(TOKEN)
