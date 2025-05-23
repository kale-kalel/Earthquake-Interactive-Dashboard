import streamlit as st
import pandas as pd
import calendar
from statsmodels.nonparametric.smoothers_lowess import lowess
from function import *

# Displays highest magnitude and shallowest depth
def top_squares(info, msg):
    st.markdown(
        f'''
        <div style = '
            height: auto;
            width: 60%;
            background-color: #ECECEC;
            border-radius: 4px;
            text-align: center;
            display: flex;
            justify-content: center;
            flex-direction: column;
            '>
            <div style = '
                font-size: 24px;
                font-weight: 600;
            '>
                {info}
            </div>
            <span>{msg}</span>
        </div>
        ''',
        unsafe_allow_html = True
    )

# Fills in missing months
def month_filler(month_incomplete):
    full_months = pd.Series(
        0,
        index = range(1,13)
    )
    full_months.update(month_incomplete)
    full_months.index = full_months.index.map(lambda x: calendar.month_name[x])
    named_months = full_months.reset_index()
    named_months.columns = ['month', 'count']
    return named_months

# Fills in missing years
def year_filler(overtime_slider_min, overtime_slider_max, year_incomplete):
    full_year_series = pd.Series(
        0,
        range(overtime_slider_min, overtime_slider_max + 1)
    )
    full_year_df = full_year_series.to_frame('count').reset_index().rename(columns={'index': 'year'})
    merged = full_year_df.merge(year_incomplete, on='year', how='left')
    merged['count'] = merged['count_y'].fillna(merged['count_x']).astype(int)
    return merged[['year', 'count']]

# Earthquake overtime x axis values
def year_range_process(df, overtime_slider):
    overtime_slider_min, overtime_slider_max = overtime_slider

    if overtime_slider_min == overtime_slider_max:
        column_to_count = 'month'
        x_label = str(overtime_slider_min) + ', Months'
        filtered_df = df.loc[df['year'] == overtime_slider_min]
        overtime_counts = month_filler(filtered_df[column_to_count].value_counts())
    else:
        column_to_count = 'year'
        x_label = column_to_count.capitalize()
        filtered_df = df.loc[(df[column_to_count] >= overtime_slider_min) & (df[column_to_count] <= overtime_slider_max)]
        overtime_counts = filtered_df[column_to_count].value_counts().reset_index()
        filled_counts = year_filler(overtime_slider_min, overtime_slider_max, overtime_counts)
        overtime_counts = filled_counts.sort_values(ascending = True, by = column_to_count)
            
    return x_label, column_to_count, overtime_counts, filtered_df

# Determines the ordering of magnitude and depth category
def earthquake_parameters_category(parameter_scale):
    st.markdown(parameter_scale)
    ordering = st.selectbox(
                'Order by:',
                ('Increasing', 'Decreasing', parameter_scale),
                index = 1
            )
    return ordering

# Returns the ordering of magnitude and depth category
def category_order_by(df, parameter_category, ordering):
    match ordering:
        case 'Increasing':
            return df[parameter_category].value_counts().sort_values(ascending = True)
        case 'Decreasing':
            return df[parameter_category].value_counts().sort_values(ascending = False)
        case _:
            return df[parameter_category].sort_values().value_counts(sort = False)
        
# Number of earthquakes per category expressed in percentage
def earthquake_parameters_pct(df, parameter_category, ordering):
    info_earthquake_parameter = category_order_by(df, parameter_category, ordering)
    total = info_earthquake_parameter.sum()
    
    for category, count in info_earthquake_parameter.items():
        pct = int((count / total) * 100)

        # Visual purposes
        if pct == 0:
            pct = 1
        if count == 0:
            pct = 0
            
        st.text(f'{category} [{count:,}]')
        st.progress(pct)