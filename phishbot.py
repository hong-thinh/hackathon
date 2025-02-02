#!/usr/bin/python3
#All code is for "Ethical Hacking" research/education purposes only.
import sys
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr
import openai
import shutil
import time
from datetime import datetime
import qrcode

class colors:
    ENDC = '\033[m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BOLD = '\033[1m'
    RED = '\033[31m'

def logo():
    print(colors.BOLD + colors.YELLOW + "\n                           __    _      __    __          __")
    print(" __                 ____  / /_  (_)____/ /_  / /_  ____  / /_")
    print("/o \\/    __        / __ \\/ __ \\/ / ___/ __ \\/ __ \\/ __ \\/ __/")
    print("\\__/\\   /o \\/     / /_/ / / / / (__  ) / / / /_/ / /_/ / /_  ")
    print("        \\__/\\    / .___/_/ /_/_/____/_/ /_/_.___/\\____/\\__/  ")
    print("                /_/ \n" + colors.ENDC)

def menu():
    print(colors.ENDC + colors.BOLD + "Select an option to begin:\n")
    print("  1) Single Target Email Phish -> Employee")
    print("  2) Multi Target Email Phish -> Employees")
    print("  3) Single Target Email Phish -> Customer")
    print("  4) Multi Target Email Phish -> Customers\n")
    print("  Press any other key to exit...\n")
    input1 = input("> ")
    if input1 == '1' or input1 == '3':
        print("\nStarting single target phish -> Employee\n")
        input2 = input(colors.ENDC + colors.BOLD + "Enter Target email address: " + colors.ENDC)
        input3 = input(colors.ENDC + colors.BOLD + "Enter Sender Alias (ex. John Doe): " + colors.ENDC)

        print("Select an language to begin:\n")
        print("  1) English")
        print("  2) Japanese")
        print("  3) Spanish")
        input4 = input("> ")
        if(input4 == '1' or input4 == '2' or input4 == '3'):
            pass
        else:
            print("Invalid input! Defaulting to english! ")
            input4 = '1' 

        if input1 == '1':
            confirm = input(colors.GREEN + colors.BOLD + "\nExecute single target phish to Employee: " + input2 + " with Sender Alias: " + input3 + " . Press \"y\" to confirm, press any other key to exit.\n> " + colors.ENDC)
            if confirm == 'y' or confirm == 'Y':
                return(input1, input2, input3, input4)
            else:
                print(colors.RED + colors.BOLD + "\nExiting...\n" + colors.ENDC)
                sys.exit()

        elif input1 == '3':
            confirm = input(colors.GREEN + colors.BOLD + "\nExecute single target phish to Customer: " + input2 + " with Sender Alias: " + input3 + " . Press \"y\" to confirm, press any other key to exit.\n> " + colors.ENDC)
            if confirm == 'y' or confirm == 'Y':
                return(input1, input2, input3, input4)
            else:
                print(colors.RED + colors.BOLD +"\nExiting...\n" + colors.ENDC)
                sys.exit()
    elif input1 == '2' or input1 == '4':
        print("\nStarting multi target phish -> Employees\n")
        input2 = input(colors.ENDC + colors.BOLD + "Enter path to file of email addresses for multi target phish (ex. /home/user/list.csv): " + colors.ENDC)
        input3 = input(colors.ENDC + colors.BOLD + "Enter Sender Alias (ex. John Doe): " + colors.ENDC)
        
        print("Select an language to begin:\n")
        print("  1) English")
        print("  2) Japanese")
        print("  3) Spanish")
        input4 = input("> ")
        if(input4 == '1' or input4 == '2' or input4 == '3'):
            pass
        else:
            print("Invalid input! Defaulting to english! ")
            input4 = '1' 

        if input1 == '2':
            confirm = input(colors.GREEN + colors.BOLD + "\nExecute multi target phish to Employees in file: " + input2 + " with Sender Alias: " + input3 + " . Press \"y\" to confirm, press any other key to exit.\n> " + colors.ENDC)
            if confirm == 'y' or confirm == 'Y':
                return(input1, input2, input3, input4)
            else:
                print(colors.RED + colors.BOLD + "\nExiting...\n" + colors.ENDC)
                sys.exit()
        elif input1 == '4':
            confirm = input(colors.GREEN + colors.BOLD + "\nExecute multi target phish to Customers in file: " + input2 + " with Sender Alias: " + input3 + " . Press \"y\" to confirm, press any other key to exit.\n> " + colors.ENDC)
            if confirm == 'y' or confirm == 'Y':
                return(input1, input2, input3, input4)
            else:
                print(colors.RED + colors.BOLD + "\nExiting...\n" + colors.ENDC)
                sys.exit()
    else:
        print(colors.RED + colors.BOLD + "\nExiting...\n" + colors.ENDC)
        sys.exit()

def single_phish(input1, input2, input3, input4):
    user,mail_server = mail_server_connect()
    email_to = input2
    send_email(user,mail_server,email_to,input1,input2,input3, input4)
    mail_server.quit()

def multi_phish(input1, input2, input3, input4):
    user,mail_server = mail_server_connect()
    try:
        email_list = open(input2, 'r')
    except:
        print(colors.RED + colors.BOLD + "file not found... Exiting...\n" + colors.ENDC)
        mail_server.quit()
        sys.exit()
    print("Starting multi phish")
    emails = email_list.readlines()
    for email in emails:
        email_to = email.rstrip('\n')
        send_email(user,mail_server,email_to,input1,input2,input3, input4)
        time.sleep(1)
    mail_server.quit()

def mail_server_connect():
    user = os.getenv('GMAIL_USER')
    pswd = os.getenv('GMAIL_PASSWORD')
    smtp_port = 587
    smtp_server = "smtp.gmail.com"
    print(colors.ENDC + colors.BOLD + "\nConnecting to mail server ... " + colors.ENDC)
    mail_server = smtplib.SMTP(smtp_server, smtp_port)
    mail_server.starttls()
    mail_server.login(user, pswd)
    return(user,mail_server)

def translate_text(text, target_language): 
    response = openai.Completion.create( 
    
    # engine="text-davinci-002",
    model="gpt-3.5-turbo-instruct", 
    prompt=f"Translate the following text into {target_language}: {text}\n", 
    max_tokens=1000, 
    n=1, 
    stop=None, 
    temperature=0.2) 
    return response.choices[0].text.strip()

def ai_gen(input1, input4):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    if input1 == '1' or input1 == '2':
        prompt_subject = 'Generate an email subject about updates to Toyota Benefits for employee under 9 words.'
        prompt_body = f'Write an email body with respect to {prompt_subject} without a greeting, intro, closing, salutation, or dates telling the employee that we have confirmed the recent changes to their benefits in under 100 words. Ask the employee to respond to this email if they have any questions. Again do not include a greeting or closing.'
    
    elif input1 == '3' or input1 == '4':
        prompt_subject = 'Generate an email subject about updates to Toyota Benefits for customer under 9 words.'
        prompt_body = f'Write an email body with respect to {prompt_subject} without a greeting, intro, closing, salutation, or dates telling the employee that we have confirmed the recent changes to their benefits in under 100 words. Ask the employee to respond to this email if they have any questions. Again do not include a greeting or closing.'

    # Call the OpenAI API to generate email subjects
    response_subject = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt_subject}
        ]
    )


    # Call the OpenAI API to generate email bodies
    response_body = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt_body}
        ]
    )
    response_subject = response_subject['choices'][0]['message']['content']
    response_subject = re.sub(r'[^a-zA-Z0-9\s]', '', response_subject)
    response_subject = response_subject.replace('"', '')
    response_body = response_body['choices'][0]['message']['content']


    if input4 == '1':
        return (response_subject, response_body)
    elif input4 == '2':
        response_subject_japanese = translate_text(response_subject, 'JAPANESE')
        response_body_japanese = translate_text(response_body, 'JAPANESE')
        return (response_subject_japanese, response_body_japanese)
    elif input4 == '3':
        response_subject_spanish = translate_text(response_subject, 'es')
        response_body_spanish = translate_text(response_body, 'es')
        return (response_subject_spanish, response_body_spanish)

    else:
        print("Invalid input! Defaulting to english! ")


def send_email(user, mail_server, email_to, input1, input2, input3, input4):    
    subject, body = ai_gen(input1, input4)
    url, qr = url_gen(input1)
    print(colors.GREEN + colors.BOLD + " <>< <><  Sending Phishbot email to " + email_to + " with email Alias " + input3 + " <>< <>< " + colors.ENDC)
    email_from = user
    if input1 == '1' or input1 == '2':
        fullbody = '<html><body><br>' + body + '<br><br><div style="text-align:center;"><a href="' + url + '" style="background-color: #008CBA; border: none; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;">OPEN IN OKTA</a></div><br><br> Thank you,<br>' + input3 + '</body></html>'
    if input1 == '3' or input1 == '4':
        fullbody = '<html><body><br>' + body + '<br><br><img style="margin: 0; border: 0; padding: 0; display: block;" src="https://toyfinancialservices.com/qrcodes/' + qr + '" width="100" height="100"></img ><br><br> Thank you,<br>' + input3 + '</body></html>'
    msg = MIMEMultipart()
    msg['From'] = formataddr((input3, email_from))
    msg['To'] = email_to
    msg['Subject'] = subject
    msg.attach(MIMEText(fullbody, 'html'))
    text = msg.as_string()
    mail_server.sendmail(email_from, email_to, text)
    create_log(email_from, email_to, subject, url, body, input1, input4)
    return(email_from, email_to, subject, body)


def url_gen(input1):
    t = str(round(time.time()))
    if input1 == '1' or input1 == '2':
        src_file = "/root/braddev/file.html"
        dst_file = "/var/www/html/" + t + "_okta"
        url = "http://toyfinancialservices.com/" + t + "_okta"
        qr="none"
    elif input1 == '3' or input1 == '4':
        src_file = "/opt/hackathon/mobilemain.html"
        dst_file = "/var/www/html/" + t + "_mobile"
        url = "https://toyfinancialservices.com/" + t + "_mobile"
        img = qrcode.make(url)
        type(img)
        img.save("/var/www/html/qrcodes/"+t+"qr.png")
        qr = t+"qr.png"
    shutil.copy(src_file,dst_file)
    print(colors.ENDC + colors.BOLD + "Creating target url: " + url + " ..." + colors.ENDC)
    return(url,qr)

def create_log(email_from,email_to,subject,url,body,input1,input4):
    print(colors.ENDC + colors.BOLD + "Create log entry ... \n" + colors.ENDC)
    body = re.sub(r'(\r|\n)',r'', body)
    if input4 == 2:
        language = "japanese"
    elif input4 == 3:
        language = "spanish"
    else:
        language = "english"
    logdate = (datetime.now()).strftime("%m/%d/%Y %H:%M:%S")
    log_output = '{"timestamp":"' + logdate + '","phishtype":"' + input1 + '","action":"send_initial_phish","aiuser":"system","sender":"' + email_from + '","recipient":"' + email_to + '","subject":"' + subject + '","phishurl":"' + url + '","body":"' + body + '","language":"' + language + '"}\n'
    l = open("/opt/hackathon/phishbot.log", "a")
    l.write(log_output)
    l.close

def main():
    logo()
    input1, input2, input3, input4 = menu()
    if input1 == '1' or input1 == '3':
        single_phish(input1, input2, input3, input4)
    if input1 == '2' or input1 == '4':
        multi_phish(input1, input2, input3, input4)

if __name__ == "__main__":
    main()
