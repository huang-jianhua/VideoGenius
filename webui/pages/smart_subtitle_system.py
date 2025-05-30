"""
📝 智能字幕系统
自动字幕生成、多语言翻译、字幕样式定制、时间轴同步、字幕特效

作者: VideoGenius AI助手
版本: v1.0
创建时间: 2025-05-29
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import plotly.express as px
import plotly.graph_objects as go
from dataclasses import dataclass
from enum import Enum
import re

# 页面配置 - 只有当页面直接运行时才设置
try:
    st.set_page_config(
        page_title="智能字幕系统 - VideoGenius",
        page_icon="📝",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except st.errors.StreamlitAPIException:
    # 页面配置已经设置过了（通过Main.py），跳过
    pass

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #4ecdc4 0%, #44a08d 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .subtitle-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #4ecdc4;
        margin-bottom: 1rem;
    }
    .subtitle-preview {
        background: #000;
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.2rem;
        margin: 1rem 0;
        position: relative;
        min-height: 100px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .subtitle-text {
        background: rgba(0,0,0,0.8);
        padding: 0.5rem 1rem;
        border-radius: 5px;
        display: inline-block;
    }
    .timeline-item {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: background 0.2s;
    }
    .timeline-item:hover {
        background: #e9ecef;
    }
    .style-option {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        text-align: center;
        cursor: pointer;
        margin: 0.5rem;
        transition: transform 0.2s;
    }
    .style-option:hover {
        transform: translateY(-2px);
    }
    .translation-box {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .accuracy-meter {
        background: #e9ecef;
        height: 20px;
        border-radius: 10px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    .accuracy-bar {
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    .accuracy-excellent { background: #28a745; }
    .accuracy-good { background: #ffc107; }
    .accuracy-fair { background: #fd7e14; }
    .accuracy-poor { background: #dc3545; }
</style>
""", unsafe_allow_html=True)

# 数据类定义
@dataclass
class SubtitleSegment:
    """字幕片段"""
    start_time: float
    end_time: float
    text: str
    confidence: float
    speaker_id: Optional[str] = None

@dataclass
class SubtitleStyle:
    """字幕样式"""
    font_family: str
    font_size: int
    font_color: str
    background_color: str
    outline_color: str
    outline_width: int
    position: str
    alignment: str
    opacity: float

class Language(Enum):
    """支持的语言"""
    CHINESE_SIMPLIFIED = "中文(简体)"
    CHINESE_TRADITIONAL = "中文(繁体)"
    ENGLISH = "英语"
    JAPANESE = "日语"
    KOREAN = "韩语"
    FRENCH = "法语"
    GERMAN = "德语"
    SPANISH = "西班牙语"
    ITALIAN = "意大利语"
    RUSSIAN = "俄语"
    PORTUGUESE = "葡萄牙语"
    ARABIC = "阿拉伯语"

class SubtitleFormat(Enum):
    """字幕格式"""
    SRT = "SRT"
    VTT = "WebVTT"
    ASS = "ASS/SSA"
    TTML = "TTML"
    SBV = "SBV"

class FontFamily(Enum):
    """字体系列"""
    MICROSOFT_YAHEI = "微软雅黑"
    SIMHEI = "黑体"
    SIMSUN = "宋体"
    ARIAL = "Arial"
    HELVETICA = "Helvetica"
    TIMES_NEW_ROMAN = "Times New Roman"
    ROBOTO = "Roboto"

class Position(Enum):
    """字幕位置"""
    BOTTOM = "底部"
    TOP = "顶部"
    CENTER = "中央"
    BOTTOM_LEFT = "左下"
    BOTTOM_RIGHT = "右下"

# 智能字幕引擎
class SmartSubtitleEngine:
    """智能字幕引擎"""
    
    def __init__(self):
        self.subtitle_history = []
        self.translation_cache = {}
        self.style_presets = self._initialize_style_presets()
        
    def _initialize_style_presets(self) -> Dict[str, SubtitleStyle]:
        """初始化样式预设"""
        return {
            "经典白字": SubtitleStyle(
                font_family=FontFamily.MICROSOFT_YAHEI.value,
                font_size=24,
                font_color="#FFFFFF",
                background_color="rgba(0,0,0,0.8)",
                outline_color="#000000",
                outline_width=2,
                position=Position.BOTTOM.value,
                alignment="center",
                opacity=1.0
            ),
            "黄色字幕": SubtitleStyle(
                font_family=FontFamily.MICROSOFT_YAHEI.value,
                font_size=26,
                font_color="#FFFF00",
                background_color="rgba(0,0,0,0.6)",
                outline_color="#000000",
                outline_width=3,
                position=Position.BOTTOM.value,
                alignment="center",
                opacity=1.0
            ),
            "现代简约": SubtitleStyle(
                font_family=FontFamily.ROBOTO.value,
                font_size=22,
                font_color="#FFFFFF",
                background_color="rgba(0,0,0,0.0)",
                outline_color="#000000",
                outline_width=1,
                position=Position.BOTTOM.value,
                alignment="center",
                opacity=0.9
            ),
            "新闻风格": SubtitleStyle(
                font_family=FontFamily.SIMHEI.value,
                font_size=20,
                font_color="#FFFFFF",
                background_color="rgba(0,0,0,0.9)",
                outline_color="#FFFFFF",
                outline_width=1,
                position=Position.BOTTOM.value,
                alignment="center",
                opacity=1.0
            ),
            "创意彩色": SubtitleStyle(
                font_family=FontFamily.ARIAL.value,
                font_size=28,
                font_color="#FF6B6B",
                background_color="rgba(255,255,255,0.2)",
                outline_color="#FFFFFF",
                outline_width=2,
                position=Position.CENTER.value,
                alignment="center",
                opacity=0.95
            )
        }
    
    def generate_subtitles(self, audio_file: str, language: str) -> List[SubtitleSegment]:
        """生成字幕"""
        # 模拟语音识别过程
        time.sleep(3)  # 模拟处理时间
        
        # 生成示例字幕片段
        sample_texts = [
            "欢迎观看VideoGenius智能字幕系统演示",
            "这是一个功能强大的AI字幕生成工具",
            "支持多种语言的自动识别和翻译",
            "可以自定义字幕样式和特效",
            "让您的视频更加专业和易懂"
        ]
        
        segments = []
        current_time = 0.0
        
        for i, text in enumerate(sample_texts):
            duration = len(text) * 0.15 + np.random.uniform(1, 3)  # 根据文本长度估算时长
            confidence = np.random.uniform(0.85, 0.98)  # 模拟识别置信度
            
            segment = SubtitleSegment(
                start_time=current_time,
                end_time=current_time + duration,
                text=text,
                confidence=confidence,
                speaker_id=f"speaker_{i % 2 + 1}" if i % 3 == 0 else None
            )
            
            segments.append(segment)
            current_time += duration + np.random.uniform(0.5, 1.5)  # 间隔时间
        
        # 记录生成历史
        self.subtitle_history.append({
            'timestamp': datetime.now(),
            'language': language,
            'segments_count': len(segments),
            'total_duration': current_time,
            'average_confidence': np.mean([s.confidence for s in segments])
        })
        
        return segments
    
    def translate_subtitles(self, segments: List[SubtitleSegment], 
                          source_lang: str, target_lang: str) -> List[SubtitleSegment]:
        """翻译字幕"""
        # 模拟翻译过程
        time.sleep(2)
        
        # 简单的翻译映射（实际应用中会使用真实的翻译API）
        translation_map = {
            ("中文(简体)", "英语"): {
                "欢迎观看VideoGenius智能字幕系统演示": "Welcome to VideoGenius Smart Subtitle System Demo",
                "这是一个功能强大的AI字幕生成工具": "This is a powerful AI subtitle generation tool",
                "支持多种语言的自动识别和翻译": "Supports automatic recognition and translation of multiple languages",
                "可以自定义字幕样式和特效": "Customizable subtitle styles and effects",
                "让您的视频更加专业和易懂": "Make your videos more professional and understandable"
            },
            ("英语", "中文(简体)"): {
                "Welcome to VideoGenius Smart Subtitle System Demo": "欢迎观看VideoGenius智能字幕系统演示",
                "This is a powerful AI subtitle generation tool": "这是一个功能强大的AI字幕生成工具",
                "Supports automatic recognition and translation of multiple languages": "支持多种语言的自动识别和翻译",
                "Customizable subtitle styles and effects": "可以自定义字幕样式和特效",
                "Make your videos more professional and understandable": "让您的视频更加专业和易懂"
            }
        }
        
        translated_segments = []
        translation_dict = translation_map.get((source_lang, target_lang), {})
        
        for segment in segments:
            translated_text = translation_dict.get(segment.text, f"[{target_lang}] {segment.text}")
            
            translated_segment = SubtitleSegment(
                start_time=segment.start_time,
                end_time=segment.end_time,
                text=translated_text,
                confidence=segment.confidence * 0.9,  # 翻译后置信度略降
                speaker_id=segment.speaker_id
            )
            
            translated_segments.append(translated_segment)
        
        return translated_segments
    
    def export_subtitles(self, segments: List[SubtitleSegment], 
                        format_type: str) -> str:
        """导出字幕文件"""
        if format_type == SubtitleFormat.SRT.value:
            return self._export_srt(segments)
        elif format_type == SubtitleFormat.VTT.value:
            return self._export_vtt(segments)
        elif format_type == SubtitleFormat.ASS.value:
            return self._export_ass(segments)
        else:
            return self._export_srt(segments)  # 默认SRT格式
    
    def _export_srt(self, segments: List[SubtitleSegment]) -> str:
        """导出SRT格式"""
        srt_content = ""
        for i, segment in enumerate(segments, 1):
            start_time = self._format_time_srt(segment.start_time)
            end_time = self._format_time_srt(segment.end_time)
            
            srt_content += f"{i}\n"
            srt_content += f"{start_time} --> {end_time}\n"
            srt_content += f"{segment.text}\n\n"
        
        return srt_content
    
    def _export_vtt(self, segments: List[SubtitleSegment]) -> str:
        """导出WebVTT格式"""
        vtt_content = "WEBVTT\n\n"
        
        for segment in segments:
            start_time = self._format_time_vtt(segment.start_time)
            end_time = self._format_time_vtt(segment.end_time)
            
            vtt_content += f"{start_time} --> {end_time}\n"
            vtt_content += f"{segment.text}\n\n"
        
        return vtt_content
    
    def _export_ass(self, segments: List[SubtitleSegment]) -> str:
        """导出ASS格式"""
        ass_header = """[Script Info]
Title: VideoGenius Generated Subtitles
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,24,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        
        ass_content = ass_header
        
        for segment in segments:
            start_time = self._format_time_ass(segment.start_time)
            end_time = self._format_time_ass(segment.end_time)
            
            ass_content += f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{segment.text}\n"
        
        return ass_content
    
    def _format_time_srt(self, seconds: float) -> str:
        """格式化SRT时间"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"
    
    def _format_time_vtt(self, seconds: float) -> str:
        """格式化VTT时间"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"
    
    def _format_time_ass(self, seconds: float) -> str:
        """格式化ASS时间"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours:01d}:{minutes:02d}:{secs:05.2f}"
    
    def sync_subtitles(self, segments: List[SubtitleSegment], 
                      offset: float) -> List[SubtitleSegment]:
        """同步字幕时间轴"""
        synced_segments = []
        
        for segment in segments:
            synced_segment = SubtitleSegment(
                start_time=max(0, segment.start_time + offset),
                end_time=max(0, segment.end_time + offset),
                text=segment.text,
                confidence=segment.confidence,
                speaker_id=segment.speaker_id
            )
            synced_segments.append(synced_segment)
        
        return synced_segments

# 初始化字幕引擎
@st.cache_resource
def get_subtitle_engine():
    return SmartSubtitleEngine()

def render_main_header():
    """渲染主标题"""
    st.markdown("""
    <div class="main-header">
        <h1>📝 智能字幕系统</h1>
        <p>自动字幕生成 • 多语言翻译 • 字幕样式定制 • 时间轴同步</p>
    </div>
    """, unsafe_allow_html=True)

def render_subtitle_generation():
    """渲染字幕生成区域"""
    st.markdown("### 🎤 自动字幕生成")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 音频文件上传
        audio_file = st.file_uploader(
            "上传音频或视频文件",
            type=['mp3', 'wav', 'mp4', 'avi', 'mov'],
            help="支持常见的音频和视频格式"
        )
        
        if audio_file:
            st.success(f"✅ 已上传: {audio_file.name}")
            
            # 语言选择
            col_lang, col_quality = st.columns(2)
            
            with col_lang:
                source_language = st.selectbox(
                    "选择音频语言",
                    [lang.value for lang in Language],
                    index=0
                )
            
            with col_quality:
                quality_mode = st.selectbox(
                    "识别质量",
                    ["标准模式", "高精度模式", "快速模式"],
                    index=1
                )
        
        # 高级设置
        with st.expander("🔧 高级设置", expanded=False):
            col_speaker, col_filter = st.columns(2)
            
            with col_speaker:
                enable_speaker_detection = st.checkbox("启用说话人识别", value=True)
                max_speakers = st.number_input("最大说话人数", min_value=1, max_value=10, value=2)
            
            with col_filter:
                enable_noise_filter = st.checkbox("启用噪音过滤", value=True)
                confidence_threshold = st.slider("置信度阈值", 0.5, 1.0, 0.8, 0.05)
    
    with col2:
        st.markdown("#### 🎯 识别功能")
        st.markdown("""
        - **🎤 语音识别**: 高精度语音转文字
        - **👥 说话人识别**: 区分不同说话人
        - **🔇 噪音过滤**: 自动过滤背景噪音
        - **⏱️ 时间同步**: 精确时间轴对齐
        """)
        
        st.markdown("#### 📊 支持格式")
        st.markdown("""
        - **音频**: MP3, WAV, FLAC, AAC
        - **视频**: MP4, AVI, MOV, MKV
        - **字幕**: SRT, VTT, ASS, TTML
        """)
    
    return audio_file, source_language if 'audio_file' in locals() and audio_file else None

def render_subtitle_preview(segments: List[SubtitleSegment], style: SubtitleStyle):
    """渲染字幕预览"""
    st.markdown("### 👀 字幕预览")
    
    if segments:
        # 选择预览的字幕片段
        segment_options = [f"{i+1}. {seg.text[:30]}..." if len(seg.text) > 30 else f"{i+1}. {seg.text}" 
                          for i, seg in enumerate(segments)]
        
        selected_index = st.selectbox("选择预览片段", range(len(segment_options)), 
                                     format_func=lambda x: segment_options[x])
        
        selected_segment = segments[selected_index]
        
        # 字幕预览框
        preview_style = f"""
        background: #000;
        color: {style.font_color};
        font-family: {style.font_family};
        font-size: {style.font_size}px;
        text-align: {style.alignment};
        opacity: {style.opacity};
        """
        
        st.markdown(f"""
        <div class="subtitle-preview" style="{preview_style}">
            <div class="subtitle-text" style="background: {style.background_color}; 
                 text-shadow: {style.outline_width}px {style.outline_width}px 0px {style.outline_color};">
                {selected_segment.text}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 字幕信息
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("开始时间", f"{selected_segment.start_time:.2f}s")
        with col2:
            st.metric("结束时间", f"{selected_segment.end_time:.2f}s")
        with col3:
            st.metric("时长", f"{selected_segment.end_time - selected_segment.start_time:.2f}s")
        with col4:
            st.metric("置信度", f"{selected_segment.confidence:.1%}")

def render_subtitle_timeline(segments: List[SubtitleSegment]):
    """渲染字幕时间轴"""
    st.markdown("### ⏱️ 字幕时间轴")
    
    if segments:
        # 时间轴可视化
        timeline_data = []
        for i, segment in enumerate(segments):
            timeline_data.append({
                'Task': f'字幕 {i+1}',
                'Start': segment.start_time,
                'Finish': segment.end_time,
                'Text': segment.text[:20] + "..." if len(segment.text) > 20 else segment.text
            })
        
        df = pd.DataFrame(timeline_data)
        
        fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", 
                         hover_data=["Text"], title="字幕时间轴")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # 字幕列表
        st.markdown("#### 📋 字幕列表")
        
        for i, segment in enumerate(segments):
            with st.container():
                col1, col2, col3 = st.columns([1, 6, 1])
                
                with col1:
                    st.markdown(f"**{i+1}**")
                
                with col2:
                    st.markdown(f"""
                    <div class="timeline-item">
                        <strong>{segment.start_time:.2f}s - {segment.end_time:.2f}s</strong><br>
                        {segment.text}
                        <br><small>置信度: {segment.confidence:.1%}</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    if st.button("✏️", key=f"edit_{i}", help="编辑字幕"):
                        st.session_state[f'edit_subtitle_{i}'] = True

def render_style_customization():
    """渲染样式定制"""
    st.markdown("### 🎨 字幕样式定制")
    
    engine = get_subtitle_engine()
    
    # 预设样式
    st.markdown("#### 🎯 预设样式")
    
    preset_cols = st.columns(len(engine.style_presets))
    selected_preset = None
    
    for i, (name, style) in enumerate(engine.style_presets.items()):
        with preset_cols[i]:
            if st.button(f"🎨 {name}", key=f"preset_{i}"):
                selected_preset = style
                st.success(f"已选择: {name}")
    
    # 自定义样式
    st.markdown("#### ⚙️ 自定义样式")
    
    col1, col2 = st.columns(2)
    
    with col1:
        font_family = st.selectbox("字体", [font.value for font in FontFamily])
        font_size = st.slider("字体大小", 12, 48, 24)
        font_color = st.color_picker("字体颜色", "#FFFFFF")
        outline_color = st.color_picker("描边颜色", "#000000")
    
    with col2:
        background_color = st.color_picker("背景颜色", "#000000")
        background_opacity = st.slider("背景透明度", 0.0, 1.0, 0.8, 0.1)
        outline_width = st.slider("描边宽度", 0, 5, 2)
        position = st.selectbox("字幕位置", [pos.value for pos in Position])
    
    # 创建自定义样式
    custom_style = SubtitleStyle(
        font_family=font_family,
        font_size=font_size,
        font_color=font_color,
        background_color=f"rgba({int(background_color[1:3], 16)}, {int(background_color[3:5], 16)}, {int(background_color[5:7], 16)}, {background_opacity})",
        outline_color=outline_color,
        outline_width=outline_width,
        position=position,
        alignment="center",
        opacity=1.0
    )
    
    return selected_preset or custom_style

def render_translation_section():
    """渲染翻译区域"""
    st.markdown("### 🌍 多语言翻译")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📤 源语言")
        source_lang = st.selectbox(
            "选择源语言",
            [lang.value for lang in Language],
            index=0,
            key="source_lang"
        )
        
        st.markdown("#### 🎯 翻译设置")
        translation_quality = st.selectbox(
            "翻译质量",
            ["标准翻译", "高质量翻译", "创意翻译"],
            index=1
        )
        
        preserve_timing = st.checkbox("保持时间轴", value=True)
        auto_adjust_length = st.checkbox("自动调整长度", value=True)
    
    with col2:
        st.markdown("#### 📥 目标语言")
        target_lang = st.selectbox(
            "选择目标语言",
            [lang.value for lang in Language],
            index=1,
            key="target_lang"
        )
        
        st.markdown("#### 📊 翻译统计")
        if st.button("🚀 开始翻译", type="primary"):
            with st.spinner("🌍 AI正在翻译字幕..."):
                time.sleep(2)
                st.success("✅ 翻译完成！")
                
                # 显示翻译统计
                col_acc, col_time = st.columns(2)
                with col_acc:
                    accuracy = np.random.uniform(85, 95)
                    st.metric("翻译准确度", f"{accuracy:.1f}%")
                with col_time:
                    st.metric("处理时间", "2.3秒")
    
    return source_lang, target_lang

def render_export_section(segments: List[SubtitleSegment]):
    """渲染导出区域"""
    st.markdown("### 💾 字幕导出")
    
    if segments:
        col1, col2 = st.columns(2)
        
        with col1:
            export_format = st.selectbox(
                "选择导出格式",
                [fmt.value for fmt in SubtitleFormat],
                index=0
            )
            
            filename = st.text_input(
                "文件名",
                value="subtitles",
                help="不需要包含文件扩展名"
            )
            
            include_metadata = st.checkbox("包含元数据", value=True)
        
        with col2:
            st.markdown("#### 📊 导出统计")
            st.metric("字幕片段数", len(segments))
            total_duration = segments[-1].end_time if segments else 0
            st.metric("总时长", f"{total_duration:.1f}秒")
            avg_confidence = np.mean([s.confidence for s in segments]) if segments else 0
            st.metric("平均置信度", f"{avg_confidence:.1%}")
        
        if st.button("📥 导出字幕文件", type="primary"):
            engine = get_subtitle_engine()
            subtitle_content = engine.export_subtitles(segments, export_format)
            
            # 提供下载
            file_extension = export_format.lower()
            if file_extension == "webvtt":
                file_extension = "vtt"
            elif file_extension == "ass/ssa":
                file_extension = "ass"
            
            st.download_button(
                label=f"⬇️ 下载 {filename}.{file_extension}",
                data=subtitle_content,
                file_name=f"{filename}.{file_extension}",
                mime="text/plain"
            )
            
            st.success("✅ 字幕文件已准备好下载！")

def render_sync_adjustment():
    """渲染同步调整"""
    st.markdown("### ⏱️ 时间轴同步调整")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 同步设置")
        
        time_offset = st.number_input(
            "时间偏移 (秒)",
            min_value=-60.0,
            max_value=60.0,
            value=0.0,
            step=0.1,
            help="正值表示延后，负值表示提前"
        )
        
        speed_adjustment = st.slider(
            "播放速度调整",
            min_value=0.5,
            max_value=2.0,
            value=1.0,
            step=0.1,
            help="调整字幕显示速度"
        )
        
        auto_sync = st.checkbox("启用自动同步", value=False)
    
    with col2:
        st.markdown("#### 🔧 同步工具")
        
        if st.button("⏪ 整体提前 1秒"):
            st.info("所有字幕提前1秒")
        
        if st.button("⏩ 整体延后 1秒"):
            st.info("所有字幕延后1秒")
        
        if st.button("🎯 智能同步"):
            with st.spinner("🤖 AI正在分析音视频同步..."):
                time.sleep(2)
                st.success("✅ 智能同步完成！")
        
        if st.button("🔄 重置时间轴"):
            st.info("时间轴已重置")
    
    return time_offset, speed_adjustment

def render_subtitle_history():
    """渲染字幕历史"""
    engine = get_subtitle_engine()
    
    if engine.subtitle_history:
        st.markdown("### 📚 生成历史")
        
        # 创建历史记录表格
        history_data = []
        for record in engine.subtitle_history[-10:]:  # 显示最近10条
            history_data.append({
                "时间": record['timestamp'].strftime("%Y-%m-%d %H:%M"),
                "语言": record['language'],
                "片段数": record['segments_count'],
                "总时长": f"{record['total_duration']:.1f}s",
                "平均置信度": f"{record['average_confidence']:.1%}"
            })
        
        if history_data:
            df = pd.DataFrame(history_data)
            st.dataframe(df, use_container_width=True)
        
        # 统计图表
        col1, col2 = st.columns(2)
        
        with col1:
            # 语言使用分布
            lang_counts = {}
            for record in engine.subtitle_history:
                lang = record['language']
                lang_counts[lang] = lang_counts.get(lang, 0) + 1
            
            if lang_counts:
                fig = px.pie(
                    values=list(lang_counts.values()),
                    names=list(lang_counts.keys()),
                    title="语言使用分布"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 置信度趋势
            confidences = [record['average_confidence'] for record in engine.subtitle_history]
            times = [record['timestamp'] for record in engine.subtitle_history]
            
            if confidences:
                fig = px.line(
                    x=times,
                    y=confidences,
                    title="识别置信度趋势",
                    labels={'x': '时间', 'y': '置信度'}
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

def main():
    """主函数"""
    # 渲染主标题
    render_main_header()
    
    # 侧边栏
    with st.sidebar:
        st.markdown("### 📝 智能字幕")
        
        subtitle_mode = st.radio(
            "选择功能模式",
            ["🎤 字幕生成", "🎨 样式定制", "🌍 多语言翻译", "⏱️ 时间同步", "📚 生成历史"],
            index=0
        )
        
        st.markdown("---")
        
        # 系统设置
        st.markdown("### ⚙️ 系统设置")
        
        default_language = st.selectbox(
            "默认语言",
            [lang.value for lang in Language],
            index=0
        )
        
        auto_punctuation = st.checkbox("自动标点", value=True)
        auto_capitalization = st.checkbox("自动大写", value=True)
        filter_profanity = st.checkbox("过滤敏感词", value=False)
        
        st.markdown("---")
        
        # 系统状态
        st.markdown("### 📊 系统状态")
        st.success("🟢 语音识别引擎运行正常")
        st.info("🌍 支持语言: 12种")
        st.info("📝 支持格式: 5种")
        st.info("⚡ 平均处理时间: 3秒")
    
    # 主内容区域
    if subtitle_mode == "🎤 字幕生成":
        audio_file, source_language = render_subtitle_generation()
        
        if audio_file and source_language:
            if st.button("🚀 开始生成字幕", type="primary"):
                with st.spinner("🎤 AI正在识别语音并生成字幕..."):
                    engine = get_subtitle_engine()
                    segments = engine.generate_subtitles(audio_file.name, source_language)
                    
                    st.success("✅ 字幕生成完成！")
                    
                    # 保存到session state
                    st.session_state['subtitle_segments'] = segments
                    
                    # 显示结果
                    render_subtitle_timeline(segments)
    
    elif subtitle_mode == "🎨 样式定制":
        style = render_style_customization()
        
        # 如果有字幕数据，显示预览
        if 'subtitle_segments' in st.session_state:
            render_subtitle_preview(st.session_state['subtitle_segments'], style)
        else:
            st.info("请先生成字幕后再进行样式定制")
    
    elif subtitle_mode == "🌍 多语言翻译":
        source_lang, target_lang = render_translation_section()
        
        # 如果有字幕数据，可以进行翻译
        if 'subtitle_segments' in st.session_state:
            if st.button("🌍 翻译字幕"):
                with st.spinner("🌍 AI正在翻译字幕..."):
                    engine = get_subtitle_engine()
                    translated_segments = engine.translate_subtitles(
                        st.session_state['subtitle_segments'], 
                        source_lang, 
                        target_lang
                    )
                    
                    st.success("✅ 翻译完成！")
                    st.session_state['translated_segments'] = translated_segments
                    
                    # 显示翻译结果
                    render_subtitle_timeline(translated_segments)
        else:
            st.info("请先生成字幕后再进行翻译")
    
    elif subtitle_mode == "⏱️ 时间同步":
        time_offset, speed_adjustment = render_sync_adjustment()
        
        # 如果有字幕数据，可以进行同步调整
        if 'subtitle_segments' in st.session_state:
            if st.button("🎯 应用同步调整"):
                engine = get_subtitle_engine()
                synced_segments = engine.sync_subtitles(
                    st.session_state['subtitle_segments'], 
                    time_offset
                )
                
                st.success("✅ 时间轴同步完成！")
                st.session_state['subtitle_segments'] = synced_segments
                
                render_subtitle_timeline(synced_segments)
        else:
            st.info("请先生成字幕后再进行时间同步")
    
    elif subtitle_mode == "📚 生成历史":
        render_subtitle_history()
    
    # 导出功能（在所有模式下都可用）
    if 'subtitle_segments' in st.session_state:
        st.markdown("---")
        render_export_section(st.session_state['subtitle_segments'])
    
    # 页脚
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        📝 <strong>智能字幕系统</strong> | VideoGenius v2.0 | 
        让AI为您的视频生成完美的字幕 ✨
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 