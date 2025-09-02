from .util import *
import cloudscraper

logger = setup_logger("Acgjc", "acgjc_checkin.log")

URL = "https://www.acgjc.com/wp-json/b2/v1/userMission"

def check_acgjc_user(authorization: str, cookie: str) -> bool:
    session = cloudscraper.create_scraper()
    
    headers = get_standard_headers()
    headers["referer"] = "https://www.acgjc.com/task"
    headers["origin"] = "https://www.acgjc.com"
    headers["authorization"] = authorization
    headers["cookie"] = cookie
    
    try:
        response = session.post(URL, headers=headers, timeout=30)
    except Exception as e:
        logger.error(f"请求失败: {e}")
        return False
    
    if "credit" in response.text:
        logger.info("签到成功！已获得今日积分")
        return True
    else:
        logger.info("今日已经签到过")
        return True

def main(config: dict) -> bool:
    logger.info("开始执行 Acgjc 自动签到")

    required_fields = ["authorization", "cookie"]
    if not validate_required_fields(config, required_fields):
        return False
    
    authorization = config["authorization"]
    cookie = config["cookie"]

    success = check_acgjc_user(authorization, cookie)

    return success

if __name__ == "__main__":
    authorization = "<your_authorization_token_here>"
    cookie = "<your_cookie_here>"
    
    config = {"authorization": authorization, "cookie": cookie}
    main(config)