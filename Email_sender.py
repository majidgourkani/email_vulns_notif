import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.application import MIMEApplication
from datetime import datetime

smtp_host = 'mail.email.co'  # smtp.mail.yahoo.com
smtp_port = 587
username = 'something@email.com'
password = '*********'
sender = 'sender@email.com'
targets = 'receiver@email.com'
cc_addrs = 'cc@email.com'

def send(desc):

    Message = MIMEMultipart('mixed')
    Message['Subject'] = desc.split(":")[1].strip()
    Message['From'] = sender
    Message['Cc'] = cc_addrs
    Message['To'] = targets

    msg_content = '<h3>Hello,<br> {} send in attachment.</h3>\n'.format(desc.split(":")[1].strip())
    body = MIMEText(msg_content, 'html')
    Message.attach(body)

    with open("outputs/"+desc.split(":")[0].strip()+'.html', "rb") as attachment:
        p = MIMEApplication(attachment.read(),_subtype="html")
        p.add_header('Content-Disposition', "attachment; filename= {}".format(desc.split(":")[0].strip()+'.html'))
        Message.attach(p)

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(username, password)
    server.sendmail(sender, targets, Message.as_string())
    server.quit()
    print("{t},\t{n}.html sent successfully.".format(t=datetime.now().strftime("%d/%m/%Y %H:%M:%S") ,n=desc.split(":")[0].strip()))