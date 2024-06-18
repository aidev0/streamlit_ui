import streamlit as st

# Sample data: List of dictionaries
data = [
    {"name": "Alice", "age": 25, "city": "New York"},
    {"name": "Bob", "age": 30, "city": "London"},
    {"name": "Charlie", "age": 35, "city": "Berlin"},
    {"name": "Diana", "age": 28, "city": "Paris"}
]

# Title of the app
st.title('Data Viewer App')

# Filter by city
filter_city = st.text_input("Enter a city to filter:")

# Filter by age range
min_age, max_age = st.slider("Select an age range", 18, 100, (20, 40))

# Filtering data based on city and age range
filtered_data = [item for item in data if (min_age <= item['age'] <= max_age) and filter_city.lower() in item['city'].lower()]

# Displaying the filtered data
if filter_city or (min_age, max_age) != (20, 40):
    st.write(f"Filtered Data by city: {filter_city} and age range: {min_age}-{max_age}")
else:
    st.write("Full Data")

st.write(filtered_data)


