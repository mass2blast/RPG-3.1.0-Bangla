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

# ---- Presets and Dropdowns ----
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

# Weather options and descriptions
weather_options = [
    ("স্পষ্ট (Clear)", "Clear"),
    ("বৃষ্টি (Rain)", "Rain"),
    ("কুয়াশা (Fog)", "Fog"),
    ("ঝড় (Storm)", "Storm"),
    ("তুষার (Snow)", "Snow"),
    ("মেঘলা (Overcast)", "Overcast"),
    ("অজানা (Unknown)", "Unknown")
]

weather_descriptions = {
    "Clear": "Clear weather with no clouds.",
    "Rain": "Raining with showers or light drizzle.",
    "Fog": "Visibility is low due to dense fog.",
    "Storm": "Intense storm with strong winds and heavy rain.",
    "Snow": "Falling snow, creating a cold, frosty atmosphere.",
    "Overcast": "Cloudy skies with no sunlight.",
    "Unknown": "Weather is unspecified or unclear."
}

# Lighting options and descriptions
lighting_options = [
    ("সোনালী ঘণ্টার সূর্য রশ্মি (Golden hour sunlight)", "Golden hour sunlight"),
    ("উচ্চ কনট্রাস্ট নীয়ন গ্লো (High contrast neon glow)", "High contrast neon glow"),
    ("মৃদু পরিবাহিত আলো (Soft diffused light)", "Soft diffused light"),
    ("পেছন থেকে আলোকিত সিলুয়েট (Backlit silhouette)", "Backlit silhouette"),
    ("কঠিন স্টুডিও আলো (Harsh studio lighting)", "Harsh studio lighting")
]

lighting_descriptions = {
    "Golden hour sunlight": "Soft, warm light just before sunset or after sunrise.",
    "High contrast neon glow": "Bright neon colors with dark, moody contrasts.",
    "Soft diffused light": "Gentle light that scatters and softens shadows.",
    "Backlit silhouette": "Light coming from behind the subject, casting a shadow.",
    "Harsh studio lighting": "Strong, direct light, often creating sharp shadows."
}

# Camera options and descriptions
camera_options = [
    ("৩৫ মিমি লেন্সে ধারণ করা (Captured with a 35mm lens)", "Captured with a 35mm lens"),
    ("৫০ মিমি লেন্সে ধারণ করা (Captured with a 50mm lens)", "Captured with a 50mm lens"),
    ("এয়ারিয়াল ড্রোন ভিউ (Aerial drone view)", "Aerial drone view"),
    ("ম্যাক্রো ক্লোজ-আপ (Macro close-up)", "Macro close-up"),
    ("ফিশআই লেন্স ভিউ (Fisheye lens view)", "Fisheye lens view")
]

camera_descriptions = {
    "Captured with a 35mm lens": "A classic, standard lens capturing natural perspectives.",
    "Captured with a 50mm lens": "A prime lens often used for portraits, with shallow depth of field.",
    "Aerial drone view": "A top-down perspective, as seen from a drone.",
    "Macro close-up": "Extreme close-up shots, focusing on small details.",
    "Fisheye lens view": "A wide-angle lens creating a distorted, curved perspective."
}

# ---- Inputs ----
subject = st.text_input("🧍 বিষয় / চরিত্র (Subject / Character)", "A mysterious wanderer")
character_attributes = st.text_input("🔍 চরিত্রের বৈশিষ্ট্য (Character Attributes)", "mid-30s, male, long dark coat, glowing blue eyes, cybernetic hand")
environment = st.text_input("🌆 পরিবেশ / সেটিং (Environment / Setting)", "Abandoned rooftop garden in a futuristic city")
objects = st.text_input("📦 বস্তু বা মূল উপাদান (Objects or Key Elements)", "Hovering drones, vines crawling up antennas, digital billboard flickering")
action = st.text_input("🎬 একশন বা অনুভূতি (Action / Emotion)", "The man gazes across the city, smoke trailing from his coat, lost in memory")
colors = st.text_input("🌈 রঙ প্যালেট / টেক্সচার (Color Palette / Textures)", "Moody blues, purple shadows, flickering pink neon, wet surfaces with reflections")
abstract = st.text_input("💭 বিমূর্ত ধারণা (Optional Abstract Concept)", "A metaphor for isolation in a hyper-connected world")
notes = st.text_area("📝 অতিরিক্ত নোট (Optional Notes)", "Blend cyberpunk neon with noir grain and dramatic backlighting")

# ---- Dropdown for Weather ----
weather = st.selectbox("🌦 আবহাওয়া (Weather)", [x[0] for x in weather_options], index=2)

# Show the description of the selected weather
selected_weather = [x[1] for x in weather_options if x[0] == weather][0]
st.markdown(f"### Selected Weather: {selected_weather}")
st.markdown(f"**Description**: {weather_descriptions[selected_weather]}")

# ---- Dropdown for Lighting ----
lighting = st.selectbox("💡 আলো (Lighting Style)", [x[0] for x in lighting_options])

# Show the description of the selected lighting style
selected_lighting = [x[1] for x in lighting_options if x[0] == lighting][0]
st.markdown(f"### Selected Lighting: {selected_lighting}")
st.markdown(f"**Description**: {lighting_descriptions[selected_lighting]}")

# ---- Dropdown for Camera ----
camera = st.selectbox("📷 ক্যামেরা / লেন্সের বিবরণ (Camera / Lens Details)", [x[0] for x in camera_options])

# Show the description of the selected camera style
selected_camera = [x[1] for x in camera_options if x[0] == camera][0]
st.markdown(f"### Selected Camera: {selected_camera}")
st.markdown(f"**Description**: {camera_descriptions[selected_camera]}")

# ---- Artistic Style Dropdown ----
style = st.selectbox("🎨 শৈলী (Artistic Style)", [x[0] for x in style_options])

# Show the description of the selected style
selected_style = [x[1] for x in style_options if x[0] == style][0]
st.markdown(f"### Selected Artistic Style: {selected_style}")
st.markdown(f"**Description**: {style_descriptions[selected_style]}")

# ---- Translate the Bangla Inputs to English (for output) ----
user_combined = f"""Style: {style}
Subject: {subject}
Character Details: {character_attributes}
Environment: {environment}
Objects/Scene Elements: {objects}
Time of day: {weather}
Lighting: {lighting}
Mood: {mood}
Camera Details: {camera}
Action/Emotion: {action}
Color Palette & Texture: {colors}
Abstract/Conceptual Notes: {abstract}
Extra Notes: {notes}"""

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
