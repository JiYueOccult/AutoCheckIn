from .util import *
import cloudscraper

logger = setup_logger("Vikacg", "vikacg_checkin.log")

URL = "https://www.vikacg.com/api/b2/v1/userMission"

def check_vikacg_user(authorization: str, cookie: str) -> bool:
    session = cloudscraper.create_scraper()
    
    headers = get_standard_headers()
    headers["referer"] = "https://www.vikacg.com/"
    headers["origin"] = "https://www.vikacg.com"
    headers["authorization"] = authorization
    headers["cookie"] = cookie
    
    try:
        response = session.post(URL, headers=headers, timeout=30)
    except Exception as e:
        logger.error(f"请求失败: {e}")
        return False
    
    text = response.text.strip()
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
    if text.isdigit():
        logger.info("今日已经签到过")
        return True
    else:
        logger.info("签到成功！已获得今日积分")
        return True

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
