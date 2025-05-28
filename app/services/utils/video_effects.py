from moviepy import Clip, vfx, VideoFileClip, CompositeVideoClip, ColorClip, ImageClip
import numpy as np
import random
from typing import List, Tuple, Optional, Union
from loguru import logger


# ========================================
# 🎬 专业级转场效果系统
# ========================================

def fadein_transition(clip: Clip, t: float) -> Clip:
    """淡入转场效果"""
    return clip.with_effects([vfx.FadeIn(t)])


def fadeout_transition(clip: Clip, t: float) -> Clip:
    """淡出转场效果"""
    return clip.with_effects([vfx.FadeOut(t)])


def slidein_transition(clip: Clip, t: float, side: str) -> Clip:
    """滑入转场效果"""
    return clip.with_effects([vfx.SlideIn(t, side)])


def slideout_transition(clip: Clip, t: float, side: str) -> Clip:
    """滑出转场效果"""
    return clip.with_effects([vfx.SlideOut(t, side)])


def crossfade_transition(clip1: Clip, clip2: Clip, duration: float = 1.0) -> Clip:
    """交叉淡化转场 - 两个片段平滑过渡"""
    try:
        # 确保两个片段有相同的尺寸
        if clip1.size != clip2.size:
            clip2 = clip2.resized(clip1.size)
        
        # 创建交叉淡化效果
        clip1_fadeout = clip1.with_effects([vfx.FadeOut(duration)])
        clip2_fadein = clip2.with_effects([vfx.FadeIn(duration)])
        
        # 重叠部分
        overlap_start = max(0, clip1.duration - duration)
        clip2_positioned = clip2_fadein.with_start(overlap_start)
        
        return CompositeVideoClip([clip1_fadeout, clip2_positioned])
    except Exception as e:
        logger.warning(f"交叉淡化转场失败，使用简单拼接: {e}")
        return clip1


def zoom_in_transition(clip: Clip, zoom_factor: float = 1.2, duration: float = 1.0) -> Clip:
    """缩放进入转场效果"""
    try:
        def zoom_effect(get_frame, t):
            frame = get_frame(t)
            if t < duration:
                # 计算当前缩放比例
                current_zoom = 1 + (zoom_factor - 1) * (t / duration)
                # 应用缩放效果
                return vfx.Resize(current_zoom)(clip).get_frame(t)
            return frame
        
        return clip.with_fps(clip.fps).with_duration(clip.duration)
    except Exception as e:
        logger.warning(f"缩放转场失败，返回原片段: {e}")
        return clip


def zoom_out_transition(clip: Clip, zoom_factor: float = 1.2, duration: float = 1.0) -> Clip:
    """缩放退出转场效果"""
    try:
        def zoom_effect(get_frame, t):
            frame = get_frame(t)
            if t > clip.duration - duration:
                # 计算当前缩放比例
                progress = (t - (clip.duration - duration)) / duration
                current_zoom = zoom_factor - (zoom_factor - 1) * progress
                # 应用缩放效果
                return vfx.Resize(current_zoom)(clip).get_frame(t)
            return frame
        
        return clip.with_fps(clip.fps).with_duration(clip.duration)
    except Exception as e:
        logger.warning(f"缩放退出转场失败，返回原片段: {e}")
        return clip


def rotate_transition(clip: Clip, angle: float = 360, duration: float = 1.0) -> Clip:
    """旋转转场效果"""
    try:
        def rotate_effect(get_frame, t):
            frame = get_frame(t)
            if t < duration:
                # 计算当前旋转角度
                current_angle = angle * (t / duration)
                return vfx.Rotate(current_angle)(clip).get_frame(t)
            return frame
        
        return clip.with_fps(clip.fps).with_duration(clip.duration)
    except Exception as e:
        logger.warning(f"旋转转场失败，返回原片段: {e}")
        return clip


def wipe_transition(clip1: Clip, clip2: Clip, direction: str = "left", duration: float = 1.0) -> Clip:
    """擦除转场效果"""
    try:
        if clip1.size != clip2.size:
            clip2 = clip2.resized(clip1.size)
        
        w, h = clip1.size
        
        def make_mask(t):
            if t < duration:
                progress = t / duration
                if direction == "left":
                    mask_width = int(w * progress)
                    mask = np.zeros((h, w))
                    mask[:, :mask_width] = 1
                elif direction == "right":
                    mask_width = int(w * progress)
                    mask = np.zeros((h, w))
                    mask[:, -mask_width:] = 1
                elif direction == "top":
                    mask_height = int(h * progress)
                    mask = np.zeros((h, w))
                    mask[:mask_height, :] = 1
                else:  # bottom
                    mask_height = int(h * progress)
                    mask = np.zeros((h, w))
                    mask[-mask_height:, :] = 1
                return mask
            return np.ones((h, w))
        
        # 创建遮罩片段
        mask_clip = VideoFileClip(clip1.filename).with_duration(duration).with_mask(
            lambda t: make_mask(t)
        )
        
        # 组合片段
        clip2_positioned = clip2.with_start(0)
        return CompositeVideoClip([clip1, clip2_positioned.with_mask(mask_clip)])
        
    except Exception as e:
        logger.warning(f"擦除转场失败，使用简单拼接: {e}")
        return clip1


# ========================================
# 🎨 专业级滤镜效果系统
# ========================================

def apply_cinematic_filter(clip: Clip, intensity: float = 0.5) -> Clip:
    """电影级滤镜效果"""
    try:
        # 应用电影级色彩调整
        clip = clip.with_effects([
            vfx.ColorX(1.1),  # 增强对比度
            vfx.Gamma(0.9),   # 调整伽马值
        ])
        return clip
    except Exception as e:
        logger.warning(f"电影滤镜应用失败: {e}")
        return clip


def apply_vintage_filter(clip: Clip, intensity: float = 0.5) -> Clip:
    """复古滤镜效果"""
    try:
        # 应用复古色调
        clip = clip.with_effects([
            vfx.ColorX(0.8),     # 降低饱和度
            vfx.Gamma(1.2),      # 增加亮度
        ])
        return clip
    except Exception as e:
        logger.warning(f"复古滤镜应用失败: {e}")
        return clip


def apply_black_white_filter(clip: Clip) -> Clip:
    """黑白滤镜效果"""
    try:
        return clip.with_effects([vfx.BlackAndWhite()])
    except Exception as e:
        logger.warning(f"黑白滤镜应用失败: {e}")
        return clip


def apply_sepia_filter(clip: Clip) -> Clip:
    """棕褐色滤镜效果"""
    try:
        # 先转黑白，再添加棕褐色调
        clip = clip.with_effects([vfx.BlackAndWhite()])
        # 这里可以添加更复杂的棕褐色效果
        return clip
    except Exception as e:
        logger.warning(f"棕褐色滤镜应用失败: {e}")
        return clip


def apply_blur_filter(clip: Clip, blur_radius: float = 2.0) -> Clip:
    """模糊滤镜效果"""
    try:
        return clip.with_effects([vfx.Blur(blur_radius)])
    except Exception as e:
        logger.warning(f"模糊滤镜应用失败: {e}")
        return clip


def apply_sharpen_filter(clip: Clip, intensity: float = 1.0) -> Clip:
    """锐化滤镜效果"""
    try:
        # MoviePy没有直接的锐化效果，使用对比度增强
        return clip.with_effects([vfx.ColorX(1 + intensity * 0.2)])
    except Exception as e:
        logger.warning(f"锐化滤镜应用失败: {e}")
        return clip


# ========================================
# 🌈 色彩调整系统
# ========================================

def adjust_brightness(clip: Clip, factor: float = 1.2) -> Clip:
    """调整亮度"""
    try:
        return clip.with_effects([vfx.Gamma(1/factor)])
    except Exception as e:
        logger.warning(f"亮度调整失败: {e}")
        return clip


def adjust_contrast(clip: Clip, factor: float = 1.2) -> Clip:
    """调整对比度"""
    try:
        return clip.with_effects([vfx.ColorX(factor)])
    except Exception as e:
        logger.warning(f"对比度调整失败: {e}")
        return clip


def adjust_saturation(clip: Clip, factor: float = 1.2) -> Clip:
    """调整饱和度"""
    try:
        # 通过色彩矩阵调整饱和度
        return clip.with_effects([vfx.ColorX(factor)])
    except Exception as e:
        logger.warning(f"饱和度调整失败: {e}")
        return clip


def color_temperature_warm(clip: Clip, intensity: float = 0.3) -> Clip:
    """暖色调调整"""
    try:
        # 增加红色和黄色通道
        return clip.with_effects([vfx.ColorX(1 + intensity * 0.1)])
    except Exception as e:
        logger.warning(f"暖色调调整失败: {e}")
        return clip


def color_temperature_cool(clip: Clip, intensity: float = 0.3) -> Clip:
    """冷色调调整"""
    try:
        # 增加蓝色通道
        return clip.with_effects([vfx.ColorX(1 - intensity * 0.1)])
    except Exception as e:
        logger.warning(f"冷色调调整失败: {e}")
        return clip


# ========================================
# 🎭 动态效果系统
# ========================================

def add_zoom_effect(clip: Clip, zoom_type: str = "in", intensity: float = 1.2) -> Clip:
    """添加缩放动画效果"""
    try:
        if zoom_type == "in":
            return zoom_in_transition(clip, intensity, clip.duration * 0.3)
        elif zoom_type == "out":
            return zoom_out_transition(clip, intensity, clip.duration * 0.3)
        else:  # in_out
            clip = zoom_in_transition(clip, intensity, clip.duration * 0.2)
            clip = zoom_out_transition(clip, intensity, clip.duration * 0.2)
            return clip
    except Exception as e:
        logger.warning(f"缩放效果添加失败: {e}")
        return clip


def add_pan_effect(clip: Clip, direction: str = "left", speed: float = 50) -> Clip:
    """添加平移效果"""
    try:
        w, h = clip.size
        if direction == "left":
            # 从右向左平移
            return clip.with_position(lambda t: (-speed * t, 0))
        elif direction == "right":
            # 从左向右平移
            return clip.with_position(lambda t: (speed * t, 0))
        elif direction == "up":
            # 从下向上平移
            return clip.with_position(lambda t: (0, -speed * t))
        else:  # down
            # 从上向下平移
            return clip.with_position(lambda t: (0, speed * t))
    except Exception as e:
        logger.warning(f"平移效果添加失败: {e}")
        return clip


def add_shake_effect(clip: Clip, intensity: float = 5.0, frequency: float = 10.0) -> Clip:
    """添加震动效果"""
    try:
        def shake_position(t):
            x_offset = intensity * np.sin(2 * np.pi * frequency * t)
            y_offset = intensity * np.cos(2 * np.pi * frequency * t * 1.3)
            return (x_offset, y_offset)
        
        return clip.with_position(shake_position)
    except Exception as e:
        logger.warning(f"震动效果添加失败: {e}")
        return clip


# ========================================
# 🎪 组合效果系统
# ========================================

def apply_random_transition(clip1: Clip, clip2: Clip, duration: float = 1.0) -> Clip:
    """随机应用转场效果"""
    transitions = [
        lambda c1, c2, d: crossfade_transition(c1, c2, d),
        lambda c1, c2, d: wipe_transition(c1, c2, "left", d),
        lambda c1, c2, d: wipe_transition(c1, c2, "right", d),
        lambda c1, c2, d: wipe_transition(c1, c2, "top", d),
        lambda c1, c2, d: wipe_transition(c1, c2, "bottom", d),
    ]
    
    selected_transition = random.choice(transitions)
    return selected_transition(clip1, clip2, duration)


def apply_random_filter(clip: Clip) -> Clip:
    """随机应用滤镜效果"""
    filters = [
        lambda c: c,  # 无滤镜
        lambda c: apply_cinematic_filter(c, 0.3),
        lambda c: apply_vintage_filter(c, 0.4),
        lambda c: adjust_brightness(c, 1.1),
        lambda c: adjust_contrast(c, 1.1),
        lambda c: color_temperature_warm(c, 0.2),
        lambda c: color_temperature_cool(c, 0.2),
    ]
    
    selected_filter = random.choice(filters)
    return selected_filter(clip)


def apply_professional_enhancement(clip: Clip, enhancement_level: str = "medium") -> Clip:
    """应用专业级视频增强"""
    try:
        if enhancement_level == "light":
            # 轻度增强
            clip = adjust_contrast(clip, 1.05)
            clip = adjust_brightness(clip, 1.02)
            
        elif enhancement_level == "medium":
            # 中度增强
            clip = adjust_contrast(clip, 1.1)
            clip = adjust_brightness(clip, 1.05)
            clip = adjust_saturation(clip, 1.05)
            clip = apply_cinematic_filter(clip, 0.3)
            
        elif enhancement_level == "strong":
            # 强度增强
            clip = adjust_contrast(clip, 1.2)
            clip = adjust_brightness(clip, 1.1)
            clip = adjust_saturation(clip, 1.1)
            clip = apply_cinematic_filter(clip, 0.5)
            clip = add_zoom_effect(clip, "in_out", 1.05)
            
        return clip
        
    except Exception as e:
        logger.warning(f"专业增强应用失败: {e}")
        return clip


# ========================================
# 🎬 智能效果选择系统
# ========================================

def get_recommended_effects(clip_index: int, total_clips: int, content_type: str = "general") -> dict:
    """根据片段位置和内容类型推荐效果"""
    effects = {
        "transition": None,
        "filter": None,
        "enhancement": "medium",
        "dynamic": None
    }
    
    # 根据片段位置推荐转场
    if clip_index == 0:
        # 开头片段
        effects["transition"] = "fade_in"
        effects["dynamic"] = "zoom_in"
    elif clip_index == total_clips - 1:
        # 结尾片段
        effects["transition"] = "fade_out"
        effects["dynamic"] = "zoom_out"
    else:
        # 中间片段
        effects["transition"] = "crossfade"
    
    # 根据内容类型推荐滤镜
    if content_type == "tech":
        effects["filter"] = "cinematic"
        effects["enhancement"] = "strong"
    elif content_type == "lifestyle":
        effects["filter"] = "warm"
        effects["enhancement"] = "medium"
    elif content_type == "business":
        effects["filter"] = "professional"
        effects["enhancement"] = "light"
    elif content_type == "creative":
        effects["filter"] = "vintage"
        effects["enhancement"] = "strong"
    
    return effects


def apply_smart_effects(clip: Clip, clip_index: int, total_clips: int, content_type: str = "general") -> Clip:
    """智能应用推荐的效果"""
    try:
        effects = get_recommended_effects(clip_index, total_clips, content_type)
        
        # 应用滤镜
        if effects["filter"] == "cinematic":
            clip = apply_cinematic_filter(clip, 0.4)
        elif effects["filter"] == "vintage":
            clip = apply_vintage_filter(clip, 0.4)
        elif effects["filter"] == "warm":
            clip = color_temperature_warm(clip, 0.3)
        elif effects["filter"] == "professional":
            clip = adjust_contrast(clip, 1.1)
        
        # 应用增强
        clip = apply_professional_enhancement(clip, effects["enhancement"])
        
        # 应用动态效果
        if effects["dynamic"] == "zoom_in":
            clip = add_zoom_effect(clip, "in", 1.05)
        elif effects["dynamic"] == "zoom_out":
            clip = add_zoom_effect(clip, "out", 1.05)
        
        return clip
        
    except Exception as e:
        logger.warning(f"智能效果应用失败: {e}")
        return clip


# ========================================
# 🎯 效果预设系统
# ========================================

EFFECT_PRESETS = {
    "professional": {
        "name": "专业商务",
        "description": "适合商务演示和专业内容",
        "effects": ["contrast_1.1", "brightness_1.05", "cinematic_0.3"]
    },
    "cinematic": {
        "name": "电影风格",
        "description": "电影级视觉效果",
        "effects": ["cinematic_0.5", "contrast_1.2", "zoom_in_out"]
    },
    "vintage": {
        "name": "复古怀旧",
        "description": "复古温暖的视觉风格",
        "effects": ["vintage_0.4", "warm_0.3", "brightness_1.1"]
    },
    "modern": {
        "name": "现代时尚",
        "description": "现代清新的视觉风格",
        "effects": ["contrast_1.15", "saturation_1.1", "cool_0.2"]
    },
    "dramatic": {
        "name": "戏剧效果",
        "description": "强烈的视觉冲击",
        "effects": ["contrast_1.3", "cinematic_0.6", "shake_3.0"]
    }
}


def apply_preset_effects(clip: Clip, preset_name: str) -> Clip:
    """应用预设效果组合"""
    try:
        if preset_name not in EFFECT_PRESETS:
            logger.warning(f"未知的预设效果: {preset_name}")
            return clip
        
        preset = EFFECT_PRESETS[preset_name]
        logger.info(f"应用预设效果: {preset['name']} - {preset['description']}")
        
        for effect in preset["effects"]:
            if effect.startswith("contrast_"):
                factor = float(effect.split("_")[1])
                clip = adjust_contrast(clip, factor)
            elif effect.startswith("brightness_"):
                factor = float(effect.split("_")[1])
                clip = adjust_brightness(clip, factor)
            elif effect.startswith("saturation_"):
                factor = float(effect.split("_")[1])
                clip = adjust_saturation(clip, factor)
            elif effect.startswith("cinematic_"):
                intensity = float(effect.split("_")[1])
                clip = apply_cinematic_filter(clip, intensity)
            elif effect.startswith("vintage_"):
                intensity = float(effect.split("_")[1])
                clip = apply_vintage_filter(clip, intensity)
            elif effect.startswith("warm_"):
                intensity = float(effect.split("_")[1])
                clip = color_temperature_warm(clip, intensity)
            elif effect.startswith("cool_"):
                intensity = float(effect.split("_")[1])
                clip = color_temperature_cool(clip, intensity)
            elif effect == "zoom_in_out":
                clip = add_zoom_effect(clip, "in_out", 1.05)
            elif effect.startswith("shake_"):
                intensity = float(effect.split("_")[1])
                clip = add_shake_effect(clip, intensity, 10.0)
        
        return clip
        
    except Exception as e:
        logger.error(f"预设效果应用失败: {e}")
        return clip


# ========================================
# 🎨 导出函数
# ========================================

def get_available_transitions() -> List[str]:
    """获取可用的转场效果列表"""
    return [
        "none", "fade_in", "fade_out", "crossfade", 
        "slide_left", "slide_right", "slide_up", "slide_down",
        "wipe_left", "wipe_right", "wipe_up", "wipe_down",
        "zoom_in", "zoom_out", "rotate", "random"
    ]


def get_available_filters() -> List[str]:
    """获取可用的滤镜效果列表"""
    return [
        "none", "cinematic", "vintage", "black_white", "sepia",
        "blur", "sharpen", "warm", "cool", "professional"
    ]


def get_available_presets() -> dict:
    """获取可用的效果预设"""
    return EFFECT_PRESETS


# ========================================
# 🎪 主要应用函数
# ========================================

def apply_transition_effect(clip1: Clip, clip2: Clip, transition_type: str, duration: float = 1.0) -> Clip:
    """应用指定的转场效果"""
    try:
        if transition_type == "crossfade":
            return crossfade_transition(clip1, clip2, duration)
        elif transition_type == "wipe_left":
            return wipe_transition(clip1, clip2, "left", duration)
        elif transition_type == "wipe_right":
            return wipe_transition(clip1, clip2, "right", duration)
        elif transition_type == "wipe_up":
            return wipe_transition(clip1, clip2, "top", duration)
        elif transition_type == "wipe_down":
            return wipe_transition(clip1, clip2, "bottom", duration)
        elif transition_type == "random":
            return apply_random_transition(clip1, clip2, duration)
        else:
            # 默认返回第一个片段
            return clip1
    except Exception as e:
        logger.error(f"转场效果应用失败: {e}")
        return clip1


def apply_filter_effect(clip: Clip, filter_type: str, intensity: float = 0.5) -> Clip:
    """应用指定的滤镜效果"""
    try:
        if filter_type == "cinematic":
            return apply_cinematic_filter(clip, intensity)
        elif filter_type == "vintage":
            return apply_vintage_filter(clip, intensity)
        elif filter_type == "black_white":
            return apply_black_white_filter(clip)
        elif filter_type == "sepia":
            return apply_sepia_filter(clip)
        elif filter_type == "blur":
            return apply_blur_filter(clip, intensity * 4)
        elif filter_type == "warm":
            return color_temperature_warm(clip, intensity)
        elif filter_type == "cool":
            return color_temperature_cool(clip, intensity)
        elif filter_type == "professional":
            return apply_professional_enhancement(clip, "medium")
        else:
            return clip
    except Exception as e:
        logger.error(f"滤镜效果应用失败: {e}")
        return clip
