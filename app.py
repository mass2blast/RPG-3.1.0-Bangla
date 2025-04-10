import streamlit as st
import openai
from googletrans import Translator

# Initialize OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Translator setup for Bangla to English
translator = Translator()

# Streamlit page setup
st.set_page_config(page_title="Realistic Prompt Generator", page_icon="🎨")
st.title("🧠 Ultra-Realistic Prompt Generator")
st.markdown("Craft vivid, cinematic prompts for AI-generated images with highly detailed control.")

# ---- Artistic Styles and their descriptions ----
style_options = [
    ("ফটোরিয়ালিজম (Photorealism)", "Photorealism"),
    ("সাইবারপঙ্ক (Cyberpunk)", "Cyberpunk"),
    ("রেনেসাঁ (Renaissance)", "Renaissance"),
    ("বারোক (Baroque)", "Baroque"),
    ("গ্লিচ আর্ট (Glitch Art)", "Glitch Art"),
    ("সুররিয়ালিজম (Surrealism)", "Surrealism"),
    ("ফ্যান্টাসি ইলাস্ট্রেশন (Fantasy Illustration)", "Fantasy Illustration"),
    ("নিও-নোয়্যার (Neo-noir)", "Neo-noir")
]

style_descriptions = {
    "Photorealism": "Photorealism aims to make artwork appear as realistic as a photograph, with extreme attention to detail.",
    "Cyberpunk": "Cyberpunk art typically blends futuristic technology with dystopian settings, emphasizing neon lights and a high-tech low-life atmosphere.",
    "Renaissance": "Renaissance style focuses on realism, human emotion, and the beauty of nature, often using detailed light and shadow.",
    "Baroque": "Baroque art is dramatic, emotional, and extravagant, characterized by rich colors, intense contrasts, and movement.",
    "Glitch Art": "Glitch Art involves digital distortion, showcasing corrupted visuals that have aesthetic value.",
    "Surrealism": "Surrealism presents dream-like scenes that defy logic, blending reality with the fantastical in often bizarre ways.",
    "Fantasy Illustration": "Fantasy illustration brings to life fantastical worlds, creatures, and characters in a highly imaginative and often whimsical style.",
    "Neo-noir": "Neo-noir is a modern take on the classic film noir genre, often involving dark themes, high contrast, and moody atmospheres."
}

# ---- Inputs ----
subject = st.text_input("🧍 বিষয় / চরিত্র (Subject / Character)", "A mysterious wanderer")
character_attributes = st.text_input("🔍 চরিত্রের বৈশিষ্ট্য (Character Attributes)", "mid-30s, male, long dark coat, glowing blue eyes, cybernetic hand")
environment = st.text_input("🌆 পরিবেশ / সেটিং (Environment / Setting)", "Abandoned rooftop garden in a futuristic city")

# ---- Dropdown for Artistic Style ----
style = st.selectbox("🎨 শৈলী (Artistic Style)", [x[0] for x in style_options])

# Show the description of the selected style
selected_style = [x[1] for x in style_options if x[0] == style][0]
st.markdown(f"### Selected Artistic Style: {selected_style}")
st.markdown(f"**Description**: {style_descriptions[selected_style]}")

# ---- Translate the Bangla Inputs to English (for output) ----
# Here we're translating inputs that might be in Bangla or Banglish to English
user_combined = f"""Style: {style}
Subject: {subject}
Character Details: {character_attributes}
Environment: {environment}"""

translated_combined = translator.translate(user_combined, src='bn', dest='en').text

# Define system_prompt here
system_prompt = """You are a professional prompt engineer specializing in generating highly detailed, vivid, and imaginative prompts for AI image generation.

Your format must always follow this structure:
[Style] | [Subject/Character] | [Environment] | [Details about action/emotion] | [Color Scheme/Lighting/Texture]

Use elevated, visual language and cinematic descriptions.
Follow these rules:
- Focus on character traits, mood, emotion, atmosphere, materials, and depth
- Include abstract or conceptual ideas when given
- Blend artistic styles when requested
- No bullet points. Only output the final prompt in one block.

The goal: craft something a visual artist could bring to life immediately.
"""

# Button to trigger prompt generation
if st.button("🎯 Generate Prompt"):
    with st.spinner("Crafting a cinematic prompt..."):
        try:
            # OpenAI API call using the updated method for completions
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use "gpt-4" if you want the latest model (paid version)
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": translated_combined}
                ],
                temperature=0.8,
                max_tokens=400
            )

            # Extract the result correctly from the response
            result = response['choices'][0]['message']['content'].strip()

            # Display the result in the app
            st.markdown("### 🖼️ Final Prompt")
            st.code(result, language="text")

        except Exception as e:
            st.error(f"Error: {e}")
