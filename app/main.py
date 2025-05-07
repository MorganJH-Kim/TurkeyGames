from contextlib import asynccontextmanager
import asyncio # Added import

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Updated imports: router creation function and TriggerDetector
from app.routers.video_router import create_video_router
from app.routers.yacht_router import router as yacht_router
from app.routers.api_router import router as api_router
from app.video.service import VideoService
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

# video 초기화 and router registration within lifespan
@asynccontextmanager
async def lifespan(app_instance: FastAPI): # Renamed app to app_instance to avoid conflict
    print("🚀 Application startup: Initializing services...")
    video_service = VideoService()
    app_instance.state.video_service = video_service # Store for potential access if needed

    current_loop = asyncio.get_event_loop()
    trigger_detector = TriggerDetector(
        config=video_service.config,  # Use config from the single video_service
        callback=video_service.on_trigger,
        loop=current_loop
    )
    app_instance.state.trigger_detector = trigger_detector # Store for potential access

    # Create and include the video router, passing dependencies
    video_router_instance = create_video_router(video_service, trigger_detector)
    app_instance.include_router(video_router_instance)

    # Include other routers
    app_instance.include_router(yacht_router)
    app_instance.include_router(api_router)
    
    print("✅ Services initialized and routers included.")
    yield
    
    print("⏳ 애플리케이션 종료 중... VideoService 중지 시도...")
    video_service.stop()
    print("🛑 VideoService 중지 완료.")

# Assign lifespan to the app
app.router.lifespan_context = lifespan

@app.get("/")
def read_root():
    return {"message": "Welcome to Turkey Games API"}


# This code will only run if this file is executed directly (not imported)
if __name__ == "__main__":
    # Run the server with Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
