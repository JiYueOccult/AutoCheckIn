from .util import *
import cloudscraper

logger = setup_logger("Hifiti", "hifiti_checkin.log")

URL = "https://www.hifiti.com/sg_sign.htm"

def check_hifiti_user(cookie: str) -> bool:
    session = cloudscraper.create_scraper()
    
    headers = get_standard_headers()
    headers["referer"] = "https://www.hifiti.com/"
    headers["origin"] = "https://www.hifiti.com"
    headers["cookie"] = cookie
    
    try:
        response = session.post(URL, headers=headers, timeout=30)
    except Exception as e:
        logger.error(f"请求失败: {e}")
        return False
    
    if response.status_code != 200:
        logger.error(f"请求失败，状态码: {response.status_code}")
        return False
    
    response_text = response.text
    
    if "已经签过" in response_text:
        logger.info("今日已经签到过")
        return True
    elif "成功签到" in response_text:
        logger.info("签到成功！")
        return True
    else:
        logger.error("签到失败")
        return False

def main(config: dict) -> bool:
    logger.info("开始执行 hifiti 自动签到")
    
    required_fields = ["cookie"]
    if not validate_required_fields(config, required_fields):
        return False
    
    cookie = config["cookie"]

    success = check_hifiti_user(cookie)

    return success

if __name__ == "__main__":
    cookie = "<your_cookie_here>"

    config = {"cookie": cookie}
    main(config)
