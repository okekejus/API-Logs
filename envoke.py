import requests 
from requests.auth import HTTPBasicAuth
import os
import json 
import pandas as pd 
import datetime as dt 
from dotenv import load_dotenv, dotenv_values
import time
import numpy as np 


# Functions for formatting data 
def left(s, amount): 
    return s[:amount]

def mid(s, offset, amount): 
    return s[offset:offset+amount]

def expander(list, phrase, offset=2, amount=2): 
    detection = [s.find(phrase) > 0 for s in list]

    try:
        detection = detection.index(True)
        resp = list[detection]
        resp = mid(resp, offset, amount)
        return resp
    except ValueError as v: 
        return np.nan
    
# Gathering
def get_email_metrics(run_date): 

        url = f"https://e1.envoke.com/v1/reports/emailActivityMetrics?start_date={run_date}&end_date={run_date}"
        params = {'filter[sent_date]': [f"{run_date}"]}
        payload = {}
        headers = {}


        try: 
            resp = requests.get(url=url, headers=headers, data=payload, auth=basic, params=params) # sending request to API using url, filter, and authorization 

            if resp.status_code == 200: # if response is successful, turn the json file into a df for future use
                
                resp_df = pd.DataFrame(resp.json()) # conversion into dataframe
                resp_df = resp_df[resp_df['sent_date'] == run_date] # additional filtering required at the moment, for some reason the date filter doesn't work.
                
                
                if len(resp_df['message_name']) > 0:
                    old_message_stats = pd.read_csv('envoke/Messages/aggregate_message_metrics.csv')
                    resp_df.to_csv(f'envoke/Messages/message_stats_{run_date}.csv', index=False)
                    new_aggregate = pd.concat([old_message_stats, resp_df])
                    new_aggregate.to_csv("envoke/Messages/aggregate_message_metrics.csv", index=False)
                    return resp_df
                else: 
                    print(f"There have been no messages sent using Envoke on {run_date}")

            else: 
                print(f"Initial request failed due to error code {resp.status_code}")

        except Exception as e: 
            print(f"Error occurred during the request: {e}")

        except requests.exceptions.RequestException as e: # this will handle specific requests exceptions, which can be informative
            print(f"An unexpected error occurred during the request: {e}")


def get_active_contacts(status_filters=["Implied - No Expiry","Express"], skip=0):
    resp_df = pd.DataFrame()
    check = 1
    all_results = []
    url = f"https://e1.envoke.com/v1/contacts?skip={skip}&limit=100"
    params = {'filter[consent_status]': status_filters}
    payload = {}
    headers = {}

    # need to add a filter for people with status: 'Implied - No Expiry', 'Express' to prevent fetching ALL contacts in the database. 
    try: 
        response = requests.get(url, headers=headers, data=payload, auth=basic, params=params)

        if response.status_code == 200: 
            response_df = pd.DataFrame(response.json()) # convert initial response to dataframe
            all_results.append(response.json()) # append results to list for future concatenation
            check = len(response.json()) # check the length of the response to the request
        else: 
            print(f"Initial request failed with status code {response.status_code}")
            check = 0 
    except Exception as e: 
        print(f"Error occurred during initial request: {e}")
        check = 0 # stop loop if there is request error 

    while check > 0: 
        skip += 100 # adding 100 to the skip number as you are limited to a maximum of 100 contacts per request
        url = f"https://e1.envoke.com/v1/contacts?skip={skip}&limit=100"
        print(f"Skipping {skip-100} contacts.")

        try:
            response = requests.get(url, headers=headers, data=payload, auth=basic, params=params) # send next request 

            if response.status_code == 200: 
                results = response.json() # get the json response 
                all_results.append(results)
                check = len(results)


                time.sleep(1) 
            else: 
                print(f"Request failed with code {response.status_code}")
                check = 0 # stop loop 
        except Exception as e: 
            print(f"Error occurred during the request: {e}")
            check = 0 
    current_contacts = pd.concat([pd.DataFrame(result) for result in all_results], ignore_index=True)

    current_contacts['full_name'] = current_contacts['first_name'] + ' ' + current_contacts['last_name'] # full name to make things easier 
    current_contacts['full_name'] = current_contacts['full_name'].replace(r"^\s*$", np.nan, regex=True)
    current_contacts['date_created'] = current_contacts['date_created'].apply(lambda x: left(x, 10))
    current_contacts['current_director'] = current_contacts['interests'].apply(lambda x: expander(x, "currently a director", amount=3))
    current_contacts['been_director'] = current_contacts['interests'].apply(lambda x: expander(x, "been a director",  amount=3))
    current_contacts['is_condo_owner'] = current_contacts['interests'].apply(lambda x: expander(x, "a condo owner", amount=3))
    current_contacts['referral'] = current_contacts['interests'].apply(lambda x: True if expander(x, "Referral") == "Ref" else False)
    current_contacts["full_name"] = current_contacts["full_name"].str.title()
    return current_contacts


def get_revoked_contacts(status_filters=['Revoked']):
    resp_df = pd.DataFrame()
    skip = 0
    check = 1
    all_results = []
    url = f"https://e1.envoke.com/v1/contacts?skip={skip}&limit=100"
    params = {'filter[consent_status]': status_filters}
    payload = {}
    headers = {}

    # need to add a filter for people with status: 'Implied - No Expiry', 'Express' to prevent fetching ALL contacts in the database. 
    try: 
        response = requests.get(url, headers=headers, data=payload, auth=basic, params=params)

        if response.status_code == 200: 
            response_df = pd.DataFrame(response.json()) # convert initial response to dataframe
            all_results.append(response.json()) # append results to list for future concatenation
            check = len(response.json()) # check the length of the response to the request
        else: 
            print(f"Initial request failed with status code {response.status_code}")
            check = 0 
    except Exception as e: 
        print(f"Error occurred during initial request: {e}")
        check = 0 # stop loop if there is request error 

    while check > 0: 
        skip += 100 # adding 100 to the skip number as you are limited to a maximum of 100 contacts per request
        url = f"https://e1.envoke.com/v1/contacts?skip={skip}&limit=100"
        print(f"Skipping {skip-100} contacts.")

        try:
            response = requests.get(url, headers=headers, data=payload, auth=basic, params=params) # send next request (headers and payload are needed to maintain i guess)

            if response.status_code == 200: 
                results = response.json() # get the json response 
                all_results.append(results)
                check = len(results)


                time.sleep(1) 
            else: 
                print(f"Request failed with code {response.status_code}")
                check = 0 # stop loop 
        except Exception as e: 
            print(f"Error occurred during the request: {e}")
            check = 0 

    revoked_contacts = pd.concat([pd.DataFrame(result) for result in all_results])
    revoked_contacts['full_name'] = revoked_contacts['first_name'] + ' ' + revoked_contacts['last_name'] # full name to make things easier 
    revoked_contacts['full_name'] = revoked_contacts['full_name'].replace(r"^\s*$", np.nan, regex=True)
    revoked_contacts['date_created'] = revoked_contacts['date_created'].apply(lambda x: left(x, 10))
    revoked_contacts['revoked_director'] = revoked_contacts['interests'].apply(lambda x: expander(x, "revokedly a director", amount=3))
    revoked_contacts['been_director'] = revoked_contacts['interests'].apply(lambda x: expander(x, "been a director",  amount=3))
    revoked_contacts['is_condo_owner'] = revoked_contacts['interests'].apply(lambda x: expander(x, "a condo owner", amount=3))
    revoked_contacts['referral'] = revoked_contacts['interests'].apply(lambda x: True if expander(x, "Referral") == "Ref" else False)
    revoked_contacts["full_name"] = revoked_contacts["full_name"].str.title()
    return revoked_contacts


if __name__ == "__main__":
    load_dotenv() 
    basic = HTTPBasicAuth(os.getenv("USERNAME"), os.getenv("PASSWORD"))
    run_date = str(dt.date.today() - dt.timedelta(days = 1))

    get_email_metrics(run_date=run_date)

    current_contacts = get_active_contacts()
    revoked_contacts = get_revoked_contacts()

    d = {'date': [run_date], 
     'total_active_contacts': [len(current_contacts['id'])], 
     'total_revoked_contacts': [len(revoked_contacts['id'])]}
    
    master_contact_list_addon = pd.DataFrame(d)
    current_contacts = current_contacts.drop(columns=['custom_fields','interests', 'autoresponders'])
    current_contacts.to_csv(f"current_contacts.csv", index=False) 
    revoked_contacts.to_csv(f"revoked_contacts.csv", index=False) 
    master_contact_list_addon.to_csv(f"addon.csv", index=False)
     
