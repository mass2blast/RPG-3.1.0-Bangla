import streamlit as st
import openai
from googletrans import Translator
import base64
import os

# 🟢 MUST BE FIRST Streamlit command
st.set_page_config(page_title="রিয়ালিস্টিক প্রম্পট জেনারেটর", page_icon="🎨")

# ---------- Branding Section ----------

# Telegram or branding link
branding_url = "https://t.me/YourTelegramChannel"  # Replace with your actual link
logo_path = "logo.png"

def get_base64_logo(logo_path):
    with open(logo_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

if os.path.exists(logo_path):
    logo_base64 = get_base64_logo(logo_path)
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <a href="{branding_url}" target="_blank">
                <img src="data:image/png;base64,{logo_base64}" alt="Logo" style="height:50px;">
            </a>
            <a href="{branding_url}" target="_blank" style="text-decoration: none; font-size: 14px; color: #888;">
                Powered by <strong>YourBrand</strong>
            </a>
        </div>
        <hr style="margin-top: 5px;">
    """, unsafe_allow_html=True)
else:
    st.warning("Logo file not found.")

# Set OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Translator setup
translator = Translator()

# Initialize session state trackers if not present
if 'api_calls' not in st.session_state:
    st.session_state.api_calls = 0
if 'total_tokens' not in st.session_state:
    st.session_state.total_tokens = 0

# ---- Title and Description ----
st.title("🧠 বাস্তবধর্মী প্রম্পট জেনারেটর")
st.markdown("AI চিত্র তৈরির জন্য চিত্রনাট্য স্টাইলের প্রম্পট তৈরি করুন। ইংরেজি, বাংলা বা বাংলিশে ইনপুট দিন।")

# ---- Dropdown Options ----
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

fusion_options = [
    ("কিছুই না (None)", "None"),
    ("ভিনটেজ সাইফাই এবং বারোক প্রভাব", "Vintage sci-fi with Baroque influences"),
    ("সাইবারপঙ্ক এবং ওয়াটারকলার টেক্সচার", "Cyberpunk with watercolor textures"),
    ("মিনিমালিস্ট রিয়েলিজম এবং গ্লিচ ইফেক্টস", "Minimalist realism with glitch effects"),
    ("ফিল্ম নোয়ার এবং সুররিয়ালিস্ট ড্রিমস্কেপ", "Film noir meets surrealist dreamscape")
]

mood_options = [
    ("সুখী ও রহস্যময়", "Serene and ethereal"),
    ("অন্ধকার এবং দুঃস্বপ্ন", "Dark and dystopian"),
    ("মনখারাপ এবং বিষণ্ণ", "Melancholic and moody"),
    ("আত্মবিশ্বাসী এবং শক্তিশালী", "Chaotic and energetic"),
    ("শান্তিপূর্ণ ও ধ্যানমগ্ন", "Peaceful and meditative")
]

lighting_options = [
    ("সোনালী আলো", "Golden hour sunlight"),
    ("উচ্চ কন্ট্রাস্ট নিওন আলো", "High contrast neon glow"),
    ("সোফট এবং ডিফিউসড আলো", "Soft diffused light"),
    ("ব্যাকলিট সিলুয়েট", "Backlit silhouette"),
    ("কঠিন স্টুডিও আলো", "Harsh studio lighting")
]

camera_options = [
    ("৩৫ মিমি লেন্স", "Captured with a 35mm lens"),
    ("৫০ মিমি লেন্স", "Captured with a 50mm lens"),
    ("এয়ারিয়াল ড্রোন ভিউ", "Aerial drone view"),
    ("ম্যাক্রো ক্লোজ-আপ", "Macro close-up"),
    ("ফিশআই লেন্স ভিউ", "Fisheye lens view")
]

weather_options = [
    ("স্পষ্ট", "Clear"),
    ("বৃষ্টি", "Rain"),
    ("কুয়াশা", "Fog"),
    ("ঝড়", "Storm"),
    ("তুষারপাত", "Snow"),
    ("অপরিষ্কার", "Overcast"),
    ("অজানা", "Unknown")
]

# ---- User Inputs ----
subject = st.text_input("🧍 বিষয় / চরিত্র", "A mysterious wanderer")
character_attributes = st.text_input("🔍 বৈশিষ্ট্য", "mid-30s, male, long dark coat, glowing blue eyes, cybernetic hand")
environment = st.text_input("🌆 পরিবেশ", "Abandoned rooftop garden in a futuristic city")
objects = st.text_input("📦 উপাদান", "Hovering drones, vines crawling up antennas, digital billboard flickering")
weather = st.selectbox("🌦 আবহাওয়া", [x[0] for x in weather_options], index=2)
time_of_day = st.selectbox("🕐 সময়", ["Dawn", "Morning", "Noon", "Golden Hour", "Dusk", "Night", "Midnight"], index=0)
lighting = st.selectbox("💡 আলো", [x[0] for x in lighting_options])
mood = st.selectbox("🎭 মুড", [x[0] for x in mood_options])
style = st.selectbox("🎨 শৈলী", [x[0] for x in style_options])
artistic_fusion = st.selectbox("🔀 সংমিশ্রণ", [x[0] for x in fusion_options])
camera = st.selectbox("📷 ক্যামেরা", [x[0] for x in camera_options])
action = st.text_input("🎬 ক্রিয়া", "The man gazes across the city, smoke trailing from his coat, lost in memory")
colors = st.text_input("🌈 রঙের প্যালেট", "Moody blues, purple shadows, flickering pink neon, wet surfaces with reflections")
abstract = st.text_input("💭 বিমূর্ত ধারণা", "A metaphor for isolation in a hyper-connected world")
notes = st.text_area("📝 অতিরিক্ত নোট", "Blend cyberpunk neon with noir grain and dramatic backlighting")

# ---- System Prompt ----
system_prompt = """You are a professional prompt engineer specializing in generating highly detailed, vivid, and imaginative prompts for AI image generation.

Your format must always follow this structure:
[Style] | [Subject/Character] | [Environment] | [Details about action/emotion] | [Color Scheme/Lighting/Texture]

Use elevated, visual language and cinematic descriptions.
The goal: craft something a visual artist could bring to life immediately.
"""

# ---- Combine Inputs ----
user_combined = f"""Style: {style}
Artistic Fusion: {artistic_fusion}
Subject: {subject}
Character Details: {character_attributes}
Environment: {environment}
Objects/Scene Elements: {objects}
Time of day: {time_of_day}
Weather: {weather}
Lighting: {lighting}
Mood: {mood}
Camera Details: {camera}
Action/Emotion: {action}
Color Palette & Texture: {colors}
Abstract/Conceptual Notes: {abstract}
Extra Notes: {notes}"""

# ---- Translate to English ----
translated_combined = translator.translate(user_combined, src='auto', dest='en').text

# ---- Track User Inputs ----
st.write("Tracking Info:")
st.write(f"Subject: {subject}")
st.write(f"Weather: {weather}")
st.write(f"Action: {action}")

# ---- Prompt Generation ----
if st.button("🎯 Generate Prompt"):
    with st.spinner("Crafting a cinematic prompt..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": translated_combined}
                ],
                temperature=0.8,
                max_tokens=400
            )

            result = response['choices'][0]['message']['content'].strip()
            tokens_used = response['usage']['total_tokens']

            st.session_state.total_tokens += tokens_used
            st.session_state.api_calls += 1

            st.markdown("### 🖼️ Final Prompt")
            st.code(result, language="text")
            st.markdown(f"🔄 API Calls Made: {st.session_state.api_calls}")
            st.markdown(f"💬 Total Tokens Consumed: {st.session_state.total_tokens}")

        except Exception as e:
            st.error(f"Error: {e}")
