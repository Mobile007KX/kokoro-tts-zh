# 参考音频目录

这个目录用于存放StableTTS引擎的参考音频文件。

## 支持的音频格式

- WAV (.wav)
- MP3 (.mp3) 
- FLAC (.flac)
- M4A (.m4a)

## 音频要求

- 采样率: 建议22050Hz或24000Hz
- 时长: 3-10秒为佳
- 质量: 清晰、无噪声
- 内容: 单人说话，语调自然

## 文件命名

建议使用描述性的文件名，例如:
- `female_young_gentle.wav`
- `male_mature_serious.wav`
- `child_cheerful.wav`

## 使用方法

在使用StableTTS引擎时，可以通过文件名（不包含扩展名）来指定参考音频:

```python
# 使用 female_young_gentle.wav 作为参考音频
result = manager.generate_speech(
    text="你好，世界！",
    engine_name="stable_tts", 
    voice="female_young_gentle"
)
```

## 注意事项

- 确保参考音频的语言与合成文本的语言匹配
- 参考音频的说话风格会影响合成结果的风格
- 建议准备多个不同风格的参考音频以满足不同需求