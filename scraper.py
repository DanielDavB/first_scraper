import requests
import lxml.html as html 
import datetime
import os
import time
import re
import supabase

HOME_URL = "https://thehackernews.com/"
XPATH_LINK_TO_ARTICLE = '//a[@class="story-link"]/@href'
XPATH_TITLE = '//h1[@class="story-title"]//text()'

# Supabase configuration
SUPABASE_URL = "https://db.asniuqxpkwgyoyprturw.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFzbml1cXhwa3dneW95cHJ0dXJ3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTk5ODQ1MjYsImV4cCI6MjAxNTU2MDUyNn0.2XVpfJvrAdrLt7sZ8_WlSbG8v_s9kbJoy9yQx-IkmWo"
SUPABASE_PROJECT_NAME = "infosecur"
SUPABASE_TABLE_NAME = "data_links"

def insert_into_database(title, link):
    try:
        # Connect to Supabase
        supabase_client = supabase.create_client(
            SUPABASE_URL,
            SUPABASE_API_KEY,
            SUPABASE_PROJECT_NAME
        )

        # Insert into the database
        response = supabase_client.table(SUPABASE_TABLE_NAME).upsert([{"title": title, "link": link}], returning="minimal")

        if response.status_code != 200:
            print("Error inserting into database:", response.text)

    except Exception as e:
        print("Error:", e)

def sanitize_title(title):
    # Remove characters that are not allowed in filenames
    title = re.sub(r'[\/:*?"<>|]', '', title)
    # Replace spaces with underscores
    title = title.replace(' ', '_')
    return title

def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\n', '').strip()
                title = sanitize_title(title)  # Sanitize the title
                
                print(link, title)
                # Insert into the database
                insert_into_database(title, link)

            except IndexError:
                return
            
                
        else:
            raise ValueError(f'Error: {response.status_code}')    
    except ValueError as ve:
        print(ve)

def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notice = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_notice:
                parse_notice(link, today)   
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()
