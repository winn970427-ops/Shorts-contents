import json
import os
import time
import subprocess

# Configuration
PLAN_FILE = 'plan.json'
IMG_DIR = 'assets/images'
VID_DIR = 'assets/videos'
FINAL_OUTPUT = 'final_shorts.mp4'

# YouTube API configurations
CLIENT_SECRETS_FILE = 'client_secret.json'

def fetch_trends_and_create_plan():
    print("1. 최신 건강 트렌드 검색 및 plan.json 업데이트 진행 중...")
    # 실무에서는 YouTube Data API 검색이나 뉴스 크롤링 사용
    if not os.path.exists(PLAN_FILE):
        print(f"{PLAN_FILE} 이 존재하지 않습니다.")
        return []
    with open(PLAN_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_images(plan):
    print("\n2. Flow AI에서 9:16 비율 이미지 생성 중...")
    os.makedirs(IMG_DIR, exist_ok=True)
    for item in plan:
        scene_id = item['scene']
        prompt = item['image_prompt']
        print(f"   - Scene {scene_id} 이미지 생성 요청: {prompt[:30]}...")
        # API 연동 영역 (예: Gemini/Flow AI API 호출)
        time.sleep(1) # Mock delay
        output_path = os.path.join(IMG_DIR, f"scene_{scene_id}.png")
        print(f"   - {output_path} 저장 완료.")

def generate_videos(plan):
    print("\n3. Flow (Veo 3.1-Lite)에서 이미지 기반 동영상 생성 중...")
    os.makedirs(VID_DIR, exist_ok=True)
    for item in plan:
        scene_id = item['scene']
        print(f"   - Scene {scene_id} 영상 변환 중...")
        # API 연동 영역 (예: Veo API 호출)
        time.sleep(2) # Mock delay
        output_path = os.path.join(VID_DIR, f"scene_{scene_id}.mp4")
        print(f"   - {output_path} 저장 완료.")

def compile_final_video():
    print("\n4. FFmpeg를 활용한 최종 영상 합성 진행 중...")
    # 비디오 파일 목록 생성
    list_file = 'videos.txt'
    with open(list_file, 'w') as f:
        for i in range(1, 6):
            f.write(f"file '{VID_DIR}/scene_{i}.mp4'\n")
    
    print("   - 영상을 하나로 병합하는 중...")
    try:
        # ffmpeg 명령어 실행
        subprocess.run([
            'ffmpeg', '-y', '-f', 'concat', '-safe', '0', 
            '-i', list_file, '-c', 'copy', FINAL_OUTPUT
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"   - 최종 영상 {FINAL_OUTPUT} 완성.")
    except Exception as e:
        print("   - [경고] FFmpeg가 설치되지 않았거나 오류가 발생했습니다. (Mock 처리)")

def upload_to_youtube():
    print("\n5. YouTube 채널 자동 업로드 중...")
    # youtube api v3 로직 삽입부
    print("   - 제목: '오늘의 건강상식'")
    print("   - 설명: '요즘 건강상식 트렌드를 알려드립니다.'")
    print("   - 상태: 공개(Public)")
    print("   - 업로드 완료!")

if __name__ == '__main__':
    print("=== [일일 자동화] 유튜브 건강 쇼츠 제작 파이프라인 시작 ===")
    plan_data = fetch_trends_and_create_plan()
    if plan_data:
        generate_images(plan_data)
        generate_videos(plan_data)
        compile_final_video()
        upload_to_youtube()
    print("=== 모든 작업이 완료되었습니다! ===")
