#!/usr/bin/env python3
import yaml
import re
import argparse

# Function to load and sort the companies data
def sort_companies(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:  # Set encoding to utf-8
        data = yaml.safe_load(file)

    asn_entries = {}
    non_asn_entries = {}
    for key, value in data.items():
        if key.startswith('as') and re.match(r'^as(\d+)$', key):
            asn_number = int(key[2:])
            asn_entries[asn_number] = {**value, 'asn': asn_number}
        else:
            non_asn_entries[key] = value

    sorted_non_asn_entries = dict(sorted(non_asn_entries.items(), key=lambda item: item[0]))
    sorted_asn_entries = dict(sorted(asn_entries.items(), key=lambda item: item[0]))

    # Re-add the 'as' prefix to the ASN entries
    final_asn_entries = {'as' + str(key): value for key, value in sorted_asn_entries.items()}

    sorted_data = {**sorted_non_asn_entries, **final_asn_entries}
    return sorted_data

# Function to load and sort the users data
def sort_users(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:  # Set encoding to utf-8
        data = yaml.safe_load(file)

    sorted_data = dict(sorted(data.items(), key=lambda item: item[0]))
    return sorted_data

# Function to write sorted data to a file
def write_to_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:  # Set encoding to utf-8
        file.write('---\n')
        yaml.dump(data, file, default_flow_style=False, sort_keys=False, allow_unicode=True)

# Set up argument parsing
parser = argparse.ArgumentParser(description="Sort YAML files for companies and users.")
parser.add_argument('--write', action='store_true', help="Write the sorted data back to the files instead of printing.")
args = parser.parse_args()

# Path to the YAML files
companies_file_path = "../data/companies.yml"
users_file_path = "../data/users.yml"

# Sort the data
sorted_companies = sort_companies(companies_file_path)
sorted_users = sort_users(users_file_path)

if args.write:
    # Write sorted data back to the files
    write_to_file(companies_file_path, sorted_companies)
    write_to_file(users_file_path, sorted_users)
else:
    # Convert to YAML and print
    sorted_companies_yaml = yaml.dump(sorted_companies, default_flow_style=False, sort_keys=False, allow_unicode=True)
    sorted_users_yaml = yaml.dump(sorted_users, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print("Sorted Companies YAML:")
    print('---\n' + sorted_companies_yaml)
    print("Sorted Users YAML:")
    print('---\n' + sorted_users_yaml)
