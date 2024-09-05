import gradio as gr
import os
from PIL import Image
import json
import zipfile

# 模型推理函数
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

# 文件夹图片推理
def folder_image_inference(folder_path, img_files, current_index):
    unzip_folder_path = folder_path.split('.zip')[0]
    with zipfile.ZipFile(folder_path, 'r') as zip_ref:
        zip_ref.extractall(unzip_folder_path) # 解压后的目录
    folder_path = unzip_folder_path
    image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    image_files.sort()
    print('***', image_files)
    image = load_image(image_files[0])
    label = model_inference(image)
    save_label(image_files[0], label)
    return image, label, image_files, 0  # 返回新的列表和索引值

# 下一张图片按钮的回调
def next_image(img_files, current_index):
    new_index = current_index + 1
    if new_index < len(img_files):
        image = load_image(img_files[new_index])
        label = model_inference(image)
        save_label(img_files[new_index], label)
        return image, label, new_index, True, True
    else:
        return img_files[current_index], {}, current_index, False, True

# 上一张图片按钮的回调
def prev_image(img_files, current_index):
    new_index = current_index - 1
    if new_index >= 0:
        image = load_image(img_files[new_index])
        label = model_inference(image)
        save_label(img_files[new_index], label)
        return image, label, new_index, True, True
    else:
        return img_files[current_index], {}, current_index, True, False

# 创建Gradio界面
with gr.Blocks() as demo:
    gr.Markdown("数据自动标注工具")

    with gr.Row():
        with gr.Column():
            single_image_input = gr.Image(label="请选择图片")
            folder_input = gr.File(label="请选择文件夹", type='filepath')
            btn_run_single = gr.Button("单张图片推理")
            btn_run_folder = gr.Button("文件夹推理")
            btn_next = gr.Button("下一张")
            btn_prev = gr.Button("上一张")
            img_files = gr.State([])
            current_index = gr.State(0)

        with gr.Column():
            output_image = gr.Image(label="图片显示")
            output_label = gr.JSON(label="推理结果")

    # 设置按钮回调
    btn_run_single.click(fn=single_image_inference, inputs=single_image_input, outputs=[output_image, output_label])
    btn_run_folder.click(fn=folder_image_inference, inputs=[folder_input, img_files, current_index], outputs=[output_image, output_label, img_files, current_index])

    # 下一张图片按钮的回调
    btn_next.click(fn=next_image, inputs=[img_files, current_index], outputs=[output_image, output_label, current_index, btn_prev, btn_next])

    # 上一张图片按钮的回调
    btn_prev.click(fn=prev_image, inputs=[img_files, current_index], outputs=[output_image, output_label, current_index, btn_prev, btn_next])

# 启动Gradio界面
demo.launch(server_name="0.0.0.0", server_port=8089)
