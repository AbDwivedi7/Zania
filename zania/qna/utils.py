import PyPDF2
import os
import json
from django.core.files.storage import default_storage
from langchain.document_loaders.json_loader import JSONLoader

def parse_pdf_file(file):
    try:
        text_list = []
        sources_list = []

        pdf_reader = PyPDF2.PdfReader(file)
        for page, content in enumerate(pdf_reader.pages):
            page_obj = content
            text = page_obj.extract_text()
            page_obj.clear()
            text_list.append(text)
            sources_list.append(file.name + "_page_"+str(page))
        return [text_list,sources_list]
    except Exception as e:
        print(e, "Exception")
        return []

def parse_json_file(file):
    try:
        file_exists = os.path.isfile("data.json")
        if file_exists:
            os.remove("data.json")
        _ = default_storage.save("data.json", file)
        loader = JSONLoader("data.json", jq_schema='.[].comment', text_content=False)
        docs = loader.load()

        text_list = []
        sources_list = []
        for doc in docs:
            doc_dict = doc.dict()
            text_list.append(doc_dict["page_content"])
            sources_list.append(doc_dict["metadata"]["source"] + "_line_" + str(doc_dict["metadata"]["seq_num"]))
        return [text_list,sources_list]
    
    except Exception as e:
        print("parse_json_file:", e)
        return []