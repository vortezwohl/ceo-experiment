import random
from ceo import ability

CERTAIN = False


def toss_a_coin() -> bool:
    resample = 3
    rand_sum = 0.0
    for i in range(resample):
        rand_sum += random.uniform(0, 1)
    rand_avg = rand_sum / resample
    if rand_avg > 0.5:
        return False
    return True


@ability
def search(location: str) -> str:
    # 搜索指定位置的物品或信息
    # :param location: 需要搜索的位置
    # return: 搜索结果描述
    if toss_a_coin() or CERTAIN:
        return f"成功, 在{location}找到了相关物品或信息。"
    return f"失败, 在{location}没有找到相关物品或信息。"


@ability
def move(destination: str) -> str:
    # 移动到指定位置
    # :param destination: 目标位置
    # :return: 移动结果描述
    if toss_a_coin() or CERTAIN:
        return f"成功, 已成功移动到{destination}。"
    return f"移动失败, 你留在了原位置。"


@ability
def use(item: str) -> str:
    # 使用指定物品或工具
    # :param item: 需要使用的物品或工具
    # :return: 使用结果描述
    if toss_a_coin() or CERTAIN:
        return f"已成功使用{item}。"
    return f"使用{item}失败, 你可以考虑重新尝试。"


@ability
def check(target: str) -> str:
    # 检查指定物品或位置的状态
    # :param target: 需要检查的目标
    # :return: 检查结果描述
    if toss_a_coin() or CERTAIN:
        return f"{target}的状态正常。"
    return f"{target}的状态异常。"
