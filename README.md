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