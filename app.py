import streamlit as st
import openai

# Set OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit page setup
st.set_page_config(page_title="Realistic Prompt Generator", page_icon="🎨")
st.title("🧠 Ultra-Realistic Prompt Generator")

st.markdown("Craft vivid, cinematic prompts for AI-generated images with highly detailed control.")

# ---- Presets and Dropdowns ----
style_options = [
    ("Photorealism", "Realistic, highly detailed images with life-like quality."),
    ("Cyberpunk", "Futuristic style blending high-tech with dystopian environments."),
    ("Renaissance", "Classical painting style, highly detailed and dramatic."),
    ("Baroque", "Dramatic and grand style with deep contrast and rich detail."),
    ("Glitch Art", "Digital aesthetic featuring visual glitches and distortion."),
    ("Surrealism", "Dreamlike, illogical, and strange visuals often defying reality."),
    ("Fantasy Illustration", "Highly imaginative, often involving fantasy creatures and mythical landscapes."),
    ("Neo-noir", "Modern take on film noir with a dark, stylish atmosphere.")
]

mood_options = [
    ("Serene and ethereal", "Peaceful, calm, and otherworldly vibes."),
    ("Dark and dystopian", "Gloomy, bleak, and futuristic environment."),
    ("Melancholic and moody", "Sad, introspective, and emotionally heavy mood."),
    ("Chaotic and energetic", "Full of action, fast-paced with high energy."),
    ("Peaceful and meditative", "Calm, serene, and tranquil atmosphere.")
]

lighting_options = [
    ("Golden hour sunlight", "Soft, warm light during the golden hour."),
    ("High contrast neon glow", "Bright neon lights with sharp contrast."),
    ("Soft diffused light", "Gentle, soft light providing even illumination."),
    ("Backlit silhouette", "Light from behind creating dark outlines."),
    ("Harsh studio lighting", "Intense light often used in studio photography.")
]

camera_options = [
    ("Captured with a 35mm lens", "Standard lens providing natural perspective."),
    ("Captured with a 50mm lens", "Standard prime lens, ideal for portraits."),
    ("Aerial drone view", "Top-down view from a high angle, often a bird's eye perspective."),
    ("Macro close-up", "Extreme close-up of objects, highlighting fine details."),
    ("Fisheye lens view", "Wide-angle lens distorting the image with curved lines.")
]

weather_options = [
    ("Clear", "Bright and cloudless skies."),
    ("Rain", "Wet, stormy weather with rain."),
    ("Fog", "Low visibility, misty and foggy conditions."),
    ("Storm", "Dark and intense weather with strong winds and rain."),
    ("Snow", "Cold and snowy with snowflakes falling."),
    ("Overcast", "Cloudy skies with no direct sunlight."),
    ("Unknown", "Ambiguous or undefined weather conditions.")
]

# ---- Inputs ----
subject = st.text_input("🧍 Subject / Character", "A mysterious wanderer")
character_attributes = st.text_input("🔍 Character Attributes", "mid-30s, male, long dark coat, glowing blue eyes, cybernetic hand")
environment = st.text_input("🌆 Environment / Setting", "Abandoned rooftop garden in a futuristic city")
objects = st.text_input("📦 Objects or Key Elements", "Hovering drones, vines crawling up antennas, digital billboard flickering")
weather = st.selectbox("🌦 আবহাওয়া (Weather)", [x[0] for x in weather_options], index=2)
lighting = st.selectbox("💡 আলো (Lighting Style)", [x[0] for x in lighting_options])
mood = st.selectbox("🎭 মুড / আবেগপূর্ণ পরিবেশ (Mood / Emotional Tone)", [x[0] for x in mood_options])
style = st.selectbox("🎨 শৈলী (Artistic Style)", [x[0] for x in style_options])
camera = st.selectbox("📷 ক্যামেরা / লেন্সের বিস্তারিত (Camera / Lens Details)", [x[0] for x in camera_options])
action = st.text_input("🎬 Action / Emotion", "The man gazes across the city, smoke trailing from his coat, lost in memory")
colors = st.text_input("🌈 Color Palette / Textures", "Moody blues, purple shadows, flickering pink neon, wet surfaces with reflections")

abstract = st.text_input("💭 Abstract Concept (Optional)", "A metaphor for isolation in a hyper-connected world")

notes = st.text_area("📝 Extra Notes (Optional)", "Blend cyberpunk neon with noir grain and dramatic backlighting")

# ---- Weather Description ----
weather_descriptions = {
    "Clear": "Clear sky with no clouds, bright daylight.",
    "Rain": "Heavy rain and wet surroundings.",
    "Fog": "Low visibility, mist and foggy.",
    "Storm": "Thunderstorm with heavy rain and lightning.",
    "Snow": "Snow falling gently, cold and frosty.",
    "Overcast": "Overcast skies with no direct sunlight.",
    "Unknown": "Indeterminate or undefined weather conditions."
}

weather_description = weather_descriptions.get(weather, "No description available.")

# ---- System prompt definition ----
system_prompt = """You are a professional prompt engineer specializing in generating highly detailed, vivid, and imaginative prompts for AI image generation.

Your format must always follow this structure:
[Style] | [Subject/Character] | [Environment] | [Details about action/emotion] | [Color Scheme/Lighting/Texture]

Use elevated, visual language and cinematic descriptions.
Follow these rules:
- Focus on character traits, mood, emotion, atmosphere, materials, and depth.
- Include abstract or conceptual ideas when given.
- Blend artistic styles when requested.
- No bullet points. Only output the final prompt in one block.

The goal: craft something a visual artist could bring to life immediately.
"""

# ---- Combine user inputs into a single string ----
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

# ---- Display the prompt generation info ----
if st.button("🎯 Generate Prompt"):
    with st.spinner("Crafting a cinematic prompt..."):
        try:
            # OpenAI API call
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use "gpt-4" if you want the latest model (paid version)
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_combined}
                ],
                temperature=0.8,
                max_tokens=400
            )

            # Extract the result
            result = response['choices'][0]['message']['content'].strip()

            # Display the result in the app
            st.markdown("### 🖼️ Final Prompt")
            st.code(result, language="text")

        except Exception as e:
            st.error(f"Error: {e}")
    
    # Display descriptions (both Bangla and English in small font)
    st.markdown(f"<p class='small-font'><i>Weather Description: {weather_description} (বাংলা: {weather_description})</i></p>", unsafe_allow_html=True)
