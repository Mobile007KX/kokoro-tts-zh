#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一TTS应用程序
支持Kokoro和StableTTS两个引擎的语音合成
"""

import os
import sys
import time
import argparse
import soundfile as sf
from pathlib import Path
from typing import Optional, Dict, Any

# 导入引擎管理器
from tts_engine_manager import TTSEngineManager, TTSResult

class UnifiedTTSApp:
    """统一TTS应用程序"""
    
    def __init__(self, config_path: str = 'tts_config.json'):
        self.manager = TTSEngineManager(config_path)
        self.output_dir = Path('./output')
        self.temp_dir = Path('./temp')
        
        # 创建输出目录
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)
    
    def initialize(self) -> bool:
        """初始化应用程序"""
        print("🚀 初始化统一TTS应用程序")
        print("=" * 50)
        
        # 初始化引擎
        results = self.manager.initialize_engines()
        
        # 检查是否至少有一个引擎可用
        available_engines = [name for name, success in results.items() if success]
        
        if not available_engines:
            print("❌ 没有可用的TTS引擎")
            return False
        
        print(f"\n✅ 初始化完成，可用引擎: {', '.join(available_engines)}")
        return True
    
    def show_status(self):
        """显示系统状态"""
        print("\n📊 系统状态")
        print("=" * 30)
        
        # 引擎信息
        info = self.manager.get_engine_info()
        print(f"默认引擎: {info['default_engine']}")
        print(f"可用引擎: {len(info['available_engines'])} 个")
        
        for engine_name in info['available_engines']:
            details = info['engine_details'][engine_name]
            status = "✅ 就绪" if details['is_ready'] else "❌ 未就绪"
            print(f"  - {engine_name}: {status} | {details['device']} | {details['sample_rate']}Hz")
        
        # 音色统计
        all_voices = self.manager.get_all_voices()
        print(f"\n🎤 音色统计:")
        for engine_name, voices in all_voices.items():
            total = sum(len(v) for v in voices.values())
            print(f"  - {engine_name}: {total} 个音色")
            for category, voice_list in voices.items():
                if voice_list:  # 只显示非空类别
                    print(f"    {category}: {len(voice_list)} 个")
    
    def list_voices(self, engine_name: str = None):
        """列出音色"""
        all_voices = self.manager.get_all_voices()
        
        if engine_name:
            if engine_name not in all_voices:
                print(f"❌ 引擎 {engine_name} 不可用")
                return
            voices = {engine_name: all_voices[engine_name]}
        else:
            voices = all_voices
        
        print(f"\n🎤 可用音色列表")
        print("=" * 40)
        
        for engine, voice_dict in voices.items():
            print(f"\n📱 {engine.upper()} 引擎:")
            for category, voice_list in voice_dict.items():
                if voice_list:
                    print(f"  📂 {category} ({len(voice_list)} 个):")
                    # 分行显示，每行5个
                    for i in range(0, len(voice_list), 5):
                        batch = voice_list[i:i+5]
                        print(f"    {', '.join(batch)}")
    
    def generate_speech(self, text: str, engine_name: str = None, 
                       voice: str = None, output_file: str = None,
                       **engine_params) -> Optional[TTSResult]:
        """生成语音"""
        try:
            # 验证输入
            if not text.strip():
                print("❌ 输入文本不能为空")
                return None
            
            # 确定引擎
            if engine_name is None:
                engine_name = self.manager.default_engine
            
            if engine_name not in self.manager.get_available_engines():
                available = ', '.join(self.manager.get_available_engines())
                print(f"❌ 引擎 {engine_name} 不可用，可用引擎: {available}")
                return None
            
            print(f"\n🎯 开始语音合成")
            print(f"引擎: {engine_name}")
            print(f"文本: {text[:50]}{'...' if len(text) > 50 else ''}")
            if voice:
                print(f"音色: {voice}")
            
            # 准备参数
            params = {}
            if voice:
                if engine_name == 'kokoro':
                    params['voice'] = voice
                elif engine_name == 'stable_tts':
                    # StableTTS使用参考音频
                    ref_audio_path = Path('./reference_audios') / f"{voice}.wav"
                    if ref_audio_path.exists():
                        params['ref_audio'] = str(ref_audio_path)
                    else:
                        print(f"⚠️  参考音频不存在: {ref_audio_path}")
            
            # 添加引擎特定参数
            params.update(engine_params)
            
            # 生成语音
            start_time = time.time()
            result = self.manager.generate_speech(text, engine_name, **params)
            total_time = time.time() - start_time
            
            # 保存音频
            if output_file is None:
                timestamp = int(time.time())
                output_file = self.output_dir / f"tts_{engine_name}_{timestamp}.wav"
            else:
                output_file = Path(output_file)
            
            # 确保输出目录存在
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # 写入音频文件
            sf.write(str(output_file), result.audio, result.sample_rate)
            
            # 显示结果
            print(f"\n✅ 语音合成完成")
            print(f"输出文件: {output_file}")
            print(f"音频时长: {result.audio_length:.2f} 秒")
            print(f"生成时间: {result.generation_time:.2f} 秒")
            print(f"总耗时: {total_time:.2f} 秒")
            print(f"实时倍率: {result.audio_length/result.generation_time:.1f}x")
            
            return result
            
        except Exception as e:
            print(f"❌ 语音合成失败: {str(e)}")
            return None
    
    def interactive_mode(self):
        """交互模式"""
        print("\n🎤 进入交互模式")
        print("输入 'help' 查看命令，输入 'quit' 退出")
        print("=" * 40)
        
        while True:
            try:
                user_input = input("\n> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 再见！")
                    break
                
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                if user_input.lower() == 'status':
                    self.show_status()
                    continue
                
                if user_input.lower().startswith('voices'):
                    parts = user_input.split()
                    engine = parts[1] if len(parts) > 1 else None
                    self.list_voices(engine)
                    continue
                
                if user_input.lower().startswith('engine'):
                    parts = user_input.split()
                    if len(parts) > 1:
                        new_engine = parts[1]
                        if new_engine in self.manager.get_available_engines():
                            self.manager.default_engine = new_engine
                            print(f"✅ 默认引擎已切换到: {new_engine}")
                        else:
                            available = ', '.join(self.manager.get_available_engines())
                            print(f"❌ 引擎不可用，可用引擎: {available}")
                    else:
                        print(f"当前默认引擎: {self.manager.default_engine}")
                    continue
                
                # 默认作为TTS文本处理
                self.generate_speech(user_input)
                
            except KeyboardInterrupt:
                print("\n👋 再见！")
                break
            except Exception as e:
                print(f"❌ 错误: {str(e)}")
    
    def _show_help(self):
        """显示帮助信息"""
        print("\n📖 命令帮助:")
        print("  help           - 显示此帮助")
        print("  status         - 显示系统状态")
        print("  voices [引擎]  - 列出音色 (可选指定引擎)")
        print("  engine [名称]  - 查看/切换默认引擎")
        print("  quit/exit/q    - 退出程序")
        print("  其他文本       - 直接进行语音合成")

def main():
    parser = argparse.ArgumentParser(description='统一TTS应用程序')
    parser.add_argument('--config', default='tts_config.json', help='配置文件路径')
    parser.add_argument('--text', '-t', help='要合成的文本')
    parser.add_argument('--engine', '-e', help='指定TTS引擎')
    parser.add_argument('--voice', '-v', help='指定音色')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--interactive', '-i', action='store_true', help='交互模式')
    parser.add_argument('--list-voices', action='store_true', help='列出所有音色')
    parser.add_argument('--status', action='store_true', help='显示系统状态')
    
    # StableTTS参数
    parser.add_argument('--step', type=int, default=25, help='StableTTS推理步数')
    parser.add_argument('--temperature', type=float, default=1.0, help='StableTTS温度参数')
    parser.add_argument('--length-scale', type=float, default=1.0, help='StableTTS长度缩放')
    parser.add_argument('--cfg', type=float, default=3.0, help='StableTTS CFG强度')
    
    args = parser.parse_args()
    
    # 创建应用程序
    app = UnifiedTTSApp(args.config)
    
    # 初始化
    if not app.initialize():
        sys.exit(1)
    
    # 处理命令
    if args.status:
        app.show_status()
    elif args.list_voices:
        app.list_voices()
    elif args.text:
        # 准备引擎参数
        engine_params = {}
        if args.step:
            engine_params['step'] = args.step
        if args.temperature:
            engine_params['temperature'] = args.temperature
        if args.length_scale:
            engine_params['length_scale'] = args.length_scale
        if args.cfg:
            engine_params['cfg'] = args.cfg
        
        app.generate_speech(
            text=args.text,
            engine_name=args.engine,
            voice=args.voice,
            output_file=args.output,
            **engine_params
        )
    elif args.interactive:
        app.interactive_mode()
    else:
        app.show_status()
        print("\n💡 使用 --help 查看更多选项")
        print("💡 使用 --interactive 进入交互模式")

if __name__ == '__main__':
    main()