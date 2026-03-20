import asyncio
import httpx
import time
import os
import datetime
import sys

MODEL_NAME = "cyankiwi/Qwen3.5-35B-A3B-AWQ-4bit"
BASE_URL = "http://localhost:8000/v1/chat/completions"

async def main():
    # 실행 인자로 타임스탬프 디렉터리 이름을 받음 (없으면 새로 생성)
    run_timestamp = sys.argv[1] if len(sys.argv) > 1 else datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    
    prompt = "퀵소트 구현을 하고, 각 줄마다 주석을 달라."
    print(f"질문: {prompt}")
    
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2048,
        "temperature": 0,
        "stream": False
    }
    
    async with httpx.AsyncClient() as client:
        start_time = time.perf_counter()
        response = await client.post(BASE_URL, json=payload, timeout=None)
        end_time = time.perf_counter()
        
    duration = end_time - start_time
    data = response.json()
    content = data['choices'][0]['message']['content']
    tokens = data['usage']['completion_tokens']
    tps = tokens / duration if duration > 0 else 0
    
    req_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    save_dir = f"./test/{run_timestamp}/senario1"
    os.makedirs(save_dir, exist_ok=True)
    filename = f"{save_dir}/{req_timestamp}-1.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"답변 파일: {filename}")
    print(f"초당 토큰 생성량 (TPS): {tps:.2f} tokens/s")
    print(f"총 소요 시간: {duration:.4f}초")
    print(f"총 생성 토큰 수: {tokens}")

if __name__ == "__main__":
    asyncio.run(main())
