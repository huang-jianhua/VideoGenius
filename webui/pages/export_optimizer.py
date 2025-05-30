# -*- coding: utf-8 -*-
"""
VideoGenius 导出优化系统
支持多格式导出、质量预设和压缩优化

作者: AI助手
创建时间: 2025-05-28
"""

import streamlit as st
import time
import json
import datetime
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

class ExportFormat(Enum):
    MP4_H264 = "MP4 (H.264)"
    MP4_H265 = "MP4 (H.265/HEVC)"
    AVI = "AVI"
    MOV = "MOV (QuickTime)"
    MKV = "MKV"
    WEBM = "WebM"
    GIF = "GIF动图"

class QualityPreset(Enum):
    ULTRA_HIGH = "超高清 (4K)"
    HIGH = "高清 (1080p)"
    MEDIUM = "标清 (720p)"
    LOW = "低清 (480p)"
    MOBILE = "手机优化 (360p)"
    WEB = "网页优化"

class PlatformOptimization(Enum):
    YOUTUBE = "YouTube"
    TIKTOK = "TikTok/抖音"
    INSTAGRAM = "Instagram"
    WECHAT = "微信视频号"
    BILIBILI = "哔哩哔哩"
    KUAISHOU = "快手"
    XIAOHONGSHU = "小红书"
    GENERAL = "通用格式"

@dataclass
class ExportSettings:
    """导出设置类"""
    format: ExportFormat
    quality: QualityPreset
    platform: PlatformOptimization
    resolution: Tuple[int, int]
    framerate: int
    bitrate: str
    audio_bitrate: str
    compression_level: int  # 1-10
    enable_hardware_acceleration: bool = True
    custom_filename: Optional[str] = None
    watermark_enabled: bool = False
    watermark_text: Optional[str] = None
    watermark_position: str = "bottom_right"

class ExportOptimizer:
    """导出优化系统"""
    
    def __init__(self):
        # 平台优化预设
        self.platform_presets = {
            PlatformOptimization.YOUTUBE: {
                "name": "YouTube优化",
                "description": "适合YouTube平台的高质量设置",
                "recommended_format": ExportFormat.MP4_H264,
                "recommended_quality": QualityPreset.HIGH,
                "resolution_options": [(1920, 1080), (1280, 720), (3840, 2160)],
                "framerate_options": [24, 30, 60],
                "aspect_ratios": ["16:9", "4:3"],
                "max_file_size": "2GB",
                "recommended_bitrate": "5000k",
                "audio_bitrate": "192k"
            },
            PlatformOptimization.TIKTOK: {
                "name": "TikTok/抖音优化",
                "description": "竖屏短视频优化设置",
                "recommended_format": ExportFormat.MP4_H264,
                "recommended_quality": QualityPreset.HIGH,
                "resolution_options": [(1080, 1920), (720, 1280)],
                "framerate_options": [30, 25],
                "aspect_ratios": ["9:16"],
                "max_file_size": "500MB",
                "recommended_bitrate": "3000k",
                "audio_bitrate": "128k"
            },
            PlatformOptimization.INSTAGRAM: {
                "name": "Instagram优化",
                "description": "Instagram视频和Story优化",
                "recommended_format": ExportFormat.MP4_H264,
                "recommended_quality": QualityPreset.HIGH,
                "resolution_options": [(1080, 1080), (1080, 1920), (1920, 1080)],
                "framerate_options": [30, 25],
                "aspect_ratios": ["1:1", "9:16", "16:9"],
                "max_file_size": "100MB",
                "recommended_bitrate": "2500k",
                "audio_bitrate": "128k"
            },
            PlatformOptimization.WECHAT: {
                "name": "微信视频号优化",
                "description": "微信平台视频优化设置",
                "recommended_format": ExportFormat.MP4_H264,
                "recommended_quality": QualityPreset.MEDIUM,
                "resolution_options": [(1080, 1920), (720, 1280)],
                "framerate_options": [25, 30],
                "aspect_ratios": ["9:16", "16:9"],
                "max_file_size": "200MB",
                "recommended_bitrate": "2000k",
                "audio_bitrate": "128k"
            },
            PlatformOptimization.BILIBILI: {
                "name": "哔哩哔哩优化",
                "description": "B站视频上传优化设置",
                "recommended_format": ExportFormat.MP4_H264,
                "recommended_quality": QualityPreset.HIGH,
                "resolution_options": [(1920, 1080), (1280, 720)],
                "framerate_options": [30, 25, 60],
                "aspect_ratios": ["16:9"],
                "max_file_size": "8GB",
                "recommended_bitrate": "6000k",
                "audio_bitrate": "192k"
            },
            PlatformOptimization.KUAISHOU: {
                "name": "快手优化",
                "description": "快手平台视频优化设置",
                "recommended_format": ExportFormat.MP4_H264,
                "recommended_quality": QualityPreset.HIGH,
                "resolution_options": [(1080, 1920), (720, 1280)],
                "framerate_options": [30, 25],
                "aspect_ratios": ["9:16"],
                "max_file_size": "500MB",
                "recommended_bitrate": "3000k",
                "audio_bitrate": "128k"
            },
            PlatformOptimization.XIAOHONGSHU: {
                "name": "小红书优化",
                "description": "小红书平台视频优化设置",
                "recommended_format": ExportFormat.MP4_H264,
                "recommended_quality": QualityPreset.HIGH,
                "resolution_options": [(1080, 1920), (1080, 1080)],
                "framerate_options": [30, 25],
                "aspect_ratios": ["9:16", "1:1"],
                "max_file_size": "100MB",
                "recommended_bitrate": "2500k",
                "audio_bitrate": "128k"
            },
            PlatformOptimization.GENERAL: {
                "name": "通用格式",
                "description": "通用视频格式，适合多平台使用",
                "recommended_format": ExportFormat.MP4_H264,
                "recommended_quality": QualityPreset.HIGH,
                "resolution_options": [(1920, 1080), (1280, 720)],
                "framerate_options": [30, 25],
                "aspect_ratios": ["16:9"],
                "max_file_size": "2GB",
                "recommended_bitrate": "5000k",
                "audio_bitrate": "192k"
            }
        }
        
        # 质量预设详细配置
        self.quality_presets = {
            QualityPreset.ULTRA_HIGH: {
                "resolution": (3840, 2160),
                "bitrate": "15000k",
                "audio_bitrate": "320k",
                "compression": 3,
                "description": "4K超高清，适合专业用途"
            },
            QualityPreset.HIGH: {
                "resolution": (1920, 1080),
                "bitrate": "5000k",
                "audio_bitrate": "192k", 
                "compression": 5,
                "description": "1080p高清，平衡质量与文件大小"
            },
            QualityPreset.MEDIUM: {
                "resolution": (1280, 720),
                "bitrate": "2500k",
                "audio_bitrate": "128k",
                "compression": 6,
                "description": "720p标清，适合网络传输"
            },
            QualityPreset.LOW: {
                "resolution": (854, 480),
                "bitrate": "1000k",
                "audio_bitrate": "96k",
                "compression": 7,
                "description": "480p低清，文件较小"
            },
            QualityPreset.MOBILE: {
                "resolution": (640, 360),
                "bitrate": "500k",
                "audio_bitrate": "64k",
                "compression": 8,
                "description": "移动设备优化，最小文件"
            },
            QualityPreset.WEB: {
                "resolution": (1280, 720),
                "bitrate": "1500k",
                "audio_bitrate": "96k",
                "compression": 7,
                "description": "网页播放优化，快速加载"
            }
        }
        
        # 格式特性 - 补充完整的格式定义
        self.format_features = {
            ExportFormat.MP4_H264: {
                "compatibility": "极高",
                "compression": "优秀",
                "quality": "高",
                "file_size": "中等",
                "description": "最通用的格式，所有设备都支持"
            },
            ExportFormat.MP4_H265: {
                "compatibility": "高",
                "compression": "极佳",
                "quality": "极高",
                "file_size": "小",
                "description": "新一代编码，更小文件更高质量"
            },
            ExportFormat.AVI: {
                "compatibility": "高",
                "compression": "一般",
                "quality": "高",
                "file_size": "大",
                "description": "经典格式，兼容性好但文件较大"
            },
            ExportFormat.MOV: {
                "compatibility": "中等",
                "compression": "优秀",
                "quality": "极高",
                "file_size": "大",
                "description": "苹果QuickTime格式，专业级质量"
            },
            ExportFormat.MKV: {
                "compatibility": "中等",
                "compression": "优秀",
                "quality": "极高",
                "file_size": "中等",
                "description": "开源格式，支持多音轨和字幕"
            },
            ExportFormat.WEBM: {
                "compatibility": "中等",
                "compression": "优秀",
                "quality": "高",
                "file_size": "小",
                "description": "网页优化格式，Google支持"
            },
            ExportFormat.GIF: {
                "compatibility": "极高",
                "compression": "差",
                "quality": "中等",
                "file_size": "大",
                "description": "动图格式，支持透明背景"
            }
        }
    
    def get_recommended_settings(self, platform: PlatformOptimization) -> ExportSettings:
        """获取平台推荐设置"""
        preset = self.platform_presets[platform]
        quality_preset = self.quality_presets[preset["recommended_quality"]]
        
        return ExportSettings(
            format=preset["recommended_format"],
            quality=preset["recommended_quality"],
            platform=platform,
            resolution=quality_preset["resolution"],
            framerate=preset["framerate_options"][0],
            bitrate=preset["recommended_bitrate"],
            audio_bitrate=preset["audio_bitrate"],
            compression_level=quality_preset["compression"]
        )
    
    def estimate_file_size(self, settings: ExportSettings, duration_seconds: int) -> str:
        """估算文件大小"""
        # 简化的文件大小估算
        bitrate_kbps = int(settings.bitrate.replace('k', ''))
        audio_bitrate_kbps = int(settings.audio_bitrate.replace('k', ''))
        
        total_bitrate = bitrate_kbps + audio_bitrate_kbps
        file_size_mb = (total_bitrate * duration_seconds) / (8 * 1000)  # 转换为MB
        
        # 根据压缩级别调整
        compression_factor = 1.0 - (settings.compression_level - 1) * 0.1
        file_size_mb *= compression_factor
        
        if file_size_mb < 1:
            return f"{file_size_mb * 1000:.0f} KB"
        elif file_size_mb < 1000:
            return f"{file_size_mb:.1f} MB"
        else:
            return f"{file_size_mb / 1000:.2f} GB"

# 全局导出优化器实例
export_optimizer = ExportOptimizer()

def render_platform_selector():
    """渲染平台选择器"""
    st.markdown("## 🎯 平台优化选择")
    
    # 平台选择
    platform_options = {platform: preset["name"] for platform, preset in export_optimizer.platform_presets.items()}
    
    selected_platform = st.selectbox(
        "选择目标平台：",
        options=list(platform_options.keys()),
        format_func=lambda x: platform_options[x],
        help="选择视频发布平台，系统会自动优化设置"
    )
    
    # 显示平台信息
    platform_info = export_optimizer.platform_presets[selected_platform]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"📝 **描述**: {platform_info['description']}")
        st.success(f"📐 **宽高比**: {', '.join(platform_info['aspect_ratios'])}")
        
    with col2:
        st.warning(f"📦 **文件限制**: {platform_info['max_file_size']}")
        st.info(f"🎬 **推荐帧率**: {platform_info['framerate_options'][0]} fps")
    
    # 自动应用推荐设置
    if st.button("✨ 使用推荐设置", type="primary"):
        recommended_settings = export_optimizer.get_recommended_settings(selected_platform)
        st.session_state.export_settings = recommended_settings
        st.success(f"✅ 已应用 {platform_info['name']} 的推荐设置！")
        st.rerun()
    
    return selected_platform

def render_advanced_settings():
    """渲染高级设置"""
    st.markdown("## ⚙️ 高级设置")
    
    if 'export_settings' not in st.session_state:
        st.session_state.export_settings = ExportSettings(
            format=ExportFormat.MP4_H264,
            quality=QualityPreset.HIGH,
            platform=PlatformOptimization.GENERAL,
            resolution=(1920, 1080),
            framerate=30,
            bitrate="5000k",
            audio_bitrate="192k",
            compression_level=5
        )
    
    settings = st.session_state.export_settings
    export_optimizer = ExportOptimizer()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📁 格式设置")
        
        # 输出格式选择 - 添加错误处理
        format_options = {fmt: fmt.value for fmt in ExportFormat}
        try:
            # 尝试找到当前格式的索引
            format_keys = list(format_options.keys())
            if settings.format in format_keys:
                default_format_index = format_keys.index(settings.format)
            else:
                default_format_index = 0  # 默认选择第一个
        except (ValueError, AttributeError):
            default_format_index = 0
            
        selected_format = st.selectbox(
            "输出格式：",
            options=list(format_options.keys()),
            format_func=lambda x: format_options[x],
            index=default_format_index
        )
        
        # 显示格式特性
        if selected_format in export_optimizer.format_features:
            features = export_optimizer.format_features[selected_format]
            with st.expander("📊 格式特性"):
                st.write(f"**兼容性**: {features['compatibility']}")
                st.write(f"**压缩效果**: {features['compression']}")
                st.write(f"**画质**: {features['quality']}")
                st.write(f"**文件大小**: {features['file_size']}")
                st.info(features['description'])
        
        # 质量预设 - 添加错误处理
        try:
            quality_options = {}
            for quality in QualityPreset:
                if quality in export_optimizer.quality_presets:
                    quality_options[quality] = f"{quality.value} - {export_optimizer.quality_presets[quality]['description']}"
                else:
                    # 为缺失的预设提供默认值
                    quality_options[quality] = f"{quality.value} - 标准设置"
                    
            # 安全地获取质量预设索引
            quality_keys = list(quality_options.keys())
            if settings.quality in quality_keys:
                default_quality_index = quality_keys.index(settings.quality)
            else:
                default_quality_index = 0
                
        except Exception as e:
            st.error(f"质量预设加载错误: {e}")
            quality_options = {QualityPreset.HIGH: "高清 (1080p) - 标准设置"}
            default_quality_index = 0
            
        selected_quality = st.selectbox(
            "质量预设：",
            options=list(quality_options.keys()),
            format_func=lambda x: quality_options[x],
            index=default_quality_index
        )
    
    with col2:
        st.markdown("### 🎬 视频参数")
        
        # 分辨率设置 - 添加错误处理
        try:
            if selected_quality in export_optimizer.quality_presets:
                quality_preset = export_optimizer.quality_presets[selected_quality]
                default_resolution = quality_preset["resolution"]
            else:
                # 如果找不到预设，使用默认值
                default_resolution = (1920, 1080)
        except (KeyError, AttributeError):
            default_resolution = (1920, 1080)
        
        resolution_options = [
            (3840, 2160, "4K Ultra HD"),
            (1920, 1080, "Full HD 1080p"),
            (1280, 720, "HD 720p"),
            (854, 480, "SD 480p"),
            (640, 360, "低清 360p")
        ]
        
        resolution_labels = [f"{w}x{h} ({label})" for w, h, label in resolution_options]
        try:
            default_index = [r[:2] for r in resolution_options].index(default_resolution)
        except ValueError:
            default_index = 1
            
        selected_resolution_idx = st.selectbox(
            "分辨率：",
            options=range(len(resolution_options)),
            format_func=lambda x: resolution_labels[x],
            index=default_index
        )
        
        selected_resolution = resolution_options[selected_resolution_idx][:2]
        
        # 帧率设置
        framerate = st.selectbox(
            "帧率 (FPS)：",
            options=[24, 25, 30, 50, 60],
            index=2  # 默认30fps
        )
        
        # 比特率设置
        bitrate = st.selectbox(
            "视频比特率：",
            options=["1000k", "2500k", "5000k", "8000k", "15000k"],
            index=2,  # 默认5000k
            help="更高的比特率意味着更好的画质，但文件更大"
        )
        
        audio_bitrate = st.selectbox(
            "音频比特率：",
            options=["64k", "96k", "128k", "192k", "320k"],
            index=3  # 默认192k
        )
    
    # 压缩和优化设置
    st.markdown("### 🗜️ 压缩优化")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        compression_level = st.slider(
            "压缩级别",
            min_value=1,
            max_value=10,
            value=settings.compression_level,
            help="1=最高质量(文件大), 10=最高压缩(文件小)"
        )
    
    with col2:
        hardware_acceleration = st.checkbox(
            "硬件加速",
            value=settings.enable_hardware_acceleration,
            help="使用GPU加速编码，提高导出速度"
        )
    
    with col3:
        # 估算文件大小
        temp_settings = ExportSettings(
            format=selected_format,
            quality=selected_quality,
            platform=settings.platform,
            resolution=selected_resolution,
            framerate=framerate,
            bitrate=bitrate,
            audio_bitrate=audio_bitrate,
            compression_level=compression_level,
            enable_hardware_acceleration=hardware_acceleration
        )
        
        estimated_size = export_optimizer.estimate_file_size(temp_settings, 180)  # 假设3分钟视频
        st.metric("预估文件大小", estimated_size, help="基于3分钟视频的估算")
    
    # 水印设置
    st.markdown("### 🏷️ 水印设置")
    
    watermark_enabled = st.checkbox("添加水印", value=settings.watermark_enabled)
    
    if watermark_enabled:
        col1, col2 = st.columns(2)
        
        with col1:
            watermark_text = st.text_input(
                "水印文字：",
                value=settings.watermark_text or "VideoGenius",
                placeholder="输入水印文字..."
            )
        
        with col2:
            watermark_position = st.selectbox(
                "水印位置：",
                options=["top_left", "top_right", "bottom_left", "bottom_right", "center"],
                format_func=lambda x: {
                    "top_left": "左上角",
                    "top_right": "右上角", 
                    "bottom_left": "左下角",
                    "bottom_right": "右下角",
                    "center": "居中"
                }[x],
                index=3  # 默认右下角
            )
    else:
        watermark_text = None
        watermark_position = "bottom_right"
    
    # 文件名设置
    st.markdown("### 📁 输出设置")
    
    custom_filename = st.text_input(
        "自定义文件名（可选）：",
        value=settings.custom_filename or "",
        placeholder="留空则自动生成文件名",
        help="不需要包含文件扩展名"
    )
    
    # 更新设置
    updated_settings = ExportSettings(
        format=selected_format,
        quality=selected_quality,
        platform=settings.platform,
        resolution=selected_resolution,
        framerate=framerate,
        bitrate=bitrate,
        audio_bitrate=audio_bitrate,
        compression_level=compression_level,
        enable_hardware_acceleration=hardware_acceleration,
        custom_filename=custom_filename if custom_filename else None,
        watermark_enabled=watermark_enabled,
        watermark_text=watermark_text,
        watermark_position=watermark_position
    )
    
    st.session_state.export_settings = updated_settings
    
    return updated_settings

def render_export_preview():
    """渲染导出预览"""
    st.markdown("## 👁️ 导出预览")
    
    if 'export_settings' not in st.session_state:
        st.info("请先配置导出设置")
        return
    
    settings = st.session_state.export_settings
    
    # 设置摘要
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 导出摘要")
        st.write(f"**格式**: {settings.format.value}")
        st.write(f"**质量**: {settings.quality.value}")
        st.write(f"**分辨率**: {settings.resolution[0]}x{settings.resolution[1]}")
        st.write(f"**帧率**: {settings.framerate} fps")
        st.write(f"**视频比特率**: {settings.bitrate}")
        st.write(f"**音频比特率**: {settings.audio_bitrate}")
    
    with col2:
        st.markdown("### ⚙️ 优化设置")
        st.write(f"**压缩级别**: {settings.compression_level}/10")
        st.write(f"**硬件加速**: {'✅ 启用' if settings.enable_hardware_acceleration else '❌ 禁用'}")
        st.write(f"**水印**: {'✅ 启用' if settings.watermark_enabled else '❌ 禁用'}")
        
        if settings.watermark_enabled:
            st.write(f"**水印文字**: {settings.watermark_text}")
            st.write(f"**水印位置**: {settings.watermark_position}")
    
    # 文件大小估算
    st.markdown("### 📊 文件大小估算")
    
    durations = [60, 180, 300, 600]  # 1分钟, 3分钟, 5分钟, 10分钟
    
    size_data = []
    for duration in durations:
        estimated_size = export_optimizer.estimate_file_size(settings, duration)
        size_data.append({
            "时长": f"{duration//60}分钟",
            "预估大小": estimated_size
        })
    
    for data in size_data:
        st.write(f"• **{data['时长']}**: {data['预估大小']}")
    
    # 导出按钮
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🚀 开始导出", type="primary", use_container_width=True):
            simulate_export(settings)

def simulate_export(settings: ExportSettings):
    """模拟导出过程"""
    st.markdown("## 🔄 正在导出...")
    
    # 创建进度条
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # 模拟导出过程
    steps = [
        "初始化导出设置...",
        "加载视频文件...", 
        "应用视频效果...",
        "编码视频流...",
        "编码音频流...",
        "合并音视频...",
        "应用压缩优化...",
        "添加水印..." if settings.watermark_enabled else "跳过水印添加...",
        "写入输出文件...",
        "完成导出！"
    ]
    
    for i, step in enumerate(steps):
        status_text.text(step)
        progress = (i + 1) / len(steps)
        progress_bar.progress(progress)
        time.sleep(0.5)  # 模拟处理时间
    
    # 导出完成
    st.balloons()
    st.success("🎉 视频导出完成！")
    
    # 生成文件信息
    filename = settings.custom_filename or f"video_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    extension = ".mp4" if "MP4" in settings.format.value else ".webm" if "WebM" in settings.format.value else ".avi"
    full_filename = f"{filename}{extension}"
    
    file_size = export_optimizer.estimate_file_size(settings, 180)  # 假设3分钟
    
    st.info(f"📁 **文件名**: {full_filename}")
    st.info(f"📦 **文件大小**: {file_size}")
    st.info(f"📍 **保存位置**: output/{full_filename}")
    
    # 下载按钮（模拟）
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("📥 下载视频"):
            st.success("下载功能开发中...")
    
    with col2:
        if st.button("📤 分享视频"):
            st.success("分享功能开发中...")
    
    with col3:
        if st.button("🔄 导出其他格式"):
            st.rerun()

def render_export_presets():
    """渲染导出预设"""
    st.markdown("## 📋 快速预设")
    
    # 预设选项
    presets = {
        "social_media": {
            "name": "🎭 社交媒体优化",
            "description": "适合抖音、快手等短视频平台",
            "settings": ExportSettings(
                format=ExportFormat.MP4_H264,
                quality=QualityPreset.HIGH,
                platform=PlatformOptimization.TIKTOK,
                resolution=(1080, 1920),
                framerate=30,
                bitrate="3000k",
                audio_bitrate="128k",
                compression_level=6
            )
        },
        "youtube_hd": {
            "name": "🎬 YouTube高清",
            "description": "YouTube平台高质量设置",
            "settings": ExportSettings(
                format=ExportFormat.MP4_H264,
                quality=QualityPreset.HIGH,
                platform=PlatformOptimization.YOUTUBE,
                resolution=(1920, 1080),
                framerate=30,
                bitrate="5000k",
                audio_bitrate="192k",
                compression_level=5
            )
        },
        "web_optimized": {
            "name": "🌐 网页优化",
            "description": "适合网站嵌入的小文件",
            "settings": ExportSettings(
                format=ExportFormat.WEBM,
                quality=QualityPreset.MEDIUM,
                platform=PlatformOptimization.GENERAL,
                resolution=(1280, 720),
                framerate=25,
                bitrate="2000k",
                audio_bitrate="128k",
                compression_level=7
            )
        },
        "mobile_friendly": {
            "name": "📱 移动设备友好",
            "description": "文件小，适合移动设备观看",
            "settings": ExportSettings(
                format=ExportFormat.MP4_H264,
                quality=QualityPreset.MOBILE,
                platform=PlatformOptimization.GENERAL,
                resolution=(640, 360),
                framerate=25,
                bitrate="800k",
                audio_bitrate="96k",
                compression_level=8
            )
        }
    }
    
    # 显示预设选项
    for preset_key, preset_data in presets.items():
        with st.expander(f"{preset_data['name']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(preset_data['description'])
                settings = preset_data['settings']
                st.write(f"• **格式**: {settings.format.value}")
                st.write(f"• **分辨率**: {settings.resolution[0]}x{settings.resolution[1]}")
                st.write(f"• **比特率**: {settings.bitrate}")
                
                # 估算文件大小
                estimated_size = export_optimizer.estimate_file_size(settings, 180)
                st.write(f"• **估算大小**: {estimated_size} (3分钟)")
            
            with col2:
                if st.button(f"使用预设", key=f"preset_{preset_key}"):
                    st.session_state.export_settings = preset_data['settings']
                    st.success(f"✅ 已应用 {preset_data['name']} 预设！")
                    st.rerun()

def main():
    """主函数"""
# 页面配置 - 只有当页面直接运行时才设置
try:
    st.set_page_config(
        page_title="导出优化器 - VideoGenius",
        page_icon="📤",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except st.errors.StreamlitAPIException:
    # 页面配置已经设置过了（通过Main.py），跳过
    pass
    
    # 页面标题
    st.title("📤 VideoGenius 导出优化系统")
    st.markdown("*多格式导出，质量优化，让您的视频适配各种平台*")
    st.markdown("---")
    
    # 主要功能选项卡
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 平台优化", "⚙️ 高级设置", "👁️ 导出预览", "📋 快速预设"])
    
    with tab1:
        render_platform_selector()
    
    with tab2:
        render_advanced_settings()
    
    with tab3:
        render_export_preview()
    
    with tab4:
        render_export_presets()
    
    # 侧边栏
    with st.sidebar:
        st.markdown("### 📊 当前设置")
        
        if 'export_settings' in st.session_state:
            settings = st.session_state.export_settings
            st.info(f"**格式**: {settings.format.value}")
            st.info(f"**质量**: {settings.quality.value}")
            st.info(f"**分辨率**: {settings.resolution[0]}x{settings.resolution[1]}")
            
            # 快速估算
            estimated_size = export_optimizer.estimate_file_size(settings, 180)
            st.metric("预估大小", estimated_size, help="3分钟视频")
        else:
            st.warning("未设置导出参数")
        
        st.markdown("---")
        st.markdown("### 🔗 快速链接")
        if st.button("🏠 返回首页"):
            st.switch_page("Main.py")
        if st.button("📚 模板库"):
            st.switch_page("pages/template_library.py")
        if st.button("🔄 批量处理"):
            st.switch_page("pages/batch_processor.py")
        
        st.markdown("---")
        st.markdown("### 💡 使用提示")
        with st.expander("📖 导出指南"):
            st.markdown("""
            **格式选择建议**：
            • MP4 - 最兼容，推荐首选
            • WebM - 网页优化，文件更小
            • H.265 - 新设备，质量更好
            
            **质量设置建议**：
            • 社交媒体：720p-1080p
            • 专业用途：1080p-4K
            • 网页嵌入：480p-720p
            """)

if __name__ == "__main__":
    main() 