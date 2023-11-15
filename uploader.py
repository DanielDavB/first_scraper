
SUPABASE_URL = "https://db.asniuqxpkwgyoyprturw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFzbml1cXhwa3dneW95cHJ0dXJ3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTk5ODQ1MjYsImV4cCI6MjAxNTU2MDUyNn0.2XVpfJvrAdrLt7sZ8_WlSbG8v_s9kbJoy9yQx-IkmWo"
SUPABASE_PROJECT_NAME = "infosecur"
SUPABASE_TABLE_NAME = "data_links"

import os
from supabase import create_client, Client

# Get Supabase URL and API key from environment variables
url: str = os.environ.get("https://db.asniuqxpkwgyoyprturw.supabase.co")
key: str = os.environ.get('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFzbml1cXhwa3dneW95cHJ0dXJ3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTk5ODQ1MjYsImV4cCI6MjAxNTU2MDUyNn0.2XVpfJvrAdrLt7sZ8_WlSbG8v_s9kbJoy9yQx-IkmWo')

# Create Supabase client
supabase: Client = create_client(url, key)

# Define data to insert into the 'countries' table
data_links = {"title_notice": "titulo", "link": "asdasddsa"}  # Modify as needed

# Insert data into the 'countries' table
data, count = supabase.table('data_links').insert(data_links).execute()

# Print the response
print("Data inserted:", data)
print("Number of rows inserted:", count)
