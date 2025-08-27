# Models package

from . import example
from . import vikacg
from . import acgjc
from . import hifiti

TASK_MODULES = {
    "example": example,
    "vikacg": vikacg,
    "acgjc": acgjc,
    "hifiti": hifiti,
    # 添加新任务时，在这里注册
}

def get_task_module(task_name: str):
    return TASK_MODULES.get(task_name)

def get_available_tasks():
    return list(TASK_MODULES.keys())
