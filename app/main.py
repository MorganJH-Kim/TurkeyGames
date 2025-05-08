from contextlib import asynccontextmanager
import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.routers import yacht_router
from app.routers import fivesec_router
from app.routers.video_router import create_video_router
from app.websocket.manager import socket_app
from app.video import VideoService
from app.video.trigger_detector import TriggerDetector

# FastAPI 앱 초기화
app = FastAPI(title="Turkey Games")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포 시에는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(yacht_router)
app.include_router(fivesec_router)

# lifespan context manager for initialization and cleanup
@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    print("🚀 Application startup: Initializing services...")
    video_service = VideoService()
    app_instance.state.video_service = video_service

    current_loop = asyncio.get_event_loop()
    trigger_detector = TriggerDetector(
        config=video_service.config,
        callback=video_service.on_trigger,
        loop=current_loop
    )
    app_instance.state.trigger_detector = trigger_detector

    # video_router만 의존성이 필요하므로 lifespan 내부에서 생성 및 등록
    video_router_instance = create_video_router(video_service, trigger_detector)
    app_instance.include_router(video_router_instance)

    print("✅ Services initialized and routers included.")
    yield

    print("⏳ 애플리케이션 종료 중... VideoService 중지 시도...")
    video_service.stop()
    print("🛑 VideoService 중지 완료.")

# Assign lifespan to the app
app.lifespan = lifespan

@app.get("/")
def read_root():
    return {"message": "Welcome to Turkey Games API"}

# Socket.IO 앱 마운트
app.mount("/", socket_app)

# This code will only run if this file is executed directly (not imported)
if __name__ == "__main__":
    # Run the server with Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)