"""
配置验证模块
用于验证各种配置项的有效性，提供友好的错误提示
"""

import os
import re
import requests
import time
from typing import Dict, List, Tuple, Optional
from loguru import logger


class ConfigValidator:
    """配置验证器"""
    
    def __init__(self):
        self.timeout = 10  # 网络请求超时时间
        
    def validate_api_key(self, provider: str, api_key: str) -> Tuple[bool, str]:
        """
        验证API密钥格式和有效性
        
        Args:
            provider: 服务提供商名称
            api_key: API密钥
            
        Returns:
            (是否有效, 错误信息或成功信息)
        """
        if not api_key or not api_key.strip():
            return False, "API密钥不能为空"
            
        # 基础格式验证
        api_key = api_key.strip()
        
        # 不同提供商的密钥格式验证
        if provider.lower() == "openai":
            if not api_key.startswith("sk-"):
                return False, "OpenAI API密钥应以 'sk-' 开头"
            if len(api_key) < 20:
                return False, "OpenAI API密钥长度不足"
                
        elif provider.lower() == "deepseek":
            if not api_key.startswith("sk-"):
                return False, "DeepSeek API密钥应以 'sk-' 开头"
                
        elif provider.lower() == "moonshot":
            if not api_key.startswith("sk-"):
                return False, "Moonshot API密钥应以 'sk-' 开头"
                
        elif provider.lower() == "gemini":
            # Gemini API密钥通常是39个字符的字母数字组合
            if not re.match(r'^[A-Za-z0-9_-]{35,45}$', api_key):
                return False, "Gemini API密钥格式不正确"
                
        elif provider.lower() == "qwen":
            # 通义千问API密钥格式验证
            if len(api_key) < 20:
                return False, "通义千问API密钥长度不足"
                
        return True, "API密钥格式验证通过"
    
    def test_connection(self, provider: str, config: Dict) -> Tuple[bool, str]:
        """
        测试服务连接
        
        Args:
            provider: 服务提供商
            config: 配置信息
            
        Returns:
            (连接是否成功, 结果信息)
        """
        try:
            if provider.lower() == "openai":
                return self._test_openai_connection(config)
            elif provider.lower() == "deepseek":
                return self._test_deepseek_connection(config)
            elif provider.lower() == "moonshot":
                return self._test_moonshot_connection(config)
            elif provider.lower() == "gemini":
                return self._test_gemini_connection(config)
            elif provider.lower() == "qwen":
                return self._test_qwen_connection(config)
            else:
                return False, f"暂不支持 {provider} 的连接测试"
                
        except Exception as e:
            logger.error(f"连接测试失败: {str(e)}")
            return False, f"连接测试出错: {str(e)}"
    
    def _test_openai_connection(self, config: Dict) -> Tuple[bool, str]:
        """测试OpenAI连接"""
        api_key = config.get("api_key", "")
        base_url = config.get("base_url", "https://api.openai.com/v1")
        
        if not api_key:
            return False, "API密钥未设置"
            
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            # 测试模型列表接口
            url = f"{base_url.rstrip('/')}/models"
            response = requests.get(url, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                return True, "连接成功！API密钥有效"
            elif response.status_code == 401:
                return False, "API密钥无效或已过期"
            elif response.status_code == 429:
                return False, "请求频率过高，请稍后再试"
            else:
                return False, f"连接失败，状态码: {response.status_code}"
                
        except requests.exceptions.Timeout:
            return False, "连接超时，请检查网络或服务地址"
        except requests.exceptions.ConnectionError:
            return False, "无法连接到服务器，请检查网络和服务地址"
        except Exception as e:
            return False, f"连接测试失败: {str(e)}"
    
    def _test_deepseek_connection(self, config: Dict) -> Tuple[bool, str]:
        """测试DeepSeek连接"""
        # DeepSeek使用OpenAI兼容接口
        config_copy = config.copy()
        if not config_copy.get("base_url"):
            config_copy["base_url"] = "https://api.deepseek.com"
        return self._test_openai_connection(config_copy)
    
    def _test_moonshot_connection(self, config: Dict) -> Tuple[bool, str]:
        """测试Moonshot连接"""
        config_copy = config.copy()
        if not config_copy.get("base_url"):
            config_copy["base_url"] = "https://api.moonshot.cn/v1"
        return self._test_openai_connection(config_copy)
    
    def _test_gemini_connection(self, config: Dict) -> Tuple[bool, str]:
        """测试Gemini连接"""
        api_key = config.get("api_key", "")
        
        if not api_key:
            return False, "API密钥未设置"
            
        try:
            # 测试Gemini API
            url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                return True, "连接成功！API密钥有效"
            elif response.status_code == 400:
                return False, "API密钥格式错误"
            elif response.status_code == 403:
                return False, "API密钥无效或权限不足"
            else:
                return False, f"连接失败，状态码: {response.status_code}"
                
        except Exception as e:
            return False, f"连接测试失败: {str(e)}"
    
    def _test_qwen_connection(self, config: Dict) -> Tuple[bool, str]:
        """测试通义千问连接"""
        # 通义千问连接测试的具体实现
        return True, "通义千问连接测试暂未实现，请手动验证"
    
    def validate_file_path(self, path: str, check_exists: bool = True) -> Tuple[bool, str]:
        """
        验证文件路径
        
        Args:
            path: 文件路径
            check_exists: 是否检查文件是否存在
            
        Returns:
            (路径是否有效, 结果信息)
        """
        if not path or not path.strip():
            return False, "文件路径不能为空"
            
        path = path.strip()
        
        # 检查路径格式
        if not os.path.isabs(path) and not os.path.exists(path):
            return False, "请提供有效的文件路径"
            
        if check_exists and not os.path.exists(path):
            return False, f"文件不存在: {path}"
            
        if check_exists and not os.path.isfile(path):
            return False, f"路径不是文件: {path}"
            
        return True, "文件路径验证通过"
    
    def validate_url(self, url: str) -> Tuple[bool, str]:
        """
        验证URL格式
        
        Args:
            url: URL地址
            
        Returns:
            (URL是否有效, 结果信息)
        """
        if not url or not url.strip():
            return False, "URL不能为空"
            
        url = url.strip()
        
        # 基础URL格式验证
        url_pattern = re.compile(
            r'^https?://'  # http:// 或 https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # 域名
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP地址
            r'(?::\d+)?'  # 可选端口
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            
        if not url_pattern.match(url):
            return False, "URL格式不正确"
            
        return True, "URL格式验证通过"
    
    def check_model_availability(self, provider: str, model: str, config: Dict) -> Tuple[bool, str]:
        """
        检查模型可用性
        
        Args:
            provider: 服务提供商
            model: 模型名称
            config: 配置信息
            
        Returns:
            (模型是否可用, 结果信息)
        """
        if not model or not model.strip():
            return False, "模型名称不能为空"
            
        # 常见模型名称验证
        common_models = {
            "openai": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-4o-mini"],
            "deepseek": ["deepseek-chat", "deepseek-coder"],
            "moonshot": ["moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"],
            "gemini": ["gemini-pro", "gemini-1.0-pro", "gemini-1.5-pro"],
            "qwen": ["qwen-max", "qwen-plus", "qwen-turbo"]
        }
        
        provider_models = common_models.get(provider.lower(), [])
        if provider_models and model not in provider_models:
            suggested = ", ".join(provider_models[:3])
            return False, f"模型名称可能不正确，建议使用: {suggested}"
            
        return True, "模型名称验证通过"
    
    def validate_config_section(self, section: str, config: Dict) -> List[Dict]:
        """
        验证配置段落
        
        Args:
            section: 配置段落名称 (llm, tts, material等)
            config: 配置数据
            
        Returns:
            验证结果列表，每个结果包含 {field, status, message}
        """
        results = []
        
        if section == "llm":
            results.extend(self._validate_llm_config(config))
        elif section == "tts":
            results.extend(self._validate_tts_config(config))
        elif section == "material":
            results.extend(self._validate_material_config(config))
        elif section == "system":
            results.extend(self._validate_system_config(config))
            
        return results
    
    def _validate_llm_config(self, config: Dict) -> List[Dict]:
        """验证LLM配置"""
        results = []
        
        provider = config.get("llm_provider", "")
        if not provider:
            results.append({
                "field": "llm_provider",
                "status": "error",
                "message": "未选择AI模型提供商"
            })
            return results
            
        # 验证API密钥
        api_key = config.get(f"{provider}_api_key", "")
        is_valid, message = self.validate_api_key(provider, api_key)
        results.append({
            "field": f"{provider}_api_key",
            "status": "success" if is_valid else "error",
            "message": message
        })
        
        # 验证Base URL
        base_url = config.get(f"{provider}_base_url", "")
        if base_url:
            is_valid, message = self.validate_url(base_url)
            results.append({
                "field": f"{provider}_base_url",
                "status": "success" if is_valid else "warning",
                "message": message
            })
            
        # 验证模型名称
        model = config.get(f"{provider}_model_name", "")
        if model:
            is_valid, message = self.check_model_availability(provider, model, config)
            results.append({
                "field": f"{provider}_model_name",
                "status": "success" if is_valid else "warning",
                "message": message
            })
            
        return results
    
    def _validate_tts_config(self, config: Dict) -> List[Dict]:
        """验证TTS配置"""
        results = []
        
        tts_server = config.get("tts_server", "")
        if not tts_server:
            results.append({
                "field": "tts_server",
                "status": "warning",
                "message": "未选择语音合成服务"
            })
            return results
            
        if tts_server == "azure-tts-v2":
            # 验证Azure配置
            speech_key = config.get("azure_speech_key", "")
            speech_region = config.get("azure_speech_region", "")
            
            if not speech_key:
                results.append({
                    "field": "azure_speech_key",
                    "status": "error",
                    "message": "Azure语音密钥未设置"
                })
            else:
                results.append({
                    "field": "azure_speech_key",
                    "status": "success",
                    "message": "Azure语音密钥已设置"
                })
                
            if not speech_region:
                results.append({
                    "field": "azure_speech_region",
                    "status": "error",
                    "message": "Azure语音区域未设置"
                })
            else:
                results.append({
                    "field": "azure_speech_region",
                    "status": "success",
                    "message": "Azure语音区域已设置"
                })
                
        elif tts_server == "siliconflow":
            # 验证SiliconFlow配置
            api_key = config.get("siliconflow_api_key", "")
            if not api_key:
                results.append({
                    "field": "siliconflow_api_key",
                    "status": "error",
                    "message": "SiliconFlow API密钥未设置"
                })
            else:
                results.append({
                    "field": "siliconflow_api_key",
                    "status": "success",
                    "message": "SiliconFlow API密钥已设置"
                })
                
        return results
    
    def _validate_material_config(self, config: Dict) -> List[Dict]:
        """验证素材配置"""
        results = []
        
        video_source = config.get("video_source", "")
        if not video_source:
            results.append({
                "field": "video_source",
                "status": "warning",
                "message": "未选择视频素材来源"
            })
            return results
            
        if video_source == "pexels":
            pexels_keys = config.get("pexels_api_keys", [])
            if not pexels_keys or not any(pexels_keys):
                results.append({
                    "field": "pexels_api_keys",
                    "status": "warning",
                    "message": "Pexels API密钥未设置，将使用本地素材"
                })
            else:
                results.append({
                    "field": "pexels_api_keys",
                    "status": "success",
                    "message": f"Pexels API密钥已设置 ({len([k for k in pexels_keys if k])}个)"
                })
                
        elif video_source == "pixabay":
            pixabay_keys = config.get("pixabay_api_keys", [])
            if not pixabay_keys or not any(pixabay_keys):
                results.append({
                    "field": "pixabay_api_keys",
                    "status": "warning",
                    "message": "Pixabay API密钥未设置，将使用本地素材"
                })
            else:
                results.append({
                    "field": "pixabay_api_keys",
                    "status": "success",
                    "message": f"Pixabay API密钥已设置 ({len([k for k in pixabay_keys if k])}个)"
                })
                
        elif video_source == "local":
            # 检查本地素材目录
            local_dir = "storage/local_videos"
            if os.path.exists(local_dir):
                video_files = [f for f in os.listdir(local_dir) if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]
                if video_files:
                    results.append({
                        "field": "local_videos",
                        "status": "success",
                        "message": f"本地素材已准备 ({len(video_files)}个文件)"
                    })
                else:
                    results.append({
                        "field": "local_videos",
                        "status": "warning",
                        "message": "本地素材目录为空，请添加视频文件"
                    })
            else:
                results.append({
                    "field": "local_videos",
                    "status": "error",
                    "message": "本地素材目录不存在"
                })
                
        return results
    
    def _validate_system_config(self, config: Dict) -> List[Dict]:
        """验证系统配置"""
        results = []
        
        # 检查并发任务数
        concurrent_tasks = config.get("concurrent_tasks", 1)
        if concurrent_tasks < 1 or concurrent_tasks > 8:
            results.append({
                "field": "concurrent_tasks",
                "status": "warning",
                "message": "建议并发任务数设置在1-4之间"
            })
        else:
            results.append({
                "field": "concurrent_tasks",
                "status": "success",
                "message": f"并发任务数设置合理: {concurrent_tasks}"
            })
            
        # 检查GPU设置
        enable_gpu = config.get("enable_gpu", False)
        if enable_gpu:
            results.append({
                "field": "enable_gpu",
                "status": "info",
                "message": "GPU加速已启用，确保有NVIDIA显卡"
            })
        else:
            results.append({
                "field": "enable_gpu",
                "status": "info",
                "message": "使用CPU模式，如有显卡可启用GPU加速"
            })
            
        return results


# 创建全局验证器实例
validator = ConfigValidator() 