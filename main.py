#------------------Jan 2025---------------------
#--------------This code is about getting all tags for all service this save it by csv file---------------
#---------------onlyyy you need to change thw aws profile in your account---------------------

import boto3
import csv
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def list_all_tags(profile_name):
    try:
        session = boto3.Session(profile_name=profile_name)
        resourcegroupstaggingapi = session.client('resourcegroupstaggingapi')
        paginator = resourcegroupstaggingapi.get_paginator('get_resources')
        
        all_tags = []
        
        for page in paginator.paginate():
            for resource in page['ResourceTagMappingList']:
                resource_arn = resource['ResourceARN']
                tags = {tag['Key']: tag['Value'] for tag in resource.get('Tags', [])}
                all_tags.append({'ResourceARN': resource_arn, **tags})

        return all_tags

    except NoCredentialsError:
        print("no aWS credentials found. pplease configure your credentials.")
        return []
    except PartialCredentialsError:
        print("please check your configuration for aws :))))")
        return []
    except Exception as e:
        print(f"An error here, please look : {e}")
        return []

def save_tags_to_csv(tags, filename):
    if not tags:
        print("No tags to save.")
        return

    keys = set()
    for tag_dict in tags:
        keys.update(tag_dict.keys())

    keys = list(keys)  

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(tags)

    print(f"Tags saved to {filename}")
#=================================================================================
if __name__ == "__main__":
    profile_name = "rnad-acconuttt"  
    print(f"fetching all tags for AWS services using profile .......: {profile_name}...")
    tags = list_all_tags(profile_name)

    if tags:
        csv_filename = "aws_service_tags.csv"
        print("daving tags to CSV file...")
        save_tags_to_csv(tags, csv_filename)
    else:
        print("no tags here :).")


