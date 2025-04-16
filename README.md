# API Logs
A repository for code used to interact with APIs from various data sources. These are mainly code snippets from previous/ongoing work projects. Over time I expect to revisit these, and would like to improve my work in the process.

APIs used are listed below. None of the data collected using these scripts belongs to me, so I will be unable to share any of the datasets associated with the files.

# Meta (Instagram/Facebook) 

I used this API as part of a data pipeline when creating a report for my current organization's Communications Team. To interact with it, I had to create an app using Meta's Developer platform, and register the *Instagram* and *Facebook Login for Business* products to the app. These granted access to Instagram and Facebook data respectively. Business verification was required to use these services at no extra cost.

The Instagram connection was fairly straight forward to set up, making use of the `requests, pandas, json, os, dotenv, dateteime` modules in python. The script is set up to feed into an Azure Data Lake, as a result, it produces one row of output (.csv) a day, detailing: 
- Total Followers
- Total Following
- Total Posts
- Run Date


Outputs are fed into PowerBI using the Azure Blob connection, and then concatenated into one cohesive dataset for reporting purposes. 

# Google Analytics 
Google Analytics is a very popular web analytics service offered by Google. It is used to track/report website and mobile app traffic and events. There are reporting options available within Google Analytics, but the storage options are restricted to a 12 month period (anything older is deleted). As a result, there was a need for automated extraction and storage of data before its deletion. 

The script makes use of the `os, pandas, datetime, dotenv, google.analytics.data_v1beta, google.auth` modules. Google Analytics groups its information into Metrics and Dimensions. Each request will contain specific combinations of the two, and the associated values for a specified project will be returned. The specific metrics and dimensions can be viewed within the file. 

The output is fed into an Azure Data Lake. Script is run daily, monthly, quarterly and annually, as specific metrics (Unique Users) will differ based on the time frames used in the request. If I access the website once today, and once tomorrow, I will be counted as a unique user each day. If I request data for this month however, I will be counted only once. 

# Envoke 
[Envoke](https://envoke.com/) is a platform for sending optional and mandatory emails to stakeholders and members of an organization. It is used frequently by my current employer to contact various individuals on various topics. Envoke provides business accounts with an API at no additional cost. Users begin with a limit of 1000 API calls a day, and 3 requests per call. 

My script uses a combination of the Contacts and Reporting APIs provided by Envoke. The `requests, os, json, pandas, datetime, dotenv, time, and numpy` modules were used in this script. The outputs (.csv) are as follows: 
- A list of active contacts based on consent status, updated daily
- Count of all active contacts on run date
- Messages sent on run date + associated metrics (Bounces, Clicks, Opens, Unsubscribes)

They are all fed into an Azure Data Lake and read into PowerBI for reporting purposes.

At the moment, filtering through + downloading contacts takes 25 minutes, as there are over 100,000 contacts, and the request is capped at 100 rows per page. My immediate next steps are to speed up its runtime by making 3 requests per call using `concurrent`, as well as adding a progress bar to the contact download process. 

# LinkedIn 

