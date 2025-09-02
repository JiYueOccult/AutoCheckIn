from models.util import setup_logger, load_config_from_env
from models import get_task_module, get_available_tasks

logger = setup_logger("AutoTask", "auto_task.log")

def execute_task(task_name: str, task_config: dict) -> bool:
    logger.info(f"开始执行网站任务: {task_name}")
    
    module = get_task_module(task_name)
    if not module:
        logger.error(f"不支持的任务类型: {task_name}")
        return False
    try:
        result = module.main(task_config)
        logger.info(f"网站任务 {task_name} 执行{'成功' if result else '失败'}")
        return result
    except Exception as e:
        logger.error(f"执行网站任务 {task_name} 时发生异常: {e}")
        return False

def main():
    logger.info("=" * 50)
    logger.info("自动网站任务程序启动")
    logger.info(f"支持的任务: {', '.join(get_available_tasks())}")
    
    config = load_config_from_env("CONFIG_TASK")
    if not config:
        logger.error("无法加载网站任务配置，程序退出")
        return
    
    logger.info(f"成功加载网站任务配置，包含 {len(config)} 个任务")
    
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
    
    logger.info(f"所有网站任务执行完成！成功 {success_tasks}/{total_tasks} 个任务")
    logger.info("=" * 50)

if __name__ == "__main__":
    main()
