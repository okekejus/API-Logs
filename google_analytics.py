
# Standard modules 
import os 
import pandas as pd 
import sys 
from datetime import datetime, timedelta
from dotenv import load_dotenv, dotenv_values

# Analytics modules
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta import DateRange, Metric, Dimension, RunReportRequest
from google.auth.transport.requests import Request 



# important metrics
report_date = datetime.today().date() - timedelta(days=1) 

# Clients accepts yesterday as a prompt, so will use this - set the report to run once a day at like 12:01 AM - gathering the previous day's worth of reporting. 
load_dotenv()
starting_date = 'yyyy-mm-dd'
ending_date = 'yyyy-mm-dd'
property_id = os.getenv('PROPERTY_ID')

# relevant authentication details
def get_metrics(starting_date, ending_date):
    
    client = BetaAnalyticsDataClient()
    date_range = DateRange(start_date=starting_date, end_date=ending_date)
    offset = 0 

    metrics = [Metric(name='sessions'), 
               Metric(name='activeUsers'), 
               Metric(name='userEngagementDuration'), 
               Metric(name='totalUsers'), 
               Metric(name='scrolledUsers'), 
               Metric(name='screenPageViewsPerUser'), 
               Metric(name='bounceRate'), 
               Metric(name='eventCount')
               ] # need to set this up as list to be entered 

    dimensions = [Dimension(name='eventName'), 
                  Dimension(name='country'), 
                  Dimension(name='city'), 
                  Dimension(name='pageTitle'), 
                  Dimension(name='PageLocation'), 
                  Dimension(name='date'), 
                  Dimension(name='percentScrolled'), 
                  Dimension(name='platformDeviceCategory'),
                  Dimension(name='browser')]


    # submit request 
    request = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[date_range],
            metrics=metrics,
            dimensions=dimensions,
            limit = 250000, 
            offset = 0)
    
        # Run the report
    response = client.run_report(request)
    
    
    data = []
    
    for row in response.rows:
        row_data = {}
        for i, dimension in enumerate(row.dimension_values):
            row_data[dimensions[i].name] = dimension.value
        for i, metric in enumerate(row.metric_values):
            row_data[metrics[i].name] = metric.value
        data.append(row_data)
        

    total_rows = response.row_count
    
    if total_rows > 250000: 
        addon = []
        reps = ((total_rows - 250000)/250000)
        iterations = math.ceil(reps)
    
        for i in tqdm(range(iterations), desc="Downloading..."): 
            offset = offset + 250000
            print
    
            request = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[date_range],
            metrics=metrics,
            dimensions=dimensions,
            limit = 250000, 
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

    # Correcting date format    
    results_df['date'] = results_df['date'].apply(lambda x: datetime.strptime(x, '%Y%m%d').date().strftime('%Y-%m-%d'))
    results_df.columns = ['event_name', 'country', 'city', 'page_title', 'page_location', 'date', 'percent_scrolled', 'platform_device', 'browser', 'sessions', 'active_users', 'user_engagement_duration', 'total_users', 
                          'scrolled_users', 'screen_page_views_per_user', 'bounce_rate', 'event_count']
    results_df.sort_values('date', ascending=True, inplace=True)
        # Resetting index
    results_df.reset_index(drop=True, inplace=True)
    
    dtypes = {'sessions': 'int', 
              'active_users': 'int', 
              'user_engagement_duration': 'int', 
              'total_users': 'int',
              'scrolled_users': 'int',
              'screen_page_views_per_user': 'float',
              'bounce_rate': 'float',
              'event_count': 'int'}
        # changing types 
    results_df = results_df.astype(dtypes)
    
    return results_df

    

def main(): 
    results = get_metrics(starting_date, ending_date)
    results.to_csv(f'data/website_data_{report_date}.csv', index=False)

if __name__ == "__main__": 
    main()
