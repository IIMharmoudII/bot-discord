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

# ===  Gestion des tickets de partenariat ===
# === Variables globales ===
already_replied = set()  # Garde une trace des tickets où le bot a déjà répondu

# === Variables globales ===
already_replied = set()  # Garde une trace des tickets où le bot a déjà répondu

@bot.event
async def on_message(message):
    # ID de la catégorie de support
    support_category_id = 1312414647386640424
    conditions_channel_id = 1312830314653155479
    pub_channel_id = 1312850532293017631

    # Vérifier si le message est dans un canal de la catégorie support
    if message.channel.category_id == support_category_id:
        # Vérifier si le message contient un embed avec "Demande de partenariat"
        if message.author.bot and message.embeds:
            for embed in message.embeds:
                # Vérifier si "Demande de partenariat" est dans le titre, la description, ou les champs
                if "Demande de partenariat" in (embed.title or "") or \
                   "Demande de partenariat" in (embed.description or ""):
                    # Vérifier si le bot a déjà répondu dans ce ticket
                    if message.channel.id not in already_replied:
                        # Marquer ce ticket comme traité
                        already_replied.add(message.channel.id)

                        # Obtenir les canaux nécessaires
                        conditions_channel = bot.get_channel(conditions_channel_id)
                        pub_channel = bot.get_channel(pub_channel_id)

                        # Récupérer l'auteur du ticket (mentionné par Draft Bot)
                        opener = message.mentions[0] if message.mentions else "utilisateur inconnu"

                        # Construire la réponse
                        response = (
                            f"Bonjour {opener}, merci d'avoir ouvert un ticket de partenariat !\n"
                            f"Veuillez lire le salon {conditions_channel.mention}. Une fois que vous avez lu et respecté les conditions, "
                            f"envoyez votre pub dans ce salon (attention : il faut s'attribuer le rôle partenariat pour pouvoir envoyer des liens). Notre pub est disponible dans le salon {pub_channel.mention}.\n"
                            f"Copiez-la avec les 3 petits points pour qu’elle s'affiche correctement et ajoutez les captures d'écran comme preuve de la pub dans le ticket.\n"
                            f"Un administrateur enverra votre pub dès que possible et vous identifiera dans ce ticket dès que ce sera fait pour le clôturer."
                        )
                        # Envoyer la réponse dans le ticket
                        await message.channel.send(response)
                        break  # Stopper la boucle après avoir traité un embed correspondant

    # Continuer à traiter les commandes
    await bot.process_commands(message)

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
    if message.author.bot:
        return

    if message.channel.id == TARGET_CHANNEL_ID:
        if not message.attachments:
            await message.delete()
            return

        for reaction in VALID_REACTIONS:
            await message.add_reaction(reaction)

        thread_name = f"Fil de {message.author.display_name}"
        thread = await message.create_thread(name=thread_name)
        message_threads[message.id] = thread.id

        await thread.send(
            f"Bienvenue dans le fil de discussion pour l'image postée par {message.author.mention}.\n"
            f"Merci de respecter la personne et de rester courtois. Tout propos méprisant, dévalorisant, insultant ou méchant est interdit et sera sanctionné !"
        )

    await bot.process_commands(message)
# Role IDs (replace with actual IDs from your server)
ROLE_IDS = {
    "Owner": 1312432485472276490,
    "Co-Owner": 1312432486604734494,
    "Perm_V": 1312432490392326305,
    "GS": 1312427749981552690,
    "Modération": 1312427543843835914,
    "GM": 1312426671152042055
}

# Channel IDs
SANCTIONS_CHANNEL = 1312414751304978462

# Warn storage
warns = {}

# Helper function to log sanctions
def log_sanction(guild, user, action, reason, duration=None):
    channel = guild.get_channel(SANCTIONS_CHANNEL)
    if channel:
        embed = discord.Embed(title="Sanction appliquée", color=discord.Color.red())
        embed.add_field(name="Action", value=action, inline=False)
        embed.add_field(name="Utilisateur", value=user.mention, inline=False)
        embed.add_field(name="Raison", value=reason, inline=False)
        if duration:
            embed.add_field(name="Durée", value=str(duration), inline=False)
        embed.timestamp = datetime.utcnow()
        return channel.send(embed=embed)

# Check reason decorator
def requires_reason():
    async def predicate(ctx):
        if len(ctx.message.content.split()) < 3:
            await ctx.send("❌ Vous devez fournir une raison pour cette action.")
            return False
        return True
    return commands.check(predicate)

# Command: tempmute
@bot.command()
@requires_reason()
async def tempmute(ctx, member: discord.Member, duration: int, *, reason):
    role = ctx.author.top_role
    if role.id not in ROLE_IDS.values():
        return await ctx.send("❌ Vous n'avez pas la permission d'utiliser cette commande.")

    # Role-based limits
    max_durations = {
        ROLE_IDS['Modération']: 40,
        ROLE_IDS['GM']: 60,
        ROLE_IDS['GS']: 30,
        ROLE_IDS['Owner']: 10
    }

    max_duration = max_durations.get(role.id, 0)
    if duration > max_duration:
        return await ctx.send(f"❌ Vous ne pouvez pas mute pendant plus de {max_duration} minutes.")

    # Apply mute
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not mute_role:
        mute_role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role, send_messages=False, speak=False)

    await member.add_roles(mute_role, reason=reason)
    await ctx.send(f"✅ {member.mention} a été mute pour {duration} minutes.")

    # Log action
    await log_sanction(ctx.guild, member, "Tempmute", reason, duration)

    # Schedule unmute
    await asyncio.sleep(duration * 60)
    await member.remove_roles(mute_role, reason="Fin du mute")

# Command: warn
@bot.command()
@requires_reason()
async def warn(ctx, member: discord.Member, *, reason):
    if member.id not in warns:
        warns[member.id] = []
    warns[member.id].append(reason)
    await ctx.send(f"✅ {member.mention} a reçu un avertissement.")

    # Log action
    await log_sanction(ctx.guild, member, "Warn", reason)

# Command: view warns
@bot.command()
async def warnlist(ctx, member: discord.Member):
    user_warns = warns.get(member.id, [])
    if not user_warns:
        return await ctx.send(f"ℹ️ {member.mention} n'a aucun avertissement.")

    embed = discord.Embed(title=f"Avertissements pour {member.display_name}", color=discord.Color.orange())
    for i, warn in enumerate(user_warns, 1):
        embed.add_field(name=f"Warn {i}", value=warn, inline=False)
    await ctx.send(embed=embed)

# Command: tempexclude
@bot.command()
@requires_reason()
async def tempexclude(ctx, member: discord.Member, duration: int, *, reason):
    role = ctx.author.top_role
    if role.id != ROLE_IDS['GM']:
        return await ctx.send("❌ Seuls les GM peuvent utiliser cette commande.")
    if duration > 1440:
        return await ctx.send("❌ Vous ne pouvez pas exclure temporairement pendant plus d'un jour.")

    # Restrict user access
    excluded_role = discord.utils.get(ctx.guild.roles, name="Excluded")
    if not excluded_role:
        excluded_role = await ctx.guild.create_role(name="Excluded")
        for channel in ctx.guild.channels:
            await channel.set_permissions(excluded_role, read_messages=False, send_messages=False)

    await member.add_roles(excluded_role, reason=reason)
    await ctx.send(f"✅ {member.mention} a été exclu temporairement pour {duration} minutes.")

    # Log action
    await log_sanction(ctx.guild, member, "Tempexclude", reason, duration)

    # Schedule role removal
    await asyncio.sleep(duration * 60)
    await member.remove_roles(excluded_role, reason="Fin de l'exclusion temporaire")

# Command: derank
@bot.command()
async def derank(ctx, member: discord.Member):
    role = ctx.author.top_role
    target_role = member.top_role

    if role.id not in ROLE_IDS.values() or role <= target_role:
        return await ctx.send("❌ Vous ne pouvez pas rétrograder cet utilisateur.")

    await member.remove_roles(target_role, reason="Rétrogradation effectuée")
    await ctx.send(f"✅ {member.mention} a été rétrogradé de {target_role.name}.")

# Lancement du bot
keep_alive()
bot.run(TOKEN)
