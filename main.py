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

# Sauvegarder les données lorsque le bot est arrêté
@bot.event
async def on_close():
    save_data()

# === Gestion des erreurs globales ===
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il manque un argument requis pour cette commande.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("L'argument fourni n'est pas valide.")
    elif isinstance(error, commands.CommandNotFound):
        closest_command = next((cmd for cmd in command_list if cmd.startswith(ctx.invoked_with[:2])), None)
        if closest_command:
            await ctx.send(f"Cette commande n'existe pas. Vouliez-vous dire `!{closest_command}` ?")
        else:
            await ctx.send("Cette commande n'existe pas. Tapez `!commandes` pour voir les commandes disponibles.")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Cette commande est en cooldown. Réessayez dans {int(error.retry_after)} secondes.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions nécessaires pour exécuter cette commande.")
    else:
        await ctx.send("Une erreur inattendue s'est produite.")
        raise error

# === Commandes du bot ===
@bot.command()
async def commandes(ctx):
    embed = discord.Embed(title="Liste des commandes disponibles", color=discord.Color.blue())
    embed.description = "\n".join([f"`!{cmd}`" for cmd in command_list])
    await ctx.send(embed=embed)

@bot.command()
@cooldown(1, 30, BucketType.user)
async def insulte(ctx, member: discord.Member = None):
    if member is None or member == ctx.author:
        member = random.choice([m for m in ctx.guild.members if m != ctx.author and not m.bot])

    insultes = [
        "moulin à bite", "je te pisse dessus, cordialement.",
        "tu es moche, sacré glope.", "tu n'es qu'un manche canette.",
        "t'es qu'un bouffeur de niglo", "Ton QI est tellement bas qu'il est en négatif."
    ]

    user_aura[member.id] = user_aura.get(member.id, 1000) - 10
    save_data()
    await ctx.send(f"{member.mention}, {random.choice(insultes)} (Aura restante : {user_aura[member.id]})")

@bot.command()
@cooldown(1, 30, BucketType.user)
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
    save_data()
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
        if not member.bot and member.id not in user_aura:
            user_aura[member.id] = 1000

    classement = sorted(user_aura.items(), key=lambda x: x[1], reverse=True)
    embed = discord.Embed(title="Classement des Auras", color=discord.Color.gold())
    for i, (user_id, aura) in enumerate(classement[:10], start=1):
        user = await bot.fetch_user(user_id)
        embed.add_field(name=f"{i}. {user.name}", value=f"{aura} points", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def pub(ctx):
    pubs = [
        "Rejoignez notre serveur pour des événements exclusifs !",
        "Invitez vos amis pour doubler vos récompenses d'aura !",
        "Visitez notre site web pour plus d'informations."
    ]
    await ctx.send(random.choice(pubs))

@bot.command()
async def qi(ctx):
    if ctx.author.id in user_qi:
        await ctx.send("Votre QI a déjà été mesuré et ne peut pas être modifié.")
    else:
        qi = random.randint(50, 150)
        user_qi[ctx.author.id] = qi
        save_data()
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
        ("Pourquoi les éléphants ne bronzent-ils pas ? Parce qu’ils ont peur des coups de soleil !", 10),
        ("Que dit un électricien quand il est content ? Je suis au courant !", 20),
        ("Pourquoi est-ce que les plongeurs plongent toujours en arrière et jamais en avant ? Parce que sinon ils tombent dans le bateau !", -10),
        ("Qu’est-ce qui est jaune et qui attend ? Jonathan !", -20)
    ]
    blague, aura_change = random.choice(blagues)
    user_aura[ctx.author.id] = user_aura.get(ctx.author.id, 1000) + aura_change
    save_data()
    aura_msg = f"(Aura {'gagnée' if aura_change > 0 else 'perdue'} : {abs(aura_change)} points)"
    await ctx.send(f"{ctx.author.mention}, {blague} {aura_msg}")

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong ! 🏓 Latence : {latency}ms")

@bot.command()
async def addaura(ctx, member: discord.Member, points: int):
    if ctx.author.id != 911189303625924631:
        await ctx.send("Vous n'avez pas la permission d'ajouter de l'aura.")
        return

    user_aura[member.id] = user_aura.get(member.id, 1000) + points
    save_data()
    await ctx.send(f"{member.mention} a maintenant {user_aura[member.id]} points d'aura.")

@bot.command()
async def supaura(ctx, member: discord.Member, points: int):
    if ctx.author.id != 911189303625924631:
        await ctx.send("Vous n'avez pas la permission de supprimer de l'aura.")
        return

    user_aura[member.id] = user_aura.get(member.id, 1000) - points
    save_data()
    await ctx.send(f"{member.mention} a maintenant {user_aura[member.id]} points d'aura.")

@bot.command()
async def lancerdé(ctx):
    result = random.randint(1, 6)
    await ctx.send(f"{ctx.author.mention}, vous avez lancé un dé et obtenu : {result}.")
    
