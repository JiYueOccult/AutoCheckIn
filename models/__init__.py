# Models package

from . import vikacg
from . import acgjc
from . import hifiti
from . import tsdm

from . import tsdmtask

TASK_MODULES = {
    "vikacg": vikacg,
    "acgjc": acgjc,
    "hifiti": hifiti,
    "tsdm": tsdm,
    
    "tsdmtask": tsdmtask,
    # 添加新任务时，在这里注册
}

def get_task_module(task_name: str):
    return TASK_MODULES.get(task_name)

def get_available_tasks():
    return list(TASK_MODULES.keys())
