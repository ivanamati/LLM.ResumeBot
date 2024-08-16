import os

def make_unique(name, existing_names):
    if name in existing_names:
        return None  # Indicates the name already exists
    return name

file_path = "recruiter_company.txt"

def name_checker(company_name):
    if company_name:
        # Load existing names from the file
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                existing_names = file.read().splitlines()
        else:
            existing_names = []
        # Check if the company name is unique
        unique_name = make_unique(company_name, existing_names)

        if unique_name:
        # Append the input to the file
            with open(file_path, "a") as file:
                file.write(company_name + "\n")

