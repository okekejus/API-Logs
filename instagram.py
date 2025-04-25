
    import requests
    import pandas as pd
    import json
    import os
    from dotenv import load_dotenv, dotenv_values
    import datetime as dt


    load_dotenv()
    tkn = os.getenv('INSTA_TOKEN')
    run_date = dt.datetime.today().date()

   def fetch_public(me = f\"https://graph.instagram.com/v22.0/me?fields=followers_count,follows_count,media_count&access_token={tkn}\"): 
      instagram_info = requests.get(me)
      vals = instagram_info.json()
      vals['run_date'] = run_date
    
      vals = pd.DataFrame([vals])
      vals.to_csv(f\"{run_date}_instagram.csv\", index=False)

if __name__ == "__main__": 
    load_dotenv()
    tkn = os.getenv('INSTA_TOKEN')
    run_date = dt.datetime.today().date()
    fetch_public()


 
 
