from dataclasses import dataclass

@dataclass
class ModelConfig:
    model: str = "qwen2.5-3b-instruct"
    base_url: str = "http://127.0.0.1:8080/v1"
    api_key: str = "NULL"
    temperature: float = 0.2
