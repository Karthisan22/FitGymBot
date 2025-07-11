import os
import streamlit as st
import pandas as pd
import cohere
from dotenv import load_dotenv

# --- Load API Key ---
load_dotenv()
cohere_api_key = "f0CXfqp4A6RdycZf2QXGkipnF5dDitBa5v3IQkig"
co = cohere.Client(cohere_api_key)

# --- Load Dataset (optional, if needed) ---
def load_exercise_data(csv_file):
    if os.path.exists(csv_file):
        return pd.read_csv(csv_file)
    else:
        return None

# --- User Preferences ---
def gather_user_preferences():
    goal = st.selectbox("🏋️ What’s your main fitness goal?",
                        ["Weight Loss", "Build Muscle", "Endurance", "General Fitness"])
    
    experience = st.radio("📊 Your experience level:",
                          ["Beginner", "Intermediate", "Advanced"])
    
    restrictions = st.checkbox("⚠️ Do you have any injuries or limitations?")
    
    return goal, experience, restrictions

# --- Detect if User Asked About an Exercise ---
def user_asks_about_exercise(query):
    keywords = ["describe", "how to", "what is", "guide", "form of"]
    return any(keyword in query.lower() for keyword in keywords)

# --- Extract Exercise Name ---
def extract_exercise_name(query):
    for kw in ["describe", "how to", "what is"]:
        if kw in query.lower():
            return query.lower().split(kw)[-1].strip()
    return query.strip()

def display_exercise_media(exercise_name):
    folder_name = exercise_name.strip().lower()
    folder_path = os.path.join(os.getcwd(), folder_name)

    if not os.path.isdir(folder_path):
        st.error(f"❌ Folder not found: `{folder_name}`")
        return

    media_files = [f for f in os.listdir(folder_path)
                   if f.lower().endswith((".mp4", ".mov", ".webm", ".jpg", ".jpeg", ".png"))]

    if not media_files:
        st.warning("⚠️ No media files (videos or images) found in this folder.")
        return

    for media_file in media_files:
        media_path = os.path.join(folder_path, media_file)
        st.markdown(f"**📂 {media_file}**")
        if media_file.lower().endswith((".mp4", ".mov", ".webm")):
            st.video(media_path)
        else:
            st.image(media_path, use_column_width=True)


# --- Process Query ---
def process_query(user_input, goal, experience, restrictions):
    prompt = f"""
You are a fitness assistant. Based on the user's input, goal: {goal}, experience: {experience}, and restriction: {'Yes' if restrictions else 'No'}, answer the following query:
{user_input}
    """

    response = co.chat(
        model="command-nightly",
        message=prompt
    )

    return response.text

# --- Streamlit App ---
st.set_page_config(page_title="Fitness Chatbot", layout="centered")
st.title("💪 Personalized Fitness & Health Chatbot")

st.markdown("Ask me anything related to your fitness journey!")

# Get user preferences
goal, experience, restrictions = gather_user_preferences()

# Get user input
user_query = st.text_input("💬 Type your question here:")
# --- Input Box ---


if user_query:
    st.subheader("🤖 Bot Response")
    bot_response = process_query(user_query, goal, experience, restrictions)
    st.write(bot_response)

    exercise_query = st.text_input("🔍 Enter Exercise Name (e.g., squat, bench press):")
    if exercise_query:
        st.subheader(f"📁 Media for: `{exercise_query.title()}`")
        display_exercise_media(exercise_query)

