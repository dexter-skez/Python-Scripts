import os

def rename_files(folder_path, keyword, company_name):
  # Get list of files in the folder
  files = os.listdir(folder_path)
  start_number = 1  # Adjust if you want a different starting number

  for filename in files:
    # Extract file extension
    extension = os.path.splitext(filename)[1]

    # Create new filename with sequence number, keyword, and company name
    new_filename = f"{keyword} - {start_number:01d} - {company_name}{extension}"
    old_path = os.path.join(folder_path, filename)
    new_path = os.path.join(folder_path, new_filename)
    # Rename the file
    os.rename(old_path, new_path)
    start_number += 1

# Specify the folder path, keyword, and company name
folder_path = "/Users/willstaton/Downloads/Case Study 4/02_Geo"  # Replace with your actual path
keyword = "Replaced with"  # Replace with your desired keyword
company_name = "This is a test"  # Replace with the company name
rename_files(folder_path, keyword, company_name)

print("Files renamed successfully!")
