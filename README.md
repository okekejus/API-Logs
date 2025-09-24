# API Logs
A repository for API pulls I have done for various work projects. Each one is built to reflect a different business need, and those needs will be described in their respective sections below. 

# Meta (Instagram/Facebook) 

I used this API as part of a data pipeline when creating a report for my current organization's Communications Team. To interact with it, I had to create an app using Meta's Developer platform, and register the *Instagram* and *Facebook Login for Business* products to the app. These granted access to Instagram and Facebook data respectively. Business verification was required to use these services at no extra cost.

The Instagram connection was fairly straight forward to set up, making use of the `requests, pandas, json, os, dotenv, dateteime` modules in python. The script is set up to feed into an Azure Data Lake, as a result, it produces one row of output (.csv) a day, detailing: 
- Total Followers
- Total Following
- Total Posts
- Run Date


Outputs are fed into PowerBI using the Azure Blob connection, and then concatenated into one cohesive dataset for reporting purposes. The Facebook interaction is a work in progress - additional verification is required before scope access can be granted. I am currently working on acquiring said verification for my workplace. 

# Google Analytics 
Google Analytics is a very popular web analytics service offered by Google. It is used to track/report website and mobile app traffic and events. There are reporting options available within Google Analytics, but the storage options are restricted to a 12 month period (anything older is deleted). As a result, there was a need for automated extraction and storage of data before its deletion. 

The script makes use of the `os, pandas, datetime, dotenv, google.analytics.data_v1beta, google.auth` modules. Google Analytics groups its information into Metrics and Dimensions. Each request will contain specific combinations of the two, and the associated values for a specified project will be returned. The specific metrics and dimensions can be viewed within the file. 

The output is fed into an Azure Data Lake. Script is run daily, monthly, quarterly and annually, as specific metrics (Unique Users) will differ based on the time frames used in the request. If I access the website once today, and once tomorrow, I will be counted as a unique user each day. If I request data for this month however, I will be counted only once. 

# Envoke 
[Envoke](https://envoke.com/) is a platform for sending optional and mandatory emails to stakeholders and members of an organization. It is used frequently by my current employer to contact various individuals on various topics. Envoke provides business accounts with an API at no additional cost. Users begin with a limit of 1000 API calls a day, and 3 requests per call. 

The request was to create a tool that sends out emails to contacts from a list that is updated weekly. The [envoke.py](https://github.com/okekejus/API-Logs/blob/main/envoke.py) script takes this list of contacts, filters out repetitions (users only need to get the email once), and sends out an email with the survey link. 

It is run using an Azure pipeline, set for excecution every Friday. 


# Next Steps 
Implementation of "concurrent" module. 


