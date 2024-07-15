import requests
import json
import smtplib
import logging
URL ='https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political,racist,sexist,explicit'
with open('creds.json','r')as f:
  creds =json.load(f)
  f.close()
LOGFILE ='email_send.log'
EMAIL = creds['email']
PASSWORD =creds['password']
RECEIVER = EMAIL

logging.basicConfig(filemode='a',filename=LOGFILE,level=logging.INFO,format='%(levelname)s-%(asctime)s-%(message)s')

def send_email(joke):
  s= smtplib.SMTP('smtp.gmail.com',587) 
  s.starttls()
  try:
    s.login(EMAIL,PASSWORD)
  except smtplib.SMTPAuthenticationError:
   logging.error('auth failure')
   exit()
  message=f'\n{joke}'
  try:
   s.sendmail(EMAIL,RECEIVER,message)
  except smtplib.SMTPException:
   logging.error('unable to send email due to error')
   exit()
  s.quit()

def get_joke_content():
 try:
  response = requests.get(URL)
 except requests.HTTPError:
  logging.error('HTTP request issue')
  exit()
 return response.json()

def extract_joke(result):
  if result['type']== 'twopart':
    setup=result['setup']
    delivery =result['delivery']
    joke_string = f'Setup: {setup}\nDelivery :{delivery}'
  else:
    joke_string =result['joke']
    return(joke_string)
  
if __name__=="__main__":
 result= get_joke_content()
 joke = extract_joke(result)
 logging.info('joke retrieved succesfully')
 send_email(joke)
 logging.info('Joke email complete')
