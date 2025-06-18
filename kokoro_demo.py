#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kokoro TTS 中文语音合成演示脚本
支持多种语音和批量处理
"""

import kokoro
import torchaudio
import os
from pathlib import Path
import argparse
import warnings

# 忽略警告信息
warnings.filterwarnings("ignore")

class KokoroTTSDemo:
    def __init__(self, device='cpu'):
        """初始化Kokoro TTS"""
        print("正在初始化Kokoro TTS...")
        self.pipeline = kokoro.KPipeline('z', device=device)
        self.sample_rate = 24000  # Kokoro的默认采样率
        print(f"Kokoro TTS初始化完成，使用设备: {device}")
    
    def synthesize(self, text, voice='af_heart', output_path=None):
        """合成语音"""
        print(f"正在合成文本: {text}")
        print(f"使用语音: {voice}")
        
        try:
            # 生成语音
            results = list(self.pipeline(text, voice=voice))
            
            if not results:
                print("错误: 没有生成任何结果")
                return None
            
            result = results[0]
            audio = result.audio
            
            print(f"生成成功！音频长度: {len(audio)} samples ({len(audio)/self.sample_rate:.2f}秒)")
            
            # 保存音频文件
            if output_path:
                # 确保输出目录存在
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # 保存为WAV文件
                torchaudio.save(output_path, audio.unsqueeze(0), self.sample_rate)
                print(f"音频已保存为: {output_path}")
            
            return {
                'audio': audio,
                'sample_rate': self.sample_rate,
                'duration': len(audio) / self.sample_rate,
                'phonemes': result.phonemes,
                'text_index': result.text_index
            }
            
        except Exception as e:
            print(f"合成失败: {e}")
            return None
    
    def batch_synthesize(self, texts, voice='af_heart', output_dir='output'):
        """批量合成语音"""
        print(f"开始批量合成 {len(texts)} 个文本...")
        
        results = []
        for i, text in enumerate(texts):
            output_path = os.path.join(output_dir, f"kokoro_output_{i+1:03d}.wav")
            result = self.synthesize(text, voice, output_path)
            if result:
                results.append({
                    'index': i + 1,
                    'text': text,
                    'output_path': output_path,
                    'duration': result['duration']
                })
        
        print(f"批量合成完成！成功生成 {len(results)} 个音频文件")
        return results

def main():
    parser = argparse.ArgumentParser(description='Kokoro TTS 中文语音合成演示')
    parser.add_argument('--text', '-t', type=str, 
                      default='你好，这是Kokoro中文语音合成系统的演示。',
                      help='要合成的文本')
    parser.add_argument('--voice', '-v', type=str, default='af_heart',
                      help='语音模型名称')
    parser.add_argument('--output', '-o', type=str, default='output/demo.wav',
                      help='输出音频文件路径')
    parser.add_argument('--device', '-d', type=str, default='cpu',
                      help='计算设备 (cpu/cuda)')
    parser.add_argument('--batch', action='store_true',
                      help='批量处理模式')
    
    args = parser.parse_args()
    
    # 初始化TTS
    tts = KokoroTTSDemo(device=args.device)
    
    if args.batch:
        # 批量处理示例文本
        texts = [
            "欢迎使用Kokoro中文语音合成系统。",
            "这是一个高质量的神经网络语音合成模型。",
            "它可以生成自然流畅的中文语音。",
            "感谢您的使用！"
        ]
        results = tts.batch_synthesize(texts, voice=args.voice)
        
        print("\n=== 批量处理结果 ===")
        total_duration = 0
        for result in results:
            print(f"文件 {result['index']}: {result['output_path']} "
                  f"(时长: {result['duration']:.2f}秒)")
            total_duration += result['duration']
        print(f"总时长: {total_duration:.2f}秒")
    
    else:
        # 单个文本处理
        result = tts.synthesize(args.text, voice=args.voice, output_path=args.output)
        
        if result:
            print("\n=== 合成结果 ===")
            print(f"文本: {args.text}")
            print(f"语音: {args.voice}")
            print(f"时长: {result['duration']:.2f}秒")
            print(f"采样率: {result['sample_rate']}Hz")
            print(f"输出文件: {args.output}")
            print(f"音素序列: {result['phonemes'][:50]}..." if len(result['phonemes']) > 50 else f"音素序列: {result['phonemes']}")

if __name__ == "__main__":
    main()