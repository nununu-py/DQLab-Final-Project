import random
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

FONT = {'family': 'serif',
        'color':  '#2C3639',
        'weight': 'bold',
        'size': 13,
        }

# SETTING WEB PAGE
st.set_page_config(
    page_title="nununu_project_airbnb",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# READ DATA
listing_df = pd.read_csv(
    './Data/listing_byCountry.csv')

review_df = pd.read_csv(
    "./Data/DQLab_reviews(22Sep2022).csv")

neighbourhoodsGroup_df = pd.read_csv(
    "./Data/DQLab_nieghbourhood(22Sep2022).csv")

# DROP UNNECESSARY COLUMN FROM DATA LISTING
listing_df.drop(labels=["Unnamed: 0", "lat-long"], axis=1, inplace=True)
listing_df['id'] = listing_df.id.astype(np.int64)

# FILTER DATA LISTING COUNTRY ONLY SINGAPORE
listing_df = listing_df[listing_df['country name'] == "Singapore"]

# FILTER DATA PRICE = 0
price = listing_df.price != 0
avail = listing_df.availability_365 != 0
listing_df = listing_df[(price) & (avail)]

# CLEAN DATA LISTING WHICH IS "HAVING PRICE PERNIGHT > 2000"
listing_df = listing_df.sort_values("price", ascending=False)
listing_df = listing_df[15:][:]

# SIDE BAR
sidebar = st.sidebar
sidebar.image(
    "https://skillacademy-prod-image.skillacademy.com/offline-marketplace/DQLab_Icon.png")
sidebar.markdown('---')
sidebar.caption("Click This Button To Show Listing Data Table")
showdata_BNT = sidebar.button(label="Show Data Table")
sidebar.caption("Click This Button To Hide Listing Data Table")
hidedata_BTN = sidebar.button(label="Hide Data Table")

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
            <h2 style='text-align: center; color: #18978F;'>AIRBNB SINGAPORE LISTINGS DATA ANALYSIS</h2>
        """, unsafe_allow_html=True)
    st.caption("<h4 style='text-align: center; color: #18978F;'>Final Project Data Analyst Bootcamp With Python And SQL DQLab</h4>",
               unsafe_allow_html=True)
    st.markdown("---")

    # Question1
    question1 = st.container()
    with question1:
        st.markdown(
            """
            ##### Analysis Question 1. How is the distribution of airbnb listing prices in Singapore?
            """)

        col1, col2 = st.columns(2)

        with col1:

            fig, ax = plt.subplots()
            sns.kdeplot(x=listing_df['price'],
                        hue=listing_df['country name'], ax=ax)
            ax.set_xlabel("\nCountry Name", fontdict=FONT)
            ax.set_ylabel("Density", fontdict=FONT)

            st.pyplot(fig)

#         with col2:
          
#             fig, ax = plt.subplots()
#             sns.boxplot(data=listing_df, x="country name", y="price", ax=ax)
#             ax.set_xlabel("\nCountry Name", fontdict=FONT)
#             ax.set_ylabel("Price", fontdict=FONT)

#             st.pyplot(fig)

        st.text_area(
            label="", value="According to the diagrams above we can see the distribution of listing prices from Airbnb singapore from 2018 to 2022")
        st.markdown('---')

    # Question2
    question2 = st.container()
    with question2:
        st.markdown(
            """
            ##### Analysis Question 2. What are the average and median prices of the data per neighbourhood and room type?
            """)
        # st.dataframe(listing_df.describe())
        price = ["price"]
        feature = ["neighbourhood", "room_type"]
        group = price + feature

        col1, col2 = st.columns(2)

        with col1:
            price_trendNei_mean = listing_df[group].groupby(
                feature).mean().unstack()

            price_trendNei_mean.fillna(0, inplace=True)

            neighbourhoods = list(price_trendNei_mean.index)

            select_box1 = st.multiselect(
                label="Select Neighbourhood Mean You Want To Visualize", options=neighbourhoods,
                default=["Rochor", "Pasir Ris", "Marina South", "Southern Islands"], max_selections=7)

            if select_box1 == []:
                select_box1 = random.choice(neighbourhoods)

            price_distributionNei_select = price_trendNei_mean.loc[select_box1]

            fig, ax = plt.subplots()
            price_distributionNei_select.plot(kind="bar", ax=ax, stacked=False, color=[
                "#488FB1", "#F24C4C", "#EC9B3B", "#F7D716"])

            for tick in ax.get_xticklabels():
                tick.set_rotation(50)

            ax.legend(loc="center left", bbox_to_anchor=(1.03, 0.8))
            ax.set_xlabel("\nNeighbourhood", fontdict=FONT)
            ax.set_ylabel("Average Price", fontdict=FONT)

            st.pyplot(fig)

            # st.dataframe(price_trendNei_mean)

            check_priceDisNei_avg = st.expander(
                label="Check Table : Average Price Distribution by Neighbourhood")

            with check_priceDisNei_avg:
                st.dataframe(price_trendNei_mean)

        with col2:
            price_trendNei_median = listing_df[group].groupby(
                feature).median().unstack()

            price_trendNei_median.fillna(0, inplace=True)

            select_box2 = st.multiselect(
                label="Select Neighbourhood Median You Want To Visualize", options=neighbourhoods,
                default=["Rochor", "Pasir Ris", "Marina South", "Southern Islands"], max_selections=6)

            if select_box2 == []:
                select_box2 = random.choice(neighbourhoods)

            price_distributionNei_select = price_trendNei_median.loc[select_box2]

            fig, ax = plt.subplots()
            price_distributionNei_select.plot(kind="bar", ax=ax, stacked=False, color=[
                "#488FB1", "#F24C4C", "#EC9B3B", "#F7D716"])

            for tick in ax.get_xticklabels():
                tick.set_rotation(50)

            ax.legend(loc="center left", bbox_to_anchor=(1.03, 0.8))
            ax.set_xlabel("\nNeighbourhood", fontdict=FONT)
            ax.set_ylabel("Median Price", fontdict=FONT)
            st.pyplot(fig)

            check_priceDisNei_med = st.expander(
                label="Check Table : Median Price Distribution by Neighbourhood")

            with check_priceDisNei_med:
                st.dataframe(price_trendNei_median)

        st.text_area(
            label=" ", value="By exploring the data visualization above, we can conclude that the neighborhood with the highest average price based on the room type \"Entire Home/apt\" is in Southern Island. The \"Private Room\" room type is in Marina South, the \"Hotel Room\" type is in the Rochor area and finally, the \"Shared Room\" is located in Pasir Ris neighbourhood, this can be happend because there aren't a lot of properties available for rent in this neighborhood area.")

        st.markdown('---')

    # Question3
    question3 = st.container()
    with question3:
        st.markdown(
            """
            ##### Analysis Question 3. Does room type affect the price?
            """)

        col1, col2 = st.columns(2)

        with col1:

            price = ['price']
            feature = ['room_type']
            price_byRoom = listing_df[price +
                                      feature].groupby('room_type').mean()

            fig, ax = plt.subplots()
            price_byRoom.plot(kind="bar", ax=ax,
                              stacked=False, color="#47B5FF")

            for tick in ax.get_xticklabels():
                tick.set_rotation(0)

            ax.legend(loc="center left", bbox_to_anchor=(1.03, 0.8))
            ax.set_xlabel("\nRoom Type", fontdict=FONT)
            ax.set_ylabel("Average Price", fontdict=FONT)

            st.pyplot(fig)

        with col2:

            with st.expander("Check Table : Average Price Distribution For Each Room Type"):
                st.dataframe(price_byRoom)

        st.text_area(
            label="  ", value="Based on the data visualization above, it can be clearly concluded that the room type greatly influences the price of a property for rent.")

        st.markdown('---')

    # Question4
    question4 = st.container()

    with question4:
        st.markdown(
            """
            ##### Analysis Question 4. How is the rental trend from 01-01-2018 to 22-09-2022?
            """)

        # avg_price1 = data1.merge(avg_price, left_on='id', right_on='listing_id')

        review_df = review_df.drop(labels=["Unnamed: 0"], axis=1)

        order = listing_df.merge(
            review_df, left_on="id", right_on="listing_id")

        # st.dataframe(order)
        # st.dataframe(order.dtypes)

        date = ["date"]
        feature = ["name", "id"]

        order_df = order[feature +
                         date].groupby(date).size().to_frame("Count").reset_index()

        fig = px.line(
            order_df,
            x="date",
            y="Count",
            labels={
                "date": "Date From 01-01-2018 to 22-09-2022",  "Count": "Total Orders"
            }
        )

        # fig.update_layout(
        #     title="Orders Trends From From 01-01-2018 to 22-09-2022", title_x=0.5)

        fig.update_traces(line_color='#59CE8F', line_width=1)

        st.plotly_chart(fig)

        with st.expander("Check Table : Top 20 Orders Trend From 01-01-2018 to 22-09-2022"):

            top20_trendsOrder = order_df.sort_values(
                by="Count", ascending=False).reset_index()
            top20_trendsOrder.drop(labels=["index"], axis=1, inplace=True)
            st.dataframe(top20_trendsOrder.head(20))

        st.text_area(label="    ", value="According to the results of the data visualization with the line chart above, we can conclude that the trend order listing of all the highest room type and neighborhood categories is in the range from September 2019 to February 2020 and thereafter decreased until the following year. This could be due to an outbreak covid, so people prefer to stay at home. This listing trend only experienced an increase again in May 2022, because All remaining COVID-19 restrictions were lifted progressively on 29 March 2022 and 26 April 2022 but mask wearing is optional for some places.")
        st.markdown("---")

# NEW FRAME
# ------------------------------------------------------------------------------------------------

    neighbourhoodsGroup_df = neighbourhoodsGroup_df.drop(
        labels=["Unnamed: 0"], axis=1)

    mergeAll_data = order.merge(
        neighbourhoodsGroup_df, left_on="neighbourhood", right_on="neighbourhood")

    groupAll_byDate = mergeAll_data.groupby(['room_type', 'name', 'id', 'neighbourhood_group', 'latitude', 'longitude'])[
        'date'].size().to_frame('order').reset_index()

    averageOrder_NG = groupAll_byDate[["neighbourhood_group", "order"]].groupby(
        "neighbourhood_group").mean()

    # st.dataframe(averageOrder_NG)

    list_averageOrder_NG = list(averageOrder_NG["order"])
    list_averageOrder_index = list(averageOrder_NG.index)

    dataframeFilter_list = []
    for i in range(5):
        grouping = groupAll_byDate[(groupAll_byDate["neighbourhood_group"] == list_averageOrder_index[i])
                                   & (groupAll_byDate["order"] > list_averageOrder_NG[i])]
        dataframeFilter_list.append(grouping)

    high_reviews = pd.concat(dataframeFilter_list)

    # st.dataframe(high_reviews)

    question5 = st.container()

    with question5:
        st.markdown(
            """
            ##### Analysis Question 5. How many listings have reviews above the average per each \
            neighborhood_group ?
            """)

        high_reviews_map = px.scatter_mapbox(high_reviews, lat="latitude", lon="longitude", color="neighbourhood_group",
                                             hover_name='name', zoom=9, width=750, hover_data=["room_type", "order"])
        high_reviews_map.update_layout(mapbox_style="open-street-map")
        high_reviews_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.plotly_chart(high_reviews_map)

        st.warning(
            "Show the table to see which neighborhood group has the most listings reviews")

        with st.expander(label="Check Table : Listing that have above average reviews per neighborhood group"):

            data = high_reviews.groupby(['neighbourhood_group'])[
                'name'].size().to_frame('Total Listing').reset_index()

            st.dataframe(data)

# FOOTER
# ------------------------------------------------------------------------------------------------

for i in range(4):
    st.write("")

st.markdown("""
    <h5 style='text-align: center; color: #1746A2;'>For more airbnb singapore listing analysis and data visualization, \
    kindly check my Friend streamlit webapp</h5>
""", unsafe_allow_html=True)

st.markdown("""
    
    [<h5 style='text-align: center; color: #5F9DF7 ;'>Gustav Airbnb Project</h5>](https://gustavsmnt-airbnb-project-project-airbnb-uszn1j.streamlit.app/
)

""", unsafe_allow_html=True)
