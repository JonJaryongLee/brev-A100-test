import asyncio
import httpx
import time
import os
import datetime
import sys

MODEL_NAME = "cyankiwi/Qwen3.5-35B-A3B-AWQ-4bit"
BASE_URL = "http://localhost:8000/v1/chat/completions"

async def main():
    run_timestamp = sys.argv[1] if len(sys.argv) > 1 else datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    
    # 100code.py 파일 내용 읽기
    if not os.path.exists("100code.py"):
        with open("100code.py", "w", encoding="utf-8") as f:
            f.write("# dummy code for testing\nprint('hello world')\n")

    with open("100code.py", "r", encoding="utf-8") as f:
        code_content = f.read()

    prompt = f"다음 코드를 보고 어떤 내용인지 3줄로 분석하라:\n\n{code_content}"
    print("질문: 100code.py 분석")
    
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
    save_dir = f"./test/{run_timestamp}/senario2"
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
