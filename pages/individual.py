import os
import tempfile
import markdown as md_lib
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

    if "pdf_file" not in st.session_state:
        st.session_state.pdf_file = None

    if "image_file" not in st.session_state:
        st.session_state.image_file = None

    if "knowledge_ready" not in st.session_state:
        st.session_state.knowledge_ready = False

    if "pages" not in st.session_state:
        st.session_state.pages = 0

    if "chunks" not in st.session_state:
        st.session_state.chunks = 0

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "build_error" not in st.session_state:
        st.session_state.build_error = None

    # ======================================================
    # DOCUMENT LIBRARY
    # ======================================================

    left, right = st.columns(
        [1, 2.4],
        gap="large"
    )

    # ======================================================
    # LEFT COLUMN
    # ======================================================

    with left:

        st.markdown(
            """
            <h2 style="
                font-size:28px;
                font-weight:700;
                margin-bottom:25px;
            ">
                Document Library
            </h2>
            """,
            unsafe_allow_html=True
        )

        # --------------------------------------------------
        # PDF
        # --------------------------------------------------

        st.markdown(
            """
            <h3 style="
                font-size:18px;
                margin-bottom:10px;
            ">
                PDF Document
            </h3>
            """,
            unsafe_allow_html=True
        )

        uploaded_pdf = st.file_uploader(
            "Upload PDF",
            type=["pdf"],
            key="pdf_uploader",
            label_visibility="collapsed"
        )

        # --------------------------------------------------
        # Detect NEW PDF
        # --------------------------------------------------

        if uploaded_pdf is not None:

            current_pdf_id = (
                uploaded_pdf.name,
                uploaded_pdf.size
            )

            old_pdf_id = st.session_state.get(
                "pdf_id"
            )

            if current_pdf_id != old_pdf_id:

                # New PDF selected
                st.session_state.pdf_file = uploaded_pdf

                st.session_state.pdf_id = current_pdf_id

                st.session_state.knowledge_ready = False

                st.session_state.pages = 0

                st.session_state.chunks = 0

                st.session_state.messages = []

                st.session_state.build_error = None

        # --------------------------------------------------
        # Show uploaded PDF
        # --------------------------------------------------

        if st.session_state.pdf_file is not None:

            pdf = st.session_state.pdf_file

            st.success(
                f"PDF: {pdf.name}"
            )

            if st.button(
                "Remove PDF",
                use_container_width=True
            ):

                # Clear PDF state
                st.session_state.pdf_file = None

                st.session_state.pdf_id = None

                st.session_state.knowledge_ready = False

                st.session_state.pages = 0

                st.session_state.chunks = 0

                st.session_state.messages = []

                st.session_state.build_error = None

                # Reset uploader
                st.rerun()

        # --------------------------------------------------
        # IMAGE
        # --------------------------------------------------

        st.markdown(
            """
            <h3 style="
                font-size:18px;
                margin-top:35px;
                margin-bottom:10px;
            ">
                Image
            </h3>
            """,
            unsafe_allow_html=True
        )

        uploaded_image = st.file_uploader(
            "Upload Image",
            type=[
                "png",
                "jpg",
                "jpeg",
                "webp"
            ],
            key="image_uploader",
            label_visibility="collapsed"
        )

        if uploaded_image is not None:

            st.session_state.image_file = uploaded_image

            st.success(
                f"Image: {uploaded_image.name}"
            )

        # ==================================================
        # BUILD KNOWLEDGE BASE
        # ==================================================

        if st.button(
            "Build Knowledge Base",
            use_container_width=True,
            disabled=(
                st.session_state.pdf_file is None
            )
        ):

            pdf = st.session_state.pdf_file

            temp_path = None

            try:

                # ------------------------------------------
                # Save uploaded PDF temporarily
                # ------------------------------------------

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as temp_file:

                    temp_file.write(
                        pdf.getvalue()
                    )

                    temp_path = temp_file.name

                # ------------------------------------------
                # Build Chroma database
                # ------------------------------------------

                with st.spinner(
                    "Building knowledge base..."
                ):

                    pages, chunks = (
                        create_vector_database(
                            temp_path
                        )
                    )

                # ------------------------------------------
                # Store result
                # ------------------------------------------

                st.session_state.pages = pages

                st.session_state.chunks = chunks

                st.session_state.knowledge_ready = True

                st.session_state.build_error = None

                st.session_state.messages = []

                st.success(
                    "Knowledge Base Ready"
                )

            except Exception as e:

                st.session_state.knowledge_ready = False

                st.session_state.build_error = str(e)

            finally:

                # ------------------------------------------
                # Remove temporary PDF
                # ------------------------------------------

                if (
                    temp_path is not None
                    and os.path.exists(temp_path)
                ):

                    os.remove(temp_path)

        # ==================================================
        # ERROR
        # ==================================================

        if st.session_state.build_error:

            st.error(
                "Failed to build knowledge base:\n\n"
                + st.session_state.build_error
            )


    # ======================================================
    # RIGHT COLUMN
    # ======================================================

    with right:

        with st.container(border=True):

            st.markdown(
                """
                <h2 style="
                    font-size:28px;
                    font-weight:700;
                    margin:0 0 20px 0;
                ">
                    Dialogue
                </h2>
                """,
                unsafe_allow_html=True
            )

            # --------------------------------------------------
            # Conversation (CSS-scrollable box, version-proof)
            # --------------------------------------------------

            chat_html = """
            <div style="
                height:450px;
                overflow-y:auto;
                padding:10px 14px;
                border:1px solid rgba(255,255,255,0.1);
                border-radius:10px;
                display:flex;
                flex-direction:column;
                gap:10px;
            ">
            """

            for message in st.session_state.messages:

                is_user = message["role"] == "user"

                bubble_align = "flex-end" if is_user else "flex-start"
                bubble_bg = "#2b5fd9" if is_user else "#2a2a2a"
                bubble_color = "#ffffff"

                # Escape HTML-sensitive characters so message
                # content can't break the layout.
                if is_user:
                    # Plain text for user messages — escape only.
                    content = (
                        message["content"]
                        .replace("&", "&amp;")
                        .replace("<", "&lt;")
                        .replace(">", "&gt;")
                        .replace("\n", "<br>")
                    )
                else:
                    # Render assistant markdown (bold, headers,
                    # code blocks) as real HTML.
                    content = md_lib.markdown(
                        message["content"],
                        extensions=["fenced_code", "tables"]
                    )

                chat_html += f"""
                <div style="
                    align-self:{bubble_align};
                    background:{bubble_bg};
                    color:{bubble_color};
                    padding:10px 14px;
                    border-radius:12px;
                    max-width:80%;
                    font-size:15px;
                    line-height:1.4;
                ">
                    {content}
                </div>
                """

            chat_html += """
                <div id="chat-bottom-anchor"></div>
            </div>
            <script>
                var anchor = document.getElementById("chat-bottom-anchor");
                if (anchor) {
                    anchor.scrollIntoView({behavior: "instant", block: "end"});
                }
            </script>
            """

            chat_html = "\n".join(
                line.strip()
                for line in chat_html.split("\n")
            )

            st.markdown(
                chat_html,
                unsafe_allow_html=True
            )
        # --------------------------------------------------
        # Suggested Questions
        # --------------------------------------------------

        st.markdown(
            "### Suggested Questions"
        )

        col1, col2 = st.columns(2)

        with col1:

            summarize = st.button(
                "Summarize Document",
                use_container_width=True
            )

            key_points = st.button(
                "Extract Key Points",
                use_container_width=True
            )

        with col2:

            notes = st.button(
                "Generate Notes",
                use_container_width=True
            )

            diagrams = st.button(
                "Explain Diagrams",
                use_container_width=True
            )

        # --------------------------------------------------
        # Response controls
        # --------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            response_style = st.selectbox(
                "Response Style",
                [
                    "📖 Accurate",
                    "⚖️ Balanced",
                    "🎨 Creative"
                ]
            )

        with col2:

            answer_length = st.selectbox(
                "Answer Length",
                [
                    "Short",
                    "Medium",
                    "Detailed"
                ]
            )

        # --------------------------------------------------
        # Suggested question mapping
        # --------------------------------------------------

        question = None

        if summarize:

            question = (
                "Summarize this document."
            )

        elif key_points:

            question = (
                "Extract the key points "
                "from this document."
            )

        elif notes:

            question = (
                "Generate useful study notes "
                "from this document."
            )

        elif diagrams:

            question = (
                "Explain the diagrams "
                "present in this document."
            )

        # --------------------------------------------------
        # Chat input
        # --------------------------------------------------

        user_question = st.chat_input(
            "Ask anything about your document..."
        )

        if user_question:

            question = user_question

        # --------------------------------------------------
        # Generate response
        # --------------------------------------------------

        if question:

            if not st.session_state.knowledge_ready:

                st.warning(
                    "Please build the Knowledge Base first."
                )

            else:

                st.session_state.messages.append(
                    {
                        "role": "user",
                        "content": question
                    }
                )

                try:

                    with st.spinner(
                        "Searching document..."
                    ):

                        answer, docs = (
                            generate_response(
                                question=question,
                                image=(
                                    st.session_state.image_file
                                ),
                                response_style=response_style,
                                answer_length=answer_length
                            )
                        )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    )

                    st.rerun()

                except Exception as e:

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content":
                            f"Error: {str(e)}"
                        }
                    )

                    st.rerun()