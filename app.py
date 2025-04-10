import streamlit as st
import openai

# Set OpenAI API key from secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit page setup
st.set_page_config(page_title="Realistic Prompt Generator", page_icon="🎨")
st.title("🧠 Ultra-Realistic Prompt Generator")

st.markdown("Craft vivid, cinematic prompts for AI-generated images with highly detailed control.")

# ---- Presets and Dropdowns ----
style_options = [
    "Photorealism", "Cyberpunk", "Renaissance", "Baroque", "Glitch Art", "Surrealism", "Fantasy Illustration", "Neo-noir"
]

fusion_options = [
    "None", "Vintage sci-fi with Baroque influences", "Cyberpunk with watercolor textures",
    "Minimalist realism with glitch effects", "Film noir meets surrealist dreamscape"
]

mood_options = [
    "Serene and ethereal", "Dark and dystopian", "Melancholic and moody", "Chaotic and energetic", "Peaceful and meditative"
]

lighting_options = [
    "Golden hour sunlight", "High contrast neon glow", "Soft diffused light", "Backlit silhouette", "Harsh studio lighting"
]

camera_options = [
    "Captured with a 35mm lens", "Captured with a 50mm lens", "Aerial drone view", "Macro close-up", "Fisheye lens view"
]

# ---- Inputs ----
subject = st.text_input("🧍 Subject / Character", "A mysterious wanderer")
character_attributes = st.text_input("🔍 Character Attributes", "mid-30s, male, long dark coat, glowing blue eyes, cybernetic hand")
environment = st.text_input("🌆 Environment / Setting", "Abandoned rooftop garden in a futuristic city")
objects = st.text_input("📦 Objects or Key Elements", "Hovering drones, vines crawling up antennas, digital billboard flickering")
weather = st.selectbox("🌦 Weather", ["Clear", "Rain", "Fog", "Storm", "Snow", "Overcast", "Unknown"], index=2)
time_of_day = st.selectbox("🕐 Time of Day", ["Dawn", "Morning", "Noon", "Golden Hour", "Dusk", "Night", "Midnight"], index=0)
lighting = st.selectbox("💡 Lighting Style", lighting_options)
mood = st.selectbox("🎭 Mood / Emotional Tone", mood_options)
style = st.selectbox("🎨 Artistic Style", style_options)
artistic_fusion = st.selectbox("🔀 Style Fusion", fusion_options)
camera = st.selectbox("📷 Camera / Lens Details", camera_options)
action = st.text_input("🎬 Action / Emotion", "The man gazes across the city, smoke trailing from his coat, lost in memory")
colors = st.text_input("🌈 Color Palette / Textures", "Moody blues, purple shadows, flickering pink neon, wet surfaces with reflections")
abstract = st.text_input("💭 Abstract Concept (Optional)", "A metaphor for isolation in a hyper-connected world")
notes = st.text_area("📝 Extra Notes (Optional)", "Blend cyberpunk neon with noir grain and dramatic backlighting")

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

# Button to trigger prompt generation
if st.button("🎯 Generate Prompt"):
    with st.spinner("Crafting a cinematic prompt..."):
        try:
            # OpenAI API call using the updated method for completions
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use "gpt-4" if you want the latest model (paid version)
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_combined}
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
