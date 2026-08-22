import os
import re
import hashlib
import fitz

from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_mistralai import MistralAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import (
    RESEARCH_CHROMA_DB_PATH,
    RESEARCH_COLLECTION_NAME,
    MISTRAL_API_KEY,
)


# =====================================================
# EMBEDDING MODEL
# =====================================================

def load_embeddings():

    return MistralAIEmbeddings(
        api_key=MISTRAL_API_KEY
    )


# =====================================================
# UNIQUE PAPER ID
# =====================================================

def make_paper_id(file_bytes):

    return hashlib.md5(
        file_bytes
    ).hexdigest()[:12]



# =====================================================
# CHECK EXISTING PAPER
# =====================================================

def paper_exists(
    vectorstore,
    paper_id
):

    try:

        result = vectorstore.get(
            where={
                "paper_id": paper_id
            }
        )

        return len(
            result.get("ids", [])
        ) > 0

    except Exception:

        return False



# =====================================================
# SECTION DETECTION
# =====================================================

def is_heading(text):

    text=text.strip()

    if not text:

        return False


    if len(text)>120:

        return False


    patterns=[

        r"^\d+\.\s",

        r"^\d+\.\d+\s",

        r"^(abstract|introduction|"
        r"methodology|methods|"
        r"experiments|results|"
        r"discussion|conclusion|"
        r"references)$"

    ]


    for p in patterns:

        if re.match(
            p,
            text,
            re.IGNORECASE
        ):

            return True


    return False



# =====================================================
# EXTRACT TEXT
# =====================================================

def extract_text(
    pdf_path,
    paper_id,
    paper_name
):

    pdf=fitz.open(
        pdf_path
    )


    docs=[]

    section="Unknown"


    for page_no,page in enumerate(
        pdf,
        start=1
    ):


        text=page.get_text(
            "text"
        )


        lines=[]


        for line in text.splitlines():

            line=line.strip()


            if not line:

                continue


            if is_heading(line):

                section=line

            else:

                lines.append(
                    line
                )


        content="\n".join(
            lines
        )


        if content:


            docs.append(

                Document(

                    page_content=content,

                    metadata={

                        "paper_id":paper_id,

                        "paper_name":paper_name,

                        "page":page_no,

                        "section":section,

                        "type":"text"

                    }

                )

            )


    pdf.close()


    return docs



# =====================================================
# CHUNKING
# =====================================================

def create_chunks(
    documents
):


    splitter=RecursiveCharacterTextSplitter(

        chunk_size=2000,

        chunk_overlap=150

    )


    chunks=splitter.split_documents(
        documents
    )


    for i,chunk in enumerate(chunks):


        chunk.metadata["chunk_id"]=(
            f"chunk_{i}"
        )


        chunk.page_content=(

            f"""
Section:
{chunk.metadata.get('section')}

Page:
{chunk.metadata.get('page')}

Content:

{chunk.page_content}
"""

        )


    return chunks



# =====================================================
# BUILD INDEX
# =====================================================

def build_research_index(
    pdf_files,
    temp_folder
):


    os.makedirs(
        RESEARCH_CHROMA_DB_PATH,
        exist_ok=True
    )


    vectorstore=Chroma(

        persist_directory=
        RESEARCH_CHROMA_DB_PATH,

        collection_name=
        RESEARCH_COLLECTION_NAME,

        embedding_function=
        load_embeddings()

    )


    information=[]



    for pdf in pdf_files:


        data=pdf.getvalue()


        paper_id=make_paper_id(
            data
        )


        if paper_exists(
            vectorstore,
            paper_id
        ):

            information.append({

                "paper_name":pdf.name,

                "status":"Already indexed"

            })

            continue



        path=os.path.join(

            temp_folder,

            f"{paper_id}.pdf"

        )


        with open(
            path,
            "wb"
        ) as f:

            f.write(
                data
            )



        docs=extract_text(

            path,

            paper_id,

            pdf.name

        )


        chunks=create_chunks(
            docs
        )



        if chunks:


            vectorstore.add_documents(
                chunks
            )



        information.append({

            "paper_name":pdf.name,

            "status":"Indexed",

            "chunks":len(chunks)

        })


    return (
        information,
        len(information)
    )