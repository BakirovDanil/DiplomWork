import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from docx import Document
from methods.main import paragraphs, checking, dict_checking_code, code_run_text

app = FastAPI()

@app.post("/check_document/")
def check_document(file: UploadFile = File(...)):
    try:
        document = Document(file.file)
        paragraphs(document)
        for element in code_run_text:
            checking(element)
        # Форматируем результат в JSON
        result = {
            "errors": dict_checking_code,
            "valid_codes": [code for code in code_run_text if dict_checking_code.get(code) == "Код соответствует кодировке"]
        }

        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("service:app", port=8080, reload=True)