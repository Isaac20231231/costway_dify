from flask import Flask, request, jsonify
import json
from common.log import logger

app = Flask(__name__)


def validate_data(data_list):
    # 检查data_list是否为列表类型
    if not isinstance(data_list, list):
        raise ValueError('data_list必须为列表类型')
    # 检查data_list是否为空
    if not data_list:
        raise ValueError('data_list不能为空')
    # 遍历data_list,检查每个元素是否包含必要的字段
    for data in data_list:
        if not isinstance(data, dict):
            raise ValueError('data_list的每个元素必须为字典类型')
        if 'message' not in data:
            raise ValueError('每个消息必须包含message')


@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        # 获取请求中的数据
        data_list = request.json.get('data_list', [])  # 获取消息列表
        try:
            validate_data(data_list)
        except ValueError as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400

        # 将数据写入到message.json文件中
        with open('message.json', 'w') as file:
            json.dump(data_list, file, ensure_ascii=False)
        logger.info(f"写入成功,写入内容{data_list}")

        return jsonify({'status': 'success', 'message': '发送成功'}), 200
    except Exception as e:
        logger.error(f"处理请求时发生错误: {str(e)}")
        return jsonify({'status': 'error', 'message': '服务器内部错误'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8899, debug=False)
