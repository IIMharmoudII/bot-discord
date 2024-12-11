import discord
from discord.ext import commands
import random
import json

# Initialisation du bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Fichier pour sauvegarder les données
data_file = "user_data.json"

# Chargement et sauvegarde des données
def load_data():
    try:
        with open(data_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(data_file, "w") as file:
        json.dump(data, file)

user_data = load_data()

# Gestion des utilisateurs
def get_user_data(user_id):
    if str(user_id) not in user_data:
        user_data[str(user_id)] = {"aura": 0, "qi": random.randint(80, 140)}
    return user_data[str(user_id)]

def update_user_data(user_id, aura_change=0):
    user = get_user_data(user_id)
    user["aura"] += aura_change
    save_data(user_data)

# Commandes de base
@bot.command()
async def qi(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author
    user = get_user_data(member.id)
    await ctx.send(f"Le QI de {member.mention} est de {user['qi']}.")

@bot.command()
async def aura(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author
    user = get_user_data(member.id)
    await ctx.send(f"{member.mention} a {user['aura']} d'aura.")
# Listes d'insultes et de compliments
insultes = {
    "glope saucisse": -500,
    "sac à foutre": -1000,
    "rammasi de fond d'capote": -1500,
    "t'es un gluant": -200,
    "t qu'un bouffeur de niglo": -800,
    "bouffe mes couilles et étouffe-toi avec": -2000
}

compliments = {
    "Tu es génial(e)!": 500,
    "Ton sourire illumine la pièce.": 1000,
    "Tu es une inspiration pour tout le monde.": 1500,
    "Bravo pour ton travail exceptionnel!": 2000
}

# Commande !insulte
@bot.command()
async def insulte(ctx, member: discord.Member = None):
    if member and member.bot:
        await ctx.send("Tu ne peux pas insulter un bot.")
        return
    if member == ctx.author:
        await ctx.send("Tu ne peux pas t'insulter toi-même.")
        return
    if not member:
        member = random.choice(ctx.guild.members)

    insult, aura_loss = random.choice(list(insultes.items()))
    update_user_data(member.id, aura_change=aura_loss)
    await ctx.send(f"{member.mention}, {insult}! (Aura perdue : {abs(aura_loss)})")

# Commande !compliment
@bot.command()
async def compliment(ctx, member: discord.Member = None):
    if member and member.bot:
        await ctx.send("Tu ne
@bot.command()
async def pub(ctx):
    pub_message = """𓂃ꕤ 🎀  Sydney 🧸 #ғя  est un Nouveau serveur 🎀
    
🎓 Avec une communauté safe
🏰 Où faire de nouvelles rencontres
🏆 Gagne des rôles en étant Actif sur le serveur
🎲 Du Gambling et pleins d'autres jeux
🎉 Pleins d'évènements qui arrivent
✨ Un rôle OG pour le début du serveur !

🏯 https://discord.gg/sydneyfr"""
    await ctx.send(pub_message)

@bot.command()
async def commandes(ctx):
    commands_list = """
**Commandes disponibles :**
- `!qi`: Affiche votre QI ou celui d'une autre personne.
- `!aura`: Affiche votre aura ou celle d'une autre personne.
- `!insulte`: Insulte une personne.
- `!compliment`: Complimente une personne.
- `!pub`: Affiche la pub du serveur.
- `!classement`: Affiche le classement des utilisateurs.
"""
    await ctx.send(commands_list)

@bot.command()
async def classement(ctx):
    sorted_users = sorted(user_data.items(), key=lambda x: x[1]["aura"], reverse=True)[:10]
    leaderboard = "**Classement des auras :**\n"
    for i, (user_id, data) in enumerate(sorted_users, start=1):
        member = await ctx.guild.fetch_member(int(user_id))
        leaderboard += f"{i}. {member.display_name} - {data['aura']} auras\n"
    await ctx.send(leaderboard)
@bot.command()
async def pfc(ctx):
    await ctx.send("Qui veut jouer à Pierre Feuille Ciseaux avec moi ? Cliquez sur le bouton pour commencer.")

# Commande Pile ou Face
@bot.command()
async def pileouface(ctx):
    options = ["Pile", "Face"]
    result = random.choice(options)
    await ctx.send(f"La pièce est tombée sur : {result}.")
