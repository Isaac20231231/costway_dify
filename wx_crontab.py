import json
import time
from datetime import datetime
from common.log import logger
from typing import Union


def create_data(message: str, receiver_name: str, group_names: list) -> dict:
    """
    创建数据
    :param message: 消息内容
    :param receiver_name: 接收者名称
    :param group_names: 群名列表
    :return: 数据字典
    """
    return {
        "data_list": [
            {
                'receiver_name': receiver_name,
                'message': message,
                'group_name': group_name
            } for group_name in group_names
        ]
    }


def get_message(nowtime: str, receiver_name: str, group_names: list, group_type: str) -> Union[dict, None]:
    """
    获取消息
    :param nowtime: 当前时间
    :param receiver_name: 接收者名称
    :param group_names: 群名列表
    :param group_type: 群类型 myself:自己的群 game:游戏群
    :return: 消息字典
    """
    nowtime_ymd = datetime.now().strftime("%Y{0}%m{1}%d{2} %H:%M:%S").format(*'年月日')
    messages = {
        'myself': {
            # '09:30': f'早上好☀️\n现在是北京时间: {nowtime_ymd}\n上班了😭\n今天也是活力满满的一天哦💪\n今天也别忘记摸鱼哦😄',
            # '12:00': f'中午好🌞\n现在是北京时间: {nowtime_ymd}\n中午了😄\n午饭时间到了😄\n中午一定要吃饱饱哦❤️',
            # '17:50': f'下午好🌅\n现在是北京时间: {nowtime_ymd}\n还有10分钟就下班了🥳\n下班了下班了下班了🎉\n下班了就可以回家喽😄',
            # '23:00': f'晚上好🌙\n现在是北京时间: {nowtime_ymd}\n晚上了😴\n快去睡觉吧😴\n晚安晚安🌛',
        },
        'game': {
            '21:55': f' 竞技场开始偷排名❗️❗️❗\n俱乐部BOOS也不要忘记了❗️❗️❗️',
            '12:01': lambda: f'厨神擂台活动开始了\n别忘记打❗️❗️❗️' if datetime.now().weekday() in [1, 6]
            else f'俱乐部排位赛报名开始了\n别忘记报名❗️❗️❗️' if datetime.now().weekday() in [2, 3, 4] else None,
            '19:50': lambda: f'盐场马上就要开始了,大家做好准备\n上号❗️上号❗️\n今晚吃鸡❗️❗️❗️️'
            if datetime.now().weekday() == 5 else None
        }
    }
    message = messages.get(group_type, {}).get(nowtime)
    if message:
        return create_data(message, receiver_name, group_names)
    return None


def write_message_specified_time():
    """
    编写一个指定时间写入data.json文件的方法
    用来做定时发微信提醒
    """
    receiver_name = ''  # 接收者名称
    game_receiver_name = '所有人'  # 游戏群接收者名称
    myself_group_names = ['小宝之家', '聊天群']  # 自己的群名列表
    game_group_names = ['云聚丨惊涛盐场战团群', '12745（鸡泥钛美闲之宝）']  # 游戏群名列表
    last_write_time = None  # 初始化上一次写入的时间
    while True:
        nowtime = datetime.now().strftime('%H:%M')  # 获取当前时间
        if nowtime != last_write_time:  # 如果当前时间与上一次写入的时间不同
            data_dict = (get_message(nowtime, receiver_name, myself_group_names, 'myself') or
                         get_message(nowtime, game_receiver_name, game_group_names, 'game'))
            if data_dict:  # 检查 data_dict 是否为空列表
                with open('plugins/file_writer/data.json', 'w') as file:
                    json.dump(data_dict["data_list"], file, ensure_ascii=False)
                    last_write_time = nowtime  # 更新上一次写入的时间
                    time.sleep(1)
                    logger.info(f"写入成功, 写入时间:{nowtime} 写入内容:{data_dict['data_list']}")
            time.sleep(1)


if __name__ == '__main__':
    write_message_specified_time()
