""" Import des librairies & ressources """

# Import de l'API
from quart import Quart, redirect
from bot import bot
from os import system



""" Initialisation du serveur web """

# On init l'app
app = Quart(__name__)



""" Définition des endpoints """

# Racine
@app.route('/')
async def home():
    return 'Coucou la MPSI1'

# Pull
@app.route('/pull', methods=['POST'])
async def pull():
    # On pull et on reboot le bot
    system('git pull && sh start.sh')
    await bot.logout()
    quit()
    return 'OK'

# Liens discord (MPSI1)
@app.route('/discord/mpsi1')
async def discord_mpsi1():
    return redirect('https://discord.gg/TMVjYg9N2f')

# Liens discord (Option info)
@app.route('/discord/info')
async def discord_info():
    return redirect('https://discord.gg/M2UEMmfu8E')
