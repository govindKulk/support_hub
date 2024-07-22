import pandas as pd

def preprocess(df):
    print("Preprocessing data")


    cols = ['Symbol', 'Name', 'Period', 'EPS', 'Estimated EPS', 'Surprise % EPS', 'Revenue', 'Estimated Revenue', 'Surprise % Revenue', 'Date Announced']
    req_df = df[cols]
    req_df.rename(columns={'Symbol': 'TIKR'}, inplace=True)
    req_df.to_csv('bz.csv')