import smtplib
import imapclient
import email
import settings
import os.path as op
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders


# TASK1
# Send Hello world to a list of recipients

def create_mail(name):
    # Creating base mail
    msg = MIMEMultipart()
    # Adding default values for Date, Subject, and Text
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = 'Hello World!'
    msg.attach(MIMEText('Hello ' + name + '!'))
    # Adding attachment
    # Uploads from a list of attachments, fixed with example for now
    files = ['sample1.pdf', 'sample2.pdf']

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="{}"'.format(op.basename(path)))
        msg.attach(part)
    # retuns full e-mail to send
    return msg

# List of tuples with recipients to send Hello World to. Containing addresses and Names. Hard coded for now
hw_recipients = [('pyscript2018@gmail.com', 'Mr. Python'), ('petar.popovic.bg@gmail.com', 'Mr. Petar'), ('darrenreid@gmail.com', 'Mr. Darren')]

# Smtp connection, parameters from settings file.
smtp = smtplib.SMTP(settings.smtpserver, settings.smtpport)
# Starting tls encryption
smtp.starttls()
# Log in to the account
smtp.login(settings.username, settings.password)

# Send e-mails
for hw_recipient in hw_recipients:
    smtp.sendmail(settings.username, hw_recipient[0], create_mail(hw_recipient[1]).as_string())
    print('Hello World sent to: ' + hw_recipient[0])


# TASK 2
# Forward unseen email to list

# List of recipients to forward received e-mails to
reply_recipients = ['petar.popovic.bg@gmail.com', 'pyscript2018@gmail.com', 'darrenreid@gmail.com']

client = imapclient.IMAPClient(settings.imapserver)
client.login(settings.username, settings.password)

client.select_folder('INBOX')
UIDs = client.search(['UNSEEN'])
print('Unseen: ' + str(len(UIDs)))
print(UIDs)
for UID in UIDs:
    for send_to in reply_recipients:
        fetch_data = client.fetch(UID, ['RFC822'])
        msg = email.message_from_bytes(fetch_data[UID][b'RFC822'])
        smtp.sendmail(settings.username, send_to, msg.as_string())
        print('E-mail (id=' + str(UID) + ') forwarded to: ' + send_to)

client.close_folder()
client.logout()
# Disconnect from smtp server
smtp.quit()
