# Testing Guide - 项目测试指南

这是给新手准备的详细测试指南，教您如何在本地测试这个项目。

## 前置要求

- ✅ Mac 或 Linux 系统
- ✅ 已安装 Python 3.7+
- ✅ 有 MiniMax API Key

## 🚀 快速开始

### 1. 下载项目

打开终端（Terminal），复制粘贴以下命令：

```bash
# 进入桌面
cd ~/Desktop

# 克隆项目
git clone https://github.com/irismaker/pdf-to-audio.git

# 进入项目目录
cd pdf-to-audio
```

### 2. 安装依赖

```bash
pip3 install -r requirements.txt
```

如果提示权限错误，使用：
```bash
pip3 install --user -r requirements.txt
```

### 3. 配置 API Key

```bash
# 复制配置文件
cp config_example.py config.py

# 用编辑器打开（Mac）
open -e config.py

# 用编辑器打开（Linux）
# nano config.py
```

修改这一行：
```python
"minimax": "your_minimax_api_key_here",  # 改成你的真实 API Key
```

保存并关闭文件。

### 4. 准备 PDF 文件

**选项 A：使用测试 PDF**

如果您已经有 PDF 文件，复制到项目目录：
```bash
cp ~/Downloads/your-file.pdf ./test.pdf
```

**选项 B：创建测试 PDF**

在 Mac 上：
1. 打开 TextEdit 或任何应用
2. 写一些文字，比如："这是一个测试文档。Hello, this is a test."
3. 文件 → 打印 → 存储为 PDF
4. 保存为 `test.pdf` 到项目目录

### 5. 运行程序

```bash
# 使用快速启动（推荐）
python3 quick_start.py
```

或者：

```bash
# 使用主程序
python3 pdf_to_audio.py
```

按照屏幕提示操作即可！

### 6. 查看结果

转换完成后：

```bash
# 打开输出目录
open audio_output

# 或者查看文件列表
ls -lh audio_output/
```

在 `audio_output` 目录中找到生成的 MP3 文件，双击播放！

## 📝 示例操作流程

```bash
# 完整的操作示例
cd ~/Desktop
git clone https://github.com/irismaker/pdf-to-audio.git
cd pdf-to-audio
pip3 install -r requirements.txt
cp config_example.py config.py

# 编辑 config.py，填入 API Key
open -e config.py

# 复制 PDF 文件到当前目录
cp ~/Downloads/document.pdf ./

# 运行程序
python3 quick_start.py

# 程序会显示找到的 PDF 文件，选择转换
# 转换完成后，查看结果
open audio_output
```

## ⚙️ 自定义设置

### 更改语音设置

编辑 `config.py`：

```python
MINIMAX_CONFIG = {
    "default_voice_settings": {
        "speed": 1.2,        # 语速加快 20%
        "pitch": 2,          # 音调提高 2 度
        "voice_id": "female-tianmei",  # 使用甜美女声
        "emotion": "happy"   # 快乐情感
    }
}
```

### 可用的音色

**男声：**
- `male-qn-qingse` - 青涩男声
- `male-qn-jingying` - 精英男声
- `male-qn-badao` - 霸道男声
- `male-qn-daxuesheng` - 大学生男声

**女声：**
- `female-shaonv` - 少女音
- `female-yujie` - 御姐音
- `female-chengshu` - 成熟女声
- `female-tianmei` - 甜美女声

## 🐛 常见问题

### 问题 1：`ModuleNotFoundError: No module named 'requests'`

**解决方案：**
```bash
pip3 install requests PyPDF2
```

### 问题 2：`Permission denied`

**解决方案：**
```bash
# 使用 --user 安装
pip3 install --user -r requirements.txt
```

### 问题 3：PDF 提取不到文字

**原因：** PDF 可能是扫描版（图片）

**解决方案：** 使用包含可选择文字的 PDF

### 问题 4：API 返回 401 错误

**原因：** API Key 无效或未设置

**解决方案：**
1. 检查 `config.py` 中的 API Key 是否正确
2. 确保已保存文件
3. 确认 API Key 有效且有额度

### 问题 5：转换速度慢

**原因：**
- 网络连接慢
- API 服务器响应慢
- PDF 文本很长

**解决方案：**
- 检查网络连接
- 尝试较小的 PDF 文件
- 等待处理完成

## 📚 进阶使用

### 作为 Python 模块使用

创建一个新文件 `my_script.py`：

```python
from pdf_to_audio import PDFToAudioConverter

# 创建转换器
converter = PDFToAudioConverter(
    provider_name="minimax",
    api_key="your_api_key_here"
)

# 转换单个文件
converter.convert_pdf_to_audio(
    pdf_path="document.pdf",
    output_dir="my_audio"
)

# 批量转换
converter.batch_convert(
    pdf_dir="./pdfs",
    output_dir="./audio"
)
```

运行：
```bash
python3 my_script.py
```

## 🎉 完成！

现在您已经成功测试了项目！如果遇到任何问题，请查看：
- GitHub Issues: https://github.com/irismaker/pdf-to-audio/issues
- 主 README: https://github.com/irismaker/pdf-to-audio

Happy converting! 🎙️
