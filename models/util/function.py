import os
import json
import logging
from typing import Dict, Optional

def setup_logger(name: str = "AutoCheckIn", log_file: str = "checkin.log") -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file, encoding='utf-8')
        ]
    )
    return logging.getLogger(name)

def get_standard_headers() -> Dict[str, str]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Ch-Ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"'
    }
    return headers

def load_config_from_env(env_var: str = "CONFIG") -> Optional[Dict]:
    config_str = os.getenv(env_var, "")
    if not config_str:
        logging.error(f"未找到环境变量: {env_var}")
        return None
    
    try:
        config = json.loads(config_str)
        return config
    except json.JSONDecodeError as e:
        logging.error(f"配置JSON解析失败: {e}")
        return None

def validate_required_fields(config: Dict, required_fields: list) -> bool:
    for field in required_fields:
        if field not in config:
            logging.error(f"配置缺少必需字段: {field}")
            return False
        if not config[field]:
            logging.error(f"配置字段不能为空: {field}")
            return False
    return True
