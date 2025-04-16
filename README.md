# API Logs
A repository for code used to interact with APIs from various data sources. These are mainly code snippets from previous/ongoing work projects. Over time I expect to revisit these, and would like to improve my work in the process.

APIs used are listed below. Majority of these are written in python, with the exception of the [REDCap API](https://project-redcap.org/), which is something I saved from my time working with the [Ontario Birth Study](https://ontariobirthstudy.com/). 

None of the data collected using these scripts belongs to me, so I will be unable to share any of the datasets associated with the files.

# Google Analytics 
# Meta (Instagram/Facebook) 

I used this API as part of a data pipeline when creating a report for my current organization's Communications Team. To interact with it, I had to create an app using Meta's Developer platform, and register the *Instagram* and *Facebook Login for Business* products to the app. These granted access to Instagram and Facebook data respectively. Business verification was required to use these services at no extra cost.

The Instagram connection was fairly straight forward to set up, making use of the `requests, pandas, json, os, dotenv, dateteime` modules in python. The script is set up to feed into an Azure Data Lake, as a result, it produces one row of output (.csv) a day, detailing: 
- Total Followers
- Total Following
- Total Posts
- Run Date


Outputs are read into PowerBI using the Azure Blob connection, and then concatenated into one cohesive dataset for use within the report. 

# Envoke 
[Envoke](https://envoke.com/) is a platform for sending optional and mandatory emails to stakeholders and members of an organization. It is used frequently by my current employer to contact various individuals on various topics. Envoke provides business accounts with an API at no additional cost. Users begin with a limit of 1000 API calls a day, and 3 requests per call. 

My script uses a combination of the Contacts and Reporting APIs provided by Envoke. They were used to gather a list of currently active subscribers, a daily count of said subscribers, and metrics related to messages sent out on a given day. The `requests, os, json, pandas, datetime, dotenv, time, and numpy` modules were used in this script. 

At the moment, filtering through + downloading contacts takes 25 minutes, as there are over 100,000 contacts, and the request is capped at 100 rows per page. My immediate next steps are to speed up its runtime by making 3 requests per call using `concurrent`, as well as adding a progress bar to the contact download process. 
# LinkedIn 
# REDCap
