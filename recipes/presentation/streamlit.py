import tempfile
from pathlib import Path

import streamlit as st
from PIL import Image, ImageEnhance
from uuid_utils import uuid7

from recipes.application.config import settings
from recipes.application.flows import RecipeGenerationFlow

st.set_page_config(page_title="Brightbeam Vision Chef", page_icon=":man_cook:", layout="wide")


def save_uploaded_file(uploaded_file) -> Path | None:
    # Open image with Pillow
    img: Image.Image = Image.open(uploaded_file)

    # 1. Resize if huge (LLMs struggle with 4k+ resolution sometimes, and it's slow)
    max_size = (1024, 1024)
    img.thumbnail(max_size)

    # 2. Convert to RGB (fixes issues with PNG transparency)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # 3. Enhance Sharpness slightly to help with text/labels
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.5)

    file_path = Path(tempfile.gettempdir()) / f"ingredients_{uuid7().hex}.jpg"

    with file_path.open(mode="wb") as tmp_file:
        img.save(file_path, quality=95)

    return Path(file_path)


def webform():  # noqa: C901
    st.title("🧑‍🍳 Brightbeam Vision Chef")

    with st.sidebar:
        st.header("Settings")

        uploaded_file = st.file_uploader(
            "Take a photo of ingredients", type=["jpg", "png", "jpeg"]
        )
        preferences = st.text_area(
            "What do you feel like eating?", placeholder="e.g. Low carb, 30 mins, spicy"
        )

        start_btn = st.button("Cook!", type="primary")

    if start_btn and uploaded_file:
        image_path = save_uploaded_file(uploaded_file)

        if image_path:
            col_img, col_status = st.columns([1, 2])
            with col_img:
                st.image(image_path, caption="Your Ingredients", width=250)

            with col_status:
                with st.status("Chef is thinking...", expanded=True) as status:
                    status_label = "👀 Scanning the image..."
                    if settings.DEBUG:
                        status_label += f" - {image_path}"
                    st.write(status_label)
                    flow = RecipeGenerationFlow(
                        image_path=str(image_path), user_preferences=preferences or "None."
                    )

                    try:
                        flow.kickoff()
                    except Exception as e:  # noqa: BLE001
                        st.error(f"Flow Error: {e}")
                        st.stop()
                    else:
                        detected = flow.state.detected_ingredients
                        recipes = flow.state.final_recipes
                        status_label = "Done!"
                        if settings.DEBUG:
                            status_label += f" Image description: {detected.image_description}"
                        status.update(label=status_label, state="complete", expanded=False)

            # Results Display
            st.divider()
            c1, c2 = st.columns([1, 2])

            with c1:
                st.subheader("Detected Ingredients")
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

            image_path.unlink()
