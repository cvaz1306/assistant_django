import docx
class docxprocessor():
    def processDocx(docx_file):
        doc = docx.Document(docx_file)
        # Extract the text from the document
        document_text = ""
        for para in doc.paragraphs:
            document_text += para.text + "\n    "
        return document_text