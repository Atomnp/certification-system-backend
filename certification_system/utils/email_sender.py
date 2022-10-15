from email.message import EmailMessage
import ssl
import smtplib #imap,pop

email_sender = 'hairisgod@gmail.com' #your email


'''
You will have to create app password for email_sender email account

follow this link : 
https://towardsdatascience.com/automate-sending-emails-with-gmail-in-python-449cc0c3c317


'''

email_password = 'rahgxlgftrcugffd' #app_password

email_receivers = ['dawek23744@charav.com','neupane0403@gmail.com']


subject = 'Hello Test'


em = EmailMessage()

em['From'] = email_sender
em['Subject'] = subject

context = ssl.create_default_context()


with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:

    for email_receiver in email_receivers:
        
        body = f'''
            Hello, {email_receiver.split('@')[0]} are you okey?
        '''
        
        em.set_content(body)

        

        smtp.login(email_sender,email_password)
        smtp.sendmail(email_sender,email_receiver,em.as_string())
        print(email_receiver)


