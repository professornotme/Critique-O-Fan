import streamlit as st
import random
from PIL import Image
import cv2
import tempfile

# --- Abstract Colorful Gradient Aesthetic ---
st.markdown("""
<style>
body {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #6a11cb 100%);
  color: #f0f0f0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.css-18e3th9, .main {
  padding-top: 3rem;
}
h1, h2, h3, h4, h5, h6 {
  color: #ffffff !important;
  font-weight: 700;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.6);
}
.stButton>button {
  background: linear-gradient(90deg, #764ba2 0%, #6a11cb 100%);
  color: white;
  border-radius: 12px;
  padding: 10px 24px;
  font-weight: bold;
  font-size: 1.1em;
  box-shadow: 0 4px 8px rgba(118, 75, 162, 0.4);
  transition: background 0.3s ease;
  border: none;
}
.stButton>button:hover {
  background: linear-gradient(90deg, #6a11cb 0%, #764ba2 100%);
}
.stFileUploader {
  background: rgba(255, 255, 255, 0.18);
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}
.stImage > img {
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(106, 17, 203, 0.18);
}
.stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
  color: #f0f0f0 !important;
}
.stAlert, .stSuccess {
  background-color: rgba(106, 17, 203, 0.8) !important;
  border-radius: 12px;
  padding: 10px 20px;
  color: white !important;
  font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Virtual Ceiling Fan Reviewer", page_icon="🌀")
st.title("🌀 Critique-O-Fan")

def video_has_motion(video_path, threshold=50000, sample_rate=10):
    cap = cv2.VideoCapture(video_path)
    ret, prev = cap.read()
    if not ret:
        cap.release()
        return False
    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    motion_detected = False
    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1
        if frame_idx % sample_rate != 0:
            continue
        curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(prev_gray, curr_gray)
        non_zero_count = cv2.countNonZero(diff)
        if non_zero_count > threshold:
            motion_detected = True
            break
        prev_gray = curr_gray
    cap.release()
    return motion_detected

uploaded_file = st.file_uploader(
    "Upload a short video of your ceiling fan",
    type=['mp4', 'mov', 'avi']
)

if uploaded_file:
    # Save to temp and show video
    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        tmpfile.write(uploaded_file.read())
        video_path = tmpfile.name

    st.video(video_path)

    with st.spinner("Checking for fan motion..."):
        has_motion = video_has_motion(video_path)

    if has_motion:
        st.success("✅ Motion detected: Fan appears to be working!")
    else:
        st.warning("⚠️ No significant motion detected. Fan may not be spinning (or video is unclear).")

    reviewers = [
        {
            "name": "Rohit Harikumar",
            "review": """തൂവൽ സ്പർശം പോൽ തഴുകുമീ മന്ദമായ കാറ്റ് 
ആഹാ. വളരെ നൈസർഗികമായ ഈ കാറ്റ് ഞാൻ വളരെയധികം ആസ്വദിച്ചു""",
            "avatar": "rhk.jpg"
        },
        {
            "name": "Arattuannan",
            "review": "First half Nala lag ayrnu.. second half pakshe speed undayrnu. Climax oke aaradukayayrnu. Alin jose perera enik 4000 tharan und",
            "avatar": "arattuannan.jpg"
        },
        {
            "name": "Alin Jose Perera",
            "review": "Fake News",
            "avatar": "ajp.jpg"
        }
    ]

    st.markdown("### Critics' Reviews")
    for reviewer in reviewers:
        try:
            img = Image.open(reviewer["avatar"])
            st.image(img, width=80)
        except Exception as e:
            st.error(f"Could not load image '{reviewer['avatar']}': {e}")
        st.markdown(f"**{reviewer['name']}**")
        st.markdown(f"*{reviewer['review']}*")
        st.markdown("---")
    st.divider()

    reviews = [
        "oru onn onnara karakam ayrnu",
        "pambaram karangi karangi njan 🎵",
        
    ]
    review = random.choice(reviews)
    stars = random.randint(3, 5)
    awards = [
        "Best Supporting Blades",
        "Lifetime Achievement in Rotation",
        "Most Spirited Spin",
        "Viewer’s Choice: Most Consistent Whirl"
    ]
    award = random.choice(awards)

    st.subheader("Summarized Main Review")
    st.markdown(f'<span style="font-size: 1.5em;">“{review}”</span>', unsafe_allow_html=True)
    st.write("Rating:", "★" * stars + "☆" * (5 - stars))
    st.write("Award:", award)
