#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kokoro TTS 中文版 - 声音库分析工具
分析voices目录中的所有音色文件，统计数量和分类
"""

import os
from pathlib import Path
import torch

def analyze_voice_library():
    """
    分析voices目录中的音色文件
    """
    voices_dir = Path(__file__).parent / "voices"
    
    if not voices_dir.exists():
        print(f"错误: voices目录不存在: {voices_dir}")
        return
    
    # 获取所有.pt文件
    voice_files = list(voices_dir.glob("*.pt"))
    
    # 分类统计
    female_voices = [f for f in voice_files if f.name.startswith("zf_")]
    male_voices = [f for f in voice_files if f.name.startswith("zm_")]
    english_voices = [f for f in voice_files if f.name.startswith(("af_", "bf_"))]
    
    print("=" * 60)
    print("Kokoro TTS 中文版 - 声音库分析报告")
    print("=" * 60)
    
    print(f"\n📁 声音库目录: {voices_dir}")
    print(f"📊 总音色数量: {len(voice_files)} 个")
    
    print("\n🎭 音色分类统计:")
    print(f"  👩 女声音色 (zf_): {len(female_voices)} 个")
    print(f"  👨 男声音色 (zm_): {len(male_voices)} 个")
    print(f"  🌍 英文音色 (af_/bf_): {len(english_voices)} 个")
    
    # 详细列表
    print("\n👩 女声音色列表:")
    for voice in sorted(female_voices):
        file_size = voice.stat().st_size / (1024 * 1024)  # MB
        print(f"  - {voice.name:<12} ({file_size:.1f} MB)")
    
    print("\n👨 男声音色列表:")
    for voice in sorted(male_voices):
        file_size = voice.stat().st_size / (1024 * 1024)  # MB
        print(f"  - {voice.name:<12} ({file_size:.1f} MB)")
    
    print("\n🌍 英文音色列表:")
    for voice in sorted(english_voices):
        file_size = voice.stat().st_size / (1024 * 1024)  # MB
        print(f"  - {voice.name:<12} ({file_size:.1f} MB)")
    
    # 计算总文件大小
    total_size = sum(f.stat().st_size for f in voice_files) / (1024 * 1024)  # MB
    print(f"\n💾 声音库总大小: {total_size:.1f} MB")
    
    # 检查文件完整性
    print("\n🔍 文件完整性检查:")
    corrupted_files = []
    for voice_file in voice_files:
        try:
            # 尝试加载文件检查是否损坏
            torch.load(voice_file, map_location='cpu')
            print(f"  ✅ {voice_file.name}")
        except Exception as e:
            print(f"  ❌ {voice_file.name} - 错误: {str(e)}")
            corrupted_files.append(voice_file.name)
    
    if corrupted_files:
        print(f"\n⚠️  发现 {len(corrupted_files)} 个损坏文件")
    else:
        print(f"\n✅ 所有 {len(voice_files)} 个音色文件完整无损")
    
    # 推荐音色
    print("\n🌟 推荐音色:")
    print("  女声推荐:")
    print("    - zf_001: 清澈年轻女声，适合教学内容")
    print("    - zf_018: 温和成熟女声，适合正式场合")
    print("    - zf_039: 活泼女声，适合儿童内容")
    print("  男声推荐:")
    print("    - zm_010: 磁性男声，适合新闻播报")
    print("    - zm_025: 温和男声，适合教学解说")
    print("    - zm_041: 年轻男声，适合互动内容")
    
    print("\n" + "=" * 60)
    print("分析完成!")
    print("=" * 60)

def get_voice_recommendations(content_type="general"):
    """
    根据内容类型推荐合适的音色
    
    Args:
        content_type (str): 内容类型
            - 'education': 教育内容
            - 'news': 新闻播报
            - 'children': 儿童内容
            - 'formal': 正式场合
            - 'casual': 休闲内容
            - 'general': 通用
    
    Returns:
        dict: 推荐的音色配置
    """
    recommendations = {
        'education': {
            'female': ['zf_001', 'zf_018', 'zf_027'],
            'male': ['zm_025', 'zm_033', 'zm_052'],
            'description': '清晰标准，适合教学'
        },
        'news': {
            'female': ['zf_018', 'zf_028', 'zf_047'],
            'male': ['zm_010', 'zm_030', 'zm_062'],
            'description': '权威庄重，适合新闻'
        },
        'children': {
            'female': ['zf_039', 'zf_044', 'zf_071'],
            'male': ['zm_041', 'zm_058', 'zm_089'],
            'description': '活泼亲切，适合儿童'
        },
        'formal': {
            'female': ['zf_002', 'zf_023', 'zf_048'],
            'male': ['zm_015', 'zm_034', 'zm_066'],
            'description': '正式得体，适合商务'
        },
        'casual': {
            'female': ['zf_006', 'zf_042', 'zf_075'],
            'male': ['zm_020', 'zm_045', 'zm_091'],
            'description': '轻松自然，适合日常'
        },
        'general': {
            'female': ['zf_001', 'zf_018', 'zf_039'],
            'male': ['zm_010', 'zm_025', 'zm_041'],
            'description': '通用推荐，平衡各方面'
        }
    }
    
    return recommendations.get(content_type, recommendations['general'])

if __name__ == "__main__":
    analyze_voice_library()
    
    print("\n" + "=" * 60)
    print("音色推荐示例:")
    print("=" * 60)
    
    for content_type in ['education', 'news', 'children']:
        rec = get_voice_recommendations(content_type)
        print(f"\n📚 {content_type.upper()} - {rec['description']}")
        print(f"  女声: {', '.join(rec['female'])}")
        print(f"  男声: {', '.join(rec['male'])}")