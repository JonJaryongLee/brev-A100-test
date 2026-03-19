from huggingface_hub import snapshot_download

def download_hf_model():
    model_ids = [
        "cyankiwi/Qwen3-Coder-30B-A3B-Instruct-AWQ-4bit",
        "cyankiwi/Qwen3.5-35B-A3B-AWQ-4bit"
    ]
    
    for model_id in model_ids:
        print(f"모델 다운로드 시작: {model_id}")
        
        snapshot_download(
            repo_id=model_id,
        )

        print(f"{model_id} 다운로드가 완료되었습니다.")

if __name__ == "__main__":
    download_hf_model()