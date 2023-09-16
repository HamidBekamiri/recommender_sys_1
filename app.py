# Import Libraries
import streamlit as st
import pandas as pd
from sklearn.impute import KNNImputer
from math import radians, sin, cos, sqrt, asin
import numpy as np

# Load Data
@st.cache
def load_data():
    df = pd.read_csv('path/to/your/trips.csv')
    return df

# Haversine Distance Function
def haversine_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371.0
    distance = r * c
    return distance

# Main App
st.title('Trip Recommender and Planner')

# Load the dataset
df = load_data()

# User Input for Trip Planner
st.subheader('Plan Your Trip')
budget = st.number_input("Enter your budget for the trip ($):", min_value=0, max_value=10000, value=2000)
trip_duration = st.number_input("Enter the desired trip duration (in days):", min_value=1, max_value=30, value=10)
preferred_place = st.text_input("Enter your preferred destination (optional):", "")

# Average cost per day (for demonstration)
average_cost_per_day = {
    'London': 150,
    'New York City': 200,
    'Berlin': 100,
    'Bangkok': 50,
    'Chiang Mai': 40
}

# Recommend places based on budget and duration
if st.button('Find My Trip!'):
    recommended_places = []
    
    if preferred_place in average_cost_per_day.keys():
        cost_for_preferred_place = average_cost_per_day[preferred_place]
        if cost_for_preferred_place * trip_duration <= budget:
            recommended_places.append({
                'Place': preferred_place,
                'Estimated Cost': cost_for_preferred_place * trip_duration,
                'Estimated Duration': trip_duration
            })
            budget -= cost_for_preferred_place * trip_duration
            trip_duration = 0  # Reset the remaining duration
    
    for place, cost_per_day in average_cost_per_day.items():
        if place == preferred_place:
            continue
        if cost_per_day * trip_duration <= budget:
            recommended_places.append({
                'Place': place,
                'Estimated Cost': cost_per_day * trip_duration,
                'Estimated Duration': trip_duration
            })
            budget -= cost_per_day * trip_duration
            break  # We've used up the user's available time
            
    if recommended_places:
        st.table(pd.DataFrame(recommended_places))
    else:
        st.warning('No trips could be found within the specified budget and duration.')
