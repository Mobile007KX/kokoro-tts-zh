#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kokoro TTS 中文语音合成系统使用示例
展示各种使用场景和功能
"""

import os
import time
import soundfile as sf
from pathlib import Path
from tts_engine_manager import TTSEngineManager

def basic_example():
    """基础使用示例"""
    print("=" * 50)
    print("🎯 基础使用示例")
    print("=" * 50)
    
    # 创建引擎管理器
    manager = TTSEngineManager('tts_config.json')
    
    # 初始化引擎
    print("正在初始化TTS引擎...")
    results = manager.initialize_engines()
    print(f"初始化结果: {results}")
    
    # 检查可用引擎
    available = manager.get_available_engines()
    print(f"可用引擎: {available}")
    
    if not available:
        print("❌ 没有可用的TTS引擎")
        return
    
    # 基础语音合成
    text = "你好，欢迎使用Kokoro TTS中文语音合成系统！这是一个基础使用示例。"
    
    print(f"\n正在合成语音: {text}")
    result = manager.generate_speech(text)
    
    if result:
        # 保存音频
        output_path = "./output/basic_example.wav"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        sf.write(output_path, result.audio, result.sample_rate)
        
        print(f"✅ 语音合成完成!")
        print(f"输出文件: {output_path}")
        print(f"音频时长: {result.audio_length:.2f} 秒")
        print(f"生成时间: {result.generation_time:.2f} 秒")
        print(f"实时倍率: {result.audio_length/result.generation_time:.1f}x")
    else:
        print("❌ 语音合成失败")

def multi_engine_example():
    """多引擎对比示例"""
    print("\n" + "=" * 50)
    print("🔄 多引擎对比示例")
    print("=" * 50)
    
    manager = TTSEngineManager('tts_config.json')
    manager.initialize_engines()
    
    text = "这是一个多引擎对比测试，我们将使用不同的TTS引擎合成相同的文本。"
    available_engines = manager.get_available_engines()
    
    for engine_name in available_engines:
        print(f"\n🎯 正在使用 {engine_name} 引擎合成...")
        
        start_time = time.time()
        result = manager.generate_speech(text, engine_name=engine_name)
        total_time = time.time() - start_time
        
        if result:
            output_path = f"./output/multi_engine_{engine_name}.wav"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            sf.write(output_path, result.audio, result.sample_rate)
            
            print(f"✅ {engine_name} 合成完成")
            print(f"  文件: {output_path}")
            print(f"  时长: {result.audio_length:.2f}s")
            print(f"  生成: {result.generation_time:.2f}s")
            print(f"  总耗: {total_time:.2f}s")
            print(f"  倍率: {result.audio_length/result.generation_time:.1f}x")
        else:
            print(f"❌ {engine_name} 合成失败")

def voice_comparison_example():
    """音色对比示例"""
    print("\n" + "=" * 50)
    print("🎤 音色对比示例")
    print("=" * 50)
    
    manager = TTSEngineManager('tts_config.json')
    manager.initialize_engines()
    
    text = "大家好，我是语音助手，很高兴为您服务。"
    
    # 获取所有音色
    all_voices = manager.get_all_voices()
    
    for engine_name, voice_dict in all_voices.items():
        if engine_name not in manager.get_available_engines():
            continue
            
        print(f"\n🔊 {engine_name.upper()} 引擎音色测试:")
        
        # 只测试几个代表性音色
        test_voices = []
        for category, voices in voice_dict.items():
            if voices:
                test_voices.extend(voices[:2])  # 每个类别取前2个
        
        for voice in test_voices[:4]:  # 最多测试4个音色
            print(f"  正在测试音色: {voice}")
            
            if engine_name == 'kokoro':
                result = manager.generate_speech(
                    text, 
                    engine_name=engine_name, 
                    voice=voice
                )
            else:
                # StableTTS需要参考音频
                ref_audio_path = f"./reference_audios/{voice}.wav"
                if Path(ref_audio_path).exists():
                    result = manager.generate_speech(
                        text,
                        engine_name=engine_name,
                        ref_audio=ref_audio_path
                    )
                else:
                    print(f"    ⚠️  参考音频不存在: {ref_audio_path}")
                    continue
            
            if result:
                output_path = f"./output/voice_{engine_name}_{voice}.wav"
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                sf.write(output_path, result.audio, result.sample_rate)
                print(f"    ✅ 保存到: {output_path}")
            else:
                print(f"    ❌ 合成失败")

def batch_processing_example():
    """批量处理示例"""
    print("\n" + "=" * 50)
    print("📦 批量处理示例")
    print("=" * 50)
    
    manager = TTSEngineManager('tts_config.json')
    manager.initialize_engines()
    
    # 要处理的文本列表
    texts = [
        "欢迎使用语音合成系统。",
        "今天天气很好，适合外出游玩。",
        "人工智能技术正在快速发展。",
        "请注意安全，保持社交距离。",
        "感谢您的使用，再见！"
    ]
    
    print(f"正在批量处理 {len(texts)} 个文本...")
    
    start_time = time.time()
    results = []
    
    for i, text in enumerate(texts):
        print(f"\n处理第 {i+1}/{len(texts)} 个: {text[:20]}...")
        
        result = manager.generate_speech(text)
        
        if result:
            output_path = f"./output/batch_{i+1:02d}.wav"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            sf.write(output_path, result.audio, result.sample_rate)
            
            results.append({
                'index': i+1,
                'text': text,
                'duration': result.audio_length,
                'generation_time': result.generation_time,
                'file': output_path
            })
            
            print(f"  ✅ 完成 ({result.audio_length:.1f}s, {result.generation_time:.1f}s)")
        else:
            print(f"  ❌ 失败")
    
    total_time = time.time() - start_time
    total_audio_duration = sum(r['duration'] for r in results)
    total_generation_time = sum(r['generation_time'] for r in results)
    
    print(f"\n📊 批量处理统计:")
    print(f"  总文本数: {len(texts)}")
    print(f"  成功数量: {len(results)}")
    print(f"  总音频时长: {total_audio_duration:.1f} 秒")
    print(f"  总生成时间: {total_generation_time:.1f} 秒")
    print(f"  总耗时: {total_time:.1f} 秒")
    print(f"  平均实时倍率: {total_audio_duration/total_generation_time:.1f}x")

def parameter_tuning_example():
    """参数调优示例"""
    print("\n" + "=" * 50)
    print("⚙️ 参数调优示例")
    print("=" * 50)
    
    manager = TTSEngineManager('tts_config.json')
    manager.initialize_engines()
    
    text = "这是一个参数调优测试，我们将尝试不同的参数设置。"
    
    # 如果StableTTS可用，测试不同参数
    if 'stable_tts' in manager.get_available_engines():
        print("\n🔧 StableTTS 参数调优:")
        
        # 不同的参数组合
        param_sets = [
            {'step': 10, 'temperature': 0.8, 'cfg': 2.0, 'length_scale': 1.0},
            {'step': 25, 'temperature': 1.0, 'cfg': 3.0, 'length_scale': 1.0},
            {'step': 50, 'temperature': 1.2, 'cfg': 4.0, 'length_scale': 0.9},
        ]
        
        for i, params in enumerate(param_sets):
            print(f"\n  测试参数组合 {i+1}: {params}")
            
            result = manager.generate_speech(
                text,
                engine_name='stable_tts',
                **params
            )
            
            if result:
                output_path = f"./output/param_test_{i+1}.wav"
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                sf.write(output_path, result.audio, result.sample_rate)
                
                print(f"    ✅ 保存到: {output_path}")
                print(f"    时长: {result.audio_length:.2f}s")
                print(f"    生成时间: {result.generation_time:.2f}s")
            else:
                print(f"    ❌ 合成失败")
    
    print("\n💡 参数调优建议:")
    print("  - step: 推理步数，越高质量越好但速度越慢 (10-50)")
    print("  - temperature: 温度参数，控制随机性 (0.8-1.2)")
    print("  - cfg: CFG强度，控制条件引导 (2.0-5.0)")
    print("  - length_scale: 长度缩放，控制语速 (0.8-1.2)")

def error_handling_example():
    """错误处理示例"""
    print("\n" + "=" * 50)
    print("🚨 错误处理示例")
    print("=" * 50)
    
    # 使用错误的配置文件
    try:
        manager = TTSEngineManager('nonexistent_config.json')
        print("❌ 这里应该出现错误")
    except Exception as e:
        print(f"✅ 正确捕获配置文件错误: {type(e).__name__}")
    
    # 正确的管理器
    manager = TTSEngineManager('tts_config.json')
    manager.initialize_engines()
    
    # 测试空文本
    print("\n测试空文本...")
    result = manager.generate_speech("")
    if result is None:
        print("✅ 正确处理空文本")
    
    # 测试不存在的引擎
    print("\n测试不存在的引擎...")
    result = manager.generate_speech("测试", engine_name="nonexistent_engine")
    if result is None:
        print("✅ 正确处理不存在的引擎")
    
    # 测试不存在的音色
    print("\n测试不存在的音色...")
    if 'kokoro' in manager.get_available_engines():
        result = manager.generate_speech(
            "测试", 
            engine_name="kokoro", 
            voice="nonexistent_voice"
        )
        if result is None:
            print("✅ 正确处理不存在的音色")

def performance_benchmark():
    """性能基准测试"""
    print("\n" + "=" * 50)
    print("🏁 性能基准测试")
    print("=" * 50)
    
    manager = TTSEngineManager('tts_config.json')
    manager.initialize_engines()
    
    # 不同长度的文本测试
    test_texts = {
        "短文本": "你好。",
        "中等文本": "这是一个中等长度的测试文本，包含了一些常见的中文词汇和句子结构。",
        "长文本": "这是一个相对较长的测试文本，用来评估TTS系统在处理长文本时的性能表现。" * 3
    }
    
    available_engines = manager.get_available_engines()
    
    print(f"测试引擎: {available_engines}")
    print(f"测试文本类型: {list(test_texts.keys())}")
    
    results = {}
    
    for text_type, text in test_texts.items():
        print(f"\n📝 测试 {text_type} ({len(text)} 字符):")
        
        for engine in available_engines:
            print(f"  🔧 {engine} 引擎...")
            
            # 预热
            manager.generate_speech("预热", engine_name=engine)
            
            # 正式测试
            start_time = time.time()
            result = manager.generate_speech(text, engine_name=engine)
            total_time = time.time() - start_time
            
            if result:
                if engine not in results:
                    results[engine] = {}
                
                results[engine][text_type] = {
                    'audio_length': result.audio_length,
                    'generation_time': result.generation_time,
                    'total_time': total_time,
                    'rtf': result.audio_length / result.generation_time,
                    'chars_per_sec': len(text) / result.generation_time
                }
                
                print(f"    ✅ 时长: {result.audio_length:.1f}s")
                print(f"    ⏱️  生成: {result.generation_time:.1f}s")
                print(f"    🚀 实时倍率: {result.audio_length/result.generation_time:.1f}x")
                print(f"    📊 字符/秒: {len(text)/result.generation_time:.1f}")
            else:
                print(f"    ❌ 测试失败")
    
    # 性能总结
    print(f"\n📈 性能总结:")
    for engine, engine_results in results.items():
        print(f"\n🔧 {engine.upper()} 引擎:")
        avg_rtf = sum(r['rtf'] for r in engine_results.values()) / len(engine_results)
        avg_cps = sum(r['chars_per_sec'] for r in engine_results.values()) / len(engine_results)
        print(f"  平均实时倍率: {avg_rtf:.1f}x")
        print(f"  平均字符/秒: {avg_cps:.1f}")

def main():
    """主函数 - 运行所有示例"""
    print("🎉 Kokoro TTS 中文语音合成系统 - 完整使用示例")
    print("=" * 60)
    
    examples = [
        ("基础使用", basic_example),
        ("多引擎对比", multi_engine_example),
        ("音色对比", voice_comparison_example),
        ("批量处理", batch_processing_example),
        ("参数调优", parameter_tuning_example),
        ("错误处理", error_handling_example),
        ("性能基准", performance_benchmark),
    ]
    
    print("\n选择要运行的示例:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print(f"  0. 运行所有示例")
    
    try:
        choice = input("\n请输入选择 (0-7): ").strip()
        
        if choice == '0':
            for name, func in examples:
                print(f"\n{'='*20} {name} {'='*20}")
                try:
                    func()
                except Exception as e:
                    print(f"❌ {name} 示例运行失败: {e}")
        elif choice.isdigit() and 1 <= int(choice) <= len(examples):
            name, func = examples[int(choice) - 1]
            print(f"\n运行 {name} 示例...")
            func()
        else:
            print("❌ 无效选择")
            
    except KeyboardInterrupt:
        print("\n👋 用户取消操作")
    except Exception as e:
        print(f"❌ 运行错误: {e}")
    
    print("\n🎉 示例运行完成！")
    print("💡 查看 ./output/ 目录中的生成音频文件")

if __name__ == '__main__':
    main()