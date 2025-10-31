from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse


app = FastAPI()

# 기존 엔드포인트
@app.get("/")
def read_root():
    return {"message": "Hello NKS!"}

@app.get("/healthz")
def health_check():
    return {"status": "ok"}


# DeepFace 엔드포인트
@app.get("/models")
def list_models():
    """사용 가능한 모델 목록"""
    return get_available_models()


@app.post("/face/analyze")
async def analyze_face(
    img: UploadFile = File(...),
    actions: str = Form(default="age,gender,race,emotion")
):
    """얼굴 속성 분석 (나이, 성별, 인종, 감정)"""
    temp_path = None
    try:
        temp_path = FaceAnalyzer.save_temp_file(img.file, img.filename)
        action_list = [a.strip() for a in actions.split(',')]
        
        result = FaceAnalyzer.analyze(temp_path, action_list)
        return JSONResponse(content=result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 실패: {str(e)}")
    finally:
        FaceAnalyzer.cleanup_temp_file(temp_path)


@app.post("/face/verify")
async def verify_faces(
    img1: UploadFile = File(...),
    img2: UploadFile = File(...),
    model_name: str = Form(default="VGG-Face"),
    distance_metric: str = Form(default="cosine"),
    detector_backend: str = Form(default="opencv")
):
    """두 사진에서 동일인 여부 판별"""
    temp_path1 = None
    temp_path2 = None
    try:
        temp_path1 = FaceAnalyzer.save_temp_file(img1.file, img1.filename)
        temp_path2 = FaceAnalyzer.save_temp_file(img2.file, img2.filename)
        
        result = FaceAnalyzer.verify(
            temp_path1, temp_path2, 
            model_name, distance_metric, detector_backend
        )
        return JSONResponse(content=result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"검증 실패: {str(e)}")
    finally:
        FaceAnalyzer.cleanup_temp_file(temp_path1)
        FaceAnalyzer.cleanup_temp_file(temp_path2)


@app.post("/face/find")
async def find_person(
    img: UploadFile = File(...),
    db_path: str = Form(default="./dataset"),
    model_name: str = Form(default="Facenet"),
    distance_metric: str = Form(default="euclidean_l2")
):
    """폴더(DB) 내에서 동일한 인물 찾기"""
    temp_path = None
    try:
        temp_path = FaceAnalyzer.save_temp_file(img.file, img.filename)
        
        result = FaceAnalyzer.find(temp_path, db_path, model_name, distance_metric)
        return JSONResponse(content=result)
        
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"검색 실패: {str(e)}")
    finally:
        FaceAnalyzer.cleanup_temp_file(temp_path)


@app.post("/face/represent")
async def get_embedding(
    img: UploadFile = File(...),
    model_name: str = Form(default="Facenet512")
):
    """얼굴 임베딩 벡터 추출"""
    temp_path = None
    try:
        temp_path = FaceAnalyzer.save_temp_file(img.file, img.filename)
        
        result = FaceAnalyzer.represent(temp_path, model_name)
        return JSONResponse(content=result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"임베딩 추출 실패: {str(e)}")
    finally:
        FaceAnalyzer.cleanup_temp_file(temp_path)


@app.post("/face/extract")
async def extract_faces(
    img: UploadFile = File(...),
    detector_backend: str = Form(default="fastmtcnn"),
    align: bool = Form(default=True)
):
    """이미지에서 얼굴 영역 추출 및 정렬"""
    temp_path = None
    try:
        temp_path = FaceAnalyzer.save_temp_file(img.file, img.filename)
        
        result = FaceAnalyzer.extract_faces(temp_path, detector_backend, align)
        return JSONResponse(content=result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"얼굴 추출 실패: {str(e)}")
    finally:
        FaceAnalyzer.cleanup_temp_file(temp_path)