#!/bin/bash

MODEL_NAME="cyankiwi/Qwen3-Coder-30B-A3B-Instruct-AWQ-4bit"

until curl -s localhost:8000/v1/models | grep -q "$MODEL_NAME"; do
    echo "vLLM 서버 대기 중..."
    sleep 5
done

PROMPTS=(
    "파이썬에서 리스트를 정렬하는 함수를 작성해줘."
    "파이썬 데코레이터의 사용법과 예시를 설명해줘."
    "C++로 빠른 푸리에 변환(FFT)을 구현해봐."
    "Rust에서 메모리 관리는 어떻게 이루어지는지 설명해줘."
    "간단한 FastAPI 애플리케이션 예제 코드를 짜줘."
    "Node.js 앱을 위한 Dockerfile을 작성해줘."
    "프로세스와 스레드의 차이점을 코드 레벨에서 설명해줘."
    "SQL에서 중복 데이터를 찾는 쿼리를 작성해줘."
    "PostgreSQL 데이터베이스 성능 최적화 방법을 알려줘."
    "로그인 기능을 테스트하기 위한 유닛 테스트 코드를 작성해줘."
)

TMP_FILE=$(mktemp)

start_time=$(date +%s.%N)

for i in {0..9}; do
    # tee -a를 사용하여 터미널에 출력함과 동시에 임시 파일에 기록합니다.
    curl -s -o /dev/null -w "User $i: %{time_total}s\n" -X POST "http://localhost:8000/v1/chat/completions" \
    -H "Content-Type: application/json" \
    -d "{
        \"model\": \"$MODEL_NAME\",
        \"messages\": [{\"role\": \"user\", \"content\": \"${PROMPTS[$i]}\"}],
        \"max_tokens\": 512,
        \"temperature\": 0,
        \"stream\": false
    }" | tee -a "$TMP_FILE" &
    pids[${i}]=$!
done

for pid in ${pids[*]}; do
    wait $pid
done

end_time=$(date +%s.%N)

total_duration=$(awk -v e="$end_time" -v s="$start_time" 'BEGIN {print e - s}')
# 파일에서 숫자(초) 부분만 추출하여 평균을 계산합니다.
avg_latency=$(awk -F': ' '{gsub(/s/,"",$2); sum+=$2; count++} END {if (count > 0) print sum/count}' "$TMP_FILE")

echo "--------------------------------------"
echo "L40S (48GiB) 성능 테스트 결과"
echo "총 소요 시간: ${total_duration}초"
echo "평균 개별 응답 시간(Latency): ${avg_latency}초"
echo "초당 처리 요청 수(Throughput): $(awk -v t="$total_duration" 'BEGIN {print 10 / t}') req/s"
echo "--------------------------------------"

rm "$TMP_FILE"