from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime
import smtplib
import settings
import os.path as op
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders


def create_mail(drname, clientname):
    # Creating base mail
    msg = MIMEMultipart()
    # Adding default values for Date, Subject, and Text
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = 'Latest records for ' + clientname
    msg.attach(MIMEText(
        'Hello Dr.' + drname + '\n\nWe are writing to get the latest records for our client ' + clientname + '.'))
    # Adding attachment
    # # Uploads from a list of attachments, fixed with example for now
    # files = ['sample1.pdf', 'sample2.pdf']
    #
    # for path in files:
    #     part = MIMEBase('application', "octet-stream")
    #     with open(path, 'rb') as file:
    #         part.set_payload(file.read())
    #     encoders.encode_base64(part)
    #     part.add_header('Content-Disposition',
    #                     'attachment; filename="{}"'.format(op.basename(path)))
    #     msg.attach(part)
    # retuns full e-mail to send
    return msg


# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

sheet_id = '1HNfsOKcbPwx9P2InoFqBi5blj4Ntz_iQen7a5UeJURY'
data_range = 'A2:G'

data = []


def main():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id,
                                range=data_range).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        for row in values:
            data.append(row)

    smtp = smtplib.SMTP(settings.smtpserver, settings.smtpport)
    smtp.starttls()
    smtp.login(settings.username, settings.password)

    for row in data:
        joinday = int(row[3][:2])
        if datetime.now().day == joinday:
            print("\nSending mail to Dr. " + row[4] + ' regarding client ' + row[2])
            # smtp.sendmail(settings.username, row[5], create_mail(row[4], row[2]).as_string())
            print(
                'Reminder sent to: ' + row[5] + ' / Subject: ' + create_mail(row[4], row[2]).get('subject') + '\n')
        else:
            pass
    smtp.close()


if __name__ == '__main__':
    main()
