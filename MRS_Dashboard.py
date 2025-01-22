# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 11:26:09 2024

@author: Muhammad Rasoul Sahibzadah
"""

# Import relevant libraries
import pandas as pd 
import numpy as np 
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime

# Set the page to wide mode
st.set_page_config(layout="wide")

# Define Functions 
def style_negative(v, props=''):
    """Style negative values in dataframe."""
    try:
        return props if v < 0 else None
    except:
        pass

def style_positive(v, props=''):
    """Style positive values in dataframe."""
    try:
        return props if v > 0 else None
    except:
        pass

def audience_simple(country):
    """Map country codes to country names."""
    return {'US': 'USA', 'IN': 'India'}.get(country, 'Other')

@st.cache_data 
def load_data():
    """Loads in 4 dataframes and performs light feature engineering."""
    df_agg = pd.read_csv('Aggregated_Metrics_By_Video.csv').iloc[1:, :]
    df_agg.columns = [
        'Video', 'Video title', 'Video publish time', 'Comments added', 
        'Shares', 'Dislikes', 'Likes', 'Subscribers lost', 'Subscribers gained', 
        'RPM(USD)', 'CPM(USD)', 'Average % viewed', 'Average view duration',
        'Views', 'Watch time (hours)', 'Subscribers', 
        'Your estimated revenue (USD)', 'Impressions', 'Impressions ctr(%)'
    ]
    
    # Date parsing
    df_agg['Video publish time'] = pd.to_datetime(df_agg['Video publish time'], errors='coerce')
    df_agg['Average view duration'] = pd.to_timedelta(df_agg['Average view duration'], errors='coerce')
    df_agg['Avg_duration_sec'] = df_agg['Average view duration'].dt.total_seconds()
    
    # Calculating engagement metrics
    df_agg['Engagement_ratio'] = (df_agg['Comments added'] + df_agg['Shares'] + df_agg['Dislikes'] + df_agg['Likes']) / df_agg['Views']
    df_agg['Views / sub gained'] = df_agg['Views'] / df_agg['Subscribers gained']
    df_agg.sort_values('Video publish time', ascending=False, inplace=True)
    
    # Load additional data
    df_agg_sub = pd.read_csv('Aggregated_Metrics_By_Country_And_Subscriber_Status.csv')
    df_comments = pd.read_csv('Aggregated_Metrics_By_Video.csv')
    df_time = pd.read_csv('Video_Performance_Over_Time.csv')
    df_time['Date'] = pd.to_datetime(df_time['Date'], errors='coerce')
    
    return df_agg, df_agg_sub, df_comments, df_time 

# Create dataframes from the function 
df_agg, df_agg_sub, df_comments, df_time = load_data()

# Additional data engineering for aggregated data 
df_agg_diff = df_agg.copy()
metric_date_12mo = df_agg_diff['Video publish time'].max() - pd.DateOffset(months=12)

# Select only numeric columns for median calculation
numeric_columns = df_agg_diff.select_dtypes(include=[np.number]).columns
median_agg = df_agg_diff[df_agg_diff['Video publish time'] >= metric_date_12mo][numeric_columns].median()

# Create differences from the median for values 
df_agg_diff[numeric_columns] = (df_agg_diff[numeric_columns] - median_agg).div(median_agg)

# Merge daily data with publish data to get delta 
df_time_diff = pd.merge(df_time, df_agg[['Video', 'Video publish time']], left_on='External Video ID', right_on='Video', how='left')
df_time_diff['days_published'] = (df_time_diff['Date'] - df_time_diff['Video publish time']).dt.days

# Get last 12 months of data rather than all data 
date_12mo = df_agg['Video publish time'].max() - pd.DateOffset(months=12)
df_time_diff_yr = df_time_diff[df_time_diff['Video publish time'] >= date_12mo]

# Get daily view data (first 30), median & percentiles 
views_days = pd.pivot_table(df_time_diff_yr, index='days_published', values='Views', 
                             aggfunc=[np.mean, np.median, lambda x: np.percentile(x, 80), lambda x: np.percentile(x, 20)]).reset_index()
views_days.columns = ['days_published', 'mean_views', 'median_views', '80pct_views', '20pct_views']
views_days = views_days[views_days['days_published'].between(0, 30)]
views_cumulative = views_days[['days_published', 'median_views', '80pct_views', '20pct_views']]
views_cumulative[['median_views', '80pct_views', '20pct_views']] = views_cumulative[['median_views', '80pct_views', '20pct_views']].cumsum()

###############################################################################
# Start building Streamlit App
###############################################################################

add_sidebar = st.sidebar.selectbox('Aggregate or Individual Video', ('Aggregate Metrics', 'Individual Video Analysis'))
# Social Links
linkedin = "https://raw.githubusercontent.com/rasoul1234/MRSL.Teck-Chatbot/main/img/linkedin.gif"
instagram = "https://raw.githubusercontent.com/rasoul1234/MRSL.Teck-Chatbot/main/img/topmate.gif"
email = "https://raw.githubusercontent.com/rasoul1234/MRSL.Teck-Chatbot/main/img/email.gif"
newsletter = "https://raw.githubusercontent.com/rasoul1234/MRSL.Teck-Chatbot/main/img/newsletter.gif"
share = "https://raw.githubusercontent.com/rasoul1234/MRSL.Teck-Chatbot/main/img/share.gif"

st.sidebar.caption(
    f"""
        <div style='display: flex; align-items: center;'>
            <a href='http://www.linkedin.com/in/muhammad-rasoul-sahibzadah-b97a47218/'><img src='{linkedin}' style='width: 35px; height: 35px; margin-right: 25px;'></a>
            <a href='https://www.instagram.com/rasoulsahibzadah/profilecard/?igsh=MXJiM3BxM2RyZ2prdA=='><img src='{instagram}' style='width: 32px; height: 32px; margin-right: 25px;'></a>
            <a href='mailto:rasoul.sahibbzadah@auaf.edu.af'><img src='{email}' style='width: 28px; height: 28px; margin-right: 25px;'></a>
            <a href='https://www.linkedin.com/build-relation/newsletter-follow?entityUrn=7163516439096733696'><img src='{newsletter}' style='width: 28px; height: 28px; margin-right: 25px;'></a>
            <a href='https://www.kaggle.com/mohammadrasoul'><img src='{share}' style='width: 28px; height: 28px; margin-right: 25px;'></a>
        </div>
        """,
    unsafe_allow_html=True,
)

# Add app description as a dropdown in the sidebar
with st.sidebar.expander("About the App", expanded=False):
    st.markdown(""" 
    Welcome to the YouTube Analytics Dashboard! This web application, developed using Streamlit, provides comprehensive insights into your YouTube channel's performance. Users can explore aggregate metrics such as views, likes, and engagement ratios, as well as conduct in-depth analysis of individual video performance, including subscriber engagement trends. With interactive visualizations powered by Plotly, you can easily compare metrics over time. The user-friendly interface allows seamless navigation between aggregate and individual video metrics, empowering content creators to enhance their understanding of audience engagement and optimize their content strategy effectively.
    """)

st.sidebar.markdown(
    """
    <div style="font-weight: bold; font-size: 16px; text-align: center; color: #333;">
        <span style="color: #28a745;">Developed by</span> 
        <a href="http://www.linkedin.com/in/muhammad-rasoul-sahibzadah-b97a47218/" style="color: #0077b5; text-decoration: underline;">Muhammad Rasoul</a>. 
        <span style="color: #ffcc00;">Like this?</span> 
        <a href="mailto:rasoul.sahibbzadah@auaf.edu.af" style="color: #d14836; text-decoration: underline;">Hire me!</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# Show individual metrics 
if add_sidebar == 'Aggregate Metrics':
    st.title("YouTube Aggregated Data APP")
    
    df_agg_metrics = df_agg[['Video publish time', 'Views', 'Likes', 'Subscribers', 'Shares', 'Comments added', 
                              'RPM(USD)', 'Average % viewed', 'Avg_duration_sec', 'Engagement_ratio', 'Views / sub gained']]
    
    metric_date_6mo = df_agg_metrics['Video publish time'].max() - pd.DateOffset(months=6)
    metric_date_12mo = df_agg_metrics['Video publish time'].max() - pd.DateOffset(months=12)
    
    metric_medians6mo = df_agg_metrics[df_agg_metrics['Video publish time'] >= metric_date_6mo].median()
    metric_medians12mo = df_agg_metrics[df_agg_metrics['Video publish time'] >= metric_date_12mo].median()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]
    
    count = 0
    for i in metric_medians6mo.index:
        with columns[count]:
            value_6mo = metric_medians6mo[i]
            value_12mo = metric_medians12mo[i]
            
            # Ensure both values are numeric
            if isinstance(value_6mo, (pd.Timestamp, pd.Timedelta)):
                value_6mo = value_6mo.timestamp()
            if isinstance(value_12mo, (pd.Timestamp, pd.Timedelta)):
                value_12mo = value_12mo.timestamp()
                
            # Calculate delta if both values are numeric
            if isinstance(value_6mo, (int, float)) and isinstance(value_12mo, (int, float)):
                delta = (value_6mo - value_12mo) / value_12mo if value_12mo != 0 else 0
                st.metric(label=i, value=round(value_6mo, 1), delta="{:.2%}".format(delta))
            else:
                st.metric(label=i, value=round(value_6mo, 1))  # Fallback if not numeric

            count += 1
            if count >= 5:
                count = 0

    # Get date information / trim to relevant data 
    df_agg_diff['Publish_date'] = df_agg_diff['Video publish time'].dt.date
    df_agg_diff_final = df_agg_diff[['Video title', 'Publish_date', 'Views', 'Likes', 'Subscribers', 
                                       'Shares', 'Comments added', 'RPM(USD)', 'Average % viewed', 
                                       'Avg_duration_sec', 'Engagement_ratio', 'Views / sub gained']]
    
    # Select only numeric columns for median calculation
    numeric_columns_final = df_agg_diff_final.select_dtypes(include=[np.number]).columns.tolist()
    df_agg_numeric_lst = numeric_columns_final  # Store numeric columns for further use
    df_to_pct = {i: '{:.1%}'.format for i in df_agg_numeric_lst}
    
    st.dataframe(df_agg_diff_final.style.hide()
                  .applymap(style_negative, props='color:red;')
                  .applymap(style_positive, props='color:green;')
                  .format(df_to_pct))

if add_sidebar == 'Individual Video Analysis':
    videos = tuple(df_agg['Video title'])
    st.write("Individual Video Performance")
    video_select = st.selectbox('Pick a Video:', videos)
    
    agg_filtered = df_agg[df_agg['Video title'] == video_select]
    agg_sub_filtered = df_agg_sub[df_agg_sub['Video Title'] == video_select]
    
    # Check if the filtered DataFrames are empty
    if agg_filtered.empty or agg_sub_filtered.empty:
        st.warning("No data available for the selected video.")
    else:
        agg_sub_filtered['Country'] = agg_sub_filtered['Country Code'].apply(audience_simple)
        agg_sub_filtered.sort_values('Is Subscribed', inplace=True)

        fig = px.bar(agg_sub_filtered, x='Views', y='Is Subscribed', color='Country', orientation='h')
        st.plotly_chart(fig)
        
        agg_time_filtered = df_time_diff[df_time_diff['Video Title'] == video_select]
        first_30 = agg_time_filtered[agg_time_filtered['days_published'].between(0, 30)]
        first_30 = first_30.sort_values('days_published')
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=views_cumulative['days_published'], y=views_cumulative['20pct_views'],
                                   mode='lines', name='20th percentile', line=dict(color='purple', dash='dash')))

        fig2.add_trace(go.Scatter(x=views_cumulative['days_published'], y=views_cumulative['median_views'],
                                   mode='lines', name='50th percentile', line=dict(color='black', dash='dash')))

        fig2.add_trace(go.Scatter(x=views_cumulative['days_published'], y=views_cumulative['80pct_views'],
                                   mode='lines', name='80th percentile', line=dict(color='royalblue', dash='dash')))

        fig2.add_trace(go.Scatter(x=first_30['days_published'], y=first_30['Views'].cumsum(),
                                   mode='lines', name='Current Video', line=dict(color='firebrick', width=8)))
        
        fig2.update_layout(title='View Comparison for First 30 Days',
                           xaxis_title='Days Since Published',
                           yaxis_title='Cumulative Views')
        
        st.plotly_chart(fig2)
