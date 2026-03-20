Gemini CLI 의 답변은 한국어로 고정한다.  

현재 프로젝트엔 `qwen3.5-test/` 라는 디렉터리가 존재한다.  

이 디렉터리 안에 `senario7.py` , `senario8.py`, `senario9.py` 를 작성해야한다.  

사용 모델: `cyankiwi/Qwen3.5-35B-A3B-AWQ-4bit`  

아래 세 개의 코드를 완성해야한다.  

1. `senario7.py` : Vision 추론 - 이미지 분석 (단일 요청)
2. `senario8.py` : Vision 추론 - 이미지 분석 (10개 동시 요청 처리)
3. `senario9.py` : Vision 추론 - 이미지 분석 (30개 동시 요청 처리)

분석 대상 이미지: `./langgraph.png`  

LLM 에 이미지와 함께 할 질문: 다음 Workflow 의 Node 들의 흐름에 대해 최대한 상세히 서술하라.  

먼저, `senario1.py` ~ `senario6.py` 까지 분석한다음, `senario7.py` ~ `senario9.py` 까지 코드를 작성하라.  