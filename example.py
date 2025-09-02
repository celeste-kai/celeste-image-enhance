import asyncio
import io
import os

import streamlit as st
from celeste_core import ImageArtifact, Provider, list_models
from celeste_core.enums.capability import Capability
from celeste_image_enhance import create_image_enhancer
from PIL import Image
from streamlit_image_comparison import image_comparison


async def main() -> None:
    st.set_page_config(
        page_title="Celeste Image Enhance", page_icon="🔧", layout="wide"
    )
    st.title("🔧 Celeste Image Enhance")

    # Get providers that support image enhancement
    providers = sorted(
        {m.provider for m in list_models(capability=Capability.IMAGE_ENHANCE)},
        key=lambda p: p.value,
    )

    with st.sidebar:
        st.header("⚙️ Configuration")
        provider = st.selectbox(
            "Provider:", [p.value for p in providers], format_func=str.title
        )
        models = list_models(
            provider=Provider(provider), capability=Capability.IMAGE_ENHANCE
        )
        model_names = [m.display_name or m.id for m in models]
        selected_idx = st.selectbox(
            "Model:", range(len(models)), format_func=lambda i: model_names[i]
        )
        model = models[selected_idx].id

        # Enhancement options
        st.subheader("Options")
        enhancement_type = st.selectbox(
            "Enhancement Type", ["enhance", "denoise", "sharpen"]
        )
        scale_factor = (
            st.slider("Scale Factor", 1, 16, 2) if enhancement_type == "enhance" else 1
        )

    st.markdown(f"*Powered by {provider.title()}*")

    # File upload
    uploaded_file = st.file_uploader(
        "Choose an image", type=["jpg", "jpeg", "png"]
    ) or st.selectbox(
        "Or select from data",
        [f"data/{f}" for f in os.listdir("data") if f.endswith((".jpg", ".png"))]
        if os.path.exists("data")
        else [],
    )

    if uploaded_file:
        image_data = (
            uploaded_file.read()
            if hasattr(uploaded_file, "read")
            else open(uploaded_file, "rb").read()
        )

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original")
            st.image(image_data, use_container_width=True)

        image = ImageArtifact(data=image_data)

        if st.button("🔧 Enhance Image", type="primary", use_container_width=True):
            enhancer = create_image_enhancer(Provider(provider), model=model)

            with st.spinner("Enhancing..."):
                result = await enhancer.enhance_image(
                    image=image,
                    enhancement_type=enhancement_type,
                    scale_factor=scale_factor,
                )

                # Store result in session state for comparison
                st.session_state["enhanced_image"] = result.data
                st.session_state["metadata"] = result.metadata

                with col2:
                    st.subheader("Enhanced")
                    st.image(result.data, use_container_width=True)

                    with st.expander("📊 Details"):
                        st.write(f"**Provider:** {provider}")
                        st.write(f"**Model:** {model}")
                        st.write(f"**Enhancement:** {enhancement_type}")
                        if enhancement_type == "enhance":
                            st.write(f"**Scale Factor:** {scale_factor}x")
                        if result.metadata:
                            st.json(result.metadata)

        # Show comparison slider if enhanced image exists
        if "enhanced_image" in st.session_state:
            st.markdown("---")
            st.subheader("🔍 Before/After Comparison")

            # Create comparison slider
            original_pil = Image.open(io.BytesIO(image_data))
            enhanced_pil = Image.open(io.BytesIO(st.session_state["enhanced_image"]))

            image_comparison(
                img1=original_pil,
                img2=enhanced_pil,
                label1="Original",
                label2="Enhanced",
                width=700,
            )

    st.markdown("---")
    st.caption("Built with Streamlit • Powered by Celeste")


if __name__ == "__main__":
    asyncio.run(main())
