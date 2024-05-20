import streamlit as st
import json
import pandas as pd

# Load data from JSON file
with open('combined_insights.json', 'r') as f:
    data = json.load(f)

@st.cache_data(show_spinner=False)
def split_frame(input_df, rows):
    df = [input_df.loc[i : i + rows - 1, :] for i in range(0, len(input_df), rows)]
    return df

# Streamlit UI
st.title('Property Dashboard')

# Period selection
period = st.selectbox('Select Period for Insights:', ['March-24 to April-24'], index=0)

# Category selection
category = st.selectbox('Select Category', list(data.keys()))

# Display subcategory buttons based on category selection
if category:
    st.subheader('Select Subcategory:')
    subcategories = ['Questions', 'Concerns', 'Emotions', 'Interest']

    # Arrange buttons in columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if col1.button(subcategories[0]):
            st.session_state.selected_subcategory = subcategories[0]
    with col2:
        if col2.button(subcategories[1]):
            st.session_state.selected_subcategory = subcategories[1]
    with col3:
        if col3.button(subcategories[2]):
            st.session_state.selected_subcategory = subcategories[2]
    with col4:
        if col4.button(subcategories[3]):
            st.session_state.selected_subcategory = subcategories[3]

    # Display data based on subcategory selection in a table with pagination
    if 'selected_subcategory' in st.session_state:
        st.subheader(f"{st.session_state.selected_subcategory} related to {category}")
        st.markdown(f"#### {st.session_state.selected_subcategory.capitalize()} Summary: ")
        
        bullet_points = data[category][f'{st.session_state.selected_subcategory}_Summary']
        for point in bullet_points:
            st.markdown(f"- {point}")

        # Determine data to display based on subcategory
        if st.session_state.selected_subcategory == 'Questions':
            subcategory_data = [(question) for i, question in enumerate(data[category]['Questions'])]
        elif st.session_state.selected_subcategory == 'Concerns':
            subcategory_data = [(concern) for i, concern in enumerate(data[category]['Concerns'])]
        elif st.session_state.selected_subcategory == 'Emotions':
            subcategory_data = [(emotion) for i, emotion in enumerate(data[category]['Emotions'])]
        elif st.session_state.selected_subcategory == 'Interest':
            subcategory_data = [(interest) for i, interest in enumerate(data[category]['Interest'])]

        dataset = pd.DataFrame(subcategory_data)
        print(dataset)
        pagination = st.container()

        bottom_menu = st.columns((4, 1, 1))
        with bottom_menu[2]:
            batch_size = st.selectbox("Page Size", options=[10, 20, 50,], key='batch_size')
        with bottom_menu[1]:
            total_pages = (
                int(len(subcategory_data) / batch_size) if int(len(subcategory_data) / batch_size) > 0 else 1
            )
            current_page = st.number_input(
                "Page", min_value=1, max_value=total_pages, step=1, key='current_page'
            )

        with bottom_menu[0]:
            st.markdown(f"Page **{current_page}** of **{total_pages}** ")

        pagination.dataframe(dataset.iloc[(current_page-1)*batch_size:current_page*batch_size], hide_index=True)

