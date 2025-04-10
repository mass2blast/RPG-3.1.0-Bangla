import streamlit as st
import openai

# Set OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit app config
st.set_page_config(page_title="রিয়ালিস্টিক প্রম্পট জেনারেটর", page_icon="🎨")
st.title("🧠 বাস্তবধর্মী প্রম্পট জেনারেটর")

st.markdown("AI চিত্র তৈরির জন্য চিত্রনাট্য স্টাইলের প্রম্পট তৈরি করুন। ইংরেজি, বাংলা বা বাংলিশে ইনপুট দিন।")

# Dropdown options in Bangla
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
    "না": "None",
    "ভিন্টেজ সাই-ফাই ও বারোক": "Vintage sci-fi with Baroque influences",
    "সাইবারপাঙ্ক ও ওয়াটারকালার": "Cyberpunk with watercolor textures",
    "মিনিমাল রিয়ালিজম ও গ্লিচ": "Minimalist realism with glitch effects",
    "ফিল্ম নোয়ার ও স্বপ্নদৃশ্য": "Film noir meets surrealist dreamscape"
}

mood_options = {
    "শান্ত ও অতীন্দ্রিয়": "Serene and ethereal",
    "অন্ধকার ও ধ্বংসাত্মক": "Dark and dystopian",
    "বিষণ্ণ ও আবেগপ্রবণ": "Melancholic and moody",
    "বিশৃঙ্খল ও গতিশীল": "Chaotic and energetic",
    "শান্তিপূর্ণ ও ধ্যানমগ্ন": "Peaceful and meditative"
}

lighting_options = {
    "সোনালি রোদ": "Golden hour sunlight",
    "নিওন আলো": "High contrast neon glow",
    "নরম আলো": "Soft diffused light",
    "ব্যাকলাইট সিলুয়েট": "Backlit silhouette",
    "হার্শ স্টুডিও লাইট": "Harsh studio lighting"
}

camera_options = {
    "৩৫মিমি লেন্স": "Captured with a 35mm lens",
    "৫০মিমি লেন্স": "Captured with a 50mm lens",
    "ড্রোন ভিউ": "Aerial drone view",
    "ম্যাক্রো ক্লোজ-আপ": "Macro close-up",
    "ফিশ-আই ভিউ": "Fisheye lens view"
}

# Inputs (can be Bangla, English or Banglish)
subject = st.text_input("🧍 চরিত্র / বিষয়", "একজন রহস্যময় ভ্রমণকারী")
character_attributes = st.text_input("🔍 চরিত্রের বৈশিষ্ট্য", "৩০ বছর বয়সী, লম্বা কোট, নীল চোখ, সাইবার হাত")
environment = st.text_input("🌆 পরিবেশ / দৃশ্যপট", "ভবনের ছাদে পরিত্যক্ত বাগান, ভবিষ্যতের শহর")
objects = st.text_input("📦 গুরুত্বপূর্ণ বস্তু", "ড্রোন, অ্যান্টেনায় লতা, ঝলকানি বিলবোর্ড")
weather = st.selectbox("🌦 আবহাওয়া", ["পরিষ্কার", "বৃষ্টি", "কুয়াশা", "ঝড়", "তুষার", "মেঘলা", "অজানা"])
time_of_day = st.selectbox("🕐 সময়", ["ভোর", "সকাল", "দুপুর", "গোল্ডেন আওয়ার", "সন্ধ্যা", "রাত", "মধ্যরাত"])
lighting = st.selectbox("💡 আলো", list(lighting_options.keys()))
mood = st.selectbox("🎭 মুড / আবেগ", list(mood_options.keys()))
style = st.selectbox("🎨 আর্ট স্টাইল", list(style_options.keys()))
artistic_fusion = st.selectbox("🔀 স্টাইল ফিউশন", list(fusion_options.keys()))
camera = st.selectbox("📷 ক্যামেরা / লেন্স", list(camera_options.keys()))
action = st.text_input("🎬 কর্ম / অনুভুতি", "সে শহরজুড়ে তাকিয়ে থাকে, ধোঁয়া তার কোট থেকে উঠে যাচ্ছে")
colors = st.text_input("🌈 রং / টেক্সচার", "নীল, বেগুনি ছায়া, গোলাপি নিওন")
abstract = st.text_input("💭 বিমূর্ত ভাবনা", "একাকীত্বের প্রতীক একটি সংযুক্ত দুনিয়ায়")
notes = st.text_area("📝 অতিরিক্ত নির্দেশনা", "সাইবারপাঙ্ক নিওন ও নোয়ার শৈলী মিশ্রণ করুন")

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

user_combined = f"""Style: {style_options[style]}
Artistic Fusion: {fusion_options[artistic_fusion]}
Subject: {subject}
Character Details: {character_attributes}
Environment: {environment}
Objects/Scene Elements: {objects}
Time of day: {time_of_day}
Weather: {weather}
Lighting: {lighting_options[lighting]}
Mood: {mood_options[mood]}
Camera Details: {camera_options[camera]}
Action/Emotion: {action}
Color Palette & Texture: {colors}
Abstract/Conceptual Notes: {abstract}
Extra Notes: {notes}"""

if st.button("🎯 প্রম্পট তৈরি করুন"):
    with st.spinner("প্রম্পট প্রস্তুত হচ্ছে..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # You can change to "gpt-4" if you want
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_combined}
                ],
                temperature=0.8,
                max_tokens=400
            )

            result = response['choices'][0]['message']['content'].strip()
            total_tokens = response['usage']['total_tokens']

            st.markdown("### 🖼️ তৈরি প্রম্পট")
            st.code(result, language="text")
            st.success(f"🔢 মোট টোকেন ব্যবহৃত হয়েছে: {total_tokens}")

        except Exception as e:
            st.error(f"❌ ত্রুটি ঘটেছে: {e}")
