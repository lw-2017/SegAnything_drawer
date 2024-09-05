import os

folder_path = '/home/lwq/图片/喷水测试图片'
image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
image_files.sort()
print(image_files.value)