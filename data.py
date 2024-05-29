import streamlit as st
import pandas as pd 
import plotly.express as px
import numpy as np
from streamlit_extras.metric_cards import style_metric_cards

st.set_page_config(page_title="LIFESCAN ", page_icon="📈", layout="wide")
st.title('MAY MONTH LIFESCAN EDA')
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

df=pd.read_excel('DOB DSR FORMAT (4).xlsx', sheet_name='DSR')


with st.expander("view datasheet"):
    st.dataframe(df.head(5),use_container_width=True)


# Multi-select for filtering categories

prity_id = st.sidebar.multiselect(
    'Select  PRTIY ID',
    options=df['Sold To'].unique(),
    default=df['Sold To'].unique()[:2]
)

filtered_df = df[(df['Sold To'].isin(prity_id))]

total_sale=filtered_df['Extended Amount'].sum()
avg_sale=filtered_df['Extended Amount'].mean()
total_unit=filtered_df['Quantity'].sum()

profit_percentage = 9
profit = total_sale * (profit_percentage / 100)

# Calculate profit divided by 635
profit_per_635 = profit / 635

#create columns with metric
col1, col2, col3,col4 = st.columns(4)
with col1:
  st.info('TOTAL SALE', icon="📈")
  st.metric("INR", value=round(filtered_df['Extended Amount'].sum()))
with col2:
  st.info('AVG SALE', icon="📈")
  st.metric("INR", value=round(filtered_df['Extended Amount'].mean())) 

with col3:
  st.info('TOTAL UNITS', icon="📈")
  st.metric("INR", value=round(filtered_df['Quantity'].sum()))  

with col4:
  st.info('TOTAL METER', icon="📈")
  st.metric("NO", f"{profit_per_635:,.2f}")  
style_metric_cards(background_color='green')


# CREATE BAR CHART
total_sales = filtered_df.groupby('Description 1')['Quantity'].count().reset_index()

# Create a bar chart using Plotly Express
st.info('TOTAL SALE BY PRODUCT', icon='📊',)

fig = px.bar(total_sales, x='Description 1', y='Quantity')

# Display the chart using Streamlit

st.plotly_chart(fig, use_container_width=True)

# lice chart with
st.info('Dealer by Total Units', icon='📈') 
fig = px.line(filtered_df, x='Sold To Name', y='Quantity', title='Line Chart')
st.plotly_chart(fig, use_container_width=True)

st.info('Dealer by Total sale', icon='🟢')
fig = px.pie(filtered_df, values='Extended Amount', names='Sold To Name', title='Donut Chart', hole=0.4)


st.plotly_chart(fig, use_container_width=True)


