import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import preprocessing,helper
import plotly.figure_factory as ff


# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Olympics Analysis Dashboard",
    page_icon="🏅",
    layout="wide",
)

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
/* Dark Sidebar */
[data-testid="stSidebar"] {
    background-color: #1e1e1e !important;
}
[data-testid="stSidebar"] * {
    color: white !important;
}

/* Page background */
.main {
    background-color: #f7f7f7;
}

/* Headings */
h1, h2, h3 {
    font-family: 'Segoe UI', sans-serif;
    font-weight: 700;
    color: #333;
}

/* Statistic Cards */
.metric-card {
    padding: 18px;
    border-radius: 12px;
    background: white;
    box-shadow: 0px 3px 8px rgba(0,0,0,0.15);
    text-align: center;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)



df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")

df = preprocessing.preprocessing(df, region_df)

st.sidebar.image('Olympic.jpg')
st.sidebar.title("Olympics Analysis")
user_choice = st.sidebar.radio(
    "Select an Option",
    ("Medal Tally","Overall Analysis","Country-wise analysis","Athlete wise analysis")
)

if user_choice == "Medal Tally":
    Year,Country = helper.year_country(df)

    Selected_Country = st.sidebar.selectbox("Select Country",Country)
    Selected_Year = st.sidebar.selectbox("Select Year",Year)

    if Selected_Year == 'Overall' and Selected_Country == 'Overall':
        st.title("Overall Tally")
    if Selected_Year == 'Overall' and Selected_Country != 'Overall':
        st.title("Medal Tally in "+str(Selected_Country))
    if Selected_Year != 'Overall' and Selected_Country == 'Overall':
        st.title("Medal Tally in "+str(Selected_Year))
    if Selected_Year != 'Overall' and Selected_Country != 'Overall':
       st.title("Medal Tally of "+str(Selected_Country)+" in the year "+str(Selected_Year))

    medal_tally = helper.fetch_medal_tally(df,Selected_Year,Selected_Country)
    if isinstance(medal_tally,pd.DataFrame):
        st.table(medal_tally)
    else:
        st.header(medal_tally)

if user_choice == 'Overall Analysis':
    st.title("Top Statistics")

    filtered_years = df[df['Year'] != 1906]['Year']
    editions = filtered_years.unique().shape[0]
    cities = df['City'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    names = df['Name'].unique().shape[0]
    regions = df['region'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Events")
        st.title(events)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Countries")
        st.title(regions)
    with col2:
        st.header("Athletes")
        st.title(names)
    with col3:
        st.header("Sports")
        st.title(sports)
# just adding extra space
    st.markdown("<br><br>", unsafe_allow_html=True)
# plotting a graph
    no_of_country = helper.data_over_time(df,'region')
    st.title("No of Country over the Year")
    fig = px.line(no_of_country, x='Year', y='region',markers=True)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    st.plotly_chart(fig)

    no_of_events = helper.data_over_time(df,'Event')
    st.title("No of Events over the Year")
    fig = px.line(no_of_events, x='Year', y='Event',markers=True)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    st.plotly_chart(fig)

    no_of_athletes = helper.data_over_time(df,'Name')
    st.title("No of Athletes over the Year")
    fig = px.line(no_of_athletes, x='Year', y='Name',markers=True)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_layout(xaxis_title='Year' , yaxis_title='No of Athletes' )
    st.plotly_chart(fig)

    # No of Sports Over the year
    st.title("No of Sports' Event over the Year(Every Sport)")
    fig,ax = plt.subplots(figsize=(12,12))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    sns.heatmap(x.pivot_table(index='Sport', columns="Year", values='Event', aggfunc='count').fillna(0),ax = ax,annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sports = df['Sport'].sort_values().unique().tolist()
    sports.insert(0, "Overall")
    selected_sport = st.selectbox('Sports',sports)
    st.table(helper.most_successed(df,selected_sport))

if user_choice == 'Country-wise analysis':
    st.sidebar.subheader("Country wise Yearly Analysis")
    Country = df['region'].unique().tolist()
    Selected_Country = st.sidebar.selectbox("Select Country", Country)
    st.title("Yearly Analysis (Gold,Silver,Bronze) of "+Selected_Country)
    helper.medal_tally_yearly(df,Selected_Country)

    st.title("Excellence of "+Selected_Country+" in following sport(Total Medals)")
    temp_df = df.dropna(subset=['Medal'])
    temp_df['Total'] = temp_df['Gold'] + temp_df['Silver'] + temp_df['Bronze']
    temp_df = temp_df[temp_df['region'] == Selected_Country]
    if temp_df["Total"].empty:
        st.warning("No data found for heat map")
    else:
        helper.medal_tally_sport(temp_df,Selected_Country)

    st.title("Successful Athletes in "+Selected_Country)
    data = helper.most_successed_country(df,Selected_Country)
    st.table(data)

if user_choice == 'Athlete wise analysis':
    st.title("Distribution of Age")
    fig,ax = plt.subplots(figsize=(12,12))
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold medalist', 'Silver medalist', 'Bronze medalist'],
                       show_hist=False, show_rug=False)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_layout(xaxis_title='Age' , yaxis_title='Probability of Wining' )
    st.plotly_chart(fig)

    st.title("Participation of men and women over the year")
    fig, ax = plt.subplots(figsize=(12, 12))
    df = df.drop_duplicates(subset=['Name', 'region'])
    male = df[df['Sex'] == 'M'].groupby(['Year']).count()['Name'].reset_index()
    male.rename(columns={'Name': "Male"}, inplace=True)
    Female = df[df['Sex'] == 'F'].groupby(['Year']).count()['Name'].reset_index()
    Female.rename(columns={'Name': "Female"}, inplace=True)
    final_df = pd.merge(male, Female, left_on=['Year'], right_on=['Year'], how='left')
    final_df.fillna(0, inplace=True)
    fig = px.line(final_df, x='Year', y=['Male', 'Female'])
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

    st.plotly_chart(fig)



