import os
import pandas as pd

### WORK IN PROGRESS ###
#trying to get analytics master and FL master and combine the two

def update_FL_master():
    pass

# TODO add functionality to delete files after updating master
def update_analytics_master(create=False):
    if create==True:
        # Creating blank master dataframe
        master_df = pd.DataFrame()
    else:
        # Reading master dataframe
        master_df = pd.read_csv('analytics_master.csv', index_col='Date')

    # Concatenating each file in New_analytics_data to master
    for file in os.listdir('New_analytics_data'):
        path = 'New_analytics_data/'+file
        df = pd.read_csv(path, index_col='Date')
        df.index = pd.to_datetime(df.index)
        master_df = pd.concat([master_df, df])
    
    # Dropping irrelevant columns
    drop_columns = []
    for column in master_df.columns:
        if column[:8] == 'promoted':
            drop_columns.append(column)
    master_df.drop(drop_columns, axis='columns', inplace=True)

    # Sorting by date
    master_df = master_df.sort_index()

    # Saving file
    master_df.to_csv('analytics_master.csv')


############################
## Getting new FL data in ##
############################

# TODO Need to change day/date issue

def standardize_date_format(date):
    date = date.replace('-','/')
    day, month, year = date.split('/')
    date = '{}/{}/{}'.format(month,day,year)
    return date

# Read data
df = pd.read_csv('FL_data.csv')

# Cleaning / formatting data
df = df.dropna()
df['Gains/Follow'] = df.Gains/df.Follows
df['Date'] = df.Day.apply(standardize_date_format)
df['Date'] = pd.to_datetime(df.Date, infer_datetime_format=True)
df.drop(['Day'], axis='columns', inplace=True)
df = df.set_index('Date')
rename = {'Follows':'FL_follows',
            'Unfollows':'FL_unfollows',
            'Tweets':'FL_tweets',
            'Replies':'FL_replies',
            'Retweets':'FL_retweets',
            'Likes':'FL_likes',
            'Unlikes':'FL_unlikes',
            'DMs':'FL_DMs'}
df.rename(rename, axis='columns', inplace=True)


