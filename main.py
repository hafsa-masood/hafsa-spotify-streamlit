import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math
from PIL import Image

def highlight_first_row(s):
    return ['background-color: yellow' if i == 0 else '' for i in range(len(s))]

milliseconds_in_hour = 3600000

title_container = st.container()
bignumber = st.container()
piecharts = st.container()
top5 = st.container()
times = st.container()

spotify_data = pd.read_csv('spotify_data_with_category.csv')

spotify_data['endTime'] = pd.to_datetime(spotify_data['endTime'])
spotify_data['endTimeByHour'] = spotify_data['endTime'].dt.hour

with title_container:
    st.title('Hey Spotify User 👋')
    st.subheader("Here's your listening summary from the past year.")

with bignumber:
    st.markdown("This past year, your total listening time summed up to be:")
    _, middle, _ = st.columns([1, 3, 1])
    with middle:
        total_time_played = spotify_data['msPlayed'].sum()/milliseconds_in_hour
        start_range = spotify_data['endTime'].min().strftime('%b %Y')
        end_range = spotify_data['endTime'].max().strftime('%b %Y')
        st.metric(label="{} – {}".format(start_range, end_range), value="{} Hours Played".format(math.ceil(total_time_played)))

    st.divider()

with piecharts: 
    st.header("Breakdown by Song & Podcast")
    st.subheader("In terms of the number of individual tracks, you mostly listened to songs, but podcasts made up most of your total listening time.")
    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots()
        ax.pie(
            spotify_data['category'].value_counts().sort_index(),
            labels=sorted(spotify_data['category'].unique()),
            autopct='%.2f%%',
            startangle=90,
        )
        ax.axis('equal')
        plt.title('By Number of Listens')
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots()
        ax.pie(
            spotify_data.groupby('category')['msPlayed'].sum().sort_index() / 60000,
            labels=sorted(spotify_data['category'].unique()),
            autopct='%.2f%%',
            startangle=90,
        )
        ax.axis('equal')  
        plt.title('By Minutes Listened')
        st.pyplot(fig)
    
    st.markdown("> 💡 I used the Spotify API to categorize each track as a podcast or a song. I was able to categorize all except one of the 8054 records. My algorithm was unable to categorize an episode of *The Ringer NBA Show*, ('Boston Stays Alive … But for How Long? Plus, a Deep Dive Into LeBron’s Retirement Plan'), and marked it as 'other'. I deliberately kept this 'other' categorization to show what would happen with my visualizations in case more tracks could not be categorized properly.")

    st.divider()

with top5:
    st.header('Top 5 Listens')

    st.subheader('Top 5 Podcasts 🎙️')

    st.subheader('Your favorite podcast to listen to was The Bill Simmons Podcast.')
    
    bill_simmons = Image.open('assets/bill_simmons.jpg')
    st.image(bill_simmons)

    podcasts = spotify_data[spotify_data['category']=='podcast'].groupby('artistName').agg(
        listenCount=('msPlayed', 'count'),
        totalHoursPlayed=('msPlayed', lambda x: (x / milliseconds_in_hour).sum())
    ).sort_values('totalHoursPlayed', ascending=False).head(5)
    
    st.dataframe(
        podcasts.reset_index().style.apply(highlight_first_row, axis=0),
        column_config={
            "artistName": "Podcast",
            "listenCount": "Times Played",
            "totalHoursPlayed": "Hours Played"
        },
        hide_index=True,
    )
    
    st.subheader('Top 5 Songs & Artists 🎶')
    
    st.subheader("The artist you listened to the most was Luke Combs...")

    luke_combs = Image.open('assets/luke_combs.jpg')
    st.image(luke_combs)
    
    st.markdown("Top 5 Artists 🎸")
    artists = spotify_data[spotify_data['category']=='song'].groupby('artistName').agg(
        listenCount=('msPlayed', 'count'),
        totalHoursPlayed=('msPlayed', lambda x: (x / 3600000).sum())
    ).sort_values('totalHoursPlayed', ascending=False).head(5)

    st.dataframe(
        artists.reset_index().style.apply(highlight_first_row, axis=0),
        column_config={
            "artistName": "Artist",
            "listenCount": "Times Played",
            "totalHoursPlayed": "Hours Played"
        },
        hide_index=True,
    )
    st.subheader("... and the song you played the most was Doin' This by Luke Combs")
    doin_this = Image.open('assets/doin_this.jpg')
    st.image(doin_this)
    
    st.markdown("Top 5 Songs 🎵")
    songs = spotify_data[spotify_data['category']=='song'].groupby(['trackName', 'artistName']).agg(
        listenCount=('msPlayed', 'count'),
        totalMinutesPlayed=('msPlayed', lambda x: (x / 60000).sum())
    ).sort_values('totalMinutesPlayed', ascending=False).head(5)

    st.dataframe(
        songs.reset_index().style.apply(highlight_first_row, axis=0),
        column_config={
            "trackName": "Song",
            "artistName": "Artist",
            "listenCount": "Times Played",
            "totalMinutesPlayed": "Minutes Played ⏱"
        },
        hide_index=True,
    )
    st.divider()

with times:
    st.header("Time Analysis ⏳")
    st.subheader("Based on the Total Listen Time and the Number of Listens, you are mostly tuned into podcasts in the AM, while in the evenings you tend to enjoy your music!")

    tab1, tab2, tab3 = st.tabs(["Average Listen Time", "Total Listen Time", "Number of Listens"])

    with tab1:
        st.subheader("Average Listen Time By Hour")
        st.text('All tracks')
        groupby_hour = spotify_data.groupby(['endTimeByHour']).agg(
            avgMinutesPlayed=('msPlayed', lambda x: (x / 60000).mean())
        )

        st.bar_chart(data=groupby_hour, y='avgMinutesPlayed')

        st.text("Podcasts")
        podcasts_grouped_by_hour = spotify_data[spotify_data['category']=='podcast'].groupby(['endTimeByHour']).agg(
            avgMinutesPlayed=('msPlayed', lambda x: (x / 60000).mean())
        )
        st.bar_chart(data=podcasts_grouped_by_hour, y='avgMinutesPlayed')
        st.text("Songs")
        songs_grouped_by_hour = spotify_data[spotify_data['category']=='song'].groupby(['endTimeByHour']).agg(
            avgMinutesPlayed=('msPlayed', lambda x: (x / 60000).mean())
        )
        st.bar_chart(data=songs_grouped_by_hour, y='avgMinutesPlayed')
    
    with tab2:
        st.subheader("Total Listen Time By Hour")
        st.text('All Tracks')
        groupby_hour = spotify_data.groupby(['endTimeByHour']).agg(
            totalMinutesPlayed=('msPlayed', lambda x: (x / 60000).sum())
        )

        st.bar_chart(data=groupby_hour, y='totalMinutesPlayed')

        st.text("Podcasts")
        podcasts_grouped_by_hour = spotify_data[spotify_data['category']=='podcast'].groupby(['endTimeByHour']).agg(
            totalMinutesPlayed=('msPlayed', lambda x: (x / 60000).sum())
        )
        st.bar_chart(data=podcasts_grouped_by_hour, y='totalMinutesPlayed')
        st.text("Songs")
        songs_grouped_by_hour = spotify_data[spotify_data['category']=='song'].groupby(['endTimeByHour']).agg(
            totalMinutesPlayed=('msPlayed', lambda x: (x / 60000).sum())
        )
        st.bar_chart(data=songs_grouped_by_hour, y='totalMinutesPlayed')
    
    with tab3:
        st.subheader("Number of Times Played By Hour")

        st.text('All Tracks')
        groupby_hour = spotify_data.groupby(['endTimeByHour']).agg(
            countPlayed=('msPlayed', 'count')
        )

        st.bar_chart(data=groupby_hour, y='countPlayed')

        st.text("Podcasts")
        podcasts_grouped_by_hour = spotify_data[spotify_data['category']=='podcast'].groupby(['endTimeByHour']).agg(
            countPlayed=('msPlayed', 'count')
        )
        st.bar_chart(data=podcasts_grouped_by_hour, y='countPlayed')
        st.text("Songs")
        songs_grouped_by_hour = spotify_data[spotify_data['category']=='song'].groupby(['endTimeByHour']).agg(
            countPlayed=('msPlayed', 'count')
        )
        st.bar_chart(data=songs_grouped_by_hour, y='countPlayed')
    
    st.divider()
