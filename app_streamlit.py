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
transcribe = pd.read_csv("transcription.csv")
categories = list(summary_df.columns)

def submitted():
    st.session_state.submitted = True

def update_category(category):
    st.session_state.selected_category = category

def update_subcategory(subcategory):
    st.session_state.selected_subcategory = subcategory

analysis_type = ["Summarized", "Individual Audio"]
time_frames = ["April-May"]
subctegories = ["Questions", "Concerns", "Emotions", "Interest", "Transcript"]

# Initialize session state
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None
if 'selected_subcategory' not in st.session_state:
    st.session_state.selected_subcategory = None
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'selected_time_frame' not in st.session_state:
    st.session_state.selected_time_frame = time_frames[0]
if 'selected_analysis_type' not in st.session_state:
    st.session_state.selected_analysis_type = analysis_type[0]  # Default to Summary
if 'selected_audio' not in st.session_state:
    st.session_state.selected_audio = per_audio_df['Audio Name'].unique()[0]

def main():
    st.set_page_config(layout="wide")  

    content = "Real-estate Audio Analysis"
    # Apply CSS styling to remove margin and padding and set the color to green
    styled_component = f'<div style="margin: 0; padding: 1 0; color: #013208; font-size: 2rem">{content}</div>'

    # Display the styled component using st.markdown
    st.markdown(styled_component, unsafe_allow_html=True)

    # Inject custom CSS
    st.markdown(
        """
        <style>
        /* Change the width of the sidebar */
            [data-testid="stSidebar"] {
                width: 300px;  /* Adjust the width as needed */
            }
            
            /* Adjust the main content width to account for the wider sidebar */
            [data-testid="stSidebar"] + div {
                left: 300px;  /* Same as the sidebar width */
        }

        .st-emotion-cache-6qob1r {
            position: relative;
            width: 300px;
            overflow: overlay;
        }

        .st-emotion-cache-dvne4q {
            padding: 3rem 1.5rem;
        }

        .button {
            font-size: 16px !important;
        }
        .special-button {
            font-size: 20px !important;
        }

        .st-emotion-cache-q3uqly {
            font-size: 13px !important;
            background-color: #f0f0f0;
            color: black;
            border: 1px solid #ccc;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        .st-emotion-cache-j6qv4b p {
            font-size: 13px; /* Adjust the font size as needed */
        }
        .st-emotion-cache-13ejsyy {
            display: inline-flex;
            -webkit-box-align: center;
            align-items: center;
            -webkit-box-pack: center;
            justify-content: center;
            font-weight: 300;
            font: 12px !important;
            padding: 0rem 0.5rem;
            border-radius: 0.5rem;
            min-height: 38.4px;
            margin: 0px;
            line-height: 1.6;
            color: inherit;
            width: auto;
            user-select: none;
            background-color: rgb(249, 249, 251);
            border: 1px solid rgba(49, 51, 63, 0.2);
        }

        .st-emotion-cache-1jicfl2 {
            width: 100%;
            padding: 3rem 1rem 10rem;
            min-width: auto;
            max-width: initial;
        }
    
        .button:hover {
            background-color: lightgreen;
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    selected_time = st.sidebar.selectbox("Select Time Period", time_frames, index=time_frames.index(st.session_state.selected_time_frame) if st.session_state.selected_time_frame else 0)
    st.session_state.selected_time_frame = selected_time

    if st.session_state.selected_analysis_type:
        # Create columns for buttons
        col1, col2 = st.sidebar.columns(2)
        
        for idx, category in enumerate(categories):
            if idx % 2 == 0:
                with col1:
                    if st.button(category, type="primary"):
                        update_category(category)
            else:
                with col2:
                    if st.button(category, type="primary"):
                        update_category(category)
    
    selected_analysis_type = st.sidebar.selectbox("Analysis Type", analysis_type)
    st.session_state.selected_analysis_type = selected_analysis_type

    if st.session_state.selected_analysis_type == 'Individual Audio':
        audio_names = per_audio_df['Audio Name'].unique().tolist()
        selected_name = st.sidebar.selectbox("Select Audio", audio_names)
        st.session_state.selected_audio = selected_name

    # Create a big container
    big_container = st.container(height=500)

    # Display buttons horizontally within the big container
    with big_container:
        # Create columns for buttons
        subcategory_cols = st.columns(len(subctegories))
        
        # Track the index for two column layout
        for subcategory, cols in zip(subctegories, subcategory_cols):
            with cols:
                if st.button(subcategory):
                    update_subcategory(subcategory)
    
        if st.session_state.selected_analysis_type == "Summarized":
            if st.session_state.selected_subcategory == 'Transcript':
                st.warning("No Transcript for Summarized Analysis")
                pass
            else:
                try:
                    sb_df = summary_df[summary_df.index == st.session_state.selected_subcategory][st.session_state.selected_category]
                    if len(sb_df) == 0:
                        if not st.session_state.selected_category and st.session_state.selected_subcategory:
                            st.warning("Please Select Category and Subcategory")
                        elif not st.session_state.selected_category:
                            st.warning("Please select Category ")

                    summary_points = ast.literal_eval(sb_df.iloc[0])['Summary']
                    st.write(f"Summarized {st.session_state.selected_subcategory} for {st.session_state.selected_category}:")
                    for point in summary_points:
                        st.write(f"- {point.strip()}")
                except:
                    st.warning("Please select Sub Category")

        elif st.session_state.selected_analysis_type == 'Individual Audio':
            if st.session_state.selected_subcategory == 'Transcript':
                transcription = transcribe[transcribe['audio_name'] == st.session_state.selected_audio]['transcription'].iloc[0]
                st.write(transcription)
            else:
                if not st.session_state.selected_category and st.session_state.selected_subcategory:
                    st.warning("Please Select Category and Subcategory")
                elif not st.session_state.selected_category:
                    st.warning("Please select Category ")
                elif not st.session_state.selected_subcategory:
                    st.warning("Please select SubCategory")
                else:
                    st.write(f"{st.session_state.selected_subcategory} for {st.session_state.selected_category}:")

                    if st.session_state.selected_category == 'All':
                        audio_insights = transcribe[transcribe['audio_name'] == st.session_state.selected_audio]['Insights_new__'].iloc[0]
                        print(ast.literal_eval(audio_insights).keys())
                        if st.session_state.selected_subcategory == 'Interest':
                            summary_points = ast.literal_eval(audio_insights)['Preferences']
                        else:
                            summary_points = ast.literal_eval(audio_insights)[st.session_state.selected_subcategory]
                    else:
                        audio_df = per_audio_df[(per_audio_df["Audio Name"] == st.session_state.selected_audio) & (per_audio_df["Subcategory"] == st.session_state.selected_category)]
                        # summary_points = ast.literal_eval(audio_df[st.session_state.selected_subcategory].iloc[0])
                        print(audio_df.columns)
                        try:

                            if st.session_state.selected_subcategory == 'Interest':
                                summary_points = ast.literal_eval(audio_df['Preferences'].iloc[0])
                            else:
                                summary_points = ast.literal_eval(audio_df[st.session_state.selected_subcategory].iloc[0])
                        except:
                            st.warning(f"No {st.session_state.selected_subcategory} in {st.session_state.selected_category} for {st.session_state.selected_audio}")
                    for point in summary_points:
                        st.write(f"- {point.strip()}")

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
