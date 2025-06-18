#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTS引擎管理器 - 统一管理多个TTS引擎
支持Kokoro和StableTTS引擎的统一接口
"""

import os
import sys
import json
import time
import torch
import numpy as np
import soundfile as sf
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod

# 添加stable_tts_module到路径
sys.path.append(str(Path(__file__).parent / 'stable_tts_module'))

@dataclass
class TTSResult:
    """TTS生成结果"""
    audio: np.ndarray
    sample_rate: int
    generation_time: float
    engine: str
    voice: Optional[str] = None
    text_length: int = 0
    audio_length: float = 0.0
    
class TTSEngine(ABC):
    """TTS引擎抽象基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get('enabled', True)
        self.sample_rate = config.get('sample_rate', 24000)
        self.description = config.get('description', '')
        self.supported_languages = config.get('supported_languages', [])
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
    @abstractmethod
    def initialize(self) -> bool:
        """初始化引擎"""
        pass
        
    @abstractmethod
    def generate(self, text: str, **kwargs) -> TTSResult:
        """生成语音"""
        pass
        
    @abstractmethod
    def get_available_voices(self) -> Dict[str, List[str]]:
        """获取可用音色"""
        pass
        
    @abstractmethod
    def is_ready(self) -> bool:
        """检查引擎是否准备就绪"""
        pass

class KokoroEngine(TTSEngine):
    """Kokoro TTS引擎"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.model = None
        self.zh_pipeline = None
        self.en_pipelines = None
        self.repo_id = config.get('repo_id', 'hexgrad/Kokoro-82M-v1.1-zh')
        
    def initialize(self) -> bool:
        """初始化Kokoro引擎"""
        try:
            from kokoro import KModel, KPipeline
            
            print(f"🚀 正在初始化Kokoro引擎... (设备: {self.device})")
            
            # 加载模型
            self.model = KModel(repo_id=self.repo_id).to(self.device).eval()
            
            # 初始化中文pipeline
            en_pipeline = KPipeline(lang_code='a', repo_id=self.repo_id, model=False)
            def en_callable(text):
                if text == 'Kokoro':
                    return 'kˈOkəɹO'
                elif text == 'Sol':
                    return 'sˈOl'
                return next(en_pipeline(text)).phonemes
            
            self.zh_pipeline = KPipeline(lang_code='z', repo_id=self.repo_id, 
                                       model=self.model, en_callable=en_callable)
            
            # 初始化英文pipelines
            self.en_pipelines = [KPipeline(lang_code='b' if british else 'a', 
                                         repo_id=self.repo_id, model=self.model) 
                               for british in (False, True)]
            
            print("✅ Kokoro引擎初始化完成")
            return True
            
        except ImportError:
            print("❌ Kokoro包未安装")
            return False
        except Exception as e:
            print(f"❌ Kokoro引擎初始化失败: {str(e)}")
            return False
    
    def generate(self, text: str, voice: str = 'zf_001', language: str = 'zh', 
                **kwargs) -> TTSResult:
        """生成语音"""
        start_time = time.time()
        
        def speed_callable(len_ps):
            speed = 0.8
            if len_ps <= 83:
                speed = 1
            elif len_ps < 183:
                speed = 1 - (len_ps - 83) / 500
            return speed * 1.1
        
        try:
            if language == 'zh' or voice.startswith(('zf_', 'zm_')):
                # 中文生成
                generator = self.zh_pipeline(text, voice=voice, speed=speed_callable)
                result = next(generator)
                wav = result.audio
            else:
                # 英文生成
                british = voice.startswith('bf_')
                generator = self.en_pipelines[british](text, voice=voice)
                result = next(generator)
                wav = result.audio
            
            generation_time = time.time() - start_time
            
            return TTSResult(
                audio=wav,
                sample_rate=self.sample_rate,
                generation_time=generation_time,
                engine='kokoro',
                voice=voice,
                text_length=len(text),
                audio_length=len(wav) / self.sample_rate
            )
            
        except Exception as e:
            raise Exception(f"Kokoro生成失败: {str(e)}")
    
    def get_available_voices(self) -> Dict[str, List[str]]:
        """获取可用音色"""
        voices_dir = Path(__file__).parent / 'voices'
        if not voices_dir.exists():
            return {'female': [], 'male': [], 'english': []}
        
        voice_files = list(voices_dir.glob('*.pt'))
        
        voices = {
            'female': [],
            'male': [],
            'english': []
        }
        
        for voice_file in voice_files:
            name = voice_file.stem
            if name.startswith('zf_'):
                voices['female'].append(name)
            elif name.startswith('zm_'):
                voices['male'].append(name)
            elif name.startswith(('af_', 'bf_')):
                voices['english'].append(name)
        
        # 排序
        for category in voices:
            voices[category].sort()
        
        return voices
    
    def is_ready(self) -> bool:
        """检查引擎是否准备就绪"""
        return self.model is not None and self.zh_pipeline is not Noneclass StableTTSEngine(TTSEngine):
    """StableTTS引擎"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_model = None
        self.model_path = config.get('model_path')
        self.vocoder_path = config.get('vocoder_path')
        self.vocoder_type = config.get('vocoder_type', 'vocos')
        self.default_params = config.get('default_params', {})
        
    def initialize(self) -> bool:
        """初始化StableTTS引擎"""
        try:
            from stable_tts_api import StableTTSAPI
            
            print(f"🚀 正在初始化StableTTS引擎... (设备: {self.device})")
            
            # 检查模型文件是否存在
            model_path = Path(self.model_path)
            vocoder_path = Path(self.vocoder_path)
            
            if not model_path.exists():
                print(f"❌ StableTTS模型文件不存在: {model_path}")
                return False
                
            if not vocoder_path.exists():
                print(f"❌ Vocoder模型文件不存在: {vocoder_path}")
                return False
            
            # 初始化API模型
            self.api_model = StableTTSAPI(
                tts_model_path=str(model_path),
                vocoder_model_path=str(vocoder_path),
                vocoder_name=self.vocoder_type
            )
            self.api_model.to(self.device)
            
            print("✅ StableTTS引擎初始化完成")
            return True
            
        except ImportError as e:
            print(f"❌ StableTTS模块导入失败: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ StableTTS引擎初始化失败: {str(e)}")
            return False
    
    def generate(self, text: str, ref_audio: str, language: str = 'chinese', 
                step: int = None, temperature: float = None, 
                length_scale: float = None, solver: str = None, 
                cfg: float = None, **kwargs) -> TTSResult:
        """生成语音"""
        start_time = time.time()
        
        # 使用默认参数或传入参数
        params = {
            'step': step or self.default_params.get('step', 25),
            'temperature': temperature or self.default_params.get('temperature', 1.0),
            'length_scale': length_scale or self.default_params.get('length_scale', 1.0),
            'solver': solver or self.default_params.get('solver', 'dopri5'),
            'cfg': cfg or self.default_params.get('cfg', 3.0)
        }
        
        try:
            # 检查参考音频文件
            if not Path(ref_audio).exists():
                raise Exception(f"参考音频文件不存在: {ref_audio}")
            
            # 生成语音
            audio_output, mel_output = self.api_model.inference(
                text=text,
                ref_audio=ref_audio,
                language=language,
                **params
            )
            
            generation_time = time.time() - start_time
            
            # 转换为numpy数组
            if torch.is_tensor(audio_output):
                wav = audio_output.squeeze().numpy()
            else:
                wav = np.array(audio_output).squeeze()
            
            return TTSResult(
                audio=wav,
                sample_rate=self.sample_rate,
                generation_time=generation_time,
                engine='stable_tts',
                voice=Path(ref_audio).stem,
                text_length=len(text),
                audio_length=len(wav) / self.sample_rate
            )
            
        except Exception as e:
            raise Exception(f"StableTTS生成失败: {str(e)}")
    
    def get_available_voices(self) -> Dict[str, List[str]]:
        """获取可用的参考音频文件"""
        # StableTTS使用参考音频文件而不是预训练音色
        ref_audio_dir = Path(__file__).parent / 'reference_audios'
        if not ref_audio_dir.exists():
            return {'reference_audios': []}
        
        audio_files = []
        for ext in ['*.wav', '*.mp3', '*.flac', '*.m4a']:
            audio_files.extend(ref_audio_dir.glob(ext))
        
        return {
            'reference_audios': [f.stem for f in sorted(audio_files)]
        }
    
    def is_ready(self) -> bool:
        """检查引擎是否准备就绪"""
        return self.api_model is not None

class TTSEngineManager:
    """TTS引擎管理器"""
    
    def __init__(self, config_path: str = 'tts_config.json'):
        self.config_path = config_path
        self.config = self._load_config()
        self.engines: Dict[str, TTSEngine] = {}
        self.default_engine = self.config.get('default_engine', 'kokoro')
        
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ 配置文件不存在: {self.config_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ 配置文件格式错误: {str(e)}")
            return {}
    
    def initialize_engines(self) -> Dict[str, bool]:
        """初始化所有启用的引擎"""
        results = {}
        
        engines_config = self.config.get('tts_engines', {})
        
        for engine_name, engine_config in engines_config.items():
            if not engine_config.get('enabled', False):
                print(f"⏭️  跳过未启用的引擎: {engine_name}")
                results[engine_name] = False
                continue
            
            print(f"\n🔧 正在初始化引擎: {engine_name}")
            
            try:
                if engine_name == 'kokoro':
                    engine = KokoroEngine(engine_config)
                elif engine_name == 'stable_tts':
                    engine = StableTTSEngine(engine_config)
                else:
                    print(f"❌ 未知的引擎类型: {engine_name}")
                    results[engine_name] = False
                    continue
                
                if engine.initialize():
                    self.engines[engine_name] = engine
                    results[engine_name] = True
                    print(f"✅ {engine_name} 引擎初始化成功")
                else:
                    results[engine_name] = False
                    print(f"❌ {engine_name} 引擎初始化失败")
                    
            except Exception as e:
                print(f"❌ {engine_name} 引擎初始化异常: {str(e)}")
                results[engine_name] = False
        
        return results
    
    def get_engine(self, engine_name: str = None) -> Optional[TTSEngine]:
        """获取指定引擎"""
        if engine_name is None:
            engine_name = self.default_engine
        
        return self.engines.get(engine_name)
    
    def get_available_engines(self) -> List[str]:
        """获取可用的引擎列表"""
        return list(self.engines.keys())
    
    def generate_speech(self, text: str, engine_name: str = None, **kwargs) -> TTSResult:
        """生成语音"""
        engine = self.get_engine(engine_name)
        if engine is None:
            available = ', '.join(self.get_available_engines())
            raise Exception(f"引擎不可用: {engine_name or self.default_engine}. 可用引擎: {available}")
        
        if not engine.is_ready():
            raise Exception(f"引擎未准备就绪: {engine_name or self.default_engine}")
        
        return engine.generate(text, **kwargs)
    
    def get_all_voices(self) -> Dict[str, Dict[str, List[str]]]:
        """获取所有引擎的音色信息"""
        all_voices = {}
        for engine_name, engine in self.engines.items():
            if engine.is_ready():
                all_voices[engine_name] = engine.get_available_voices()
        return all_voices
    
    def get_engine_info(self) -> Dict[str, Any]:
        """获取引擎信息"""
        info = {
            'available_engines': [],
            'default_engine': self.default_engine,
            'engine_details': {}
        }
        
        for engine_name, engine in self.engines.items():
            info['available_engines'].append(engine_name)
            info['engine_details'][engine_name] = {
                'description': engine.description,
                'sample_rate': engine.sample_rate,
                'supported_languages': engine.supported_languages,
                'is_ready': engine.is_ready(),
                'device': engine.device
            }
        
        return info

if __name__ == '__main__':
    # 测试引擎管理器
    manager = TTSEngineManager()
    
    print("🎵 TTS引擎管理器测试")
    print("=" * 50)
    
    # 初始化引擎
    results = manager.initialize_engines()
    print(f"\n📊 引擎初始化结果: {results}")
    
    # 显示引擎信息
    info = manager.get_engine_info()
    print(f"\n🔍 引擎信息:")
    for engine_name in info['available_engines']:
        details = info['engine_details'][engine_name]
        print(f"  - {engine_name}: {details['description']}")
        print(f"    状态: {'✅ 就绪' if details['is_ready'] else '❌ 未就绪'}")
        print(f"    设备: {details['device']}")
        print(f"    采样率: {details['sample_rate']}Hz")
    
    # 显示音色信息
    all_voices = manager.get_all_voices()
    print(f"\n🎤 音色统计:")
    for engine_name, voices in all_voices.items():
        total = sum(len(v) for v in voices.values())
        print(f"  - {engine_name}: {total} 个音色")
        for category, voice_list in voices.items():
            print(f"    {category}: {len(voice_list)} 个")