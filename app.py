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

# ---- Presets and Dropdowns ---- (Bangla and English Text)
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
    ("ভিনটেজ সাইফাই এবং বারোক প্রভাব (Vintage sci-fi with Baroque influences)", "Vintage sci-fi with Baroque influences"),
    ("সাইবারপঙ্ক এবং ওয়াটারকলার টেক্সচার (Cyberpunk with watercolor textures)", "Cyberpunk with watercolor textures"),
    ("মিনিমালিস্ট রিয়েলিজম এবং গ্লিচ ইফেক্টস (Minimalist realism with glitch effects)", "Minimalist realism with glitch effects"),
    ("ফিল্ম নোয়ার এবং সুররিয়ালিস্ট ড্রিমস্কেপ (Film noir meets surrealist dreamscape)", "Film noir meets surrealist dreamscape")
]

mood_options = [
    ("সুখী ও রহস্যময় (Serene and ethereal)", "Serene and ethereal"),
    ("অন্ধকার এবং দুঃস্বপ্ন (Dark and dystopian)", "Dark and dystopian"),
    ("মনখারাপ এবং বিষণ্ণ (Melancholic and moody)", "Melancholic and moody"),
    ("আত্মবিশ্বাসী এবং শক্তিশালী (Chaotic and energetic)", "Chaotic and energetic"),
    ("শান্তিপূর্ণ ও ধ্যানমগ্ন (Peaceful and meditative)", "Peaceful and meditative")
]

lighting_options = [
    ("সোনালী আলো (Golden hour sunlight)", "Golden hour sunlight"),
    ("উচ্চ কন্ট্রাস্ট নিওন আলো (High contrast neon glow)", "High contrast neon glow"),
    ("সোফট এবং ডিফিউসড আলো (Soft diffused light)", "Soft diffused light"),
    ("ব্যাকলিট সিলুয়েট (Backlit silhouette)", "Backlit silhouette"),
    ("কঠিন স্টুডিও আলো (Harsh studio lighting)", "Harsh studio lighting")
]

camera_options = [
    ("৩৫ মিমি লেন্সের সাথে ক্যাপচার (Captured with a 35mm lens)", "Captured with a 35mm lens"),
    ("৫০ মিমি লেন্সের সাথে ক্যাপচার (Captured with a 50mm lens)", "Captured with a 50mm lens"),
    ("এয়ারিয়াল ড্রোন ভিউ (Aerial drone view)", "Aerial drone view"),
    ("ম্যাক্রো ক্লোজ-আপ (Macro close-up)", "Macro close-up"),
    ("ফিশআই লেন্স ভিউ (Fisheye lens view)", "Fisheye lens view")
]

# ---- Inputs ---- (Initial mixed Bangla, English, and Banglish)
subject = st.text_input("🧍 বিষয় / চরিত্র (Subject / Character)", "A mysterious wanderer")
character_attributes = st.text_input("🔍 চরিত্রের বৈশিষ্ট্য (Character Attributes)", "mid-30s, male, long dark coat, glowing blue eyes, cybernetic hand")
environment = st.text_input("🌆 পরিবেশ / সেটিং (Environment / Setting)", "Abandoned rooftop garden in a futuristic city")
objects = st.text_input("📦 অবজেক্টস বা মূল উপাদান (Objects or Key Elements)", "Hovering drones, vines crawling up antennas, digital billboard flickering")
weather = st.selectbox("🌦 আবহাওয়া (Weather)", [x[0] for x in weather_options], index=2)
time_of_day = st.selectbox("🕐 সময়ের পার্থক্য (Time of Day)", ["Dawn", "Morning", "Noon", "Golden Hour", "Dusk", "Night", "Midnight"], index=0)
lighting = st.selectbox("💡 আলোর ধরন (Lighting Style)", [x[0] for x in lighting_options])
mood = st.selectbox("🎭 মুড / আবেগ (Mood / Emotional Tone)", [x[0] for x in mood_options])
style = st.selectbox("🎨 শৈলী (Artistic Style)", [x[0] for x in style_options])
artistic_fusion = st.selectbox("🔀 শৈলী সংমিশ্রণ (Style Fusion)", [x[0] for x in fusion_options])
camera = st.selectbox("📷 ক্যামেরা / লেন্স বিশদ (Camera / Lens Details)", [x[0] for x in camera_options])
action = st.text_input("🎬 ক্রিয়া / আবেগ (Action / Emotion)", "The man gazes across the city, smoke trailing from his coat, lost in memory")
colors = st.text_input("🌈 রঙের প্যালেট / টেক্সচার (Color Palette / Textures)", "Moody blues, purple shadows, flickering pink neon, wet surfaces with reflections")
abstract = st.text_input("💭 বিমূর্ত ধারণা (Abstract Concept)", "A metaphor for isolation in a hyper-connected world")
notes = st.text_area("📝 অতিরিক্ত নোট (Extra Notes)", "Blend cyberpunk neon with noir grain and dramatic backlighting")

# Combine the user inputs into a single string
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

# ---- Translate the Bangla Inputs to English (for output) ----
# Here we're translating inputs that might be in Bangla or Banglish to English
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
