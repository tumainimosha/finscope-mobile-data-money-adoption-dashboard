import joblib
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

from mm_adoption_visualization import mm_adoption_visualization
from mm_raw_data import mm_raw_data
from mm_model import mm_model
from EDA_Dashboard import eda_dashboard

# Load data
df = pd.read_csv('./data/FinScope Tanzania 2023_Individual Main Data_FINAL.csv')

df_mapping = pd.read_excel('./data/Individual Main Data_Datamap.xlsx')

best_model_name = 'Gradient Boosting'
preprocessor_filename = './models/preprocessor.joblib'
model_filename = f'./models/{best_model_name}.pkl'
model = joblib.load(model_filename)
preprocessor = joblib.load(preprocessor_filename)

with st.sidebar:
    selected = option_menu(
        menu_title='Main Menu',
        options=[
            'Data Analysis', 
            'Data Model',
            'Raw Data',
            ],
    )

if selected == 'Data Analysis':
    eda_dashboard(st, df)

elif selected == 'Data Model':
    mm_model(st, model, preprocessor)

elif selected == 'Raw Data':
    mm_raw_data(st, df, df_mapping)


        

    