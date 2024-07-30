import requests
from io import BytesIO
import plugins
from plugins import *
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
import os
import json

BASE_URL_365 = "https://3650000.xyz/api/"
BASE_URL_QEMAOAPI = "http://api.qemao.com/api/"
BASE_URL_HEISI_VIDEO = "http://abc.gykj.asia/API/hssp.php"
BASE_URL_HEISI_PIC = "http://abc.gykj.asia/API/hs.php"
BASE_URL_BAISI_VIDEO = "http://abc.gykj.asia/API/bssp.php"
BASE_URL_BAISI_PIC = "http://abc.gykj.asia/API/bs.php"
BASE_URL_HEIBAISHUANGSHA_VIDEO = "http://abc.gykj.asia/API/hbss.php"
BASE_URL_XIAOGEGE = "https://api.lolimi.cn/API/boy/api.php"
BASE_URL_SHUAIGE_VIDEO = "http://abc.gykj.asia/API/sgsp.php"
BASE_URL_DASESE = "http://api.yujn.cn/api/yht.php?type=image"


@plugins.register(name="xiaojiejie_pic",
                  desc="xiaojiejie_pic插件",
                  version="1.4",
                  author="KimYx",
                  desire_priority=100)
class xiaojiejie_pic(Plugin):
    content = None
    config_data = None
    
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info(f"[{__class__.__name__}] inited")
        
    def get_help_text(self, **kwargs):
        return ("发送小哥哥/帅哥视频/小姐姐/黑丝图片/白丝图片/黑丝视频/白丝视频/黑白双煞，获取图片或视频。")

    def on_handle_context(self, e_context: EventContext):
        if e_context['context'].type != ContextType.TEXT:
            return
        self.content = e_context["context"].content.strip()

        if self.content == "小姐姐":
            self.handle_xiaojiejie(e_context)
        elif self.content == "黑丝视频":
            self.handle_heisi_video(e_context)
        elif self.content == "黑丝图片":
            self.handle_heisi_pic(e_context)
        elif self.content == "白丝视频":
            self.handle_baisi_video(e_context)
        elif self.content == "白丝图片":
            self.handle_baisi_pic(e_context)
        elif self.content == "黑白双煞":
            self.handle_heibaishuangsha_video(e_context)
        elif self.content == "小哥哥":
            self.handle_xiaogege(e_context)
        elif self.content == "帅哥视频":
            self.handle_shuaige_video(e_context)
        elif self.content == "大色色":
            self.handle_dasese_pic(e_context)


    def handle_xiaojiejie(self, e_context: EventContext):
        logger.info(f"[{__class__.__name__}] 收到消息: {self.content}")
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                self.config_data = json.load(file)
        else:
            logger.error(f"请先配置{config_path}文件")
            return
        
        reply = Reply()
        result = self.xiaojiejie_pic()
        if result is not None:
            reply.type = ReplyType.IMAGE if isinstance(result, BytesIO) else ReplyType.IMAGE_URL
            reply.content = result
        else:
            reply.type = ReplyType.ERROR
            reply.content = "获取失败,重试一次,若还失败,则等待API修复⌛️"
        e_context["reply"] = reply
        e_context.action = EventAction.BREAK_PASS

    def handle_xiaogege(self, e_context: EventContext):
        logger.info(f"[{__class__.__name__}] 收到消息: {self.content}")
        reply = Reply()
        result = self.xiaogege_pic()
        if result is not None:
            reply.type = ReplyType.IMAGE if isinstance(result, BytesIO) else ReplyType.IMAGE_URL
            reply.content = result
        else:
            reply.type = ReplyType.ERROR
            reply.content = "获取失败,重试一次,若还失败,则等待API修复⌛️"
        e_context["reply"] = reply
        e_context.action = EventAction.BREAK_PASS

    def handle_heisi_video(self, e_context: EventContext):
        logger.info(f"[{__class__.__name__}] 收到消息: {self.content}")
        reply = Reply()
        result = self.heisi_video()
        if result is not None:
            reply.type = ReplyType.VIDEO if isinstance(result, BytesIO) else ReplyType.VIDEO_URL
            reply.content = result
        else:
            reply.type = ReplyType.ERROR
            reply.content = "获取失败,重试一次,若还失败,则等待API修复⌛️"
        e_context["reply"] = reply
        e_context.action = EventAction.BREAK_PASS

    def handle_heisi_pic(self, e_context: EventContext):
        logger.info(f"[{__class__.__name__}] 收到消息: {self.content}")
        reply = Reply()
        result = self.heisi_pic()
        if result is not None:
            reply.type = ReplyType.IMAGE if isinstance(result, BytesIO) else ReplyType.IMAGE_URL
            reply.content = result
        else:
            reply.type = ReplyType.ERROR
            reply.content = "获取失败,重试一次,若还失败,则等待API修复⌛️"
        e_context["reply"] = reply
        e_context.action = EventAction.BREAK_PASS

    def handle_baisi_video(self, e_context: EventContext):
        logger.info(f"[{__class__.__name__}] 收到消息: {self.content}")
        reply = Reply()
        result = self.baisi_video()
        if result is not None:
            reply.type = ReplyType.VIDEO if isinstance(result, BytesIO) else ReplyType.VIDEO_URL
            reply.content = result
        else:
            reply.type = ReplyType.ERROR
            reply.content = "获取失败,重试一次,若还失败,则等待API修复⌛️"
        e_context["reply"] = reply
        e_context.action = EventAction.BREAK_PASS

    def handle_baisi_pic(self, e_context: EventContext):
        logger.info(f"[{__class__.__name__}] 收到消息: {self.content}")
        reply = Reply()
        result = self.baisi_pic()
        if result is not None:
            reply.type = ReplyType.IMAGE if isinstance(result, BytesIO) else ReplyType.IMAGE_URL
            reply.content = result
        else:
            reply.type = ReplyType.ERROR
            reply.content = "获取失败,重试一次,若还失败,则等待API修复⌛️"
        e_context["reply"] = reply
        e_context.action = EventAction.BREAK_PASS

    def handle_heibaishuangsha_video(self, e_context: EventContext):
        logger.info(f"[{__class__.__name__}] 收到消息: {self.content}")
        reply = Reply()
        result = self.heibaishuangsha_video()
        if result is not None:
            reply.type = ReplyType.VIDEO if isinstance(result, BytesIO) else ReplyType.VIDEO_URL
            reply.content = result
        else:
            reply.type = ReplyType.ERROR
            reply.content = "获取失败,重试一次,若还失败,则等待API修复⌛️"
        e_context["reply"] = reply
        e_context.action = EventAction.BREAK_PASS

    def handle_shuaige_video(self, e_context: EventContext):
        logger.info(f"[{__class__.__name__}] 收到消息: {self.content}")
        reply = Reply()
        result = self.shuaige_video()
        if result is not None:
            reply.type = ReplyType.VIDEO if isinstance(result, BytesIO) else ReplyType.VIDEO_URL
            reply.content = result
        else:
            reply.type = ReplyType.ERROR
            reply.content = "获取失败,重试一次,若还失败,则等待API修复⌛️"
        e_context["reply"] = reply
        e_context.action = EventAction.BREAK_PASS

    def handle_dasese_pic(self, e_context: EventContext):
        logger.info(f"[{__class__.__name__}] 收到消息: {self.content}")
        reply = Reply()
        result = self.dasese_pic()
        if result is not None:
            reply.type = ReplyType.IMAGE if isinstance(result, BytesIO) else ReplyType.IMAGE_URL
            reply.content = result
        else:
            reply.type = ReplyType.ERROR
            reply.content = "获取失败,重试一次,若还失败,则等待API修复⌛️"
        e_context["reply"] = reply
        e_context.action = EventAction.BREAK_PASS


    def xiaojiejie_pic(self):
        try:
            url = BASE_URL_QEMAOAPI + "pic/"
            params = f"type={self.config_data['xiaojiejie_pic_size']}"
            headers = {'Content-Type': "application/x-www-form-urlencoded"}
            response = requests.get(url=url, params=params, headers=headers, timeout=2)
            if response.status_code == 200:
                logger.info(f"主接口获取小姐姐:{response.content[:10]}")
                image_bytes = response.content
                image_in_memory = BytesIO(image_bytes)
                return image_in_memory
            else:
                logger.error(f"主接口请求失败:{response.status_code}")
                raise requests.exceptions.ConnectionError
        except Exception as e:
            try:
                logger.error(f"主接口抛出异常:{e}")
                url = BASE_URL_365
                params = f"type=json"
                headers = {'Content-Type': "application/x-www-form-urlencoded"}
                response = requests.get(url=url, params=params, headers=headers)
                if response.status_code == 200:
                    json_data = response.json()
                    if json_data['code'] == 200 and json_data['url']:
                        img_url = json_data['url']
                        return img_url
                    else:
                        logger.error(f"备用接口返回数据异常:{json_data}")
                else:
                    logger.error(f"备用接口请求失败:{response.status_code}")
            except Exception as e:
                logger.error(f"备用接口抛出异常:{e}")

        logger.error(f"所有接口都挂了,无法获取")
        return None

    def xiaogege_pic(self):
        try:
            response = requests.get(url=BASE_URL_XIAOGEGE)
            if response.status_code == 200:
                logger.info(f"小哥哥图片接口获取成功:{response.content[:10]}")
                image_bytes = response.content
                image_in_memory = BytesIO(image_bytes)
                return image_in_memory
            else:
                logger.error(f"小哥哥图片接口请求失败:{response.status_code}")
        except Exception as e:
            logger.error(f"小哥哥图片接口抛出异常:{e}")
        return None

    def heisi_video(self):
        try:
            response = requests.get(url=BASE_URL_HEISI_VIDEO)
            if response.status_code == 200:
                logger.info(f"黑丝视频接口获取成功:{response.content[:10]}")
                video_bytes = response.content
                video_in_memory = BytesIO(video_bytes)
                return video_in_memory
            else:
                logger.error(f"黑丝视频接口请求失败:{response.status_code}")
        except Exception as e:
            logger.error(f"黑丝视频接口抛出异常:{e}")
        return None

    def heisi_pic(self):
        try:
            response = requests.get(url=BASE_URL_HEISI_PIC)
            if response.status_code == 200:
                logger.info(f"黑丝图片接口获取成功:{response.content[:10]}")
                image_bytes = response.content
                image_in_memory = BytesIO(image_bytes)
                return image_in_memory
            else:
                logger.error(f"黑丝图片接口请求失败:{response.status_code}")
        except Exception as e:
            logger.error(f"黑丝图片接口抛出异常:{e}")
        return None

    def baisi_video(self):
        try:
            response = requests.get(url=BASE_URL_BAISI_VIDEO)
            if response.status_code == 200:
                logger.info(f"白丝视频接口获取成功:{response.content[:10]}")
                video_bytes = response.content
                video_in_memory = BytesIO(video_bytes)
                return video_in_memory
            else:
                logger.error(f"白丝视频接口请求失败:{response.status_code}")
        except Exception as e:
            logger.error(f"白丝视频接口抛出异常:{e}")
        return None

    def baisi_pic(self):
        try:
            response = requests.get(url=BASE_URL_BAISI_PIC)
            if response.status_code == 200:
                logger.info(f"白丝图片接口获取成功:{response.content[:10]}")
                image_bytes = response.content
                image_in_memory = BytesIO(image_bytes)
                return image_in_memory
            else:
                logger.error(f"白丝图片接口请求失败:{response.status_code}")
        except Exception as e:
            logger.error(f"白丝图片接口抛出异常:{e}")
        return None

    def heibaishuangsha_video(self):
        try:
            response = requests.get(url=BASE_URL_HEIBAISHUANGSHA_VIDEO)
            if response.status_code == 200:
                logger.info(f"黑白双煞视频接口获取成功:{response.content[:10]}")
                video_bytes = response.content
                video_in_memory = BytesIO(video_bytes)
                return video_in_memory
            else:
                logger.error(f"黑白双煞视频接口请求失败:{response.status_code}")
        except Exception as e:
            logger.error(f"黑白双煞视频接口抛出异常:{e}")
        return None

    def shuaige_video(self):
        try:
            response = requests.get(url=BASE_URL_SHUAIGE_VIDEO)
            if response.status_code == 200:
                logger.info(f"帅哥视频接口获取成功:{response.content[:10]}")
                video_bytes = response.content
                video_in_memory = BytesIO(video_bytes)
                return video_in_memory
            else:
                logger.error(f"帅哥视频接口请求失败:{response.status_code}")
        except Exception as e:
            logger.error(f"帅哥视频接口抛出异常:{e}")
        return None

    def dasese_pic(self):
        try:
            response = requests.get(url=BASE_URL_DASESE)
            if response.status_code == 200:
                logger.info(f"大色色图片接口获取成功:{response.content[:10]}")
                image_bytes = response.content
                image_in_memory = BytesIO(image_bytes)
                return image_in_memory
            else:
                logger.error(f"大色色图片接口请求失败:{response.status_code}")
        except Exception as e:
            logger.error(f"大色色图片接口抛出异常:{e}")
        return None

