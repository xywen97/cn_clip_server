import torch 
from PIL import Image
import numpy as np

import cn_clip.clip as clip
from cn_clip.clip import load_from_name, available_models
print("Available models:", available_models())  
# Available models: ['ViT-B-16', 'ViT-L-14', 'ViT-L-14-336', 'ViT-H-14', 'RN50']

device = "cuda:0" if torch.cuda.is_available() else "cpu"
model, preprocess = None, None

def start_model():
    global model, preprocess
    model, preprocess = load_from_name("ViT-L-14", device=device, download_root='./')
    
    warmup = model.encode_text(clip.tokenize(["你好"]).to(device))
    return warmup

def my_clip(text=None, image=None):
    global model, preprocess
    image_features = None
    text_features = None

    with torch.no_grad():
        # model, preprocess = load_from_name("ViT-L-14", device=device, download_root='./')
        # model.eval()
        # image = preprocess(Image.open("examples/pokemon.jpeg")).unsqueeze(0).to(device)
        if image is None:
            image_tmp = Image.open("examples/pokemon.jpeg")
            image = preprocess(image_tmp).unsqueeze(0).to(device)
        else:
            if not isinstance(image, Image.Image):
                if not isinstance(image, np.ndarray):
                    image = np.array(image)
                    print(image.shape)
                # convert to PIL image
                image = Image.fromarray(np.uint8(image))
                image = preprocess(image).unsqueeze(0).to(device)
                image_features = model.encode_image(image)
                # 对特征进行归一化，请使用归一化后的图文特征用于下游任务
                image_features /= image_features.norm(dim=-1, keepdim=True) 
                # convert to numpy
                image_features = image_features.cpu().numpy()
                # convert to list
                image_features = image_features.tolist()

        # text = clip.tokenize(["杰尼龟", "妙蛙种子", "小火龙", "皮卡丘"]).to(device)
        if text is None:
            text = clip.tokenize(["杰尼龟"]).to(device)
        else:
            text = clip.tokenize([text]).to(device)
            text_features = model.encode_text(text)
            text_features /= text_features.norm(dim=-1, keepdim=True)
            text_features = text_features.cpu().numpy()
            text_features = text_features.tolist()

        # print(image_features.shape, text_features.shape)  # torch.Size([1, 512]) torch.Size([4, 512]

        # logits_per_image, logits_per_text = model.get_similarity(image, text)
        # probs = logits_per_image.softmax(dim=-1).cpu().numpy()

        # print("Label probs:", probs)  # [[1.268734e-03 5.436878e-02 6.795761e-04 9.436829e-01]]

        return text_features, image_features


if __name__ == '__main__':
    my_clip()