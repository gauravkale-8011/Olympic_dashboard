import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def fetch_medal_tally(df, year, Country):
    flag = 0
    medal_tally = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])

    if year == 'Overall' and Country == 'Overall':
        temp_df = medal_tally
    if year == 'Overall' and Country != 'Overall':
        flag = 1
        temp_df = medal_tally[medal_tally['region'] == Country]
    if year != 'Overall' and Country == 'Overall':
        temp_df = medal_tally[medal_tally['Year'] == year]
    if year != 'Overall' and Country != 'Overall':
        temp_df = medal_tally[(medal_tally['Year'] == year) & (medal_tally['region'] == Country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver','Bronze']].reset_index().sort_values("Year",
                                                                                                  ascending=True)
        x = x.reset_index(drop=True)
        if x.empty:
            x = 'No medals Win'
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver','Bronze']].reset_index().sort_values("Gold",
                                                                                                    ascending=False)
        x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
        x = x.reset_index(drop=True)
        if x['Gold'].sum() + x['Silver'].sum() + x['Bronze'].sum() == 0:
            x =  pd.DataFrame()
        if x.empty:
            x = 'No medals Win'
    return x

def year_country(df):
    year = df['Year'].unique().tolist()
    year.sort()
    year.insert(0, 'Overall')
    Country = df['region'].dropna().unique().tolist()
    Country.sort()
    Country.insert(0, 'Overall')
    return year,Country

def data_over_time(df,col):
    data = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    data.rename(columns={'count': col}, inplace=True)
    return data

def most_successed(df, sport):
    temp_df = df.dropna(subset = ['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df,left_on = 'Name' , right_on = 'Name' , how = 'left')[['Name','count','Sport','region']].drop_duplicates()
    x.rename(columns={'count':"Medals"},inplace=True)
    x = x.reset_index(drop=True)
    return x


def medal_tally_yearly(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal']).groupby(
        ['region', 'Year'])[['Gold', 'Bronze', 'Silver']].sum().reset_index()
    temp_country = temp_df[temp_df['region'] == country]

    if temp_country['Gold'].sum() == 0:
        st.warning("No Gold medals won")
    else:
        fig = px.line(temp_country, x='Year', y='Gold')
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        st.plotly_chart(fig)

    if temp_country['Silver'].sum() == 0:
        st.warning("No Silver medals won")
    else:
        fig = px.line(temp_country, x='Year', y='Silver')
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        st.plotly_chart(fig)

    if temp_country['Bronze'].sum() == 0:
        st.warning("No Bronze medals won")
    else:
        fig = px.line(temp_country, x='Year', y='Bronze')
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        st.plotly_chart(fig)

def medal_tally_sport(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df['Total'] = temp_df['Gold'] + temp_df['Silver'] + temp_df['Bronze']
    temp_df = temp_df[temp_df['region'] == country]
    temp_df = temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal']).groupby(['Sport','Year'])['Total'].sum()
    fig,ax = plt.subplots(figsize=(12,12))
    sns.heatmap(temp_df.reset_index().pivot_table(index = 'Sport' , columns = 'Year' , values = 'Total',aggfunc = 'count' ).fillna(0).astype(int),annot = True)
    st.pyplot(fig)

def most_successed_country(df,country):
    temp_df = df.dropna(subset = ['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df,left_on = 'Name' , right_on = 'Name' , how = 'left')[['Name','count','Sport']].drop_duplicates()
    x.rename(columns={'count':"Medals"},inplace=True)
    x = x.reset_index(drop=True)
    return x