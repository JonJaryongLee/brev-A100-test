import asyncio
import httpx
import time
import os
import datetime
import sys
import base64

MODEL_NAME = "cyankiwi/Qwen3.5-35B-A3B-AWQ-4bit"
BASE_URL = "http://localhost:8000/v1/chat/completions"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

async def main():
    # 실행 인자로 타임스탬프 디렉터리 이름을 받음 (없으면 새로 생성)
    run_timestamp = sys.argv[1] if len(sys.argv) > 1 else datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    
    image_path = "langgraph.png"
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found.")
        return

    base64_image = encode_image(image_path)
    prompt = "다음 Workflow 의 Node 들의 흐름에 대해 최대한 상세히 서술하라."
    print(f"질문: {prompt}")
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
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
    
    if 'choices' not in data:
        print(f"Error in response: {data}")
        return

    content = data['choices'][0]['message']['content']
    tokens = data['usage']['completion_tokens']
    tps = tokens / duration if duration > 0 else 0
    
    req_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    save_dir = f"./test/{run_timestamp}/senario7"
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
