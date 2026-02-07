import pandas as pd

def preprocessing(df,region_df):
    #filterning only for summer
    df = df[df['Season'] == 'Summer']
    # merge with region_df
    df = df.merge(region_df, on='NOC', how='left')
    #drop duplicates value
    df.drop_duplicates(inplace=True)
    # one hot encoding medals
    df = pd.concat([df, pd.get_dummies(df['Medal']).astype(int)], axis=1)
    return df
