import os
import openai
from dotenv import load_dotenv
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
import pexpect
import re
import string


def group_get_SocraBot(chat_hist):
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    instructions=" Your name is SocraBot and you are a conversation guide. I want you to act as a conversation guide who is helping groups of youth in a study group about a certain topic. You will be getting messages between Users struggling with that topic and I want you to help guide conversation to help these users with their challenges by asking questions, prompting discussion between users, and answering questions they ask you. Your job is a moderator who will guide the conversation as a whole through icebreakers ad questions. Only respond as SocraBot. You will be provided with the history of this chat with all past responses including yours. Take this information and respond to the users in the optimal manner and focus on helping them with the academic topic they are struggling with. Do not simulate the whole conversation, users will respond to you. You are the conversation guide and group tutor, not the user."

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": instructions},
        {"role": "user", "content": chat_hist}
    ]
    )
    return completion.choices[0].message["content"]




# Using Chrome to access web
driver = webdriver.Chrome()

# Open the website
driver.get('http://localhost:5173/')

# Login
login_box = driver.find_element(By.CLASS_NAME, "auth-input")
login_box.send_keys('SocraBot\r\n')
time.sleep(2)

# Find users
head_text = driver.find_element(By.CLASS_NAME, "ce-custom-header-title")
time.sleep(1)
#print("gothead")
header_mems=head_text.text
user_count=header_mems.count(" ")
time.sleep(1)

while(True):
    all_messages=driver.find_elements(By.CLASS_NAME,"ce-their-message")
    time.sleep(1)

    msgcount=0
    for msg in all_messages:
        msgcount+=1
    
    if msgcount>=user_count:
        print("wow")
        break


for cycle in range(2):

    all_messages=driver.find_elements(By.CLASS_NAME,"ce-their-message")
    time.sleep(1)

    chat_hist=""
    msgcount=0
    for msg in all_messages:
        msgcount+=1
        cur_user=msg.find_element(By.CLASS_NAME,"ce-their-message-sender-username")
        print(cur_user.text)
        chat_hist+=str(cur_user.text)+": "
        cur_msgbody=msg.find_element(By.CLASS_NAME,"ce-their-message-body")
        print(cur_msgbody.text)
        chat_hist+=str(cur_msgbody.text)+" "
    
    if msgcount<user_count:
        cycle=0
        continue

    botans=group_get_SocraBot(chat_hist)
    print("AI: "+str(botans))

    # Send a Msg
    msg_box = driver.find_element(By.CLASS_NAME, "ce-custom-message-input")
    submit_button = driver.find_element(By.CLASS_NAME,'ce-custom-send-button')  # Replace with the actual class name
    time.sleep(1)
    msg_box.send_keys(botans)
    time.sleep(1)
    submit_button.click()
    time.sleep(2)

    ogcount=0
    all_messages=driver.find_elements(By.CLASS_NAME,"ce-their-message")
    for msg in all_messages:
        ogcount+=1
    #print(ogcount)
    time.sleep(1)
    while(True):
        count=0
        all_messages=driver.find_elements(By.CLASS_NAME,"ce-their-message")
        for msg in all_messages:
            count+=1
        #print(count)
        if(count%3==0 and count > ogcount):
            break
        
    
