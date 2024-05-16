# encoding:utf-8

"""
wechat channel
"""

import io
import json
import os
import threading
import time
import random
import requests

from bridge.context import *
from bridge.reply import *
from channel.chat_channel import ChatChannel
from channel import chat_channel
from channel.wechat.wechat_message import *
from common.expired_dict import ExpiredDict
from common.log import logger
from common.singleton import singleton
from common.time_check import time_checker
from config import conf, get_appdata_dir
from lib import itchat
from lib.itchat.content import *


@itchat.msg_register([TEXT, VOICE, PICTURE, NOTE, ATTACHMENT, SHARING])
def handler_single_msg(msg):
    try:
        cmsg = WechatMessage(msg, False)
    except NotImplementedError as e:
        logger.debug("[WX]single message {} skipped: {}".format(msg["MsgId"], e))
        return None
    # 如果收到的是自定义消息
    if cmsg.ctype == ContextType.TEXT and cmsg.content == "测试":
        # 发送自定义回复
        itchat.send("回复测试消息", toUserName=cmsg.other_user_id)
        return
    if cmsg.ctype == ContextType.TEXT and cmsg.content == "测试图片回复":
        # 发送图片回复
        itchat.send_image("/Users/isaac/Documents/costway_dify/static_files/image/test.jpg",
                          toUserName=cmsg.other_user_id)
        return
    if cmsg.ctype == ContextType.TEXT and cmsg.content == "测试视频回复":
        # 发送视频回复
        itchat.send_video("/Users/isaac/Documents/costway_dify/static_files/video/test.mp4",
                          toUserName=cmsg.other_user_id)
        return
    if cmsg.ctype == ContextType.TEXT and cmsg.content == "测试文件回复":
        # 发送文件回复
        itchat.send_file("/Users/isaac/Documents/costway_dify/static_files/file/test.txt",
                         toUserName=cmsg.other_user_id)
        return
    WechatChannel().handle_single(cmsg)
    return None


@itchat.msg_register([TEXT, VOICE, PICTURE, NOTE, ATTACHMENT, SHARING], isGroupChat=True)
def handler_group_msg(msg):
    image_path = "/Users/isaac/Documents/costway_dify/static_files/image/"
    image_path_data = "/Users/isaac/Documents/costway_dify/static_files/image/咸鱼资料/"

    image_path_dog = "/Users/isaac/Documents/costway_dify/static_files/image/舔狗日记"
    image_path_man = "/Users/isaac/Documents/costway_dify/static_files/image/渣男语录"
    image_dict = {
        "进阶图": f"{image_path_data}进阶图.jpg",
        "金币图": f"{image_path_data}金币图.jpg",
        "军团币": f"{image_path_data}军团币.jpg",
        "VIP图": f"{image_path_data}VIP图.jpg",
        "玩具被动": f"{image_path_data}玩具被动.jpg",
        "武将升星": f"{image_path_data}武将升星.jpg",
        "梦魔水晶": f"{image_path_data}梦魔水晶.jpg",
        "玩具扳手": f"{image_path_data}玩具扳手.jpg",
        "每日咸王": f"{image_path_data}每日咸王.jpg",
        "排位对战": f"{image_path_data}排位对战.jpg",
        "金色水晶": f"{image_path_data}金色水晶.jpg",
        "红色水晶": f"{image_path_data}红色水晶.jpg",
        "属性上限": f"{image_path_data}属性上限.jpg",
        "洗练属性": f"{image_path_data}洗练属性.jpg",
        "洗练概率": f"{image_path_data}洗练概率.jpg",
        "俱乐部人数": f"{image_path_data}俱乐部人数.jpg",
        "舔狗日记": f"{image_path_dog}/{random.choice(os.listdir(image_path_dog))}"
        if os.listdir(image_path_dog) else None,
        "渣男语录": f"{image_path_man}/{random.choice(os.listdir(image_path_man))}"
        if os.listdir(image_path_man) else None,
        "帮助": f"{image_path}menu.jpg",
        "菜单": f"{image_path}menu.jpg",
    }
    menu_text = "\n发送 '帮助' 或 '菜单' 查看更多功能"  # 菜单提示
    text_dict = {
        "sad": f"怎么啦小广，是碰到什么不好的事了嘛🥹{menu_text}",
        "贝贝": f"贝贝是爸爸的爱人，她很可爱哦😊{menu_text}",
        "吴广安": f"吴广安是小菜瓜🐸{menu_text}",
        "Isaac": f"Isaac是小宝的爸爸,他是个厉害的人💫{menu_text}",
        "朱欣园": f"Isaac是小宝的爸爸,他是个厉害的人💫{menu_text}",
    }
    video_path = "/Users/isaac/Documents/costway_dify/static_files/video/"
    video_xiaojiejie_path = "/Users/isaac/Documents/costway_dify/static_files/video/小姐姐/"
    video_xiaogege_path = "/Users/isaac/Documents/costway_dify/static_files/video/小哥哥/"
    video_dict = {
        "测试视频": f"{video_path}test.mp4",
        "小姐姐视频": f"{video_xiaojiejie_path}/{random.choice(os.listdir(video_xiaojiejie_path))}"
        if os.listdir(video_xiaojiejie_path) else None,
        "小哥哥视频": f"{video_xiaogege_path}/{random.choice(os.listdir(video_xiaogege_path))}"
        if os.listdir(video_xiaogege_path) else None,
        "狱卒": f"{video_xiaojiejie_path}/{random.choice(os.listdir(video_xiaojiejie_path))}"
        if os.listdir(video_xiaojiejie_path) else None,
        "甜美": f"{video_xiaojiejie_path}/{random.choice(os.listdir(video_xiaojiejie_path))}"
        if os.listdir(video_xiaojiejie_path) else None,
        "jk": f"{video_xiaojiejie_path}/{random.choice(os.listdir(video_xiaojiejie_path))}"
        if os.listdir(video_xiaojiejie_path) else None,
        "欲梦": f"{video_xiaojiejie_path}/{random.choice(os.listdir(video_xiaojiejie_path))}"
        if os.listdir(video_xiaojiejie_path) else None,
        "双倍快乐": f"{video_xiaojiejie_path}/{random.choice(os.listdir(video_xiaojiejie_path))}"
        if os.listdir(video_xiaojiejie_path) else None,
        "热舞": f"{video_xiaojiejie_path}/{random.choice(os.listdir(video_xiaojiejie_path))}"
        if os.listdir(video_xiaojiejie_path) else None,
        "萝莉": f"{video_xiaojiejie_path}/{random.choice(os.listdir(video_xiaojiejie_path))}"
        if os.listdir(video_xiaojiejie_path) else None,
        "蛇姐": f"{video_xiaojiejie_path}/{random.choice(os.listdir(video_xiaojiejie_path))}"
        if os.listdir(video_xiaojiejie_path) else None,
        "漫画芋": f"{video_xiaojiejie_path}/{random.choice(os.listdir(video_xiaojiejie_path))}"
        if os.listdir(video_xiaojiejie_path) else None,
    }
    file_path = "/Users/isaac/Documents/costway_dify/static_files/file/"
    file_dict = {
        "测试文件": f"{file_path}test.txt",
    }
    try:
        cmsg = WechatMessage(msg, True)
    except NotImplementedError as e:
        logger.debug("[WX]group message {} skipped: {}".format(msg["MsgId"], e))
        return None
    # 如果收到的是自定义消息
    if cmsg.ctype == ContextType.TEXT:

        # 匹配自定义回复
        match cmsg.content:
            # 匹配文本回复
            case content if content in text_dict:
                itchat.send(text_dict[content], toUserName=cmsg.other_user_id)
                return
            # 匹配图片回复
            case content if content in image_dict:
                image_path = image_dict[content]
                itchat.send_image(image_path, toUserName=cmsg.other_user_id)
                return
            # 匹配视频回复
            case content if content in video_dict:
                video_path = video_dict[content]
                itchat.send_video(video_path, toUserName=cmsg.other_user_id)
                return
            # 匹配文件回复
            case content if content in file_dict:
                file_path = file_dict[content]
                itchat.send_file(file_path, toUserName=cmsg.other_user_id)
                return
            case _:
                WechatChannel().handle_group(cmsg)
                return None
    WechatChannel().handle_group(cmsg)
    return None


# 自动接受加好友
@itchat.msg_register(FRIENDS)
def deal_with_friend(msg):
    try:
        cmsg = WechatMessage(msg, False)
    except NotImplementedError as e:
        logger.debug("[WX]friend request {} skipped: {}".format(msg["MsgId"], e))
        return None
    WechatChannel().handle_friend_request(cmsg)
    return None


def _check(func):
    def wrapper(self, cmsg: ChatMessage):
        msgId = cmsg.msg_id
        if msgId in self.receivedMsgs:
            logger.info("Wechat message {} already received, ignore".format(msgId))
            return
        self.receivedMsgs[msgId] = True
        create_time = cmsg.create_time  # 消息时间戳
        if conf().get("hot_reload") == True and int(create_time) < int(time.time()) - 60:  # 跳过1分钟前的历史消息
            logger.debug("[WX]history message {} skipped".format(msgId))
            return
        if cmsg.my_msg and not cmsg.is_group:
            logger.debug("[WX]my message {} skipped".format(msgId))
            return
        return func(self, cmsg)

    return wrapper


# 可用的二维码生成接口
# https://api.qrserver.com/v1/create-qr-code/?size=400×400&data=https://www.abc.com
# https://api.isoyu.com/qr/?m=1&e=L&p=20&url=https://www.abc.com
def qrCallback(uuid, status, qrcode):
    # logger.debug("qrCallback: {} {}".format(uuid,status))
    if status == "0":
        try:
            from PIL import Image

            img = Image.open(io.BytesIO(qrcode))
            _thread = threading.Thread(target=img.show, args=("QRCode",))
            _thread.setDaemon(True)
            _thread.start()
        except Exception as e:
            pass

        import qrcode

        url = f"https://login.weixin.qq.com/l/{uuid}"

        qr_api1 = "https://api.isoyu.com/qr/?m=1&e=L&p=20&url={}".format(url)
        qr_api2 = "https://api.qrserver.com/v1/create-qr-code/?size=400×400&data={}".format(url)
        qr_api3 = "https://api.pwmqr.com/qrcode/create/?url={}".format(url)
        qr_api4 = "https://my.tv.sohu.com/user/a/wvideo/getQRCode.do?text={}".format(url)
        print("You can also scan QRCode in any website below:")
        print(qr_api3)
        print(qr_api4)
        print(qr_api2)
        print(qr_api1)
        _send_qr_code([qr_api1, qr_api2, qr_api3, qr_api4])
        qr = qrcode.QRCode(border=1)
        qr.add_data(url)
        qr.make(fit=True)
        qr.print_ascii(invert=True)


class Watchdog:
    """
    看门狗类，用于监控文件变化
    """

    def __init__(self, filename, interval, callback):
        self.filename = filename  # 文件名
        self.interval = interval  # 检查间隔
        self.callback = callback  # 回调函数
        self.last_checked_content = None  # 上次读取的文件内容

    def check_file(self):
        try:
            with open(self.filename, 'r') as file:
                file_content = file.read().strip()
                if not file_content:
                    time.sleep(1)  # 休眠一秒钟
                    return

                try:
                    data_list = json.loads(file_content)
                except json.JSONDecodeError as e:
                    logger.error(f"JSON解析错误: {e}")
                    return

                if data_list:
                    for data in data_list:
                        handle_message(data)
                    with open(self.filename, 'w') as file:
                        file.write('')
                else:
                    logger.error("读取的JSON数据为空,不执行发送")
        except Exception as e:
            logger.error(f"读取JSON文件异常: {e}")
            time.sleep(1)

    def start(self):
        while True:
            self.check_file()
            time.sleep(self.interval)


def handle_message(data: dict) -> None:
    """
    处理消息内容
    :param data: 消息内容
    """
    try:
        receiver_name = data["receiver_name"]  # 获取接收者名称
        message = data["message"]  # 获取消息内容
        group_name = data["group_name"]  # 获取群聊名称

        # 判断是否是群聊
        if group_name:
            # 判断是否有@的名字,群聊消息,reviewer_name可以为空
            if receiver_name:
                chatroom = itchat.search_chatrooms(name=group_name)[0]  # 根据群聊名称查找群聊
                if receiver_name == "所有人" or receiver_name == "all":
                    message = f"@所有人 {message}"  # 拼接消息内容
                    itchat.send(msg=f"{message}", toUserName=chatroom.UserName)  # 发送消息
                else:
                    # 发送群聊消息,并且@指定好友
                    friends = itchat.instance.storageClass.search_friends(remarkName=receiver_name)
                    if friends:
                        nickname = friends[0].NickName
                        message = f"@{nickname} {message}"  # 拼接消息内容
                        itchat.send(msg=f"{message}", toUserName=chatroom.UserName)  # 发送消息
                    else:
                        # 如果没有找到指定好友,就直接发送消息,不@任何人
                        itchat.send(msg=message, toUserName=chatroom.UserName)  # 发送消息
                logger.info(f"手动发送微信群聊消息成功, 发送群聊:{group_name} 消息内容：{message}")
            else:
                # 发送群聊消息
                chatroom = itchat.search_chatrooms(name=group_name)[0]  # 根据群聊名称查找群聊
                if chatroom:
                    itchat.send(msg=message, toUserName=chatroom.UserName)  # 发送消息
                    logger.info(f"手动发送微信群聊消息成功, 发送群聊:{group_name} 消息内容：{message}")
        else:
            remarkName = itchat.instance.storageClass.search_friends(remarkName=receiver_name)  # 根据好友备注名查找好友
            if remarkName:
                itchat.send(message, toUserName=remarkName[0].UserName)  # 发送消息
                logger.info(f"手动发送微信消息成功, 发送人:{remarkName[0].NickName} 消息内容：{message}")
            else:
                logger.error(f"没有找到对应的好友：{remarkName}")
    except Exception as e:
        logger.error(f"处理消息时发生异常: {e}")
    finally:
        # 发送消息后,从JSON文件中删除已发送的消息
        with open('message.json', 'r') as file:
            data_list = json.load(file)
        data_list.remove(data)
        # 将删除后的数据写入到文件中
        with open('message.json', 'w') as file:
            json.dump(data_list, file, ensure_ascii=False)
        logger.info(f"已从message.json文件中删除已发送的消息{data}")


def send_message():
    """
    发送消息
    """
    # 创建看门狗实例，监控 message.json 文件，每隔5秒检查一次，有变化时调用 handle_message 处理
    watchdog = Watchdog('message.json', 5, handle_message)
    thread = threading.Thread(target=watchdog.start)  # 创建线程,并指定线程执行的函数
    thread.daemon = True  # 设置为守护线程
    thread.start()  # 启动线程


@singleton
class WechatChannel(ChatChannel):
    NOT_SUPPORT_REPLYTYPE = []

    def __init__(self):
        super().__init__()
        self.receivedMsgs = ExpiredDict(60 * 60)
        self.auto_login_times = 0

    def startup(self):
        try:
            itchat.instance.receivingRetryCount = 600  # 修改断线超时时间
            # login by scan QRCode
            hotReload = conf().get("hot_reload", False)
            status_path = os.path.join(get_appdata_dir(), "itchat.pkl")
            itchat.auto_login(
                enableCmdQR=2,
                hotReload=hotReload,
                statusStorageDir=status_path,
                qrCallback=qrCallback,
                exitCallback=self.exitCallback,
                loginCallback=self.loginCallback
            )
            self.user_id = itchat.instance.storageClass.userName
            self.name = itchat.instance.storageClass.nickName
            logger.info("Wechat login success, user_id: {}, nickname: {}".format(self.user_id, self.name))
            # 增加手动发微信通知的方法
            send_message()
            # start message listener
            itchat.run()
        except Exception as e:
            logger.error(e)

    def exitCallback(self):
        try:
            from common.linkai_client import chat_client
            if chat_client.client_id and conf().get("use_linkai"):
                _send_logout()
                time.sleep(2)
                self.auto_login_times += 1
                if self.auto_login_times < 100:
                    chat_channel.handler_pool._shutdown = False
                    self.startup()
        except Exception as e:
            pass

    def loginCallback(self):
        logger.debug("Login success")
        _send_login_success()

    # handle_* 系列函数处理收到的消息后构造Context，然后传入produce函数中处理Context和发送回复
    # Context包含了消息的所有信息，包括以下属性
    #   type 消息类型, 包括TEXT、VOICE、IMAGE_CREATE
    #   content 消息内容，如果是TEXT类型，content就是文本内容，如果是VOICE类型，content就是语音文件名，如果是IMAGE_CREATE类型，content就是图片生成命令
    #   kwargs 附加参数字典，包含以下的key：
    #        session_id: 会话id
    #        isgroup: 是否是群聊
    #        receiver: 需要回复的对象
    #        msg: ChatMessage消息对象
    #        origin_ctype: 原始消息类型，语音转文字后，私聊时如果匹配前缀失败，会根据初始消息是否是语音来放宽触发规则
    #        desire_rtype: 希望回复类型，默认是文本回复，设置为ReplyType.VOICE是语音回复
    @time_checker
    @_check
    def handle_single(self, cmsg: ChatMessage):
        # filter system message
        if cmsg.other_user_id in ["weixin"]:
            return
        if cmsg.ctype == ContextType.VOICE:
            if conf().get("speech_recognition") != True:
                return
            logger.debug("[WX]receive voice msg: {}".format(cmsg.content))
        elif cmsg.ctype == ContextType.IMAGE:
            logger.debug("[WX]receive image msg: {}".format(cmsg.content))
        elif cmsg.ctype == ContextType.PATPAT:
            logger.debug("[WX]receive patpat msg: {}".format(cmsg.content))
        elif cmsg.ctype == ContextType.TEXT:
            logger.debug("[WX]receive text msg: {}, cmsg={}".format(json.dumps(cmsg._rawmsg, ensure_ascii=False), cmsg))
        else:
            logger.debug("[WX]receive msg: {}, cmsg={}".format(cmsg.content, cmsg))
        context = self._compose_context(cmsg.ctype, cmsg.content, isgroup=False, msg=cmsg)
        if context:
            self.produce(context)

    @time_checker
    @_check
    def handle_group(self, cmsg: ChatMessage):
        if cmsg.ctype == ContextType.VOICE:
            if conf().get("group_speech_recognition") != True:
                return
            logger.debug("[WX]receive voice for group msg: {}".format(cmsg.content))
        elif cmsg.ctype == ContextType.IMAGE:
            logger.debug("[WX]receive image for group msg: {}".format(cmsg.content))
        elif cmsg.ctype in [ContextType.JOIN_GROUP, ContextType.PATPAT, ContextType.ACCEPT_FRIEND,
                            ContextType.EXIT_GROUP]:
            logger.debug("[WX]receive note msg: {}".format(cmsg.content))
        elif cmsg.ctype == ContextType.TEXT:
            # logger.debug("[WX]receive group msg: {}, cmsg={}".format(json.dumps(cmsg._rawmsg, ensure_ascii=False), cmsg))
            pass
        elif cmsg.ctype == ContextType.FILE:
            logger.debug(f"[WX]receive attachment msg, file_name={cmsg.content}")
        else:
            logger.debug("[WX]receive group msg: {}".format(cmsg.content))
        context = self._compose_context(cmsg.ctype, cmsg.content, isgroup=True, msg=cmsg)
        if context:
            self.produce(context)

    @time_checker
    @_check
    def handle_friend_request(self, cmsg: ChatMessage):
        if cmsg.ctype == ContextType.ACCEPT_FRIEND:
            logger.debug("[WX]receive friend request: {}".format(cmsg.content["NickName"]))
        else:
            logger.debug("[WX]receive friend request: {}, cmsg={}".format(cmsg.content["NickName"], cmsg))
        context = self._compose_context(cmsg.ctype, cmsg.content, msg=cmsg)
        if context:
            self.produce(context)

    # 统一的发送函数，每个Channel自行实现，根据reply的type字段发送不同类型的消息
    def send(self, reply: Reply, context: Context):
        receiver = context.get("receiver")
        if reply.type == ReplyType.TEXT:
            itchat.send(reply.content, toUserName=receiver)
            logger.info("[WX] sendMsg={}, receiver={}".format(reply, receiver))
        elif reply.type == ReplyType.ERROR or reply.type == ReplyType.INFO:
            itchat.send(reply.content, toUserName=receiver)
            logger.info("[WX] sendMsg={}, receiver={}".format(reply, receiver))
        elif reply.type == ReplyType.VOICE:
            itchat.send_file(reply.content, toUserName=receiver)
            logger.info("[WX] sendFile={}, receiver={}".format(reply.content, receiver))
        elif reply.type == ReplyType.IMAGE_URL:  # 从网络下载图片
            img_url = reply.content
            logger.debug(f"[WX] start download image, img_url={img_url}")
            pic_res = requests.get(img_url, stream=True)
            image_storage = io.BytesIO()
            size = 0
            for block in pic_res.iter_content(1024):
                size += len(block)
                image_storage.write(block)
            logger.info(f"[WX] download image success, size={size}, img_url={img_url}")
            image_storage.seek(0)
            itchat.send_image(image_storage, toUserName=receiver)
            logger.info("[WX] sendImage url={}, receiver={}".format(img_url, receiver))
        elif reply.type == ReplyType.IMAGE:  # 从文件读取图片
            image_storage = reply.content
            image_storage.seek(0)
            itchat.send_image(image_storage, toUserName=receiver)
            logger.info("[WX] sendImage, receiver={}".format(receiver))
        elif reply.type == ReplyType.FILE:  # 新增文件回复类型
            file_storage = reply.content
            itchat.send_file(file_storage, toUserName=receiver)
            logger.info("[WX] sendFile, receiver={}".format(receiver))
        elif reply.type == ReplyType.VIDEO:  # 新增视频回复类型
            video_storage = reply.content
            itchat.send_video(video_storage, toUserName=receiver)
            logger.info("[WX] sendFile, receiver={}".format(receiver))
        elif reply.type == ReplyType.VIDEO_URL:  # 新增视频URL回复类型
            video_url = reply.content
            logger.debug(f"[WX] start download video, video_url={video_url}")
            video_res = requests.get(video_url, stream=True)
            video_storage = io.BytesIO()
            size = 0
            for block in video_res.iter_content(1024):
                size += len(block)
                video_storage.write(block)
            logger.info(f"[WX] download video success, size={size}, video_url={video_url}")
            video_storage.seek(0)
            itchat.send_video(video_storage, toUserName=receiver)
            logger.info("[WX] sendVideo url={}, receiver={}".format(video_url, receiver))
        elif reply.type == ReplyType.ACCEPT_FRIEND:  # 新增接受好友申请回复类型
            # 假设 reply.content 包含了新好友的用户名
            is_accept = reply.content
            if is_accept:
                try:
                    # 自动接受好友申请
                    debug_msg = itchat.accept_friend(userName=context.content["UserName"], v4=context.content["Ticket"])
                    logger.debug("[WX] accept_friend return: {}".format(debug_msg))
                    logger.info("[WX] Accepted new friend, UserName={}, NickName={}".format(context.content["UserName"],
                                                                                            context.content[
                                                                                                "NickName"]))
                except Exception as e:
                    logger.error("[WX] Failed to add friend. Error: {}".format(e))
            else:
                logger.info("[WX] Ignored new friend, username={}".format(context.content["NickName"]))
        elif reply.type == ReplyType.INVITE_ROOM:  # 新增邀请好友进群回复类型
            # 假设 reply.content 包含了群聊的名字

            def get_group_id(group_name):
                """
                根据群聊名称获取群聊ID。
                :param group_name: 群聊的名称。
                :return: 群聊的ID (UserName)。
                """
                group_list = itchat.search_chatrooms(name=group_name)
                if group_list:
                    return group_list[0]["UserName"]
                else:
                    return None

            try:
                chatroomUserName = reply.content
                group_id = get_group_id(chatroomUserName)
                logger.debug("[WX] find group_id={}, where chatroom={}".format(group_id, chatroomUserName))
                if group_id is None:
                    raise ValueError("The specified group chat was not found: {}".format(chatroomUserName))
                # 调用 itchat 的 add_member_into_chatroom 方法来添加成员
                debug_msg = itchat.add_member_into_chatroom(group_id, receiver)
                logger.debug("[WX] add_member_into_chatroom return: {}".format(debug_msg))
                logger.info("[WX] invite members={}, to chatroom={}".format(receiver, chatroomUserName))
            except ValueError as ve:
                # 记录查找群聊失败的错误信息
                logger.error("[WX] {}".format(ve))
            except Exception as e:
                # 记录添加成员失败的错误信息
                logger.error("[WX] Failed to invite members to chatroom. Error: {}".format(e))


def _send_login_success():
    try:
        from common.linkai_client import chat_client
        if chat_client.client_id:
            chat_client.send_login_success()
    except Exception as e:
        pass


def _send_logout():
    try:
        from common.linkai_client import chat_client
        if chat_client.client_id:
            chat_client.send_logout()
    except Exception as e:
        pass


def _send_qr_code(qrcode_list: list):
    try:
        from common.linkai_client import chat_client
        if chat_client.client_id:
            chat_client.send_qrcode(qrcode_list)
    except Exception as e:
        pass
