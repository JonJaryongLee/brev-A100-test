import subprocess
import os
import datetime

SCENARIOS = [
    ("senario1.py", "LLM 추론 - 디코딩 성능 분석 (단일 요청)"),
    ("senario2.py", "LLM 추론 - 인코딩 성능 분석 (단일 요청)"),
    ("senario3.py", "LLM 추론 - 디코딩 성능 분석 및 10개 동시 요청 처리"),
    ("senario4.py", "LLM 추론 - 인코딩 성능 분석 및 10개 동시 요청 처리"),
    ("senario5.py", "LLM 추론 - 디코딩 성능 분석 및 30개 동시 요청 처리"),
    ("senario6.py", "LLM 추론 - 인코딩 성능 분석 및 30개 동시 요청 처리"),
    ("senario7.py", "Vision 추론 - 이미지 분석 (단일 요청)"),
    ("senario8.py", "Vision 추론 - 이미지 분석 (10개 동시 요청 처리)"),
    ("senario9.py", "Vision 추론 - 이미지 분석 (30개 동시 요청 처리)"),
]

def run_scenario(file_name, description, run_timestamp):
    output = ""
    output += f"\n{'='*60}\n"
    output += f"시나리오: {file_name}\n"
    output += f"목적: {description}\n"
    output += f"{'-'*60}\n"
    
    try:
        result = subprocess.run(["python3", file_name, run_timestamp], capture_output=True, text=True, check=True)
        output += result.stdout
    except subprocess.CalledProcessError as e:
        output += f"오류 발생: {e.stderr}\n"
    output += f"{'='*60}\n"
    return output

def main():
    os.makedirs("./result", exist_ok=True)
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    result_filename = f"./result/{timestamp}-result.txt"
    
    os.makedirs(f"./test/{timestamp}", exist_ok=True)
    
    full_output = f"전체 LLM 성능 테스트를 시작합니다. (ID: {timestamp})\n"
    print(full_output, end="")
    
    for file_name, description in SCENARIOS:
        scenario_output = run_scenario(file_name, description, timestamp)
        print(scenario_output, end="")
        full_output += scenario_output
        
    with open(result_filename, "w", encoding="utf-8") as f:
        f.write(full_output)
    
    print(f"\n테스트 결과가 저장되었습니다: {result_filename}")
    print(f"답변 파일 저장 위치: ./test/{timestamp}/")

if __name__ == "__main__":
    main()