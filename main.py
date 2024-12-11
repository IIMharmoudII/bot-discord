import discord
from discord.ext import commands
import random
import json
from difflib import get_close_matches

# Initialisation du bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Fichier pour sauvegarder les données utilisateur
data_file = "user_data.json"

# Charger et sauvegarder les données utilisateur
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

# Gestion des données utilisateur
def get_user_data(user_id):
    if str(user_id) not in user_data:
        user_data[str(user_id)] = {"aura": 0, "qi": random.randint(80, 140)}
    return user_data[str(user_id)]

def update_user_data(user_id, aura_change=0):
    user = get_user_data(user_id)
    user["aura"] += aura_change
    save_data(user_data)

# Suggestions en cas de commande incorrecte
available_commands = ["qi", "aura", "insulte", "compliment", "classement", "pub", "pfc", "pileouface"]

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        close_match = get_close_matches(ctx.invoked_with, available_commands, n=1, cutoff=0.6)
        if close_match:
            await ctx.send(f"Commande inconnue. Vouliez-vous dire `!{close_match[0]}` ?")
        else:
            await ctx.send("Commande inconnue. Tapez `!help` pour voir les commandes disponibles.")
    else:
        raise error

# Commandes principales
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

# Insultes et Compliments
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

@bot.command()
async def compliment(ctx, member: discord.Member = None):
    if member and member.bot:
        await ctx.send("Tu ne peux pas complimenter un bot.")
        return
    if not member:
        member = random.choice(ctx.guild.members)

    compliment, aura_gain = random.choice(list(compliments.items()))
    update_user_data(member.id, aura_change=aura_gain)
    await ctx.send(f"{member.mention}, {compliment} (Aura gagnée : {aura_gain})")

# Classement et publicité
@bot.command()
async def classement(ctx):
    sorted_users = sorted(user_data.items(), key=lambda x: x[1]["aura"], reverse=True)[:10]
    leaderboard = "**Classement des auras :**\n"
    for i, (user_id, data) in enumerate(sorted_users, start=1):
        try:
            member = await ctx.guild.fetch_member(int(user_id))
            leaderboard += f"{i}. {member.display_name} - {data['aura']} auras\n"
        except discord.NotFound:
            continue
    await ctx.send(leaderboard)

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

# Mini-jeux
@bot.command()
async def pfc(ctx):
    options = ["Pierre", "Feuille", "Ciseaux"]
    bot_choice = random.choice(options)
    await ctx.send(f"Pierre, Feuille ou Ciseaux ? Le bot a choisi : {bot_choice}.")

@bot.command()
async def pileouface(ctx):
    options = ["Pile", "Face"]
    result = random.choice(options)
    await ctx.send(f"La pièce est tombée sur : {result}.")

# Lancer le bot
if __name__ == "__main__":
    bot.run("TOKEN")
