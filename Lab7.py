import streamlit as st
import pandas as pd
import altair as alt

# --------------------
# Page configuration (no icon)
# --------------------
st.set_page_config(
    page_title="Fitness Progress Dashboard",
    layout="wide"
)

st.title("Fitness Progress Dashboard")
st.caption("Interactive fitness data visualization app built with Streamlit")

# --------------------
# Load dataset
# --------------------
@st.cache_data
def load_data():
    df = pd.read_csv("fitness_data.csv", parse_dates=["date"])
    return df

df = load_data()

# --------------------
# Sidebar filters
# --------------------
st.sidebar.header("Filter Workouts")

# Gender filter
genders = df["gender"].unique().tolist()
gender_selected = st.sidebar.multiselect(
    "Select gender:",
    options=genders,
    default=genders
)

# Workout type filter
workout_types = df["workout_type"].unique().tolist()
workout_selected = st.sidebar.multiselect(
    "Select workout type:",
    options=workout_types,
    default=workout_types
)

# Date range filter
min_date = df["date"].min()
max_date = df["date"].max()

date_range = st.sidebar.date_input(
    "Select date range:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Intensity filter
intensities = df["intensity_level"].unique().tolist()
intensity_selected = st.sidebar.multiselect(
    "Select intensity level:",
    options=intensities,
    default=intensities
)

# Apply filters
filtered_df = df[
    (df["gender"].isin(gender_selected)) &
    (df["workout_type"].isin(workout_selected)) &
    (df["intensity_level"].isin(intensity_selected)) &
    (df["date"] >= pd.to_datetime(date_range[0])) &
    (df["date"] <= pd.to_datetime(date_range[1]))
]

st.sidebar.write(f"Workouts selected: {len(filtered_df)}")

# --------------------
# Data summary section
# --------------------
st.subheader("Summary Statistics")

col1, col2, col3 = st.columns(3)

total_workouts = len(filtered_df)
total_calories = int(filtered_df["calories_burned"].sum()) if total_workouts > 0 else 0
avg_duration = filtered_df["duration_min"].mean() if total_workouts > 0 else 0

col1.metric("Total workouts", total_workouts)
col2.metric("Total calories burned", f"{total_calories} kcal")
col3.metric("Average workout duration", f"{avg_duration:.1f} minutes")

st.write("Filtered Data Preview")
st.dataframe(filtered_df)

# --------------------
# Visualizations
# --------------------
st.subheader("Visualizations")

chart_choice = st.selectbox(
    "Choose a chart:",
    ["Calories over time", "Duration vs calories (scatter)", "Steps distribution (histogram)"]
)

if len(filtered_df) == 0:
    st.warning("No data available for the selected filters. Please adjust the filters.")
else:
    if chart_choice == "Calories over time":
        line_chart = (
            alt.Chart(filtered_df)
            .mark_line(point=True)
            .encode(
                x=alt.X("date:T", title="Date"),
                y=alt.Y("calories_burned:Q", title="Calories burned"),
                color="workout_type:N",
                tooltip=["date", "workout_type", "duration_min", "calories_burned", "steps"]
            )
            .interactive()
        )
        st.altair_chart(line_chart, use_container_width=True)

    elif chart_choice == "Duration vs calories (scatter)":
        scatter = (
            alt.Chart(filtered_df)
            .mark_circle(size=80)
            .encode(
                x=alt.X("duration_min:Q", title="Duration (minutes)"),
                y=alt.Y("calories_burned:Q", title="Calories burned"),
                color="intensity_level:N",
                tooltip=["date", "workout_type", "duration_min", "calories_burned", "avg_heart_rate"]
            )
            .interactive()
        )
        st.altair_chart(scatter, use_container_width=True)

    elif chart_choice == "Steps distribution (histogram)":
        hist = (
            alt.Chart(filtered_df)
            .mark_bar()
            .encode(
                x=alt.X("steps:Q", bin=alt.Bin(maxbins=15), title="Steps"),
                y=alt.Y("count():Q", title="Number of workouts"),
                color="gender:N",
                tooltip=["steps", "gender", "workout_type", "calories_burned"]
            )
        )
        st.altair_chart(hist, use_container_width=True)

st.markdown("---")
st.caption("Fitness dashboard for data visualization assignment")
