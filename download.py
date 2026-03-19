from huggingface_hub import snapshot_download

def download_hf_model():
    model_id = "cyankiwi/Qwen3-Coder-30B-A3B-Instruct-AWQ-4bit"
    
    print(f"모델 다운로드 시작: {model_id}")
    
    # snapshot_download는 모델을 로드하지 않고 파일만 내려받습니다.
    snapshot_download(
        repo_id=model_id,
        # hf_transfer가 설치되어 있고 환경변수가 설정되어 있다면 자동으로 가속됩니다.
    )

    print(f"다운로드가 완료되었습니다.")

if __name__ == "__main__":
    download_hf_model()