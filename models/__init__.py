# Models package

from . import vikacg
from . import example

TASK_MODULES = {
    "vikacg": vikacg,
    "example": example,
    # 添加新任务时，在这里注册
}

def get_task_module(task_name: str):
    """获取指定名称的任务模块"""
    return TASK_MODULES.get(task_name)

def get_available_tasks():
    """获取所有可用的任务名称列表"""
    return list(TASK_MODULES.keys())
