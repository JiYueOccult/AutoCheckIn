from .util import *
import httpx
import re
import time

logger = setup_logger("tsdm", "tsdmtask.log")

URL = "https://www.tsdm39.com/plugin.php?id=np_cliworkdz%3Awork&inajax=1"
refer = "https://www.tsdm39.net/plugin.php?id=np_cliworkdz:work"

def tsdm_task(cookie: str) -> bool:
    headers = get_standard_headers()
    headers["referer"] = refer
    headers["content-type"]="application/x-www-form-urlencoded"
    headers["cookie"] = cookie
    
    with httpx.Client(headers=headers) as client:
        response = client.get(URL, headers=headers)
        pattern = r"您需要等待\d+小时\d+分钟\d+秒后即可进行。"
        match = re.search(pattern, response.text)
        if match:
            wait = match.group()
            logger.info(wait)
            return

        data = {"act": "clickad"}
        fail = 0
        for i in range(6):
            response = client.post(refer, headers=headers, data=data)
            if response.status_code == 200:
                i -= 1
                fail += 1
            if fail >= 10:
                logger.error("失败次数过多，终止任务")
                return False
            time.sleep(10)

        data = {"act": "getcre"}
        response = client.post(refer, headers=headers, data=data)
        logger.info("成功")

def main(config: dict) -> bool:
    logger.info("开始执行 tsdm 任务")
    
    required_fields = ["cookie"]
    if not validate_required_fields(config, required_fields):
        return False
    
    cookie = config["cookie"]

    success = tsdm_task(cookie)

    return success

if __name__ == "__main__":
    cookie = "<your_cookie_here>"

    config = {"cookie": cookie}
    main(config)
