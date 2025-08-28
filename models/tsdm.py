from .util import *
import cloudscraper
import re
import urllib.parse

logger = setup_logger("tsdm", "tsdm_checkin.log")

URL = "https://www.tsdm39.com/forum.php"

def check_tsdm_user(cookie: str) -> bool:
    session = cloudscraper.create_scraper()
    
    headers = get_standard_headers()
    headers["referer"] = "https://www.tsdm39.com/forum.php"
    headers["origin"] = "https://www.tsdm39.com"
    headers["cookie"] = cookie
    
    try:
        response = session.post(URL, headers=headers, timeout=30)
    except Exception as e:
        logger.error(f"请求失败: {e}")
        return False
    
    if response.status_code != 200:
        logger.error(f"请求失败，状态码: {response.status_code}")
        return False
    
    pattern = r'name="formhash" value="(.+?)"'
    match = re.search(pattern, response.text)
    formhash_value = match.group(1)
    encoded_formhash = urllib.parse.quote(formhash_value)
    
    headers["content-type"]="application/x-www-form-urlencoded"
    data = {"formhash": encoded_formhash, "qdxq": "kx", "qdmode": "3", "todaysay": "", "fastreply": "1"}
    response = session.post(URL, headers=headers, data=data)
    
    if response.status_code != 200:
        logger.info("签到失败")
    else:
        logger.info("签到成功")

def main(config: dict) -> bool:
    logger.info("开始执行 tsdm 自动签到")
    
    required_fields = ["cookie"]
    if not validate_required_fields(config, required_fields):
        return False
    
    cookie = config["cookie"]

    success = check_tsdm_user(cookie)

    return success

if __name__ == "__main__":
    cookie = "<your_cookie_here>"
    
    config = {"cookie": cookie}
    main(config)
