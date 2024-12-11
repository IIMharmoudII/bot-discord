import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import random
import os
from dotenv import load_dotenv
from flask import Flask
from threading import Thread
from difflib import get_close_matches
import time

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
    "pileouface", "lancerdé", "ping", "shutdown", "pub", "aura", "classement", "add", "pfc"
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
        command = ctx.invoked_with
        matches = get_close_matches(command, command_list, n=1, cutoff=0.6)
        if matches:
            view = discord.ui.View()
            button = discord.ui.Button(label=f"Utiliser !{matches[0]}", style=discord.ButtonStyle.primary)
            button.callback = lambda interaction: ctx.invoke(bot.get_command(matches[0]))
            view.add_item(button)
            await ctx.send("Cette commande n'existe pas.", view=view)
        else:
            await ctx.send("Cette commande n'existe pas. Tapez `!commandes` pour voir les commandes disponibles.")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Cette commande est en cooldown. Réessayez dans {error.retry_after:.0f} secondes.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions nécessaires pour exécuter cette commande.")
    else:
        await ctx.send("Une erreur inattendue s'est produite.")
        raise error

# === Commandes du bot ===
@bot.command()
async def pub(ctx):
    message = (
        "\U00010243\U0001fab4 \ud83c\udf80  Sydney \ud83e\uddf8 #\u044f  est un Nouveau serveur  \ud83c\udf80\n\n"
        "\ud83c\udf93   Avec une communauté safe\n"
        "\ud83c\udff0   Où faire de nouvelles rencontres\n"
        "\ud83c\udfc6   Gagne des rôles en étant Actif sur le serveur\n"
        "\ud83c\udfb2   Du Gambling et pleins d'autres jeux\n"
        "\ud83c\udf89   Pleins d'évènements qui arrive\n"
        "\u2728   Un rôle OG pour le début du serveur !\n\n"
        "彡   \ud83c\udf97\ufe0f Qu'attends-tu pour rejoindre !\n\n"
        "\ud83c\udfe2   https://discord.gg/sydneyfr"
    )
    await ctx.send(message)

@bot.command()
@cooldown(1, 1800, BucketType.user)  # Cooldown de 30 minutes par utilisateur
async def insulte(ctx, member: discord.Member = None):
    if member is None or member == ctx.author:
        await ctx.send("Tu ne peux pas t'insulter toi-même.")
        return

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
        await ctx.send("Tu ne peux pas te complimenter toi-même.")
        return

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
    if not user_aura:
        await ctx.send("Personne n'a encore modifié son aura.")
        return
    classement = sorted(user_aura.items(), key=lambda x: x[1], reverse=True)
    embed = discord.Embed(title="Classement des Auras", color=discord.Color.gold())
    for i, (user_id, aura) in enumerate(classement, start=1):
        user = await bot.fetch_user(user_id)
        embed.add_field(name=f"{i}. {user.name}", value=f"{aura} points", inline=False)
    await ctx.send(embed=embed)

@bot.command()
@commands.is_owner()
async def add(ctx, member: discord.Member, points: int):
    user_aura[member.id] = user_aura.get(member.id, 1000) + points
    await ctx.send(f"{member.mention} a maintenant {user_aura[member.id]} points d'aura.")

@bot.command()
async def pfc(ctx):
    embed = discord.Embed(
        title="Pierre-Feuille-Ciseaux",
        description="Cliquez pour rejoindre le jeu !",
        color=discord.Color.green()
    )
    view = discord.ui.View()

    async def join_game(interaction):
        if interaction.user == ctx.author:
            await interaction.response.send_message("Vous ne pouvez pas jouer contre vous-même !", ephemeral=True)
            return

        options = ["Pierre", "Feuille", "Ciseaux"]
        player_choice = random.choice(options)
        bot_choice = random.choice(options)
        result = ""

        if player_choice == bot_choice:
            result = "Égalité !"
        elif (player_choice == "Pierre" and bot_choice == "Ciseaux") or \
             (player_choice == "Feuille" and bot_choice == "Pierre") or \
             (player_choice == "Ciseaux" and bot_choice == "Feuille"):
            result = f"Bravo {interaction.user.mention}, vous avez gagné !"
            user_aura[interaction.user.id] += 20
            user_aura[ctx.author.id] -= 20
        else:
            result = f"Dommage {interaction.user.mention}, vous avez perdu."
            user_aura[interaction.user.id] -= 20
            user_aura[ctx.author.id] += 20

        await interaction.response.edit_message(
            content=f"{ctx.author.mention} a choisi {player_choice}.\n" \
                    f"{interaction.user.mention} a choisi {bot_choice}.\n" \
                    f"{result}",
            view=None
        )

    button = discord.ui.Button(label="Rejoindre", style=discord.ButtonStyle.blurple)
    button.callback = join_game
    view.add_item(button)

    await ctx.send(embed=embed, view=view)

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
    await ctx.send(f"Pong ! \ud83c\udfd3 Latence : {latency}ms")

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Arrêt du bot... \ud83d\uded1")
    await bot.close()

# Lancement du bot
keep_alive()
bot.run(TOKEN)
