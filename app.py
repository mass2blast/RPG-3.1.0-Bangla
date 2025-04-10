import streamlit as st
import openai
from googletrans import Translator

# Initialize translator
translator = Translator()

# Set OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit config
st.set_page_config(page_title="Bangla Realistic Prompt Generator", page_icon="🎨")
st.title("🧠 বাস্তবধর্মী প্রম্পট জেনারেটর (Realistic Prompt Generator)")

st.markdown("AI ইমেজ তৈরির জন্য বিস্তৃত ও সিনেমাটিক প্রম্পট তৈরি করুন।")

# ---- Dropdown Options in Bangla ----
style_options = {
    "ফটোরিয়ালিজম": "Photorealism",
    "সাইবারপাঙ্ক": "Cyberpunk",
    "রেনেসাঁ": "Renaissance",
    "বারোক": "Baroque",
    "গ্লিচ আর্ট": "Glitch Art",
    "সাররিয়ালিজম": "Surrealism",
    "ফ্যান্টাসি ইলাস্ট্রেশন": "Fantasy Illustration",
    "নিও-নোয়ার": "Neo-noir"
}

fusion_options = {
    "কোনটি না": "None",
    "ভিনটেজ সাই-ফাই এবং বারোক": "Vintage sci-fi with Baroque influences",
    "সাইবারপাঙ্ক এবং ওয়াটারকালার": "Cyberpunk with watercolor textures",
    "মিনিমালিস্ট এবং গ্লিচ": "Minimalist realism with glitch effects",
    "নোয়ার এবং স্বপ্নদৃশ্য": "Film noir meets surrealist dreamscape"
}

mood_options = {
    "শান্ত এবং ঐশ্বরিক": "Serene and ethereal",
    "অন্ধকার এবং ধ্বংসাত্মক": "Dark and dystopian",
    "বিষণ্ন এবং আবেগপ্রবণ": "Melancholic and moody",
    "অগোছালো এবং উদ্দীপনাময়": "Chaotic and energetic",
    "নিরব এবং ধ্যানমগ্ন": "Peaceful and meditative"
}

lighting_options = {
    "গোল্ডেন আওয়ার আলো": "Golden hour sunlight",
    "নিয়ন আলো": "High contrast neon glow",
    "নরম আলো": "Soft diffused light",
    "ব্যাকলিট সিলুয়েট": "Backlit silhouette",
    "হার্শ স্টুডিও আলো": "Harsh studio lighting"
}

camera_options = {
    "৩৫মিমি লেন্স": "Captured with a 35mm lens",
    "৫০মিমি লেন্স": "Captured with a 50mm lens",
    "ড্রোন ভিউ": "Aerial drone view",
    "ম্যাক্রো ক্লোজ-আপ": "Macro close-up",
    "ফিশআই লেন্স": "Fisheye lens view"
}

# ---- Input Translator Function ----
def translate_if_needed(text):
    if text.strip() == "":
        return ""
    detected = translator.detect(text)
    if detected.lang != 'en':
        return translator.translate(text, dest='en').text
    return text

# ---- Inputs (freeform) ----
subject = translate_if_needed(st.text_input("🧍 বিষয়বস্তু / চরিত্র", "একজন রহস্যময় পথিক"))
character_attributes = translate_if_needed(st.text_input("🔍 চরিত্রের বৈশিষ্ট্য", "৩০ বছর বয়সী, পুরুষ, লম্বা কোট, নীল চোখ, সাইবার হাত"))
environment = translate_if_needed(st.text_input("🌆 পরিবেশ / স্থান", "ভবনের ছাদে একটি পরিত্যক্ত বাগান"))
objects = translate_if_needed(st.text_input("📦 গুরুত্বপূর্ণ বস্তু", "ড্রোন, লতাপাতা, ডিজিটাল বিলবোর্ড"))
weather = st.selectbox("🌦 আবহাওয়া", ["পরিষ্কার", "বৃষ্টি", "কুয়াশা", "ঝড়", "তুষার", "মেঘলা", "অজানা"])
time_of_day = st.selectbox("🕐 সময়", ["ভোর", "সকাল", "দুপুর", "গোল্ডেন আওয়ার", "সন্ধ্যা", "রাত", "মধ্যরাত"])
lighting_bn = st.selectbox("💡 আলো", list(lighting_options.keys()))
mood_bn = st.selectbox("🎭 মুড / আবেগ", list(mood_options.keys()))
style_bn = st.selectbox("🎨 আর্ট স্টাইল", list(style_options.keys()))
fusion_bn = st.selectbox("🔀 স্টাইল ফিউশন", list(fusion_options.keys()))
camera_bn = st.selectbox("📷 ক্যামেরা / লেন্স", list(camera_options.keys()))
action = translate_if_needed(st.text_input("🎬 কার্যকলাপ / অনুভূতি", "সে শহরের দিকে তাকিয়ে আছে, ধোঁয়া তার কোট থেকে বের হচ্ছে"))
colors = translate_if_needed(st.text_input("🌈 রঙ ও টেক্সচার", "নীল ও বেগুনি ছায়া, ঝলমলে গোলাপি নিয়ন"))
abstract = translate_if_needed(st.text_input("💭 বিমূর্ত ভাবনা (ঐচ্ছিক)", "একটি সংযুক্ত সমাজে বিচ্ছিন্নতার প্রতিচ্ছবি"))
notes = translate_if_needed(st.text_area("📝 অতিরিক্ত মন্তব্য (ঐচ্ছিক)", "সাইবারপাঙ্ক এবং নোয়ারের মিশ্রণ"))

# System prompt
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

# Final data formatting
user_combined = f"""Style: {style_options[style_bn]}
Artistic Fusion: {fusion_options[fusion_bn]}
Subject: {subject}
Character Details: {character_attributes}
Environment: {environment}
Objects/Scene Elements: {objects}
Time of day: {time_of_day}
Weather: {weather}
Lighting: {lighting_options[lighting_bn]}
Mood: {mood_options[mood_bn]}
Camera Details: {camera_options[camera_bn]}
Action/Emotion: {action}
Color Palette & Texture: {colors}
Abstract/Conceptual Notes: {abstract}
Extra Notes: {notes}"""

# Generate Prompt
if st.button("🎯 প্রম্পট তৈরি করুন"):
    with st.spinner("সিনেমাটিক প্রম্পট তৈরি করা হচ্ছে..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_combined}
                ],
                temperature=0.8,
                max_tokens=400
            )

            result = response["choices"][0]["message"]["content"].strip()

            st.markdown("### 🖼️ Final English Prompt")
            st.code(result, language="text")

        except Exception as e:
            st.error(f"❌ Error: {e}")
