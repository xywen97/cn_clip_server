## Chinese Clip Server

### server
1. 可独立运行
2. python server.py 启动服务器
3. port: 8080
4. 接收请求格式(json)：
```
{
    "text": str,
    "image": str (base64)
}
```
5. 返回结果格式(json)：
```
{
    "result_text": list of embedding,
    "result_image": list of embedding
}
```

### client
1. 模拟客户端
2. python client.py 启动客户端
3. 两个可选参数：
```
--text: str
--image_path: str
```

### model
1. start_model：用于启动模型
2. my_clip: 用于处理文本和图片的embedding


### requirements
1. pre-trained clip models:
    1. [ViT-L-14] https://clip-cn-beijing.oss-cn-beijing.aliyuncs.com/checkpoints/clip_cn_vit-l-14.pt
    2. [ViT-B-16] https://clip-cn-beijing.oss-cn-beijing.aliyuncs.com/checkpoints/clip_cn_vit-b-16.pt
2. for Network Address Translator (NAT)：
    1. Use [花生壳] https://hsk.oray.com/
    2. 花生壳本地客户端：https://hsk.oray.com/download
        2.1 linux
        2.2 windows
    3. linux 教程 https://service.oray.com/question/11630.html