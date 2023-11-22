import requests
import lxml.html as html
import datetime
import os
import time
import re
import schedule
from supabase import create_client  # Import create_client directly
import os
from supabase import create_client, Client


HOME_URL = "https://elpais.com/noticias/seguridad-internet/"
XPATH_LINK_TO_ARTICLE = '//h2[@class="c_t "]//a/@href'
XPATH_TITLE = '//h2[@class="c_t "]//a'


def insert_into_database(title, link):
    # Create Supabase client
    supabase: Client = create_client("https://asniuqxpkwgyoyprturw.supabase.co",
                                     "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFzbml1cXhwa3dneW95cHJ0dXJ3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTk5ODQ1MjYsImV4cCI6MjAxNTU2MDUyNn0.2XVpfJvrAdrLt7sZ8_WlSbG8v_s9kbJoy9yQx-IkmWo")

    # Define data to insert into the 'data_links' table
    data_links = {"title": title, "link": link}

    # Insert data into the 'data_links' table
    data, count = supabase.table('data_links').insert(data_links).execute()

    # Print the response
    print("Data inserted:", data)
    print("Number of rows inserted:", count)


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
            

            for link in links_to_notice:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

    
def run():
    print("running task")
    parse_home()


#Comment this section to run instantly
schedule.every(2).minutes.do(run)

while True: 
    schedule.run_pending()
    time.sleep(1)

#uncomment this line to run instantly
# if __name__ == 'main':
#     run()
