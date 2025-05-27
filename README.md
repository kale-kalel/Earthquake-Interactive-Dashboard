# Earthquake Interactive Dashboard
## Overview
This project aims to demonstrate data visualization techniques by presenting meaningful insights from earthquake data through an interactive dashboard. The dataset used can be found on Kaggle, [Earthquake Occurrence](https://www.kaggle.com/datasets/greegtitan/indonesia-earthquake-data)

# Instructions & Information
## File Input Requirements
  1. Necessary columns: date, time, latitude, longitude, depth, magnitude
  2. Possible additional columns: year, month
  3. No Nan values

## Additional Information
  * Set streamlit theme to light mode for better experience
  * The slide bar controls the year range for all charts / plots
  * Slider bar and tick controls are disabled for month view
  * Additional columns will serve as the basis for analysis (e.g., the year column will be utilized instead of extracting the year from the date column)
  * Additional sample datasets are provided to demonstrate the dashboard's features
      - dataset_1.csv contains all necessary columns
      - dataset_2.csv contains data that occured within a year
      - dataset_3.csv contains an additional column (year)

## Data Visualization Techniques
  1. Matplotlib, Seaborn, Plotly are utilized
  2. Demonstrated the use of line graph, map plot, and progress bars

## Tools Used
  1. Python
  2. CSS
  3. Streamlit
  4. Pandas
  5. Numpy
  6. Matplotlib
  7. Seaborn
  8. Plotly Express
  9. Statsmodel (lowess)
  10. Function
