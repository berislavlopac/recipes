import os
import sys
import tempfile

import streamlit as st

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from recipes.application.flows import RecipeGenerationFlow

st.set_page_config(page_title="Gemini Chef", page_icon="🥘", layout="wide")


def save_uploaded_file(uploaded_file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return None


# --- UI ---
st.title("🥘 Gemini Vision Chef")
st.markdown("Powered by **Gemini 1.5 Flash** (Vision) and **Gemini 1.5 Pro** (Reasoning).")

with st.sidebar:
    st.header("Settings")

    uploaded_file = st.file_uploader("Take a photo of ingredients", type=["jpg", "png", "jpeg"])
    preferences = st.text_area(
        "What do you feel like eating?", placeholder="e.g. Low carb, 30 mins, spicy"
    )

    start_btn = st.button("Cook!", type="primary")

if start_btn and uploaded_file and preferences:
    if not os.environ.get("GEMINI_API_KEY"):
        st.error("Please provide a Gemini API Key.")
        st.stop()

    image_path = save_uploaded_file(uploaded_file)

    if image_path:
        col_img, col_status = st.columns([1, 2])
        with col_img:
            st.image(image_path, caption="Your Ingredients", width=250)

        with col_status:
            with st.status("Gemini is thinking...", expanded=True) as status:
                st.write("👀 Gemini Flash is scanning the image...")
                flow = RecipeGenerationFlow(image_path=image_path, user_preferences=preferences)

                try:
                    flow.kickoff()

                    detected = flow.state.detected_ingredients
                    recipes = flow.state.final_recipes
                    status.update(label="Done!", state="complete", expanded=False)
                except Exception as e:
                    st.error(f"Flow Error: {e}")
                    st.stop()

        # Results Display
        st.divider()
        c1, c2 = st.columns([1, 2])

        with c1:
            st.subheader("Detected")
            if detected:
                for ing in detected.ingredients:
                    st.success(f"**{ing.name}**")

        with c2:
            st.subheader("Recipes")
            if recipes:
                st.info(f"Chef: {recipes.chef_comment}")
                for r in recipes.recipes:
                    with st.expander(f"🍳 {r.title}"):
                        st.write(f"**Fit:** {r.why_it_fits}")
                        st.caption(f"Time: {r.prep_time} prep / {r.cooking_time} cook")
                        st.markdown("#### Ingredients")
                        st.markdown("\n".join([f"- {x}" for x in r.ingredients_needed]))
                        st.markdown("#### Instructions")
                        for i, s in enumerate(r.instructions):
                            st.markdown(f"**{i + 1}.** {s}")

        os.unlink(image_path)
