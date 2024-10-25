from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
import random

# 각 class_id에 해당하는 콘텐츠를 배열에 미리 정의
ping = [
    None,  # class_id 0은 없으므로 None으로 설정
    {"ping_name": "핑1", "image_path": "/static/images/1.webp", "description": "핑1 설명"},
    {"ping_name": "핑2", "image_path": "/static/images/2.webp", "description": "핑2 설명"},
    {"ping_name": "핑3", "image_path": "/static/images/3.webp", "description": "핑3 설명"},
    {"ping_name": "핑4", "image_path": "/static/images/4.webp", "description": "핑4 설명"},
    {"ping_name": "핑5", "image_path": "/static/images/5.webp", "description": "핑5 설명"},
    {"ping_name": "핑6", "image_path": "/static/images/6.webp", "description": "핑6 설명"},
    {"ping_name": "핑7", "image_path": "/static/images/7.webp", "description": "핑7 설명"},
    {"ping_name": "핑8", "image_path": "/static/images/8.webp", "description": "핑8 설명"},
    {"ping_name": "핑9", "image_path": "/static/images/9.webp", "description": "핑9 설명"},
    {"ping_name": "핑10", "image_path": "/static/images/10.webp", "description": "핑10 설명"},
    {"ping_name": "핑11", "image_path": "/static/images/11.webp", "description": "핑11 설명"},
    {"ping_name": "핑12", "image_path": "/static/images/12.webp", "description": "핑12 설명"},
    {"ping_name": "핑13", "image_path": "/static/images/13.jpeg", "description": "핑13 설명"},
    {"ping_name": "핑14", "image_path": "/static/images/14.webp", "description": "핑14 설명"},
    {"ping_name": "핑15", "image_path": "/static/images/15.webp", "description": "핑15 설명"},
    {"ping_name": "핑16", "image_path": "/static/images/16.webp", "description": "핑16 설명"},
    {"ping_name": "핑17", "image_path": "/static/images/16.webp", "description": "핑16 설명"},
    {"ping_name": "핑18", "image_path": "/static/images/16.webp", "description": "핑16 설명"},
    {"ping_name": "핑19", "image_path": "/static/images/16.webp", "description": "핑16 설명"},
    {"ping_name": "핑20", "image_path": "/static/images/16.webp", "description": "핑16 설명"},
    {"ping_name": "핑21", "image_path": "/static/images/16.webp", "description": "핑16 설명"},
    {"ping_name": "핑22", "image_path": "/static/images/16.webp", "description": "핑16 설명"},
    {"ping_name": "핑23", "image_path": "/static/images/16.webp", "description": "핑16 설명"},
    {"ping_name": "핑24", "image_path": "/static/images/16.webp", "description": "핑16 설명"},
    {"ping_name": "핑25", "image_path": "/static/images/16.webp", "description": "핑16 설명"},
    {"ping_name": "핑26", "image_path": "/static/images/16.webp", "description": "핑16 설명"},
    {"ping_name": "핑27", "image_path": "/static/images/16.webp", "description": "핑16 설명"},
    {"ping_name": "핑28", "image_path": "/static/images/16.webp", "description": "핑16 설명"},
    {"ping_name": "핑29", "image_path": "/static/images/16.webp", "description": "핑16 설명"},
    {"ping_name": "핑30", "image_path": "/static/images/16.webp", "description": "핑16 설명"}
]

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서 접근을 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드를 허용
    allow_headers=["*"],  # 모든 HTTP 헤더를 허용
)

# 정적 파일 제공 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 템플릿 설정
templates = Jinja2Templates(directory="templates")

# 업로드된 이미지와 분류 결과를 저장할 리스트
uploaded_images = []

# 랜덤 분류 생성 함수
def random_classification():
    return random.randint(1, 16)

# index.html 렌더링
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 이미지 업로드 처리 및 분류 결과 생성
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # 파일을 읽어서 이미지 데이터로 변환
    image_data = await file.read()

    # 랜덤 분류 결과 생성
    predicted_class = random_classification()

    # 업로드된 이미지와 분류 결과를 리스트에 저장
    image_id = len(uploaded_images)  # 리스트에서의 인덱스가 image_id가 됨
    uploaded_images.append({
        "image_data": image_data,
        "classification_result": predicted_class
    })

    # GET 요청으로 리디렉션 처리
    return RedirectResponse(url=f"/result?image_id={image_id}", status_code=303)

# result.html 렌더링 (image_id 전달, class_id는 배열에서 가져옴)
@app.get("/result", response_class=HTMLResponse)
async def get_result(request: Request, image_id: int):
    image_info = uploaded_images[image_id]
    class_id = image_info["classification_result"]  # 분류 결과에서 class_id 가져오기
    content = ping[class_id]
    return templates.TemplateResponse("class_result.html", {
        "request": request,
        "class_id": class_id,
        "content_text": content["ping_name"],
        "image_path": content["image_path"],
        "description": content["description"]
    })
