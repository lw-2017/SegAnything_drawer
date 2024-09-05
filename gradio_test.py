import gradio as gr
import os
from PIL import Image
import json
import zipfile

import torch
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry, SamPredictor

# 假设我们有一个模型推理函数，这里用伪代码代替
def model_inference(image):
    # 这里应该是你的模型推理代码，返回推理结果
    # 以下为示例返回值，实际应用时需要替换为模型的预测结果
    return {"prediction": "example_prediction"}

# 保存标签
def save_label(image_name, label):
    with open(image_name.replace('.jpg', '.json'), 'w') as f:
        json.dump(label, f)

# 加载图片
def load_image(image_path):
    return Image.open(image_path)

# 单张图片推理
def single_image_inference(image_path):
    image = load_image(image_path)
    label = model_inference(image)
    save_label(image_path, label)
    return image, label


if __name__ == '__main__':

    # 选择设备
    if torch.cuda.is_available():
        print('Using GPU')
        device = 'cuda'
    else:
        print('CUDA not available. Please connect to a GPU instance if possible.')
        device = 'cpu'
    # 加载模型
    sam_checkpoint = "./sam_vit_l_0b3195.pth" # "sam_vit_l_0b3195.pth" or "sam_vit_h_4b8939.pth"
    model_type = "vit_l" # "vit_l" or "vit_h"

    print("Loading model")
    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint).to(device)
    print("Finishing loading")
    predictor = SamPredictor(sam)
    mask_generator = SamAutomaticMaskGenerator(sam)
    # 模型加载完成

    # 创建Gradio界面
    with gr.Blocks() as demo:
        gr.Markdown("数据自动标注工具")

        with gr.Row():
            with gr.Column():
                single_image_input = gr.Image(label="请选择图片")
                btn_run_single = gr.Button("单张图片推理")
                img_files = gr.State([])
                current_index = gr.State(0)

            with gr.Column():
                output_image = gr.Image(label="图片显示")
                output_label = gr.JSON(label="推理结果")

        # 设置按钮回调
        btn_run_single.click(fn=single_image_inference, inputs=single_image_input, outputs=[output_image, output_label])

    # 启动Gradio界面，并指定IP和端口
    demo.launch(server_name="0.0.0.0", server_port=8089)
