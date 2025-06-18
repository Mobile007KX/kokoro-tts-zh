#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kokoro TTS API 封装
提供简洁的Python接口来使用Kokoro TTS模型
"""

import torch
import torch.nn.functional as F
import torchaudio
import numpy as np
from pathlib import Path
import logging
from typing import Optional, Dict, Any, List, Tuple
import time
import json

# Kokoro TTS 相关导入
try:
    import vocos
    from kokoro import generate
except ImportError as e:
    logging.warning(f"Kokoro TTS dependencies not found: {e}")
    logging.warning("Please install kokoro-tts package")

class KokoroTTSAPI:
    """
    Kokoro TTS API 封装类
    
    提供简洁的接口来使用Kokoro TTS进行中文语音合成
    """
    
    def __init__(self, model_path: str, vocos_path: str, device: str = "auto"):
        """
        初始化Kokoro TTS API
        
        Args:
            model_path: Kokoro模型文件路径
            vocos_path: Vocos声码器模型路径
            device: 计算设备 ('auto', 'cuda', 'cpu')
        """
        self.model_path = Path(model_path)
        self.vocos_path = Path(vocos_path)
        self.device = self._setup_device(device)
        self.model = None
        self.vocos = None
        self.is_initialized = False
        
        # 音色映射
        self.voice_mapping = {
            # 女性音色
            'female_calm': 'af_sarah',
            'female_warm': 'af_nicole', 
            'female_clear': 'af_bella',
            'female_gentle': 'af_sarah',
            'female_bright': 'af_nicole',
            
            # 男性音色
            'male_calm': 'am_adam',
            'male_warm': 'am_michael',
            'male_clear': 'am_adam', 
            'male_deep': 'am_michael',
            'male_bright': 'am_adam',
            
            # 默认音色
            'default': 'af_sarah'
        }
        
        self.logger = logging.getLogger(__name__)
    
    def _setup_device(self, device: str) -> torch.device:
        """
        设置计算设备
        
        Args:
            device: 设备类型
            
        Returns:
            torch.device: 计算设备
        """
        if device == "auto":
            if torch.cuda.is_available():
                device = "cuda"
            else:
                device = "cpu"
        
        return torch.device(device)
    
    def initialize(self) -> bool:
        """
        初始化模型
        
        Returns:
            bool: 初始化是否成功
        """
        try:
            self.logger.info(f"正在初始化Kokoro TTS模型...")
            self.logger.info(f"设备: {self.device}")
            self.logger.info(f"模型路径: {self.model_path}")
            self.logger.info(f"Vocos路径: {self.vocos_path}")
            
            # 检查文件是否存在
            if not self.model_path.exists():
                raise FileNotFoundError(f"模型文件不存在: {self.model_path}")
            if not self.vocos_path.exists():
                raise FileNotFoundError(f"Vocos文件不存在: {self.vocos_path}")
            
            # 加载Kokoro模型
            self.logger.info("加载Kokoro模型...")
            self.model = torch.load(self.model_path, map_location=self.device)
            self.model.eval()
            
            # 加载Vocos声码器
            self.logger.info("加载Vocos声码器...")
            self.vocos = vocos.Vocos.from_pretrained(str(self.vocos_path))
            self.vocos = self.vocos.to(self.device)
            self.vocos.eval()
            
            self.is_initialized = True
            self.logger.info("✅ Kokoro TTS初始化完成")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Kokoro TTS初始化失败: {e}")
            return False
    
    def get_available_voices(self) -> Dict[str, List[str]]:
        """
        获取可用音色列表
        
        Returns:
            Dict[str, List[str]]: 按类别分组的音色列表
        """
        voices = {
            "女性音色": [
                "female_calm",    # 温和女声
                "female_warm",    # 温暖女声
                "female_clear",   # 清晰女声
                "female_gentle",  # 轻柔女声
                "female_bright"   # 明亮女声
            ],
            "男性音色": [
                "male_calm",      # 温和男声
                "male_warm",      # 温暖男声
                "male_clear",     # 清晰男声
                "male_deep",      # 深沉男声
                "male_bright"     # 明亮男声
            ],
            "特殊音色": [
                "default"         # 默认音色
            ]
        }
        
        return voices
    
    def validate_voice(self, voice: str) -> str:
        """
        验证并映射音色名称
        
        Args:
            voice: 音色名称
            
        Returns:
            str: 映射后的音色名称
        """
        if voice in self.voice_mapping:
            return self.voice_mapping[voice]
        elif voice in self.voice_mapping.values():
            return voice
        else:
            self.logger.warning(f"未知音色: {voice}，使用默认音色")
            return self.voice_mapping['default']
    
    def preprocess_text(self, text: str) -> str:
        """
        预处理文本
        
        Args:
            text: 输入文本
            
        Returns:
            str: 处理后的文本
        """
        if not text or not text.strip():
            return ""
        
        # 清理文本
        text = text.strip()
        
        # 移除多余的空白字符
        text = ' '.join(text.split())
        
        # 确保句子以适当的标点结尾
        if text and text[-1] not in '。！？.!?':
            text += '。'
        
        return text
    
    def generate_speech(self, text: str, voice: str = "default", 
                       speed: float = 1.0, temperature: float = 0.7) -> Optional[Tuple[np.ndarray, int]]:
        """
        生成语音
        
        Args:
            text: 要合成的文本
            voice: 音色名称
            speed: 语速倍率 (0.5-2.0)
            temperature: 温度参数 (0.1-1.0)
            
        Returns:
            Optional[Tuple[np.ndarray, int]]: (音频数据, 采样率) 或 None
        """
        if not self.is_initialized:
            self.logger.error("模型未初始化，请先调用initialize()")
            return None
        
        # 预处理文本
        text = self.preprocess_text(text)
        if not text:
            self.logger.error("文本为空")
            return None
        
        # 验证音色
        voice = self.validate_voice(voice)
        
        # 参数范围检查
        speed = max(0.5, min(2.0, speed))
        temperature = max(0.1, min(1.0, temperature))
        
        try:
            self.logger.info(f"正在合成语音: {text[:50]}...")
            self.logger.info(f"音色: {voice}, 语速: {speed}, 温度: {temperature}")
            
            start_time = time.time()
            
            # 使用Kokoro生成语音
            with torch.no_grad():
                # 调用Kokoro的generate函数
                audio_tokens = generate(
                    model=self.model,
                    text=text,
                    voice=voice,
                    lang='zh',  # 中文
                    temperature=temperature,
                    speed=speed,
                    device=self.device
                )
                
                # 使用Vocos解码音频
                if isinstance(audio_tokens, torch.Tensor):
                    audio_tokens = audio_tokens.unsqueeze(0)
                
                audio = self.vocos.decode(audio_tokens)
                
                # 转换为numpy数组
                audio = audio.cpu().numpy().squeeze()
                
            generation_time = time.time() - start_time
            audio_length = len(audio) / 24000  # 假设采样率为24kHz
            
            self.logger.info(f"✅ 语音合成完成")
            self.logger.info(f"音频长度: {audio_length:.2f}秒")
            self.logger.info(f"生成时间: {generation_time:.2f}秒")
            self.logger.info(f"实时倍率: {audio_length/generation_time:.1f}x")
            
            return audio, 24000  # 返回音频和采样率
            
        except Exception as e:
            self.logger.error(f"❌ 语音合成失败: {e}")
            return None
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        获取模型信息
        
        Returns:
            Dict[str, Any]: 模型信息字典
        """
        info = {
            "model_path": str(self.model_path),
            "vocos_path": str(self.vocos_path),
            "device": str(self.device),
            "is_initialized": self.is_initialized,
            "available_voices": len(self.voice_mapping),
            "supported_languages": ["zh"],
            "sample_rate": 24000
        }
        
        if self.is_initialized and self.model is not None:
            try:
                # 获取模型参数数量
                total_params = sum(p.numel() for p in self.model.parameters())
                info["total_parameters"] = total_params
                info["trainable_parameters"] = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
            except:
                pass
        
        return info
    
    def cleanup(self):
        """
        清理资源
        """
        if self.model is not None:
            del self.model
            self.model = None
        
        if self.vocos is not None:
            del self.vocos
            self.vocos = None
        
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        self.is_initialized = False
        self.logger.info("🧹 Kokoro TTS资源已清理")
    
    def __del__(self):
        """
        析构函数
        """
        self.cleanup()