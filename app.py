import streamlit as st
from agent import agent, image_store


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="centered"
)


# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.stApp {
    background: #0f1117;
}

.title {
    text-align: center;
    font-size: 48px;
    font-weight: 800;
    margin-top: 30px;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #9ca3af;
    font-size: 18px;
    margin-bottom: 35px;
}

.stTextArea textarea {
    border-radius: 15px;
}

.stButton button {
    width: 100%;
    height: 50px;
    border-radius: 12px;
    font-size: 17px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# =========================
# HEADER
# =========================

st.markdown(
    '<div class="title">🎨 AI Image Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Turn your imagination into an image</div>',
    unsafe_allow_html=True
)


# =========================
# PROMPT INPUT
# =========================

prompt = st.text_area(
    "Describe your image",
    placeholder="Example: A beautiful dog sitting on a mountain during sunset...",
    height=130
)


# =========================
# GENERATE BUTTON
# =========================

if st.button("✨ Generate Image"):

    if not prompt.strip():

        st.warning("Please enter a prompt.")

    else:

        with st.spinner("🎨 Creating your image..."):

            try:

                input_message = {
                    "role": "user",
                    "content": f"Generate an image of {prompt}"
                }

                response = agent.invoke({
                    "messages": [input_message]
                })


                # -------------------------
                # Get image from memory
                # -------------------------

                if "latest" in image_store:

                    st.session_state["image_bytes"] = image_store["latest"]

                    st.success(
                        "✅ Image generated successfully!"
                    )

                else:

                    st.error(
                        "Image was generated but could not be retrieved."
                    )


            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )


# =========================
# IMAGE PREVIEW
# =========================

if "image_bytes" in st.session_state:

    st.markdown("### 🖼️ Preview")

    st.image(
        st.session_state["image_bytes"],
        use_container_width=True
    )


    # =========================
    # DOWNLOAD BUTTON
    # =========================

    st.download_button(
        label="⬇️ Download Image",
        data=st.session_state["image_bytes"],
        file_name="generated_image.png",
        mime="image/png"
    )