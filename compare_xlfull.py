import pandas as pd
import requests
import os

# GitHub raw URLs for the Excel files
server_list_url = "https://raw.githubusercontent.com/gnayyar7/ansible_python/main/All_Servers_List.xlsx"
excluded_servers_url = "https://raw.githubusercontent.com/gnayyar7/ansible_python/main/Excluded_Servers_List.xlsx"

# Local file paths
output_folder = "./output_folder"
os.makedirs(output_folder, exist_ok=True)  # Create the output folder if it doesn't exist

server_list_file = os.path.join(output_folder, "server_list.xlsx")
excluded_servers_file = os.path.join(output_folder, "excluded_server_list.xlsx")
output_file = os.path.join(output_folder, "non_excluded_servers.xlsx")

# Function to download files
def download_file(url, local_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded: {local_path}")
    else:
        raise Exception(f"Failed to download file from {url}, status code: {response.status_code}")

# Download Excel files
download_file(server_list_url, server_list_file)
download_file(excluded_servers_url, excluded_servers_file)

# Read the downloaded Excel files
server_list_df = pd.read_excel(server_list_file)
excluded_servers_df = pd.read_excel(excluded_servers_file)

# Columns to compare
comparison_columns = ["ServerName", "IP", "Tag"]  # Replace with actual column names in your Excel files

# Ensure all required columns exist in both dataframes
for col in comparison_columns:
    if col not in server_list_df.columns or col not in excluded_servers_df.columns:
        raise ValueError(f"Column '{col}' not found in both dataframes")

# Perform case-sensitive filtering
non_excluded_servers_df = server_list_df[
    ~server_list_df.apply(
        lambda row: any(
            (row[col] == excluded_row[col]) for _, excluded_row in excluded_servers_df.iterrows()
        ),
        axis=1,
    )
]

# Sort the resulting dataframe (you can specify your sorting order here)
sort_columns = ["ServerName", "IP"]  # Replace with columns you want to sort by
non_excluded_servers_df = non_excluded_servers_df.sort_values(by=sort_columns)

# Save the result to a new Excel file
non_excluded_servers_df.to_excel(output_file, index=False)

print(f"Non-excluded server list saved to: {output_file}")