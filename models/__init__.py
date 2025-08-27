# Models package

from . import vikacg
from . import example
from . import acgjc

TASK_MODULES = {
    "vikacg": vikacg,
    "example": example,
    "acgjc": acgjc,
    # 添加新任务时，在这里注册
}

def get_task_module(task_name: str):
    return TASK_MODULES.get(task_name)

def get_available_tasks():
    return list(TASK_MODULES.keys())
