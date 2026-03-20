import asyncio
import httpx
import time
import os
import datetime
import sys

MODEL_NAME = "cyankiwi/Qwen3-Coder-30B-A3B-Instruct-AWQ-4bit"
BASE_URL = "http://localhost:8000/v1/chat/completions"
CONCURRENT_USERS = 10

async def fetch_request(client, prompt, user_idx, run_timestamp):
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2048,
        "temperature": 0,
        "stream": False
    }
    response = await client.post(BASE_URL, json=payload, timeout=None)
    data = response.json()
    content = data['choices'][0]['message']['content']
    tokens = data['usage']['completion_tokens']
    
    req_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    save_dir = f"./test/{run_timestamp}/senario4"
    os.makedirs(save_dir, exist_ok=True)
    filename = f"{save_dir}/{req_timestamp}-{user_idx}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
        
    return tokens, filename

async def main():
    run_timestamp = sys.argv[1] if len(sys.argv) > 1 else datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    
    if not os.path.exists("100code.py"):
        with open("100code.py", "w", encoding="utf-8") as f:
            f.write("# dummy code for testing\nprint('hello world')\n")

    with open("100code.py", "r", encoding="utf-8") as f:
        code_content = f.read()
    prompt = f"다음 코드를 보고 어떤 내용인지 3줄로 분석하라:\n\n{code_content}"
    print("질문: 100code.py 분석")
    
    async with httpx.AsyncClient() as client:
        start_time = time.perf_counter()
        tasks = [fetch_request(client, prompt, i+1, run_timestamp) for i in range(CONCURRENT_USERS)]
        results = await asyncio.gather(*tasks)
        end_time = time.perf_counter()
        
    duration = end_time - start_time
    tokens_list = [r[0] for r in results]
    filenames = [r[1] for r in results]
    
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
