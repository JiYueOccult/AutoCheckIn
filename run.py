import os
import json
import logging
from function import setup_logger, load_config_from_env

logger = setup_logger("AutoCheckIn", "auto_checkin.log")

TASK_MODULES = {
    "vikacg": "vikacg",
    # 可以继续添加其他网站
    # "example": "example_module",
}

def import_task_module(task_name: str):
    if task_name not in TASK_MODULES:
        logger.error(f"不支持的任务类型: {task_name}")
        return None
    
    module_name = TASK_MODULES[task_name]
    try:
        module = __import__(module_name)
        return module
    except ImportError as e:
        logger.error(f"导入模块失败 {module_name}: {e}")
        return None

def execute_task(task_name: str, task_config: dict) -> bool:
    """执行指定的签到任务"""
    logger.info(f"开始执行任务: {task_name}")
    
    # 导入对应的模块
    module = import_task_module(task_name)
    if not module:
        return False
    
    try:
        result = module.main(task_config)
        logger.info(f"任务 {task_name} 执行{'成功' if result else '失败'}")
        return result
    except Exception as e:
        logger.error(f"执行任务 {task_name} 时发生异常: {e}")
        return False

def main():
    """主函数"""
    logger.info("=" * 50)
    logger.info("自动签到程序启动")
    
    config = load_config_from_env("CONFIG")
    if not config:
        logger.error("无法加载配置，程序退出")
        return
    
    logger.info(f"成功加载配置，包含 {len(config)} 个任务")
    
    total_tasks = 0
    success_tasks = 0
    
    for task_id, task_info in config.items():
        total_tasks += 1
        
        if not isinstance(task_info, dict):
            logger.error(f"任务配置格式错误: {task_id}")
            continue
        
        if "task" not in task_info:
            logger.error(f"任务配置缺少task字段: {task_id}")
            continue
        
        task_name = task_info["task"]
        
        if execute_task(task_name, task_info):
            success_tasks += 1
        
        logger.info("-" * 30)
    
    logger.info(f"所有任务执行完成！成功 {success_tasks}/{total_tasks} 个任务")
    logger.info("=" * 50)

if __name__ == "__main__":
    main()
