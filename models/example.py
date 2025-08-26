"""
示例任务模块
演示如何创建新的签到任务
"""
from .util import setup_logger, validate_required_fields

logger = setup_logger("ExampleTask", "example_checkin.log")

def main(config: dict) -> bool:
    """
    示例任务的主函数
    
    Args:
        config (dict): 任务配置，包含任务所需的参数
        
    Returns:
        bool: 任务执行是否成功
    """
    logger.info("开始执行示例任务")
    
    # 验证必需的配置字段
    required_fields = ["example_param"]  # 根据实际需求定义必需字段
    if not validate_required_fields(config, required_fields):
        return False
    
    # 获取配置参数
    example_param = config["example_param"]
    
    # 执行具体的签到逻辑
    # ... 这里实现具体的签到代码 ...
    
    logger.info("示例任务执行成功")
    return True

if __name__ == "__main__":
    # 用于独立测试的代码
    config = {"example_param": "test_value"}
    result = main(config)
    print(f"任务执行结果: {result}")
