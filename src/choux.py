# Imports
from os import getenv
from smtplib import SMTP
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Fonction qui envoie un choux
def envoyer_un_choux(target):
    # Connection au serveur
    s = SMTP(host='mail.nathanfallet.me', port=587)
    s.starttls()
    s.login('choux@latablebleuequiestaufonddujardinestentrainderouiller.fr', getenv('CHOUXPASSWORD'))

    # Creer un message
    msg = MIMEMultipart()

    # On setup les paramètres
    msg['From']='choux@latablebleuequiestaufonddujardinestentrainderouiller.fr'
    msg['To']=target
    msg['Subject']='Choux à la crème'

    # Attacher le message
    msg.attach(MIMEText('Un choux à la crème pour toi !\n\n(Ce message a été généré automatiquement, merci de ne pas y répondre)\n\n', 'plain'))

    # Attacher l'image
    with open('images/choux.jpeg', 'rb') as fil:
        attachment = MIMEApplication(fil.read(), Name="choux.jpeg")
        attachment['Content-Disposition'] = 'attachment; filename=choux.jpeg'
        msg.attach(attachment)

    # Envoyer le message
    s.send_message(msg)
    s.close()
    del msg
