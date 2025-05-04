from docx import Document

document = Document("C:\\Users\\danil\\Desktop\\Lectures\\DiplomWork\\ВКР, текст.docx")

def checking_paragraphs_on_line_spacing(doc: Document):
    for paragraph in doc.paragraphs:
        if paragraph.paragraph_format.line_spacing is None:
            print(paragraph.style.paragraph_format.line_spacing)
        else:
            print(paragraph.paragraph_format.line_spacing)

checking_paragraphs_on_line_spacing(document)