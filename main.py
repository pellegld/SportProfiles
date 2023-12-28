import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import matplotlib.pyplot as plt

st.header("Sportsprofile Comparison Dashboard")

col1, col2, col3 = st.columns(3, gap="large")

df = pd.read_csv('CSV_file_data.csv', sep=';')
transpose = pd.read_csv('transpose.csv', sep=';')

chart_data = df
c = (
    alt.Chart(chart_data)
    .mark_circle()
    .encode(x='Motor control', y=alt.Y('Physical Characteristics', scale=alt.Scale(reverse=True)), color="Sport")
)

with col1:
    option = st.selectbox(
        'Select your sport', df.Sport, index=26
    )

    donut = (
        alt.Chart(transpose)
        .mark_arc(innerRadius=50)
        .encode(
            theta=option,
            color="Sportprofile",
        )
    )
    st.write(option)
    st.altair_chart(donut, theme=None)

with col3:
    option_c = st.selectbox(
        'Select sport to compare', df.Sport,
        index=27
    )
    donut_compare = (
        alt.Chart(transpose)
        .mark_arc(innerRadius=50)
        .encode(
            theta=option_c,
            color="Sportprofile",
        )
    )
    st.write(option_c)
    st.altair_chart(donut_compare, theme=None)


# Load your data
@ st.cache_data
def load_data():
    # Adjust the path to your dataset as necessary
    data = pd.read_csv('CSV_file_data.csv', delimiter=';')
    return data


# Ensuring data is loaded before use
data = load_data()

# Define the characteristics columns
physical_characteristics = ['Endurance', 'Strength', 'Flexibility', 'Speed', 'Agility', 'CoreStability']
motor_control = ['Balance', 'EyeHandCoordination', 'Rhythm', 'Jumping', 'Throwing', 'Kicking', 'Hitting', 'Climbing']
contextual_characteristics = ['OutdoorIndoor', 'TeamIndividal', 'ContactNoContact']

# Function to create a radar chart for two sports
def create_radar_chart(data1, data2, title1, title2):
    labels = np.array(data1.index)
    stats1 = data1.values
    stats2 = data2.values

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    stats1 = np.concatenate((stats1, [stats1[0]]))
    stats2 = np.concatenate((stats2, [stats2[0]]))
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.fill(angles, stats1, color='blue', alpha=0.25)
    ax.plot(angles, stats1, color='blue', linewidth=2, label=title1)
    ax.fill(angles, stats2, color='green', alpha=0.25)
    ax.plot(angles, stats2, color='green', linewidth=2, label=title2)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
    return fig


# Streamlit app
st.subheader('Physical Characteristics')

# Select Sports to Compare
sport_1 = option    #st.selectbox('Select the first sport:', data['Sport'])
sport_2 = option_c          #st.selectbox('Select the second sport:', data['Sport'])

if sport_1 and sport_2:
    # Filter the data for the selected sports and only the physical characteristics
    sport_1_data = data[data['Sport'] == sport_1][physical_characteristics].mean(axis=0)
    sport_2_data = data[data['Sport'] == sport_2][physical_characteristics].mean(axis=0)

    # Create a combined radar chart
    fig = create_radar_chart(sport_1_data, sport_2_data, sport_1, sport_2)

    # Display the chart
    st.pyplot(fig)

# Motor Control
st.subheader('Motor Control Characteristics')
if sport_1 and sport_2:
    # Filter the data for the selected sports and only the physical characteristics
    sport_1_data = data[data['Sport'] == sport_1][motor_control].mean(axis=0)
    sport_2_data = data[data['Sport'] == sport_2][motor_control].mean(axis=0)

    # Create a combined radar chart
    fig = create_radar_chart(sport_1_data, sport_2_data, sport_1, sport_2)

    # Display the chart
    st.pyplot(fig)

#Contextual characteristics
st.subheader("Contextual Characteristics")
if sport_1 and sport_2:
    # Filter the data for the selected sports and only the physical characteristics
    sport_1_data = data[data['Sport'] == sport_1][contextual_characteristics].mean(axis=0)
    sport_2_data = data[data['Sport'] == sport_2][contextual_characteristics].mean(axis=0)

    # Create a combined radar chart
    fig = create_radar_chart(sport_1_data, sport_2_data, sport_1, sport_2)

    # Display the chart
    st.pyplot(fig)