import asyncio
import httpx
import time
import os
import datetime
import sys
import base64

MODEL_NAME = "cyankiwi/Qwen3.5-35B-A3B-AWQ-4bit"
BASE_URL = "http://localhost:8000/v1/chat/completions"
CONCURRENT_USERS = 10

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

async def fetch_request(client, payload, user_idx, run_timestamp):
    response = await client.post(BASE_URL, json=payload, timeout=None)
    data = response.json()
    
    if 'choices' not in data:
        print(f"Error in response for user {user_idx}: {data}")
        return 0, None

    content = data['choices'][0]['message']['content']
    tokens = data['usage']['completion_tokens']
    
    req_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    save_dir = f"./test/{run_timestamp}/senario8"
    os.makedirs(save_dir, exist_ok=True)
    filename = f"{save_dir}/{req_timestamp}-{user_idx}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
        
    return tokens, filename

async def main():
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
        tasks = [fetch_request(client, payload, i+1, run_timestamp) for i in range(CONCURRENT_USERS)]
        results = await asyncio.gather(*tasks)
        end_time = time.perf_counter()
        
    duration = end_time - start_time
    tokens_list = [r[0] for r in results]
    filenames = [r[1] for r in results if r[1]]
    
    for fname in filenames:
        print(f"답변 파일: {fname}")
        
    total_tokens = sum(tokens_list)
    system_tps = total_tokens / duration if duration > 0 else 0
    
    print(f"초당 토큰 생성량 (TPS): {system_tps:.2f} tokens/s")
    print(f"총 소요 시간: {duration:.4f}초")
    print(f"총 생성 토큰 수: {total_tokens}")
    print(f"평균 초당 토큰 생성량: {system_tps / CONCURRENT_USERS:.2f} tokens/s")
    print(f"평균 생성 토큰 수: {total_tokens / CONCURRENT_USERS:.2f}")

if __name__ == "__main__":
    asyncio.run(main())
