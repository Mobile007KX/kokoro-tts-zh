# 🎵 Kokoro TTS 中文版

<div align="center">

[![GitHub Stars](https://img.shields.io/github/stars/Mobile007KX/kokoro-tts-zh?style=for-the-badge)](https://github.com/Mobile007KX/kokoro-tts-zh/stargazers)
[![GitHub License](https://img.shields.io/github/license/Mobile007KX/kokoro-tts-zh?style=for-the-badge)](https://github.com/Mobile007KX/kokoro-tts-zh/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge)](https://www.python.org/downloads/)
[![GitHub Issues](https://img.shields.io/github/issues/Mobile007KX/kokoro-tts-zh?style=for-the-badge)](https://github.com/Mobile007KX/kokoro-tts-zh/issues)

**高质量中文文本转语音系统 | High-Quality Chinese Text-to-Speech System**

[English](#english) | [中文](#中文)

</div>

---

## 中文

### 🌟 项目简介

Kokoro TTS中文版是一个功能强大的文本转语音系统，集成了先进的Kokoro TTS引擎，提供高质量的中文语音合成服务。本项目包含Web界面、命令行工具和API接口，支持103种不同音色，是目前最全面的开源中文TTS解决方案之一。

### ✨ 主要特性

🎤 **丰富音色库**
- 🚺 55个女声音色 (zf系列)
- 🚹 45个男声音色 (zm系列)  
- 🌍 3个英文音色 (af_maple, af_sol, bf_vale)

⚡ **高性能**
- 🚀 实时语音合成 (1-2秒处理时间)
- 🎵 高质量24kHz音频输出
- 💻 GPU/CPU自适应运行
- 📊 平均10-20倍实时倍率

🔧 **多种使用方式**
- 🌐 用户友好的Web界面
- 💻 功能完整的命令行工具
- 🔌 程序化API调用接口
- 📱 响应式设计，支持移动端

🏗️ **先进架构**
- 🎛️ 统一TTS引擎管理器
- ⚙️ 灵活的配置系统
- 📝 完整的错误处理和日志
- 🔄 模块化设计，易于扩展

### 🎯 技术亮点

- **基于Llama架构**：采用最新的语言模型技术
- **多引擎支持**：集成Kokoro和StableTTS双引擎
- **实时合成**：支持流式和批量处理
- **声音克隆**：支持参考音频的声音复制
- **跨平台**：支持Linux、macOS、Windows

### 🚀 快速开始

#### 1. 环境要求
```bash
# Python 3.8+ (推荐3.11)
# 8GB+ RAM
# 可选：NVIDIA GPU (4GB+ VRAM)
```

#### 2. 一键启动
```bash
git clone https://github.com/Mobile007KX/kokoro-tts-zh.git
cd kokoro-tts-zh
chmod +x run.sh
./run.sh
```

#### 3. Web界面使用
访问：http://localhost:5001
- 选择音色 → 输入文本 → 生成语音 → 下载音频

#### 4. 命令行使用
```bash
# 交互模式
python unified_tts_app.py

# 直接合成
python unified_tts_app.py --text "你好世界" --voice zf_001 --output hello.wav
```

### 📊 性能测试

| 指标 | Kokoro TTS | 备注 |
|------|------------|------|
| 音频质量 | 24kHz 16-bit | 高保真输出 |
| 处理速度 | 10-20x实时 | GPU加速 |
| 延迟 | <300ms | 短文本 |
| 内存占用 | 2-3GB | GPU模式 |
| 支持语言 | 中文+英文 | 可扩展 |

### 🎵 音色预览

<details>
<summary>🚺 女声音色 (55个)</summary>

`zf_001`, `zf_002`, `zf_003`, `zf_004`, `zf_005`, `zf_006`, `zf_007`, `zf_008`, `zf_017`, `zf_018`, `zf_019`, `zf_021`, `zf_022`, `zf_023`, `zf_024`, `zf_026`, `zf_027`, `zf_028`, `zf_032`, `zf_036`, `zf_038`, `zf_039`, `zf_040`, `zf_042`, `zf_043`, `zf_044`, `zf_046`, `zf_047`, `zf_048`, `zf_049`, `zf_051`, `zf_059`, `zf_060`, `zf_067`, `zf_070`, `zf_071`, `zf_072`, `zf_073`, `zf_074`, `zf_075`, `zf_076`, `zf_077`, `zf_078`, `zf_079`, `zf_083`, `zf_084`, `zf_085`, `zf_086`, `zf_087`, `zf_088`, `zf_090`, `zf_092`, `zf_093`, `zf_094`, `zf_099`

</details>

<details>
<summary>🚹 男声音色 (45个)</summary>

`zm_009`, `zm_010`, `zm_011`, `zm_012`, `zm_013`, `zm_014`, `zm_015`, `zm_016`, `zm_020`, `zm_025`, `zm_029`, `zm_030`, `zm_031`, `zm_033`, `zm_034`, `zm_035`, `zm_037`, `zm_041`, `zm_045`, `zm_050`, `zm_052`, `zm_053`, `zm_054`, `zm_055`, `zm_056`, `zm_057`, `zm_058`, `zm_061`, `zm_062`, `zm_063`, `zm_064`, `zm_065`, `zm_066`, `zm_068`, `zm_069`, `zm_080`, `zm_081`, `zm_082`, `zm_089`, `zm_091`, `zm_095`, `zm_096`, `zm_097`, `zm_098`, `zm_100`

</details>

### 📚 项目文档

- 📖 [完整使用指南](./USAGE.md)
- 🏗️ [项目架构说明](./PROJECT_STATUS.md)
- 🔧 [API文档](./README.md#api接口)
- ❓ [常见问题](./README.md#故障排除)

### 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. **Fork** 本项目
2. **创建** 特性分支 (`git checkout -b feature/AmazingFeature`)
3. **提交** 更改 (`git commit -m 'Add some AmazingFeature'`)
4. **推送** 到分支 (`git push origin feature/AmazingFeature`)
5. **创建** Pull Request

### 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

### 🙏 致谢

- [Kokoro TTS](https://github.com/hexgrad/kokoro) - 高质量的Llama架构TTS模型
- [StableTTS](https://github.com/stability-ai/StableTTS) - 稳定的Flow-matching TTS模型
- [Vocos](https://github.com/charactr-platform/vocos) - 高质量神经声码器

---

## English

### 🌟 Project Overview

Kokoro TTS Chinese Edition is a powerful text-to-speech system that integrates advanced Kokoro TTS engine, providing high-quality Chinese speech synthesis services. This project includes web interface, command-line tools, and API interfaces, supporting 103 different voice models, making it one of the most comprehensive open-source Chinese TTS solutions available.

### ✨ Key Features

🎤 **Rich Voice Library**
- 🚺 55 Female voices (zf series)
- 🚹 45 Male voices (zm series)
- 🌍 3 English voices (af_maple, af_sol, bf_vale)

⚡ **High Performance**
- 🚀 Real-time speech synthesis (1-2 seconds processing)
- 🎵 High-quality 24kHz audio output
- 💻 GPU/CPU adaptive execution
- 📊 Average 10-20x real-time factor

🔧 **Multiple Usage Methods**
- 🌐 User-friendly web interface
- 💻 Full-featured command-line tools
- 🔌 Programmatic API interface
- 📱 Responsive design with mobile support

### 🚀 Quick Start

#### 1. Requirements
```bash
# Python 3.8+ (3.11 recommended)
# 8GB+ RAM
# Optional: NVIDIA GPU (4GB+ VRAM)
```

#### 2. One-click Setup
```bash
git clone https://github.com/Mobile007KX/kokoro-tts-zh.git
cd kokoro-tts-zh
chmod +x run.sh
./run.sh
```

#### 3. Web Interface
Visit: http://localhost:5001
- Select voice → Input text → Generate speech → Download audio

#### 4. Command Line
```bash
# Interactive mode
python unified_tts_app.py

# Direct synthesis
python unified_tts_app.py --text "Hello World" --voice zf_001 --output hello.wav
```

### 📊 Performance Benchmarks

| Metric | Kokoro TTS | Notes |
|--------|------------|-------|
| Audio Quality | 24kHz 16-bit | High fidelity |
| Processing Speed | 10-20x realtime | GPU accelerated |
| Latency | <300ms | Short text |
| Memory Usage | 2-3GB | GPU mode |
| Supported Languages | Chinese + English | Extensible |

### 📄 License

This project is licensed under the [MIT License](LICENSE).

### 🙏 Acknowledgments

- [Kokoro TTS](https://github.com/hexgrad/kokoro) - High-quality Llama-based TTS model
- [StableTTS](https://github.com/stability-ai/StableTTS) - Stable Flow-matching TTS model
- [Vocos](https://github.com/charactr-platform/vocos) - High-quality neural vocoder

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个Star支持一下！**

**⭐ If this project helps you, please give it a star!**

[🔝 回到顶部 | Back to Top](#-kokoro-tts-中文版)

</div>
