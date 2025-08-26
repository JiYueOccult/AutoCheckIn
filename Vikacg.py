import os
import json
import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('vikacg_checkin.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)

URL = "https://www.vikacg.com/api/b2/v1/userMission"

class VikacgChecker:
    def __init__(self):
        self.authorizations = os.getenv("AUTHORIZATION", "")
        self.cookies = os.getenv("COOKIE", "")
        
    def validate_config(self) -> bool:
        if not self.authorizations or not self.cookies:
            logger.error("未读取到配置信息，请检查环境变量 AUTHORIZATION 和 COOKIE")
            return False
            
        auth_list = self.authorizations.split("#")
        cookie_list = self.cookies.split("#")
        
        if len(auth_list) != len(cookie_list):
            logger.error("配置错误：authorization 和 cookie 参数数量不匹配")
            return False
            
        return True
    
    def check_single_user(self, authorization: str, cookie: str) -> bool:
        try:
            headers = {
                "authorization": authorization,
                "cookie": cookie,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            response = requests.post(URL, headers=headers, timeout=30)
            
            if response.status_code != 200:
                # logger.error(f"请求失败，状态码: {response.status_code}, 响应: {response.text}")
                logger.error(f"请求失败，状态码: {response.status_code}")
                return False
            
            try:
                data = response.json()
                # logger.info(f"API 响应数据: {data}")
                logger.info("API 请求成功，正在处理响应数据")
                
                if isinstance(data, dict):
                    credit = data.get("credit", 0)
                    mission = data.get("mission", {})
                    my_credit = mission.get("my_credit", "未知")
                    
                    # logger.info(f"签到成功！获得积分 {credit} 分，目前总积分 {my_credit} 分")
                    logger.info("签到成功！已获得今日积分")
                    return True
                    
                elif isinstance(data, str):
                    # logger.info(f"今日已经签到过，获得积分 {data} 分")
                    logger.info("今日已经签到过")
                    return True
                    
                else:
                    # logger.error(f"未知的响应格式：{type(data)}, 内容：{data}")
                    logger.error(f"未知的响应格式：{type(data)}")
                    return False
                
            except json.JSONDecodeError as e:
                # response_text = response.text.strip('"')
                # logger.error(f"JSON 解析失败：{e}, 原始响应：{response_text}")
                logger.error(f"JSON 解析失败：{e}")
                return False
                
            except Exception as e:
                # logger.error(f"处理响应数据时发生异常：{e}, 响应内容：{response.text}")
                logger.error(f"处理响应数据时发生异常：{e}")
                return False
                    
        except requests.exceptions.RequestException as e:
            logger.error(f"网络请求异常：{e}")
            return False
        except Exception as e:
            logger.error(f"签到过程中发生未知错误：{e}")
            return False
    
    def run(self) -> None:
        logger.info("开始执行 Vikacg 自动签到程序")
        
        if not self.validate_config():
            return
        
        auth_list = self.authorizations.split("#")
        cookie_list = self.cookies.split("#")
        total_users = len(auth_list)
        
        success_count = 0
        
        for i, (auth, cookie) in enumerate(zip(auth_list, cookie_list), 1):
            logger.info(f"正在签到第 {i} 个用户，共计 {total_users} 个用户")
            
            if self.check_single_user(auth.strip(), cookie.strip()):
                success_count += 1
            
            logger.info("-" * 50)
        
        logger.info(f"签到完成！成功 {success_count}/{total_users} 个用户")

def main():
    checker = VikacgChecker()
    checker.run()

if __name__ == "__main__":
    main()