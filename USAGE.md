# Kokoro TTS 中文语音合成 - 使用指南

## 快速开始

### 1. 环境准备
```bash
# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 基础使用

#### 单句合成
```bash
python kokoro_demo.py --text "你好，欢迎使用Kokoro语音合成" --output output/hello.wav
```

#### 批量合成
```bash
python kokoro_demo.py --batch
```

#### 指定语音模型
```bash
python kokoro_demo.py --text "测试不同的语音" --voice af_heart --output output/test.wav
```

### 3. Python API 调用

```python
import kokoro
import torchaudio

# 初始化
pipeline = kokoro.KPipeline('z', device='cpu')

# 合成语音
results = list(pipeline('你好世界', voice='af_heart'))
audio = results[0].audio

# 保存文件
torchaudio.save('output.wav', audio.unsqueeze(0), 24000)
```

### 4. 命令行参数

| 参数 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `--text` | `-t` | 默认测试文本 | 要合成的文本内容 |
| `--voice` | `-v` | `af_heart` | 语音模型名称 |
| `--output` | `-o` | `output/demo.wav` | 输出文件路径 |
| `--device` | `-d` | `cpu` | 计算设备 |
| `--batch` | - | - | 启用批量处理模式 |

## 可用语音模型

### 推荐语音
- `af_heart` - 女声，温暖亲切
- `zf_001` - 女声，清晰标准
- `zm_009` - 男声，沉稳有力

### 完整语音库
- **女声 (zf_)**: 55个模型
- **男声 (zm_)**: 45个模型
- **英文 (af_/bf_)**: 3个模型

## 输出规格

- **采样率**: 24kHz
- **格式**: WAV (无损)
- **位深**: 16-bit
- **声道**: 单声道
- **质量**: 接近真人语音

## 使用示例

### 教育内容合成
```bash
python kokoro_demo.py \
  --text "今天我们学习汉语拼音，请跟我一起读：a o e i u ü" \
  --voice zf_001 \
  --output lessons/pinyin_lesson.wav
```

### 新闻播报
```bash
python kokoro_demo.py \
  --text "以下是今日新闻摘要" \
  --voice zm_009 \
  --output news/news_intro.wav
```

### 故事朗读
```bash
python kokoro_demo.py \
  --text "从前有一座山，山里有座庙" \
  --voice af_heart \
  --output stories/story_intro.wav
```

## 性能优化

- **CPU模式**: 适合开发和测试
- **GPU模式**: 大批量处理时推荐
- **内存占用**: 约1-2GB
- **合成速度**: 实时倍率约10-20x

## 注意事项

1. 首次运行会下载模型文件
2. 中文文本效果最佳
3. 过长文本建议分段处理
4. 输出目录会自动创建
5. 支持标点符号自然停顿

## 故障排除

### 常见问题
1. **ImportError**: 确保已安装kokoro包
2. **CUDA错误**: 切换到CPU模式
3. **音频无声**: 检查文本编码和语音模型
4. **合成失败**: 查看错误日志，可能是文本格式问题

### 获取帮助
```bash
python kokoro_demo.py --help
```