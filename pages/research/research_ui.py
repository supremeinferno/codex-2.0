import os
import tempfile

import streamlit as st

from pages.research.research_index import (
    build_research_index
)

from pages.research.research_engine import (
    answer_research_question
)


def clear_research_cache():

    keys_to_clear = [

        "research_answer_cache",
        "research_question",
        "research_ready",
        "research_papers",
        "research_document_count"

    ]

    for key in keys_to_clear:

        if key in st.session_state:

            del st.session_state[key]


    # Clear cached Chroma / LLM resources
    st.cache_resource.clear()



def render_research():


    # ======================================================
    # HEADER
    # ======================================================

    st.title(
        "Research Mode"
    )

    st.caption(
        "Analyze one or multiple research papers "
        "with targeted retrieval."
    )


    # ======================================================
    # PDF UPLOAD
    # ======================================================

    uploaded_files = st.file_uploader(

        "Upload Research Papers",

        type=["pdf"],

        accept_multiple_files=True,

        key="research_pdf_uploader"

    )


    # ======================================================
    # PROCESS PAPERS
    # ======================================================

    if uploaded_files:


        if st.button(

            "Process Research Papers",

            type="primary",

            key="process_research_papers"

        ):


            with st.spinner(

                "Processing research papers..."

            ):


                image_directory = os.path.join(

                    tempfile.gettempdir(),

                    "codex_research_objects"

                )


                os.makedirs(

                    image_directory,

                    exist_ok=True

                )


                try:


                    # Remove previous research state

                    clear_research_cache()



                    paper_information, total_documents = (

                        build_research_index(

                            uploaded_files,

                            image_directory

                        )

                    )


                    # Save new research state

                    st.session_state[

                        "research_ready"

                    ] = True



                    st.session_state[

                        "research_papers"

                    ] = paper_information



                    st.session_state[

                        "research_document_count"

                    ] = len(uploaded_files)



                    st.session_state[

                        "research_answer_cache"

                    ] = {}



                    st.success(

                        "Research papers processed successfully."

                    )


                except Exception as error:


                    st.error(

                        f"Processing failed: {error}"

                    )



    # ======================================================
    # SHOW PROCESSED PAPERS
    # ======================================================

    if st.session_state.get(

        "research_ready",

        False

    ):


        st.divider()


        st.subheader(

            "Processed Research Papers"

        )


        papers = st.session_state.get(

            "research_papers",

            []

        )


        for paper in papers:


            st.markdown(

                f"**{paper.get('paper_name','Unknown')}**"

            )


            st.caption(

                f"Text chunks: "
                f"{paper.get('text_chunks',0)} | "
                f"Images: "
                f"{paper.get('images',0)} | "
                f"Tables: "
                f"{paper.get('tables',0)}"

            )



    # ======================================================
    # QUICK ANALYSIS
    # ======================================================

    if st.session_state.get(

        "research_ready",

        False

    ):


        st.divider()


        st.subheader(

            "Quick Analysis"

        )


        col1, col2, col3 = st.columns(3)



        # --------------------------------------------------
        # SUMMARY
        # --------------------------------------------------

        with col1:


            if st.button(

                "Short Summary",

                use_container_width=True,

                key="research_summary"

            ):


                st.session_state[

                    "research_question"

                ] = (

                    "Give me a short summary "
                    "of the uploaded research papers."

                )


                st.rerun()



        # --------------------------------------------------
        # TOPICS
        # --------------------------------------------------

        with col2:


            if st.button(

                "Important Topics",

                use_container_width=True,

                key="research_topics"

            ):


                st.session_state[

                    "research_question"

                ] = (

                    "Identify the most important "
                    "topics and concepts in the "
                    "uploaded research papers."

                )


                st.rerun()



        # --------------------------------------------------
        # QUESTIONS
        # --------------------------------------------------

        with col3:


            if st.button(

                "Make Questions",

                use_container_width=True,

                key="research_questions"

            ):


                st.session_state[

                    "research_question"

                ] = (

                    "Create important questions "
                    "based on the uploaded research papers."

                )


                st.rerun()



        # ==================================================
        # USER QUESTION
        # ==================================================

        question = st.chat_input(

            "Ask anything about your research papers..."

        )


        if question:


            st.session_state[

                "research_question"

            ] = question


            st.rerun()



        # ==================================================
        # ANSWER
        # ==================================================

        current_question = st.session_state.get(

            "research_question"

        )


        if current_question:


            st.markdown(

                f"**Question:** {current_question}"

            )


            with st.spinner(

                "Analyzing..."

            ):


                try:


                    answer, source = (

                        answer_research_question(

                            current_question,

                            st.session_state.get(

                                "research_document_count",

                                1

                            )

                        )

                    )


                    st.markdown(

                        "### Answer"

                    )


                    st.write(

                        answer

                    )


                    if source == "cache":


                        st.caption(

                            "⚡ Answer retrieved from cache"

                        )


                except Exception as error:


                    st.error(

                        f"Analysis failed: {error}"

                    )