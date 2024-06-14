import streamlit as st
import json
import pandas as pd
import warnings
import ast
from streamlit_modal import Modal

warnings.filterwarnings('ignore')

# Load data
per_audio_df = pd.read_csv("per_audio1.csv")
summary_df = pd.read_csv("summary1.csv", index_col=0)

# Initialize session state
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = summary_df.columns[0]
if 'selected_time_frame' not in st.session_state:
    st.session_state.selected_time_frame = "April-May"
if 'selected_subsection' not in st.session_state:
    st.session_state.selected_subsection = "Summary"  # Default to Summary
if 'selected_audio' not in st.session_state:
    st.session_state.selected_audio = None

def main():
    st.title("Real Estate Audio Analysis")

    modal = Modal(
        "Demo Modal", 
        key="demo-modal",
        
    )
    time_frames = ["April-May"]
    col1, _, _ = st.columns([1, 1, 1])  # Define three columns with equal width
    with col1:  # Select the second column for the select box
        selected_time_frame = st.selectbox(
            "Select Time Frame",
            time_frames,
            index=time_frames.index(st.session_state.selected_time_frame),
            on_change=lambda: st.session_state.update(
                selected_time_frame=st.session_state["selectbox_time_frame"]
            ),
            key="selectbox_time_frame"
        )

    # Custom CSS for buttons
    st.markdown(
        """
        <style>
        .section-button>button {
            background-color: #ADD8E6; /* Light Blue */
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 10px;
        }
        .section-button>button:hover {
            background-color: #B0E0E6; /* Lighter Blue on Hover */
            color: black;
        }
        .audio-button>button {
            background-color: #FFA07A; /* Light Salmon */
            border: none;
            color: white;
            padding: 8px 16px;  /* Smaller padding for smaller buttons */
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;  /* Smaller font size */
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 5px;
        }
        .audio-button>button:hover {
            background-color: #FFA07A; /* Lighter Salmon on Hover */
            color: black;
        }
        .scroll-container {
            max-height: 400px;
            overflow-y: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    categories = summary_df.columns
    selected_category = st.selectbox(
        "Select Category",
        categories,
        index=list(categories).index(st.session_state.selected_category),
        on_change=lambda: st.session_state.update(
            selected_category=st.session_state["selectbox_category"]
        ),
        key="selectbox_category"
    )

    # Create a big container
    big_container = st.container(height=500)

    with big_container:
        button_container = st.columns(6)  # Display buttons horizontally

        # Define variables to track button states
        button1_state = button_container[0].button(
            "Audio",
            key="button1",
            on_click=lambda: update_button_state("Audio")
        )
        button2_state = button_container[1].button(
            "Summary",
            key="button2",
            on_click=lambda: update_button_state("Summary")
        )

        selected_subsection = st.session_state.selected_subsection

        if selected_subsection == "Summary":
            sb_df = summary_df[[selected_category]]  # Select the column as a DataFrame
            st.markdown("<div class='scroll-container'>", unsafe_allow_html=True)
            for index, row in sb_df.iterrows():
                with st.expander(index):
                    summary_points = ast.literal_eval(row[selected_category])['Summary']
                    for point in summary_points:
                        st.write(f"- {point.strip()}")
            st.markdown("</div>", unsafe_allow_html=True)
        elif selected_subsection == "Audio":
            # Get unique audio names
            audio_names = per_audio_df['Audio Name'].unique().tolist()
            
            # Create two columns for the audio buttons
            col1, col2 = st.columns([1, 4])
            
            # Distribute the audio names into two columns
            for i, audio_name in enumerate(audio_names):
                # if i % 2 == 0:
                #     if col1.button(audio_name, key=f"audio_{i}", type="secondary"):
                #         st.session_state.selected_audio = audio_name
                # else:
                if col1.button(audio_name, key=f"audio_{i}", type="secondary"):
                    st.session_state.selected_audio = audio_name
            
            with col2:
                if st.session_state.selected_audio != None:
                    audio = per_audio_df[(per_audio_df["Audio Name"] == st.session_state.selected_audio) & (per_audio_df["Subcategory"] == selected_category)]
                    for idx, column in enumerate(['Questions', 'Concerns', 'Emotions','Preferences']):
                        with st.expander(column):
                            summary_points = ast.literal_eval(audio[column].iloc[0])
                            for point in summary_points:
                                st.write(f"- {point.strip()}")
            st.markdown("</div>", unsafe_allow_html=True)

        print(st.session_state.selected_audio)

def update_button_state(subsection):
    st.session_state.selected_subsection = subsection
    if subsection == "Audio":
        st.session_state.button1_state = True
        st.session_state.button2_state = False
    elif subsection == "Summary":
        st.session_state.button1_state = False
        st.session_state.button2_state = True

def close_popup():
    st.session_state.selected_audio = None

if __name__ == "__main__":
    main()
