// your-script.js
let imageFiles = [];
let currentIndex = 0;
const imageCanvas = document.getElementById('image-canvas');
const imageContext = imageCanvas.getContext('2d');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');

async function openFolder() {
    try {
        const directoryHandle = await window.showDirectoryPicker();
        imageFiles = await getImagesFromFolder(directoryHandle);
        if (imageFiles.length > 0) {
            enableNavigationButtons();
            displayImage(currentIndex);
        }
    } catch (error) {
        console.error("无法打开文件夹:", error);
    }
}

async function getImagesFromFolder(directoryHandle) {
    let files = [];
    for await (const entry of directoryHandle.values()) {
        if (entry.kind === 'file' && entry.name.match(/\.(jpg|jpeg|png|gif)$/i)) {
            files.push(entry);
        }
    }
    return files;
}

function displayImage(index) {
    if (index < 0 || index >= imageFiles.length) {
        console.error("图片索引超出范围");
        return;
    }

    const file = imageFiles[index];
    const image = new Image();
    image.onload = () => {
        imageContext.clearRect(0, 0, imageCanvas.width, imageCanvas.height);
        imageContext.drawImage(image, 0, 0, imageCanvas.width, imageCanvas.height);
        currentIndex = index;
    };

    if (file) {
        image.src = URL.createObjectURL(file);
    }
}

function changeImage(delta) {
    let newIndex = currentIndex + delta;
    if (newIndex >= 0 && newIndex < imageFiles.length) {
        displayImage(newIndex);
    }
}

function enableNavigationButtons() {
    prevBtn.disabled = false;
    nextBtn.disabled = false;
}

// 当页面加载完成后，可以通过点击“打开文件夹”按钮来打开文件夹
