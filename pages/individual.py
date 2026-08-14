import os
import tempfile

import streamlit as st

from create_database import create_vector_database
from main import generate_response


# ==========================================================
# INDIVIDUAL ANALYSIS
# ==========================================================

def render_individual():

    # ======================================================
    # SESSION STATE
    # ======================================================

    if "individual_db_ready" not in st.session_state:
        st.session_state.individual_db_ready = False

    if "individual_pages" not in st.session_state:
        st.session_state.individual_pages = 0

    if "individual_chunks" not in st.session_state:
        st.session_state.individual_chunks = 0

    if "individual_messages" not in st.session_state:
        st.session_state.individual_messages = []

    if "individual_sources" not in st.session_state:
        st.session_state.individual_sources = []

    if "individual_preset" not in st.session_state:
        st.session_state.individual_preset = ""


    # ======================================================
    # PAGE HEADER
    # ======================================================

    st.title("Individual Analysis")

    st.caption(
        "Analyze a single document or image using "
        "Codex's multimodal retrieval pipeline."
    )


    # ======================================================
    # MAIN LAYOUT
    # ======================================================

    left, right = st.columns(
        [0.85, 2.15],
        gap="large",
    )


    # ======================================================
    # LEFT PANEL — DOCUMENT LIBRARY
    # ======================================================

    with left:

        st.subheader("Document Library")


        # --------------------------------------------------
        # PDF
        # --------------------------------------------------

        st.markdown("**PDF Document**")

        pdf = st.file_uploader(
            "Upload PDF",
            type=["pdf"],
            key="individual_pdf",
            label_visibility="collapsed",
        )


        # --------------------------------------------------
        # IMAGE
        # --------------------------------------------------

        st.markdown("**Image**")

        image = st.file_uploader(
            "Upload Image",
            type=[
                "png",
                "jpg",
                "jpeg",
                "webp",
            ],
            key="individual_image",
            label_visibility="collapsed",
        )


        # --------------------------------------------------
        # IMAGE PREVIEW
        # --------------------------------------------------

        if image:

            st.markdown("**Image Preview**")

            st.image(
                image,
                use_container_width=True,
            )


        # --------------------------------------------------
        # BUILD KNOWLEDGE BASE
        # --------------------------------------------------

        st.write("")

        build_library = st.button(
            "Build Knowledge Base",
            key="individual_build",
            use_container_width=True,
        )


        # --------------------------------------------------
        # BUILD DATABASE
        # --------------------------------------------------

        if build_library:

            if pdf is None:

                st.warning(
                    "Please upload a PDF first."
                )

            else:

                pdf_path = None

                try:

                    # Create temporary PDF
                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".pdf",
                    ) as tmp:

                        tmp.write(
                            pdf.getvalue()
                        )

                        pdf_path = tmp.name


                    # Build vector database
                    with st.spinner(
                        "Processing PDF and building knowledge base..."
                    ):

                        pages, chunks = (
                            create_vector_database(
                                pdf_path
                            )
                        )


                    # Save information
                    st.session_state.individual_db_ready = True

                    st.session_state.individual_pages = pages

                    st.session_state.individual_chunks = chunks

                    # Clear old conversation
                    st.session_state.individual_messages = []

                    st.session_state.individual_sources = []


                    st.success(
                        "Knowledge Base Ready"
                    )


                except Exception as e:

                    st.error(
                        f"Failed to build knowledge base: {e}"
                    )


                finally:

                    if (
                        pdf_path
                        and os.path.exists(pdf_path)
                    ):

                        os.remove(pdf_path)


        # --------------------------------------------------
        # STATUS
        # --------------------------------------------------

        st.write("")

        st.markdown("**Status**")


        if pdf:

            st.success(
                f"PDF: {pdf.name}"
            )

        else:

            st.info(
                "No PDF uploaded"
            )


        if image:

            st.success(
                "Image uploaded"
            )

        else:

            st.info(
                "Image not uploaded"
            )


        # --------------------------------------------------
        # KNOWLEDGE BASE STATUS
        # --------------------------------------------------

        if st.session_state.individual_db_ready:

            st.success(
                "Knowledge Base: Ready"
            )

            st.caption(
                f"{st.session_state.individual_pages} pages • "
                f"{st.session_state.individual_chunks} chunks"
            )

        else:

            st.info(
                "Knowledge Base: Not Ready"
            )


    # ======================================================
    # RIGHT PANEL — DIALOGUE
    # ======================================================

    with right:

        st.subheader("Dialogue")


        # --------------------------------------------------
        # WELCOME
        # --------------------------------------------------

        if not st.session_state.individual_messages:

            with st.container(border=True):

                st.markdown(
                    "### Welcome to Individual Analysis"
                )

                st.write(
                    "Upload a PDF and optionally provide an image. "
                    "Build the knowledge base and start asking "
                    "questions about your content."
                )


        # --------------------------------------------------
        # SUGGESTED QUESTIONS
        # --------------------------------------------------

        if not st.session_state.individual_messages:

            st.markdown(
                "#### Suggested Questions"
            )

            q1, q2 = st.columns(2)


            with q1:

                if st.button(
                    "Summarize Document",
                    key="individual_summary",
                    use_container_width=True,
                ):

                    st.session_state.individual_preset = (
                        "Summarize this document."
                    )


                if st.button(
                    "Extract Key Points",
                    key="individual_points",
                    use_container_width=True,
                ):

                    st.session_state.individual_preset = (
                        "Extract the key points from this document."
                    )


            with q2:

                if st.button(
                    "Generate Notes",
                    key="individual_notes",
                    use_container_width=True,
                ):

                    st.session_state.individual_preset = (
                        "Generate concise notes from this document."
                    )


                if st.button(
                    "Explain Diagrams",
                    key="individual_diagrams",
                    use_container_width=True,
                ):

                    st.session_state.individual_preset = (
                        "Explain the diagrams in this document."
                    )


            st.divider()


        # --------------------------------------------------
        # CHAT HISTORY
        # --------------------------------------------------

        chat_area = st.container(
            height=450,
        )


        with chat_area:

            if not st.session_state.individual_messages:

                st.info(
                    "No conversation yet."
                )

            else:

                for message in (
                    st.session_state.individual_messages
                ):

                    with st.chat_message(
                        message["role"]
                    ):

                        st.markdown(
                            message["content"]
                        )


        # --------------------------------------------------
        # CHAT INPUT
        # --------------------------------------------------

        preset = st.session_state.individual_preset

        question = st.chat_input(
            "Ask anything about your document...",
            key="individual_chat",
        )


        # --------------------------------------------------
        # PRESET QUESTION
        # --------------------------------------------------

        if question is None and preset:

            question = preset

            st.session_state.individual_preset = ""


    # ======================================================
    # QUESTION PROCESSING
    # ======================================================

    if question:

        if not st.session_state.individual_db_ready:

            st.warning(
                "Please build the knowledge base before "
                "asking questions."
            )

            return


        # --------------------------------------------------
        # USER MESSAGE
        # --------------------------------------------------

        st.session_state.individual_messages.append(
            {
                "role": "user",
                "content": question,
            }
        )


        # --------------------------------------------------
        # GENERATE RESPONSE
        # --------------------------------------------------

        with st.spinner(
            "Searching document and generating response..."
        ):

            try:

                answer, docs = generate_response(
                    question=question,
                    image=image,
                    response_style="⚖️ Balanced",
                    answer_length="Medium",
                )

            except Exception as e:

                answer = (
                    "An error occurred while generating "
                    f"the response:\n\n{e}"
                )

                docs = []


        # --------------------------------------------------
        # ASSISTANT MESSAGE
        # --------------------------------------------------

        st.session_state.individual_messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )


        # --------------------------------------------------
        # SOURCES
        # --------------------------------------------------

        st.session_state.individual_sources = docs


        # --------------------------------------------------
        # REFRESH
        # --------------------------------------------------

        st.rerun()


    # ======================================================
    # RETRIEVED SOURCES
    # ======================================================

    if st.session_state.individual_sources:

        st.divider()

        with st.expander(
            "Retrieved Sources",
            expanded=False,
        ):

            for index, doc in enumerate(
                st.session_state.individual_sources,
                start=1,
            ):

                page = doc.metadata.get(
                    "page",
                    "?",
                )

                st.markdown(
                    f"### Source {index} · Page {page}"
                )

                st.write(
                    doc.page_content
                )

                st.divider()