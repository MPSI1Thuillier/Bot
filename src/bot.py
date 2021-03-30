""" Import des librairies & ressources """

# Import des APIs system
from os import system
from io import BytesIO

# Importation de l'API Discord
from discord.ext import commands
from discord import Embed, Game, File, VoiceChannel

# On importe nos ressources
from helper import isAlmostEqual
from quotes import random_quote, quiz_quote, quotes_count
from item_chest import generateItem
from clear import clearChannel, emptyChannel
from morpion import MorpionGame, MorpionHuman, MorpionComputer
from img import generate_image
from choux import envoyer_un_choux
from music import YTDLSource

# Import du random
from random import randint


""" Initialisation du bot """

# On init le bot
bot = commands.Bot(command_prefix='.')
bot.remove_command('help')

# Quand le bot est pret
@bot.listen()
async def on_ready():
    # On log la connexion
    print('Logged on as {0}!'.format(bot.user))

    # On update le status
    await bot.change_presence(activity=Game('https://github.com/MPSI1Thuillier/Bot'))


""" Définition des commandes """

#
# Commandes de controles
#

# Commande de ping


@bot.command()
async def ping(ctx):
    # On répond pong
    await ctx.send('Pong')
    await ctx.message.delete()

# Commande de reboot


@bot.command()
@commands.is_owner()
async def reboot(ctx):
    # On reboot le bot
    system('sh start.sh')
    await ctx.bot.logout()
    await ctx.message.delete()
    quit()

# Commande de stop


@bot.command()
@commands.is_owner()
async def stop(ctx):
    # On stop le bot
    await ctx.bot.logout()
    await ctx.message.delete()
    quit()


#
# Commandes de gestion des channels
#

# Commande help
@bot.command()
async def help(ctx):
    # Affiche ce message d'aide
    await ctx.send("""
__**Citation**__
.citation \t\t Donne une citation au hasard.
.citation [*Auteur*] \t\t Donne une citation de votre auteur preferé.
.wallpaper \t\t Affiche une citation sur un joli fond.
.questionprepa \t\t Arriverez vous à trouver la suite de cette citation ?
.count \t\t Affiche le nombre de citations.
                    
__**Jeux**__
.ping \t\t Pong !
.morpion \t\t Faites un morpion avec un ami.
.morpionbot \t\t Faites un morpion contre moi.
.pileface \t\t Pile ou face ! Que pariez vous ?
.item \t\t Affiche un item de RPG.
                    
__**Audio**__
.audio \t\t Je me joins à votre channel.
.finaudio \t\t Je me deconnecte de votre channel.
.music [*URL* ou *description*] \t\t Je joue votre musique preferée. :musical_note:
.volume [de *0* à *100*] \t\t Regle mon volume.
                    
__**Autres**__
.clear \t\t Je supprime le message que je viens d'envoyer.
.empty \t\t Je supprime :100: message d'un channel. 
.choux [*Votre Email*] \t\t Recevez un beau choux à la crème par mail. :mailbox_with_mail:
.contribution \t\t Pour ceux qui veulent contribuer au bot. ;)
.reboot \t\t Cette commande me reboot. (Oui bon ca arrive a tout le monde de bugger :unamused: )
.stop \t\t Cette commande me stop! (S'il vous plait n'appuyer pas :pray: :pray: !)
.help \t\t Affiche ce message.
.token \t\t Mon token !
""")

# Commande de clear
@bot.command()
@commands.is_owner()
async def clear(ctx):
    # On supprime tous les messages de commande et du bot du channel
    await clearChannel(ctx)
    await ctx.message.delete()

# Commande de empty


@bot.command()
async def empty(ctx):
    # On supprime tous les messages
    await emptyChannel(ctx)
    await ctx.message.delete()


#
# Commandes d'info
#

# Guide de la contribution
@bot.command()
async def contribution(ctx):
    # On explique comment fonctionne la contribution
    await ctx.send("Pour contribuer au fonctionnement du bot et l'améliorer, rendez vous sur https://github.com/MPSI1Thuillier/Bot")
    await ctx.message.delete()


#
# Commandes de citation
#

# Commande de citation
@bot.command()
async def citation(ctx, arg=None):
    # On choisi une citation
    quote = random_quote(arg)

    # On créé un embed
    embed = Embed(title=quote.text)
    embed.set_footer(text=quote.author)

    # On envoit
    await ctx.send(embed=embed)
    await ctx.message.delete()

# Commande pour compter les citations


@bot.command()
async def count(ctx):
    # On compte les citations
    n = quotes_count()

    # On créé les paramètres de l'équation
    a = randint(1, 20)
    n2 = randint(-10, -1)

    # On créé un embed
    embed = Embed(
        title="J'ai n citations, tel que :",
        description="```" + str(a) + "n² - " + str(a*(n + n2)) +
        "n - " + str(-a*n*n2) + " = 0``````n > 0```"
    )

    # On envoit
    await ctx.send(embed=embed)
    await ctx.message.delete()

# Commande de wallpaper

@bot.command()
async def wallpaper(ctx):
    # On génère une image
    async with ctx.typing():
        generate_image()

    # On l'envoie
    await ctx.message.delete()
    await ctx.send(file=File("wallpaper.jpg"))

#
# Commandes funs
#

# Commande d'item
@bot.command()
async def item(ctx):
    # On gènere un item et l'envoi
    text = generateItem()
    embed = Embed(title=text[0])
    embed.set_footer(text=text[1])

    await ctx.send(embed=embed)
    await ctx.message.delete()

# Commande de pile ou face


@bot.command()
async def pileface(ctx):
    # On décide et envoie le résultat
    await ctx.send("Le résulat est : {}".format(["Pile", "Face"][randint(0, 1)]))
    await ctx.message.delete()

# Commande de token


@bot.command()
async def token(ctx):
    # On envoi le token
    await ctx.send("Le token est : Tm9uLCBsZSB0b2tlbiBuJ2VzdCBwYXMgYWNjZXNzaWJsZSBjb21tZSDDp2E")
    await ctx.message.delete()

# Commande de choux à la crème

@bot.command()
async def choux(ctx, target):
    # On envoie un choux
    async with ctx.typing():
        envoyer_un_choux(target)

    await ctx.send("Fais un tour dans ta boite mail ! (ça peut prendre quelques minutes)")
    await ctx.message.delete()


#
# Commande de morpion et listen des reactions
#

morpion_games = []

# Commande de morpion


@bot.command()
async def morpion(ctx):
    # On démarre une partie de morpion
    game = MorpionGame(3, MorpionHuman("O", "Joueur 1"), MorpionHuman("X", "Joueur 2"), ctx)
    morpion_games.append(game)
    await ctx.message.delete()
    await game.nextMove()

# Commande de morpion


@bot.command()
async def morpionbot(ctx):
    # On démarre une partie de morpion
    game = MorpionGame(3, MorpionHuman("O", "Joueur 1"), MorpionComputer("X", "Ordinateur"), ctx)
    morpion_games.append(game)
    await ctx.message.delete()
    await game.nextMove()


@bot.listen()
async def on_reaction_add(reaction, user):
    # On check que c'est pas le bot
    if user.bot:
        return

    # On récupère la game liée au message et on joue
    for game in morpion_games:
        if game.message != None and reaction.message.id == game.message.id:
            # On joue avec la réaction
            await game.playFromReaction(reaction.emoji, user)

            # On clear la game si c'est fini
            if game.current == "*":
                morpion_games.remove(game)
                return

#
# Question pour un préparationiste
# Le but : compléter la citation donnée par le bot
#

quiz_games = []

# Commande pour lancer le jeu

@bot.command()
async def questionprepa(ctx):
    # On récupère une citation qui contient une virgule (qui se complète)
    quote = quiz_quote()

    # On coupe à la virgule
    parts = quote.text.split(", ")

    # On créé un embed
    embed = Embed(
        title="Trouver la fin de la citation :",
        description=parts[0] + ", ..."
    )
    embed.set_footer(text=quote.author)

    # On envoit
    await ctx.send(embed=embed)
    await ctx.message.delete()

    # On save la question
    question = (ctx.author.id, quote)
    quiz_games.append(question)

@bot.listen()
async def on_message(message):
    # On regarde si ya une question associée avec l'auteur
    for question in quiz_games:
        if question[0] == message.author.id:
            # On est sur la réponse à notre question
            isCorrect = isAlmostEqual(message.content, question[1].text.split(", ")[1])

            # On créé le message de réponse
            embed = Embed(
                title="Bonne réponse !!! 👍" if isCorrect else "Mauvaise réponse !!! 👎",
                description=question[1].text
            )
            embed.set_footer(text=question[1].author)
            await message.channel.send(embed=embed)
            
            # On le retire de la liste
            quiz_games.remove(question)

            # On s'arrete
            break

#
# Commandes pour la musique
#

@bot.command()
async def audio(ctx):
    channel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)
    await channel.connect()

@bot.command()
async def music(ctx, url):
    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: print('Erreur de lecture : %s' % e) if e else None)
    await ctx.send('En cours de lecture : {}'.format(player.title))

@bot.command()
async def volume(ctx, volume: int):
    if ctx.voice_client is None:
        return await ctx.send("Je ne suis pas connecté à un canal audio !")
    ctx.voice_client.source.volume = volume / 100
    await ctx.send("Volume réglé à {}%".format(volume))

@bot.command()
async def finaudio(ctx):
    await ctx.voice_client.disconnect()

@music.before_invoke
async def ensure_voice(ctx):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("Vous n'êtes pas connecté à un canal audio !")
            raise commands.CommandError("Author not connected to a voice channel.")
    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()
