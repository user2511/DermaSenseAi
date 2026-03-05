from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from services.inference_service import generate_response
from PIL import Image
import io

app = FastAPI()


@app.get("/")
def root():
    return {"message": "DermaSense AI Demo Running"}


@app.post("/ask")
async def ask(
    question: str = Form(...),
    image: UploadFile = File(...)
):

    image_path = f"/tmp/{image.filename}"

    with open(image_path, "wb") as f:
        f.write(await image.read())

    answer = generate_response(image_path, question)

    return {"answer": answer}


@app.post("/ask-stream")
async def ask_stream(
    question: str = Form(...),
    image: UploadFile = File(...)
):

    image_bytes = await image.read()

    uploaded_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    async def event_generator():

        async for token in generate_response(uploaded_image, question):
            yield token

    return StreamingResponse(
        event_generator(),
        media_type="text/plain"
    )