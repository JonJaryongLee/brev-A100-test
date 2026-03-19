import asyncio
import httpx
import time
import os
import json

MODEL_NAME = "cyankiwi/Qwen3-Coder-30B-A3B-Instruct-AWQ-4bit"
BASE_URL = "http://localhost:8000/v1/chat/completions"
PROMPTS = [
    "파이썬에서 리스트를 정렬하는 함수를 작성해줘.",
    "파이썬 데코레이터의 사용법과 예시를 설명해줘.",
    "C++로 빠른 푸리에 변환(FFT)을 구현해봐.",
    "Rust에서 메모리 관리는 어떻게 이루어지는지 설명해줘.",
    "간단한 FastAPI 애플리케이션 예제 코드를 짜줘.",
    "Node.js 앱을 위한 Dockerfile을 작성해줘.",
    "프로세스와 스레드의 차이점을 코드 레벨에서 설명해줘.",
    "SQL에서 중복 데이터를 찾는 쿼리를 작성해줘.",
    "PostgreSQL 데이터베이스 성능 최적화 방법을 알려줘.",
    "로그인 기능을 테스트하기 위한 유닛 테스트 코드를 작성해줘."
]

async def wait_for_server():
    async with httpx.AsyncClient() as client:
        while True:
            try:
                response = await client.get("http://localhost:8000/v1/models")
                if MODEL_NAME in response.text:
                    break
            except httpx.RequestError:
                pass
            print("vLLM 서버 대기 중...")
            await asyncio.sleep(5)

async def fetch_and_save(client, index, prompt):
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2048,
        "temperature": 0,
        "stream": False
    }
    
    start = time.perf_counter()
    response = await client.post(BASE_URL, json=payload, timeout=None)
    end = time.perf_counter()
    latency = end - start
    
    data = response.json()
    answer = data['choices'][0]['message']['content']
    
    # 파일 저장 부분 시작
    file_path = f"answer/{index + 1:02d}.md"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# Prompt\n{prompt}\n\n# Answer\n{answer}")
    # 파일 저장 부분 끝
        
    print(f"User {index}: {latency:.4f}s")
    return latency

async def main():
    if not os.path.exists("answer"):
        os.makedirs("answer")

    await wait_for_server()
    
    start_time = time.perf_counter()
    
    async with httpx.AsyncClient() as client:
        tasks = [fetch_and_save(client, i, prompt) for i, prompt in enumerate(PROMPTS)]
        latencies = await asyncio.gather(*tasks)

    end_time = time.perf_counter()
    total_duration = end_time - start_time
    avg_latency = sum(latencies) / len(latencies)
    throughput = len(PROMPTS) / total_duration

    print("-" * 38)
    print("L40S (48GiB) 성능 테스트 결과")
    print(f"총 소요 시간: {total_duration:.4f}초")
    print(f"평균 개별 응답 시간(Latency): {avg_latency:.4f}초")
    print(f"초당 처리 요청 수(Throughput): {throughput:.4f} req/s")
    print("-" * 38)

if __name__ == "__main__":
    asyncio.run(main())