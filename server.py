import base64
from flask import Flask, request, jsonify
from model import my_clip, start_model  # 导入现有的模型
import json
import cv2
import numpy as np
from PIL import Image

app = Flask(__name__)

@app.route('/api/process', methods=['GET', 'POST'])
def process():
    # 获取文本数据
    print('请求头:%s' % request.headers)       #打印结果为请求头信息
    print('请求方式:%s' % request.method)      #GET
    print('请求url地址:%s' % request.url)      # 请求url地址:http://127.0.0.1:5000/
    # print('请求数据:%s' % request.data)        # 请求数据:b'{name:"zs",age:18}'
    # print('请求数据:%s' % request.form)        # 请求数据:{'name': 'zs', 'age': 18}
    
    # 注意这里：如果想要得到data里面的name的值，直接使用request.data.get('name')是得不到值的，
    # 需要使用request.json.get('name')才能获取到数据，项目中觉得request.json经常会用到。
    
    # 补充：json.dumps(data)=>字典转字符串
    # 	 json.loads(data)=>字符串转字典
    
    # if request.form['text'] is not None:
    #     text = request.form['text']
    #     print("in form")
    # else:
    #     print("in data")
    #     text_json = request.data
    #     # change text to json
    #     text = json.loads(text_json)
    #     text = text['text']

    text, image = None, None

    text = request.json.get('text')
    image = request.json.get('image')
    # decode image from base64 to numpy array
    try:
        str_decode = base64.b64decode(image)
        nparr = np.fromstring(str_decode, np.uint8)
        # img_restore = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR) for python 2
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    except:
        image = None
        print("image is None")

    # if not isinstance(image, list):
    #     image = None
    # if not isinstance(text, str) or not isinstance(image, list):
    #     text = None
    print(text)
    # 调用现有的模型处理文本
    result = my_clip(text=text, image=image)

    if result is not None:
        if result[0] is not None:
            result_text = result[0]
            result_text = result_text[0]
        else:
            result_text = None

        if result[1] is not None:
            result_image = result[1]
            result_image = result_image[0]
        else:
            result_image = None

    print(result_text)
    print(result_image)

    # result = [1, 2, 3]
    # 返回处理结果
    return jsonify({'result_text': result_text, 'result_image': result_image})

if __name__ == '__main__':
    # start the model first
    warmup = start_model()
    # 运行 Flask 应用程序，允许公网访问
    app.run(host='0.0.0.0', port=8080)

