# Kokoro TTS 中文语音合成系统

这是一个集成了多个TTS引擎的统一中文语音合成系统，支持Kokoro和StableTTS两种先进的语音合成技术。

## 特性

🎯 **多引擎支持**
- Kokoro TTS: 基于Llama架构的高质量语音合成
- StableTTS: 基于Flow-matching和DiT的稳定语音合成

🎤 **丰富音色**
- 支持多种中文音色
- 男声、女声、不同年龄段
- 可自定义参考音频

⚡ **高性能**
- GPU加速
- 实时语音合成
- 批量处理支持

🔧 **易于使用**
- 统一API接口
- 命令行工具
- 交互式模式

## 项目结构

```
kokoro-tts-zh/
├── kokoro_api/              # Kokoro TTS API模块
│   ├── kokoro_tts_api.py   # Kokoro API封装
│   └── __init__.py
├── stable_tts_module/       # StableTTS模块
│   ├── stable_tts_api.py   # StableTTS API封装
│   ├── checkpoints/        # 模型检查点
│   └── vocoders/          # 声码器模型
├── reference_audios/        # 参考音频文件
├── output/                 # 输出音频文件
├── temp/                   # 临时文件
├── tts_engine_manager.py   # TTS引擎管理器
├── unified_tts_app.py      # 统一TTS应用程序
├── tts_config.json         # 配置文件
├── requirements.txt        # 依赖包
└── README.md              # 项目说明
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置系统

编辑 `tts_config.json` 文件，设置模型路径和参数：

```json
{
  "kokoro": {
    "model_path": "./models/kokoro/kokoro-v0_19.safetensors",
    "vocos_path": "./models/kokoro/vocos.safetensors",
    "device": "cuda"
  },
  "stable_tts": {
    "tts_model_path": "./stable_tts_module/checkpoints/checkpoint_0.pt",
    "vocoder_model_path": "./stable_tts_module/vocoders/vocos.pt",
    "device": "cuda"
  }
}
```

### 3. 下载模型

#### Kokoro模型
```bash
# 下载Kokoro模型文件
wget -P ./models/kokoro/ https://huggingface.co/hexgrad/Kokoro-82M/resolve/main/kokoro-v0_19.safetensors
wget -P ./models/kokoro/ https://huggingface.co/hexgrad/Kokoro-82M/resolve/main/vocos.safetensors
```

#### StableTTS模型
```bash
# 下载StableTTS模型文件（需要根据实际可用的模型调整）
# 这里提供模拟路径，实际使用时需要替换为真实模型
```

### 4. 使用方法

#### 命令行模式

```bash
# 基本用法
python unified_tts_app.py --text "你好，欢迎使用Kokoro TTS系统！"

# 指定引擎和音色
python unified_tts_app.py --text "这是一个测试" --engine kokoro --voice af_bella

# 使用StableTTS
python unified_tts_app.py --text "这是StableTTS测试" --engine stable_tts --voice female_gentle

# 指定输出文件
python unified_tts_app.py --text "保存到指定文件" --output "./my_audio.wav"
```

#### 交互模式

```bash
# 进入交互模式
python unified_tts_app.py --interactive

# 交互模式命令:
# help           - 显示帮助
# status         - 显示系统状态  
# voices         - 列出所有音色
# engine kokoro  - 切换到Kokoro引擎
# quit           - 退出程序
# 直接输入文本   - 进行语音合成
```

#### Python API

```python
from tts_engine_manager import TTSEngineManager

# 创建引擎管理器
manager = TTSEngineManager('tts_config.json')
manager.initialize_engines()

# 使用Kokoro引擎
result = manager.generate_speech(
    text="你好，这是Kokoro TTS测试",
    engine_name="kokoro",
    voice="af_bella"
)

# 使用StableTTS引擎
result = manager.generate_speech(
    text="你好，这是StableTTS测试", 
    engine_name="stable_tts",
    ref_audio="./reference_audios/female_gentle.wav"
)

# 保存音频
import soundfile as sf
sf.write('output.wav', result.audio, result.sample_rate)
```

## 配置说明

### Kokoro引擎配置

```json
{
  "kokoro": {
    "model_path": "模型文件路径",
    "vocos_path": "Vocos声码器路径", 
    "device": "cuda/cpu",
    "sample_rate": 24000,
    "speed": 1.0,
    "enable_cache": true
  }
}
```

### StableTTS引擎配置

```json
{
  "stable_tts": {
    "tts_model_path": "TTS模型路径",
    "vocoder_model_path": "声码器模型路径",
    "vocoder_name": "vocos",
    "device": "cuda/cpu",
    "sample_rate": 24000
  }
}
```

## 支持的音色

### Kokoro音色

- **女声**: af_bella, af_sarah, af_nicole, am_amy, am_emma
- **男声**: am_michael, am_adam, am_john
- **特殊**: af_sky, am_bryan

### StableTTS音色

通过参考音频文件定义，支持自定义音色。将参考音频放在 `reference_audios/` 目录下即可。

## 高级功能

### 批量处理

```python
texts = ["第一句话", "第二句话", "第三句话"]
for i, text in enumerate(texts):
    result = manager.generate_speech(text)
    sf.write(f'batch_{i}.wav', result.audio, result.sample_rate)
```

### 性能优化

- 使用GPU加速: 在配置中设置 `"device": "cuda"`
- 启用缓存: 设置 `"enable_cache": true`
- 批量推理: 一次性处理多个文本

### 自定义音色

1. 准备3-10秒的高质量参考音频
2. 保存为WAV格式到 `reference_audios/` 目录
3. 使用文件名（不含扩展名）作为音色名称

## 故障排除

### 常见问题

**Q: 模型加载失败**
A: 检查模型文件路径是否正确，确保模型文件已下载完整

**Q: CUDA内存不足**  
A: 尝试使用CPU模式或减少batch size

**Q: 音频质量不佳**
A: 检查参考音频质量，尝试不同的参数设置

**Q: 合成速度慢**
A: 确保使用GPU加速，检查CUDA环境配置

### 日志调试

程序运行时会输出详细的状态信息，包括：
- 模型加载状态
- 推理时间统计  
- 错误信息和建议

## 贡献指南

欢迎提交Issue和Pull Request！

1. Fork项目
2. 创建特性分支
3. 提交更改
4. 发起Pull Request

## 许可证

MIT License

## 致谢

- [Kokoro TTS](https://github.com/hexgrad/kokoro) - 高质量的Llama架构TTS模型
- [StableTTS](https://github.com/stability-ai/StableTTS) - 稳定的Flow-matching TTS模型
- [Vocos](https://github.com/charactr-platform/vocos) - 高质量神经声码器

## 更新日志

### v1.0.0 (2024-12-16)
- 初始版本发布
- 支持Kokoro和StableTTS双引擎
- 提供统一API和命令行工具
- 支持多种中文音色
- 包含交互模式和批量处理功能