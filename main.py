import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

FONT = {'family': 'Sans Serif',
        'color':  '#0A2647',
        'weight': 'bold',
        'size': 11,
        }

# SETTING WEB PAGE
st.set_page_config(
    page_title="nununu_project_airbnb",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# READ DATA
listing_df = pd.read_csv(
    './Data/listing_byCountry.csv')

review_df = pd.read_csv(
    "./Data/DQLab_reviews(22Sep2022).csv")

neighbourhood_df = pd.read_csv(
    "./Data/DQLab_nieghbourhood(22Sep2022).csv")

# DROP UNNECESSARY COLUMN FROM DATA LISTING
listing_df.drop(labels=["Unnamed: 0", "lat-long"], axis=1, inplace=True)
listing_df['id'] = listing_df.id.astype(np.int64)

# FILTER DATA LISTING COUNTRY ONLY SINGAPORE
listing_df = listing_df[listing_df['country name'] == "Singapore"]

# FILTER DATA PRICE = 0
price = listing_df.price != 0
available = listing_df.availability_365 != 0
listing_df = listing_df[(price) & (available)]

# CLEAN DATA LISTING WHICH IS "HAVING PRICE PERNIGHT > 2000"
listing_df = listing_df.sort_values("price", ascending=False)
listing_df = listing_df[15:][:]

# SIDE BAR
sidebar = st.sidebar
sidebar.caption("Click this button to show listing dataframe")
showdata_BNT = sidebar.button(label="Show Data")
sidebar.caption("Click this button to hide listing dataframe")
hidedata_BTN = sidebar.button(label="Hide Data")
sidebar.markdown("---")
sidebar.image(
    "https://skillacademy-prod-image.skillacademy.com/offline-marketplace/DQLab_Icon.png", width=150)
sidebar.markdown("#### Name: Adifta Wisnu Wardana")
sidebar.markdown(
    """[My Linkedin Profile</h5>](https://www.linkedin.com/in/adifta-wisnu-wardana/)""", unsafe_allow_html=True)


if showdata_BNT:
    st.markdown("""<h2 style='text-align: center; color: orange ;'>Listing Data Table</h2>""",
                unsafe_allow_html=True)
    st.dataframe(listing_df.sample(5))
    st.markdown("---")

if hidedata_BTN:

    showdata_BNT = False

# TOP PAGE

# MAIN PAGE
with st.container():
    st.markdown("""
            <h2 style='text-align: center; color: #18978F;'>AIRBNB SINGAPORE DATA ANALYSIS</h2>
        """, unsafe_allow_html=True)
    st.caption("<h4 style='text-align: center; color: #18978F;'>DQLab: Final Project Data Analyst Bootcamp with Python And SQL</h4>",
               unsafe_allow_html=True)
    st.markdown("---")

    # Question1
    question1 = st.container()
    with question1:
        st.markdown(
            """
            ##### Analysis Question 1. How is the distribution of Airbnb listing property prices in Singapore ?
            """)

        fig = px.histogram(data_frame=listing_df, x='price', histnorm='density')

        fig.update_layout(xaxis_title='Price', yaxis_title='Density')

        st.plotly_chart(fig)

        text_desc = "Based on the histogram chart above, it can be concluded that the distribution of listing prices for properties at Airbnb Singapore ranges from $6 to $1779 Singapore, but the highest number of listing prices is in the price range of $ 50-59 and $ 60-79."
        st.text_area(label="Desc : ", value=text_desc)
        st.markdown('---')

    # Question2
    question2 = st.container()
    with question2:
        st.markdown(
            """
            ##### Analysis Question 2. What are the average and median prices of the data per neighborhood and room type ?
            """)

        tips1 = st.checkbox("Tips")

        if tips1:
            st.info("Select or remove neighbourhood to visualize. (Maximum number of selected is seven)")

        price = ["price"]
        feature = ["neighbourhood", "room_type"]
        group = price + feature

        col1, col2 = st.columns(2)

        with col1:
            data = listing_df[group].groupby(feature).mean().unstack()
            data.fillna(0, inplace=True)
            neighbourhoods = list(data.index)

            select_box1 = st.multiselect(
                label="Select neighbourhood average price you want to visualize", options=neighbourhoods,
                default=["Rochor", "Pasir Ris", "Marina South", "Southern Islands"], max_selections=7)

            if not select_box1:
                st.warning('At least you must select one option')

            data_to_viz = data.loc[select_box1]
            data_to_viz.columns = ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'] 

            fig = px.bar(data_to_viz, width=590, height=380, color_discrete_sequence=['#E57C23', '#2F58CD', '#0E8388', '#DF2E38'])

            fig.update_layout(xaxis_title='Neighborhood', yaxis_title='Average Price', barmode='group', legend=dict(title='Room Type<br>'))

            st.plotly_chart(fig)

            show_dataframe = st.expander(label="Display dataframe : Average price of neighbourhood")

            with show_dataframe:

                tips2 = st.checkbox(label="Tips ")

                if tips2:
                    st.info("Click on header column to sort average price values ascending or descending")

                st.dataframe(data_to_viz)

        with col2:
            data = listing_df[group].groupby(feature).median().unstack()
            data.fillna(0, inplace=True)

            select_box2 = st.multiselect(
                label="Select neighbourhood median price you want to visualize", options=neighbourhoods,
                default=["Rochor", "Pasir Ris", "Marina South", "Southern Islands"], max_selections=6)

            if not select_box2:
                st.warning('At least you must select one option')

            data_to_viz = data.loc[select_box2]
            data_to_viz.columns = ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room']  

            fig = px.bar(data_to_viz, width=590, height=380, color_discrete_sequence=['#E57C23', '#2F58CD', '#0E8388', '#DF2E38'])

            fig.update_layout(xaxis_title='Neighborhood', yaxis_title='Median Price', barmode='group', legend=dict(title='Room Type'))

            st.plotly_chart(fig)

            show_dataframe = st.expander(label="Display dataframe : Median price of neighbourhood")

            with show_dataframe:

                tips3 = st.checkbox(label="Tips  ")

                if tips3:
                    st.info(
                        "Click on header column to sort median price values ascending or descending")

                st.dataframe(data_to_viz)

        text_desc = "By exploring the visualization data above, it can be concluded that the neighborhoods with the highest average and highest median price based on room type \"Entire House/apartment\" are in Southern Island. The \"Private Room\" room type is in Marina South, the \"Hotel Room\" type is in the Rochor area, and finally, the \"Shared Room\" is located in the Pasir Ris neighborhood, this can happen because not many properties are available for rent in this neighborhood area."
        st.text_area(label="Desc :  ", value=text_desc)
        st.markdown('---')

    # Question3
    question3 = st.container()
    with question3:
        st.markdown(
            """
            ##### Analysis Question 3. Does room type affect the price ?
            """)

        price = ['price']
        feature = ['room_type']
        data_to_viz = listing_df[price + feature].groupby('room_type').mean()

        fig = px.bar(data_frame=data_to_viz, 
                     x=data_to_viz.index,
                     y="price", color=data_to_viz.index, 
                     color_discrete_sequence=['#E57C23', '#2F58CD', '#0E8388', '#DF2E38'])

        fig.update_layout(yaxis_title="Average Price",
                          xaxis_title="Room Type", 
                          autosize=False, 
                          width=725, 
                          height=500, 
                          legend=dict(title='Room Type <br>'))

        st.plotly_chart(fig)

        with st.expander("Display dataframe : Room type average price"):
            st.dataframe(data_to_viz)

        text_desc = "Based on the bar chart above, it can be concluded that the room type greatly influences the average price of a listing property"
        st.text_area(label="Desc :   ", value=text_desc)
        st.markdown('---')

    # Question4
    question4 = st.container()

    with question4:
        st.markdown(
            """
            ##### Analysis Question 4. How is the order trends from 01-01-2018 to 22-09-2022 ?
            """)

        review_df = review_df.drop(labels=["Unnamed: 0"], axis=1)
        total_order_df = listing_df.merge(review_df, left_on="id", right_on="listing_id")

        date = ["date"]
        feature = ["id"]

        total_order_df = total_order_df[feature + date].groupby(date).count().reset_index()
        total_order_df.columns = total_order_df.columns.str.replace('date', 'Date')
        total_order_df.columns = total_order_df.columns.str.replace('id', 'Total Orders')

        fig = px.line(
            total_order_df,
            x="Date",
            y="Total Orders")

        fig.update_layout(yaxis_title="Total Orders",
                          xaxis_title="Datetime", 
                          autosize=False, 
                          width=1340, 
                          height=500)

        fig.update_traces(line_color='#277BC0', line_width=1.5)

        st.plotly_chart(fig)

        with st.expander("Display dataframe: Top 20 date with the highest total orders in the last 5 years"):

            top20_data = total_order_df.sort_values(by="Total Orders", ascending=False)
            st.dataframe(top20_data.head(20))

        text_desc = "Based on the trend of property listing orders on the Airbnb Singapore site from January 1, 2018, to September 22, 2022, it can be concluded that the number of daily orders fluctuates frequently, with both increasing and decreasing observed. However, when comparing the trend of listing orders in 2020 and subsequent years, there is a noticeable decrease in the number of daily orders compared to the previous year. This decline can be attributed to the confirmation of the first Covid-19 case in Singapore in January 2020, which led to the complete restriction of mobility for residents and visitors from outside Singapore through the implementation of lockdown measures."
        st.text_area(label="Desc :    ", value=text_desc)
        st.markdown("---")

# NEW FRAME
# ------------------------------------------------------------------------------------------------

    neighbourhood_df = neighbourhood_df.drop(labels=["Unnamed: 0"], axis=1)

    merge_data = listing_df.merge(neighbourhood_df, left_on="neighbourhood", right_on="neighbourhood")
    merge_data = merge_data.merge(review_df, left_on='id', right_on='listing_id')

    merge_data = merge_data.groupby(['room_type', 'name', 'id', 'neighbourhood_group', 'latitude', 'longitude']).agg({'date':'count'}).reset_index().sort_values(by='neighbourhood_group')
    merge_data.rename(columns={'date': 'order'}, inplace=True)
    
    total_average_order = merge_data[["neighbourhood_group", "order"]].groupby("neighbourhood_group").agg({'order':'mean'}).reset_index()
    list_average_order = list(total_average_order["order"])

    question5 = st.container()

    with question5:
        st.markdown(
            """
            ##### Analysis Question 5. How many listings have orders above the average per each neighborhood group ?
            """)
        
        col1, col2 = st.columns(2, gap="medium")
    
        with st.container():
        
                with col1:

                    high_orders_map = px.scatter_mapbox(merge_data, 
                                                         lat="latitude", 
                                                         lon="longitude", 
                                                         color="neighbourhood_group", 
                                                         size='order',
                                                         hover_name='name', 
                                                         zoom=9.5, width=700, 
                                                         height=385, 
                                                         hover_data=["room_type", "order"],
                                                         color_discrete_sequence=['#CA4E79', '#6E85B7', '#497174', '#3AB4F2', '#FFA500'])
                    
                    high_orders_map.update_layout(mapbox_style="open-street-map", 
                                                  legend=dict(title='Neighbourhood Group<br>'))
                    
                    high_orders_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
                    
                    st.plotly_chart(high_orders_map)
                
        with st.container():
                    
                with col2:

                    filter1 = ((merge_data['order'] > list_average_order[0]) & (merge_data['neighbourhood_group'] == 'Central Region'))
                    filter2 = ((merge_data['order'] > list_average_order[1]) & (merge_data['neighbourhood_group'] == 'East Region'))
                    filter3 = ((merge_data['order'] > list_average_order[2]) & (merge_data['neighbourhood_group'] == 'North Region'))
                    filter4 = ((merge_data['order'] > list_average_order[3]) & (merge_data['neighbourhood_group'] == 'North-East Region')) 
                    filter5 = ((merge_data['order'] > list_average_order[4]) & (merge_data['neighbourhood_group'] == 'West Region'))
                    
                    high_orders = merge_data[filter1 | filter2 | filter3 | filter4 | filter5]
                    data_to_viz = high_orders[['neighbourhood_group', 'order']].groupby('neighbourhood_group').agg({'order':'count'})
            
                    st.write("")

                    fig = px.bar(
                        data_to_viz,
                        x=data_to_viz.index,
                        y='order', 
                        color=data_to_viz.index,
                        color_discrete_sequence=['#CA4E79', '#6E85B7', '#497174', '#3AB4F2', '#FFA500'],
                        title='Count listing property above average orders')
                    
                    fig.update_layout(yaxis_title="Total Counts",
                                      xaxis_title="Neighbourhood", 
                                      autosize=False, 
                                      width=610,
                                      height=400)
                    
                    fig.update_layout(showlegend=False)
                    fig.update_traces(hovertemplate='Total Counts: %{y}<br> Neighbourhood: %{x}<br>')

                    st.plotly_chart(fig)

        text_desc = "Based on the visualization results, it can be concluded that the majority of property listings with above-average orders, based on neighborhood groups, are situated in the central region. This is attributed to the central area serving as the city center, housing various business activities, administrative functions, and numerous prominent companies. Consequently, it becomes a preferred choice for business individuals seeking accommodations near the industrial hub. Additionally, the central region boasts a plethora of captivating and iconic tourist attractions, making it an ideal destination for tourists to consider when selecting properties."
        st.text_area(label="Desc :     ", value=text_desc)

        st.markdown('---')

# FOOTER
# ------------------------------------------------------------------------------------------------

for i in range(4):
    st.write("")

st.markdown("""
    <h5 style='text-align: center; color: #F2DF3A;'>For more Airbnb Singapore listing property analysis, kindly check my friend streamlit webapp</h5>
    """, unsafe_allow_html=True)

st.markdown("""
    [<h5 style='text-align: center; color: #FEB139 ;'>Gustav Airbnb Project</h5>](https://gustavsmnt-airbnb-project-project-airbnb-uszn1j.streamlit.app/) 
    """, unsafe_allow_html=True)
