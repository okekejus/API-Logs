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


Outputs are read into PowerBI using the Azure Blob connection, and then concatenated into one cohesive dataset for use within the report. 

# Envoke 
# LinkedIn 
# REDCap
