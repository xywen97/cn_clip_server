import base64
import requests
import argparse
from PIL import Image
import numpy as np
import cv2

# 向 Flask 后台发送文本数据，获取处理结果
def process(text=None, image=None):
    url = 'https://3542794fy3.imdo.co/api/process'
    data = {'text': text}
    if image is None:
        data['image'] = None
    else:
        if isinstance(image, np.ndarray):
            image = image.tolist()
        if isinstance(image, Image.Image):
            image = np.array(image)
            # encode image to base64
            img_str = cv2.imencode('.jpg', image)[1].tostring()
            image = base64.b64encode(img_str)
            image = image.decode('utf-8')
        data['image'] = image

    response = requests.post(url, json=data)
    if response.status_code == 200:
        result_text = response.json().get('result_text')
        result_image = response.json().get('result_image')
        return result_text, result_image
    else:
        return None, None

if __name__ == '__main__':
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser()
    # 添加命令行参数
    parser.add_argument('--text', type=str, default='Hello, World!')
    parser.add_argument('--image_path', type=str, default=None)
    # 解析命令行参数
    args = parser.parse_args()

    text, image = None, None

    # 获取命令行参数
    text = args.text

    # 测试数据
    # text = 'Hello, World!'
    # 调用 process 函数发送文本数据并获取处理结果
    if args.image_path:
        image = Image.open(args.image_path)
    
    result_text, result_image = process(text, image)
    # 打印处理结果
    print(result_text, result_image)
