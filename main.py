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

GITHUB_OWNER = 'nununu-py'

# SETTING WEB PAGE
st.set_page_config(
    page_title="nununu_project_airbnb",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# IMPORT DATA LISTING
listing_df = pd.read_csv("./Data/listing_byCountry.csv")

# DROP UNNECESSARY COLUMN FROM DATA LISTING
listing_df.drop(labels=["Unnamed: 0", "lat-long"], axis=1, inplace=True)
listing_df['id'] = listing_df.id.astype(np.int64)

# FILTER DATA LISTING COUNTRY ONLY SINGAPORE
listing_df = listing_df[listing_df['country name'] == "Singapore"]

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
sidebar.markdown("---")

if showdata_BNT:
    st.markdown("""
        <h2 style='text-align: center; color: orange ;'>Listing Data Table</h2>
    """, unsafe_allow_html=True)
    st.dataframe(listing_df.sample(5))
    st.markdown("---")

if hidedata_BTN:

    showdata_BNT = False

# MAIN PAGE
with st.container():
    st.markdown("""
            <h2 style='text-align: center; color: #18978F;'>AIRBNB SINGAPORE DATA ANALYSIS</h2>
        """, unsafe_allow_html=True)
    st.caption("<h4 style='text-align: center; color: #18978F ;'>Final Project Data Analyst Bootcamp With Python And SQL DQLab</h4>",
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

        st.markdown('---')

    # Question2
    question2 = st.container()
    with question2:
        st.markdown(
            """
            ##### Analysis Question 2. What is the average and median price of the listings overall?
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
                default='Ang Mo Kio', max_selections=6)

            if select_box1 == []:
                select_box1 = random.choice(neighbourhoods)

            price_distributionNei_select = price_trendNei_mean.loc[select_box1]

            fig, ax = plt.subplots()
            price_distributionNei_select.plot(kind="bar", ax=ax, stacked=False, color=[
                "#293462", "#F24C4C", "#EC9B3B", "#F7D716"])

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
                default='Ang Mo Kio', max_selections=6)

            if select_box2 == []:
                select_box2 = random.choice(neighbourhoods)

            price_distributionNei_select = price_trendNei_median.loc[select_box2]

            fig, ax = plt.subplots()
            price_distributionNei_select.plot(kind="bar", ax=ax, stacked=False, color=[
                "#293462", "#F24C4C", "#EC9B3B", "#F7D716"])

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
                              stacked=False, color="#297F87")

            for tick in ax.get_xticklabels():
                tick.set_rotation(0)

            ax.legend(loc="center left", bbox_to_anchor=(1.03, 0.8))
            ax.set_xlabel("\nRoom Type", fontdict=FONT)
            ax.set_ylabel("Average Price", fontdict=FONT)

            st.pyplot(fig)

        with col2:

            with st.expander("Check Table : Average Price Distribution For Each Room Type"):
                st.dataframe(price_byRoom)

        st.markdown('---')

    # Question4
    question4 = st.container()

    with question4:
        st.markdown(
            """
            ##### Analysis Question 4. How is the rental trend from 01-01-2018 to 22-09-2022?
            """)

        # avg_price1 = data1.merge(avg_price, left_on='id', right_on='listing_id')

        review_df = pd.read_csv("./Data/DQLab_reviews(22Sep2022).csv")

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

        fig.update_traces(line_color='#B3E283', line_width=1)

        st.plotly_chart(fig)

        with st.expander("Check Table : Top 20 Orders Trend From 01-01-2018 to 22-09-2022"):

            top20_trendsOrder = order_df.sort_values(
                by="Count", ascending=False).reset_index()
            top20_trendsOrder.drop(labels=["index"], axis=1, inplace=True)
            st.dataframe(top20_trendsOrder.head(20))

        st.markdown("---")
        
st.markdown("""

    ## Create Link
    [My Twitter](https://twitter.com/sleepinkMgkawak)
    
    > * twitter https://twitter.com/sleepinkMgkawak
    > * email adiftawisnu818@gmail.com

""")
