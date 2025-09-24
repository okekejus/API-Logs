# Standard modules 
import os 
import pandas as pd 
import sys 
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from datetime import date
import numpy as np
import time 

# Analytics modules
from google.analytics.data_v1beta import BetaAnalyticsDataClient, GetMetadataRequest, Filter, FilterExpression
from google.analytics.data_v1beta import DateRange, Metric, Dimension, RunReportRequest
from google.auth.transport.requests import Request, AuthorizedSession
import math

# Progress bar, can likely be removed for azure
from tqdm import tqdm

def views_fetch(day, property_id):  
    """ Fetches page view metrics for Guided Steps forms, Hosted on Adobe Forms. Differentiated on GA using the property_id."""
    with requests.Session() as session:  
        client = BetaAnalyticsDataClient() 
        date_range = DateRange(start_date=day, end_date=day)
        limit = 250000
        offset = 0
        dimensions = [Dimension(name='pageTitle'), Dimension(name='pageLocation')]
        data = []
        metrics = [Metric(name='screenPageViews'), 
                Metric(name="totalUsers"), 
                Metric(name="activeUsers"), 
                Metric(name="screenPageViewsPerUser"), 
                Metric(name="averageSessionDuration"), 
                Metric(name="sessionsPerUser"),
                Metric(name="screenPageViewsPerSession"),
                Metric(name="newUsers"), 
                Metric(name="sessions")]
        request = RunReportRequest(
                property=f"properties/{property_id}",
                date_ranges=[date_range],
                metrics=metrics,
                dimensions=dimensions,
                limit = limit, 
                offset = 0)
        response = client.run_report(request)

        for row in response.rows:
            row_data = {}
            for i, dimension in enumerate(row.dimension_values):
                row_data[dimensions[i].name] = dimension.value
            for i, metric in enumerate(row.metric_values):
                row_data[metrics[i].name] = metric.value
            data.append(row_data)
            
        total_rows = response.row_count 
        if total_rows > limit: 
            addon = []
            reps = ((total_rows - limit)/limit)
            iterations = math.ceil(reps)

            for i in tqdm(range(iterations), desc="Downloading..."): # Can be removed, only needed for progress when run in person
                offset = offset + limit

                request = RunReportRequest(
                property=f"properties/{property_id}",
                date_ranges=[date_range],
                metrics=metrics,
                #dimensions=dimensions,
                limit = limit, 
                offset = offset)

                response = client.run_report(request)

                for row in response.rows:
                    row_data = {}
                    for i, dimension in enumerate(row.dimension_values):
                        row_data[dimensions[i].name] = dimension.value
                    for i, metric in enumerate(row.metric_values):
                        row_data[metrics[i].name] = metric.value
                    addon.append(row_data)

            results_df = pd.concat([pd.DataFrame(data), pd.DataFrame(addon)])
        else: 
            results_df = pd.DataFrame(data)
        session.close()
        results_df['date'] = day
        results_df.to_parquet(f"forms_extract_{day}.gzip", index=False)
        print(f"forms_extract_{day}.gzip saved.") 


def downloads_fetch(day, property_id):
    """Fetches Download Data for the delegated forms."""
    with requests.Session() as session: 
        client = BetaAnalyticsDataClient() 
        date_range = DateRange(start_date=day, end_date=day)
        limit = 250000
        offset = 0
        dimensions = [Dimension(name='pageTitle'), Dimension(name="eventName"), Dimension(name="pageLocation")]
        data = []
        metrics = [Metric(name='screenPageViews'), 
                Metric(name="totalUsers"), 
                Metric(name="activeUsers"), 
                Metric(name="screenPageViewsPerUser"), 
                Metric(name="averageSessionDuration"), 
                Metric(name="sessionsPerUser"),
                Metric(name="screenPageViewsPerSession"),
                Metric(name="newUsers"), 
                Metric(name="sessions")]
        request = RunReportRequest(
                property=f"properties/{property_id}",
                date_ranges=[date_range],
                metrics=metrics,
                dimensions=dimensions,
                limit = limit, 
                offset = 0,
                dimension_filter=FilterExpression(filter=Filter(field_name="eventName", in_list_filter=Filter.InListFilter(values=["cao_form_download_event", "form_submit"]))))
        response = client.run_report(request)

        for row in response.rows:
            row_data = {}
            for i, dimension in enumerate(row.dimension_values):
                row_data[dimensions[i].name] = dimension.value
            for i, metric in enumerate(row.metric_values):
                row_data[metrics[i].name] = metric.value
            data.append(row_data)
            
        total_rows = response.row_count 
        if total_rows > limit: 
            addon = []
            reps = ((total_rows - limit)/limit)
            iterations = math.ceil(reps)

            for i in tqdm(range(iterations), desc="Downloading..."): # Can be removed, only needed for progress when run in person
                offset = offset + limit

                request = RunReportRequest(
                property=f"properties/{property_id}",
                date_ranges=[date_range],
                metrics=metrics,
                #dimensions=dimensions,
                limit = limit, 
                offset = offset)

                response = client.run_report(request)

                for row in response.rows:
                    row_data = {}
                    for i, dimension in enumerate(row.dimension_values):
                        row_data[dimensions[i].name] = dimension.value
                    for i, metric in enumerate(row.metric_values):
                        row_data[metrics[i].name] = metric.value
                    addon.append(row_data)

            results_df2 = pd.concat([pd.DataFrame(data), pd.DataFrame(addon)])
        else: 
            results_df2 = pd.DataFrame(data)
        session.close()
        results_df2['date'] = day
        results_df2.to_parquet(f"forms_download_{day}.gzip", index=False)
        print(f"forms_download_{day}.gzip saved.")

def main(day, property_id): 
    views_fetch(day, property_id)
    time.sleep(0.25)
    downloads_fetch(day, property_id)
    
if __name__ == "__main__": 
    day = datetime.today().date().strftime("%Y-%m-%d")
    property_id = "PROPERTY_ID"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "CREDENTIALS.json"
    main(day, property_id)



