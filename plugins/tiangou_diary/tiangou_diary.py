import requests
import plugins
from plugins import *
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger

BASE_URL_DM = "https://api.qqsuu.cn/api/" #https://api.qqsuu.cn/
BASE_URL_QEMAOAPI = "http://api.qemao.com/api/" 


@plugins.register(name="tiangou_diary",
                  desc="tiangou_diary插件",
                  version="1.0",
                  author="masterke",
                  desire_priority=100)
class tiangou_diary(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info(f"[{__class__.__name__}] inited")

    def get_help_text(self, **kwargs):
        help_text = f"发送关键词【舔狗日记】会发送文案"
        return help_text

    def on_handle_context(self, e_context: EventContext):
        # 只处理文本消息
        if e_context['context'].type != ContextType.TEXT:
            return
        self.content = e_context["context"].content.strip()
        
        if self.content == "舔狗日记":
            logger.info(f"[{__class__.__name__}] 收到消息: {self.content}")
            reply = Reply()
            result = self.tiangou_diary()
            if result != None:
                reply.type = ReplyType.TEXT
                reply.content = result
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS
            else:
                reply.type = ReplyType.ERROR
                reply.content = "获取失败,等待修复⌛️"
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS

    def tiangou_diary(self):
        try:
            # 主接口
            url = BASE_URL_QEMAOAPI + "tiangou/"
            params = f"format=json"
            headers = {'Content-Type': "application/x-www-form-urlencoded",
            'User-Agent': 'My User Agent 1.0'}
            response = requests.get(url=url, params=params, headers=headers,timeout=2)
            if response.status_code == 200:
                json_data = response.json()
                if json_data.get('code') == 200 and json_data['text']:
                    text = json_data['text']
                    logger.info(f"主接口获取舔我成功：{text}")
                    return text
                else:
                    logger.error(f"主接口返回值异常:{json_data}")
                    raise ValueError('not found')
            else:
                logger.error(f"主接口请求失败:{response.text}")
                raise Exception('request failed')
        except Exception as e:
            try:
                logger.error(f"主接口抛出异常:{e}")
                # 备用接口
                url = BASE_URL_DM + "dm-tiangou"
                params = {}
                headers = {'Content-Type': "application/x-www-form-urlencoded",
                'User-Agent': 'My User Agent 1.0'}
                response = requests.get(url=url, params=params, headers=headers)
                if response.status_code == 200:
                    json_data = response.json()
                    if json_data.get('code') == 200 and json_data['data']['content']:
                        text = json_data['data']['content']
                        logger.info(f"备用接口获取舔我成功：{json_data}")
                        return text
                    else:
                        logger.error(f"备用接口返回值异常:{json_data}")
                else:
                    logger.error(f"备用接口请求失败:{response.status_code}")
            except Exception as e:
                logger.error(f"备用接口抛出异常:{e}")

        logger.error("所有接口都挂了,无法获取舔我日记")
        return None