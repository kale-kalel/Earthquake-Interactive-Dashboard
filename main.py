# Modules and file
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from statsmodels.nonparametric.smoothers_lowess import lowess
from function import *
with open('styles.css') as style:
   st.markdown(
       f'<style>{style.read()}</style>',
       unsafe_allow_html = True
    )

# Drop down file uploader
with st.expander('Upload a file [.csv]'):
    file_upload = st.file_uploader(
        'Choose a CSV file',
        type = 'csv'
    )

# File upload
if not file_upload: 
    st.error(
        'Please upload a file\n\n' \
        'File requirements:\n\n' \
        '1. Necessary columns: date, time, latitude, longitude, depth, magnitude\n' \
        '2. Possible additional columns: year, month\n' \
        '3. No Nan values'
    )
    
else:
    df = pd.read_csv(file_upload)

    # Adds year, month column
    df['date'] = pd.to_datetime(df['date'])

    if 'year' not in df.columns:
        df['year'] = df['date'].dt.year
    if 'month' not in df.columns:
        df['month'] = df['date'].dt.month
    
    # Sidebar
    with st.sidebar:
        st.title('Earthquake Dashboard')
        st.markdown('Year Range')

        # Determines the availability of the slider
        if len(df['year'].unique()) == 1:
            st.text('* Disabled *')
            column_to_count = 'month'
            x_label = str(df['year'].unique()[0]) + ', Months'
            overtime_counts = month_filler(df['month'].value_counts())
            ranged_df = df
        else:
            slider_counts = df['year'].value_counts().reset_index().sort_values(by='year', ascending = True)
            available_years = slider_counts['year'].tolist()
            overtime_slider = st.select_slider(
            'Select the same year to view months',
            options=available_years,
            value=(available_years[0], available_years[-1])
            )
            # Year slider
            x_label, column_to_count, overtime_counts, ranged_df = year_range_process(df, overtime_slider)

        # X ticks options
        st.markdown('X Ticks')

        # Determines the availability of the options
        if column_to_count == 'year':
            earthquakes_overtime_x_ticks_input = st.number_input(
                'Intervals',
                min_value = 1,
                max_value = overtime_counts[column_to_count].shape[0] ,
                step = 1
            )
            sorted_ticks = sorted(overtime_counts[column_to_count].unique())
            interval_ticks = sorted_ticks[::earthquakes_overtime_x_ticks_input]
        else:
            st.text('* Disabled *')
            interval_ticks = overtime_counts[column_to_count]

        # Magnitude categories
        magnitude_category_ordering = earthquake_parameters_category('Earthquake Scale')

        # Depth categories
        depth_category_ordering = earthquake_parameters_category('Depth Scale')

    # Column layout
    col_mid, col_right = st.columns([2.5,1])

    # Middle column
    with col_mid:
        # Row layout
        col_mid_first_row_left, col_mid_first_row_right = st.columns([1,1])
        col_mid_sec_row = st.columns(1)
        col_mid_third_row = st.columns(1)

        # First row
        # Peak values
        mag_info = ranged_df['magnitude'].max()
        mag_msg = 'Highest Magnitude'
        depth_info = ranged_df['depth'].min()
        depth_msg = 'Shallowest Depth'

        with col_mid_first_row_left:
            top_squares(mag_info, mag_msg)

        with col_mid_first_row_right:
            top_squares(depth_info, depth_msg)

        # Second row    
        with col_mid_sec_row[0]:
            # Viusal purposes
            st.markdown(
                '''
                    <div style = 'padding: 3%;'></div>
                ''', 
                unsafe_allow_html = True
            )

            # Line plot
            st.subheader('Earthquakes Overtime')
            fig1, ax1 = plt.subplots(
                figsize = (8, 3)
                )
            sns.lineplot(
                data=overtime_counts,
                x = overtime_counts[column_to_count],
                y = overtime_counts['count'],
                color = '#FF4B4B',
            )
            ax1.set_ylabel(
                'Count',
                size = 8
            )
            ax1.set_xlabel(
                x_label,
                size = 8
            )
            ax1.set_xticks(
                interval_ticks
            )
            ax1.set_xticklabels(
                interval_ticks,
                rotation = 45
            )
            ax1.tick_params(
                axis = 'both',
                labelsize = 6
            )
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            fig1.subplots_adjust(bottom = 0.05)
            st.pyplot(fig1)

        # 3rd row
        with col_mid_third_row[0]:
            st.subheader('Earthquakes Map')
            plotted_map = px.density_map(
                data_frame = ranged_df,
                lat = ranged_df['latitude'],
                lon = ranged_df['longitude'],
                opacity = 1,
                radius = 10,
                color_continuous_scale = ['#FFB98C', '#FF4B4B']
            )
            plotted_map.update_layout(
                width = 700,
                height = 300,
                margin = dict(l = 0, r = 0, t = 0, b = 0),
                coloraxis_colorbar = dict(
                    title = 'Density',
                    title_font = dict(size = 12),
                    showticklabels = False
                )
            )
            st.plotly_chart(plotted_map)

    # Right column
    with col_right:
        # Row layout
        col_right_first_row = st.columns(1)
        col_right_sec_row = st.columns(1)

        # First row
        with col_right_first_row[0]:
            st.subheader('Magnitude Category')
            magnitude_cutoff = [0, 2.9, 3.9, 4.9, 5.9, 6.9, 7.9, 10]
            magnitude_categories = ['Micro', 'Minor', 'Light', 'Moderate', 'Strong', 'Major', 'Great']
            ranged_df['magnitude category'] = pd.cut(
                ranged_df['magnitude'],
                bins = magnitude_cutoff,
                labels = magnitude_categories,
                right = True,
                include_lowest = True
            )
            ranged_df['magnitude category'] = pd.Categorical(
                ranged_df['magnitude category'],
                categories = magnitude_categories,
                ordered = True
            )
            earthquake_parameters_pct(ranged_df, 'magnitude category', magnitude_category_ordering)

        # 2nd row
        with col_right_sec_row[0]:
            st.subheader('Depth Category')
            depth_cutoff = [0, 70, 300, 1000]
            depth_categories = ['Shallow', 'Intermediate', 'Deep']
            ranged_df['depth category'] = pd.cut(
                ranged_df['depth'],
                bins = depth_cutoff,
                labels = depth_categories,
                right = True,
                include_lowest = True
            )
            ranged_df['depth category'] = pd.Categorical(
                ranged_df['depth category'],
                categories = depth_categories,
                ordered = True
            )
            earthquake_parameters_pct(ranged_df, 'depth category', depth_category_ordering)
