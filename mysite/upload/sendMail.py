# -*- coding: utf-8 -*-
#!/usr/bin/python
# Filename: sendMail

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def notification(code,email):
    print "in the notificaiton"
    fromaddr = "wangchao.xy.1@gmail.com"
    toaddr = email
    msg = MIMEMultipart()
    print "after multipart"
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "code de la sécurité"
    print "after set message"
    print "code is:",code

    body = "Hello,\nyour security code is:\n"+str(code)+"\n\nsincerely"
    print body
    print "before attach"
    msg.attach(MIMEText(body,'plain'))
    print "after attach"

    print "before send a mail"
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.starttls()
    mail.login(fromaddr,'kikyo313@')
    text = msg.as_string()
    mail.sendmail(fromaddr,toaddr,text)
    mail.quit()
    print "Sent"

