import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import openai

# Initialize AI model (you would replace 'your-api-key' with the actual OpenAI API key)
openai.api_key = 'your-api-key'

# Function to generate AI response
def get_ai_response(message):
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=message,
      max_tokens=150
    )
    return response.choices[0].text.strip()

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=/home/your_username/.config/google-chrome/Default")  # Adjust the path for your profile
options.add_argument('--headless')  # Run headless if you prefer

# This path might need adjustment
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Function to open WhatsApp Web
def open_whatsapp():
    driver.get('https://web.whatsapp.com')
    time.sleep(15)  # Wait for WhatsApp Web to load

# Function to check for new messages
def check_for_new_messages():
    # This selector might need specific adaptation based on WhatsApp Web's current structure
    unread_chats = driver.find_elements(By.XPATH, "//span[@class='_31gEB']")
    return unread_chats

# Function to reply to messages
def reply_to_messages(chats):
    for chat in chats:
        chat.click()
        time.sleep(2)  # Wait for the chat to open
        try:
            # Locate the message input box
            message_box = driver.find_element(By.XPATH, "//div[contains(@class, '_13NKt')]//p")
            # Read the current chat messages
            messages = driver.find_elements(By.XPATH, "//div[@class='_22Msk']//span")
            # Get the last message text
            last_message = messages[-1].text
            # Generate a response
            ai_reply = get_ai_response(last_message)
            message_box.send_keys(ai_reply + '\n')
            time.sleep(1)  # Allow a short pause between actions
        except Exception as e:
            print(f'Error: {e}')

# Main function to run the script
if __name__ == "__main__":
    open_whatsapp()
    while True:
        unread_chats = check_for_new_messages()
        if unread_chats:
            reply_to_messages(unread_chats)
        else:
            print("No new messages.")
        time.sleep(60)  # Check every minute