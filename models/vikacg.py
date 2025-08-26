import json
from .util import *

logger = setup_logger("Vikacg", "vikacg_checkin.log")

URL = "https://www.vikacg.com/api/b2/v1/userMission"

def check_vikacg_user(authorization: str, cookie: str) -> bool:
    session = create_session()
    
    headers = get_standard_headers(
        referer="https://www.vikacg.com/",
        origin="https://www.vikacg.com"
    )
    headers["authorization"] = authorization
    headers["cookie"] = cookie
    
    response = make_request(session, "POST", URL, headers)
    
    if not response:
        logger.error("请求失败，可能需要更新authorization和cookie")
        return False
    
    if response.status_code != 200:
        logger.error(f"请求失败，状态码: {response.status_code}")
        return False
    
    data = response.json()
    
    if isinstance(data, dict):
        logger.info("签到成功！已获得今日积分")
        return True
    elif isinstance(data, str):
        logger.info("今日已经签到过")
        return True
    else:
        logger.error(f"未知的响应格式：{type(data)}")
        return False

def main(config: dict) -> bool:
    logger.info("开始执行 Vikacg 自动签到")
    
    required_fields = ["authorization", "cookie"]
    if not validate_required_fields(config, required_fields):
        return False
    
    authorization = config["authorization"]
    cookie = config["cookie"]
    
    success = check_vikacg_user(authorization, cookie)
    
    return success

if __name__ == "__main__":
    authorization = "<your_authorization_token_here>"
    cookie = "<your_cookie_here>"
    
    config = {"authorization": authorization, "cookie": cookie}
    main(config)
