import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
import pexpect
import re
import string

def alone_get_SocraBot(input_text):
    eval_prompt_pt1 = """
    Below is an instruction that describes a task. Write a response that appropriately completes the request. Instruction: Your name is SocraBot and you are a conversation guide. I want you to act as a conversation guide who is helping groups of youth in a study group about a certain topic. You will be getting messages between Users struggling with that topic and I want you to help guide conversation to help these users with their challenges by asking questions, prompting discussion between users, and answering questions they ask you. Your job is a moderator who will guide the conversation as a whole through icebreakers ad questions. Only respond as SocraBot. You will be provided with the history of this chat with all past responses including yours. Take this information and respond to the users in the optimal manner and focus on helping them with the academic topic they are struggling with. Do not simulate the whole conversation, users will respond to you. You are the conversation guide and group tutor, not the user. Input: """
    eval_prompt_pt2=""" BotResponse:"""
    user_input=eval_prompt_pt1+str(input_text)+eval_prompt_pt2
    # Create a child process to run 'ollama run llama2'
    child = pexpect.spawn('ollama run llama2')
    # Create a list to store the conversation
    child.sendline(user_input)
    child.expect([pexpect.EOF, pexpect.TIMEOUT, pexpect.EOF, 'ChatbotPrompt>'], timeout=30)
    #child.expect([pexpect.EOF, pexpect.TIMEOUT, pexpect.EOF, 'ChatbotPrompt>'], timeout=20)
    response = child.before.strip().decode('utf-8')
    
    child.close()
    response=str(response)
    #ind=response.rfind("Response:")
    #ind=ind+9
    #linnd=response.rfind(">>>")
    #print(response[ind:linnd])
    return response

def group_get_SocraBot(input_text):
    eval_prompt_pt1 = """
    Below is an instruction that describes a task. Write a response that appropriately completes the request. Instruction: Your name is SocraBot and you are a conversation guide. I want you to act as a conversation guide who is helping groups of youth in a study group about a certain topic. You will be getting messages between Users struggling with that topic and I want you to help guide conversation to help these users with their challenges by asking questions, prompting discussion between users, and answering questions they ask you. Your job is a moderator who will guide the conversation as a whole through icebreakers ad questions. Only respond as SocraBot. You will be provided with the history of this chat with all past responses including yours. Take this information and respond to the users in the optimal manner and focus on helping them with the academic topic they are struggling with. Do not simulate the whole conversation, users will respond to you. You are the conversation guide and group tutor, not the user. Input: """
    eval_prompt_pt2=""" BotResponse:"""
    user_input=eval_prompt_pt1+str(input_text)+eval_prompt_pt2
    # Create a child process to run 'ollama run llama2'
    child = pexpect.spawn('ollama run llama2')
    # Create a list to store the conversation
    child.sendline(user_input)
    child.expect([pexpect.EOF, pexpect.TIMEOUT, pexpect.EOF, 'ChatbotPrompt>'], timeout=40)
    #child.expect([pexpect.EOF, pexpect.TIMEOUT, pexpect.EOF, 'ChatbotPrompt>'], timeout=20)
    response = child.before.strip().decode('utf-8')
    
    child.close()
    response=str(response)
    #ind=response.rfind("Response:")
    #ind=ind+9
    #linnd=response.rfind(">>>")
    #print(response[ind:linnd])
    return response



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
print("gothead")
header_mems=head_text.text
user_count=header_mems.count(" ")
time.sleep(1)

for cycle in range(3):

    all_messages=driver.find_elements(By.CLASS_NAME,"ce-their-message")
    time.sleep(1)

    chat_hist=""

    for msg in all_messages:
        cur_user=msg.find_element(By.CLASS_NAME,"ce-their-message-sender-username")
        print(cur_user.text)
        chat_hist+=str(cur_user.text)+": "
        cur_msgbody=msg.find_element(By.CLASS_NAME,"ce-their-message-body")
        print(cur_msgbody.text)
        chat_hist+=str(cur_msgbody.text)+" "

    botans=group_get_SocraBot(chat_hist)
    ind=botans.rfind("BotResponse:")
    ind=ind+12
    linnd=botans.rfind(">>>")
    if(linnd>ind):
        botans=botans[ind:linnd]
    else:
        botans=botans[ind:]

    allowed = set(string.ascii_lowercase + string.ascii_uppercase + string.digits + ' ' + '?'+ '.'+'!')

    def check(test_str):
        return set(test_str) <= allowed

    def cleantxt(intxt):
        ans=""
        for i in intxt:
            i = str(i)
            if (check(i)):
                ans+=i
        return ans

    #botans=remove_emojis(botans)
    #botans=botans.strip()
    botans=cleantxt(botans)
    print(botans)
    

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
    print(ogcount)
    time.sleep(1)
    while(True):
        count=0
        all_messages=driver.find_elements(By.CLASS_NAME,"ce-their-message")
        for msg in all_messages:
            count+=1
        print(count)
        if(count%3==0 and count > ogcount):
            break
        
    