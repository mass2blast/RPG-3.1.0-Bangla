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

# CSS for styling inputs and descriptions
st.markdown("""
    <style>
        .small-font {
            font-size: 12px;
            color: #555555;
            font-style: italic;
        }
        .input-text {
            color: #333333;
        }
        select {
            color: #003366; /* Change dropdown text color */
        }
    </style>
""", unsafe_allow_html=True)

# Token Tracker (Global variables to track tokens)
if "tokens_used" not in st.session_state:
    st.session_state.tokens_used = 0

# ---- Presets and Dropdowns ----
style_options = [
    ("ফটোরিয়ালিজম (Photorealism)", "Photorealism"),
    ("সাইবারপঙ্ক (Cyberpunk)", "Cyberpunk"),
    ("রেনেসাঁ (Renaissance)", "Renaissance"),
    ("বারোক (Baroque)", "Baroque"),
    ("গ্লিচ আর্ট (Glitch Art)", "Glitch Art"),
    ("সুররিয়ালিজম (Surrealism)", "Surrealism"),
    ("ফ্যান্টাসি ইলাস্ট্রেশন (Fantasy Illustration)", "Fantasy Illustration"),
    ("নিও-নোয়্যার (Neo-noir)", "Neo-noir"),
    ("ওয়াটারকলার (Watercolor)", "Watercolor"),
    ("পাস্টেল ড্রইং (Pastel Drawing)", "Pastel Drawing"),
    ("কার্টুন (Cartoon)", "Cartoon"),
    ("তেল চিত্র (Oil Painting)", "Oil Painting"),
    ("পেন্সিল স্কেচ (Pencil Sketch)", "Pencil Sketch"),
    ("পেপার কলাজ (Paper Collage)", "Paper Collage"),
    ("স্ট্রিট আর্ট (Street Art)", "Street Art"),
    ("সাইকেডেলিক (Psychedelic)", "Psychedelic")
]

style_descriptions = {
    "Photorealism": "Photorealism aims to make artwork appear as realistic as a photograph, with extreme attention to detail.",
    "Cyberpunk": "Cyberpunk art typically blends futuristic technology with dystopian settings, emphasizing neon lights and a high-tech low-life atmosphere.",
    "Renaissance": "Renaissance style focuses on realism, human emotion, and the beauty of nature, often using detailed light and shadow.",
    "Baroque": "Baroque art is dramatic, emotional, and extravagant, characterized by rich colors, intense contrasts, and movement.",
    "Glitch Art": "Glitch Art involves digital distortion, showcasing corrupted visuals that have aesthetic value.",
    "Surrealism": "Surrealism presents dream-like scenes that defy logic, blending reality with the fantastical in often bizarre ways.",
    "Fantasy Illustration": "Fantasy illustration brings to life fantastical worlds, creatures, and characters in a highly imaginative and often whimsical style.",
    "Neo-noir": "Neo-noir is a modern take on the classic film noir genre, often involving dark themes, high contrast, and moody atmospheres.",
    "Watercolor": "Watercolor art is created using water-soluble pigments, often giving a light and translucent feel to the image.",
    "Pastel Drawing": "Pastel drawing involves using soft, powdery pigments for a smooth, velvety texture with rich colors.",
    "Cartoon": "Cartoon art emphasizes exaggerated forms, bright colors, and whimsical characters for comedic or dramatic effects.",
    "Oil Painting": "Oil painting involves the use of oil-based paints, often creating rich, textured, and detailed works.",
    "Pencil Sketch": "Pencil sketches are created with graphite pencils, focusing on shading and fine details in a monochrome style.",
    "Paper Collage": "Paper collage involves assembling cut pieces of paper into artistic compositions, often creating textured and layered effects.",
    "Street Art": "Street art includes art created in public spaces, often featuring graffiti, murals, and urban themes.",
    "Psychedelic": "Psychedelic art is known for vibrant colors, surreal landscapes, and distorted, abstract shapes."
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

# Mood options and descriptions
mood_options = [
    ("সারেন এবং ইথেরিয়াল (Serene and ethereal)", "Serene and ethereal"),
    ("অন্ধকার এবং ডিস্টোপিয়ান (Dark and dystopian)", "Dark and dystopian"),
    ("মেলাঙ্কলিক এবং মুডি (Melancholic and moody)", "Melancholic and moody"),
    ("কাল্পনিক এবং শক্তিশালী (Chaotic and energetic)", "Chaotic and energetic"),
    ("শান্তিপূর্ণ এবং ধ্যানে (Peaceful and meditative)", "Peaceful and meditative")
]

mood_descriptions = {
    "Serene and ethereal": "A calm, peaceful atmosphere with a sense of purity.",
    "Dark and dystopian": "A grim, bleak setting, filled with chaos and desolation.",
    "Melancholic and moody": "An atmosphere full of sadness or introspection.",
    "Chaotic and energetic": "A vibrant, intense setting with a lot of movement and energy.",
    "Peaceful and meditative": "A tranquil scene that invites calmness and reflection."
}

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

# ---- Description Display ----
st.markdown(f"<p class='small-font'>Weather Description: {weather_descriptions[weather]}</p>", unsafe_allow_html=True)
st.markdown(f"<p class='small-font'>Lighting Description: {lighting_descriptions[lighting]}</p>", unsafe_allow_html=True)
st.markdown(f"<p class='small-font'>Mood Description: {mood_descriptions[mood]}</p>", unsafe_allow_html=True)
st.markdown(f"<p class='small-font'>Camera Description: {camera_descriptions[camera]}</p>", unsafe_allow_html=True)
st.markdown(f"<p class='small-font'>Style Description: {style_descriptions[style]}</p>", unsafe_allow_html=True)

# ---- Generate Prompt Button ----
if st.button("🎯 Generate Prompt"):
    combined = f"Style: {style_options[0][1]} | Subject: {subject} | Character Details: {character_attributes} | " \
               f"Environment: {environment} | Objects/Scene Elements: {objects} | Weather: {weather} | Lighting: {lighting} | " \
               f"Mood: {mood} | Camera: {camera} | Action: {action} | Color Palette & Texture: {colors} | " \
               f"Abstract/Conceptual Notes: {abstract} | Extra Notes: {notes}"

    # Translate inputs to English for prompt generation
    translated_combined = translator.translate(combined, src='bn', dest='en').text

    # Call OpenAI API to generate the prompt
    response = openai.Completion.create(
        model="gpt-3.5-turbo",  # or use gpt-4
        prompt=translated_combined,
        temperature=0.7,
        max_tokens=250
    )
    
    generated_prompt = response.choices[0].text.strip()

    # Track tokens used
    tokens_used = response.usage['total_tokens']
    st.session_state.tokens_used += tokens_used

    # Display the result
    st.markdown("### 🖼️ Final Prompt")
    st.code(generated_prompt, language="text")

    # Show token usage
    st.markdown(f"### Tokens Used: {tokens_used}")
    st.markdown(f"### Total Tokens Consumed: {st.session_state.tokens_used}")
