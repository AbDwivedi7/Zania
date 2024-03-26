import PyPDF2

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