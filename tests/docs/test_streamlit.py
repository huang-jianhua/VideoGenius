#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单的Streamlit测试脚本
用于验证Streamlit是否正确安装
"""

try:
    import streamlit as st
    print("✅ Streamlit导入成功！")
    print(f"📦 Streamlit版本: {st.__version__}")
    
    # 测试其他关键依赖
    try:
        import pandas as pd
        print(f"✅ Pandas版本: {pd.__version__}")
    except ImportError:
        print("❌ Pandas未安装")
    
    try:
        import numpy as np
        print(f"✅ Numpy版本: {np.__version__}")
    except ImportError:
        print("❌ Numpy未安装")
        
    try:
        import requests
        print(f"✅ Requests版本: {requests.__version__}")
    except ImportError:
        print("❌ Requests未安装")
        
    print("\n🎉 所有核心依赖检查完成！")
    print("🚀 可以启动VideoGenius了！")
    
except ImportError as e:
    print(f"❌ Streamlit导入失败: {e}")
    print("💡 请运行以下命令安装Streamlit:")
    print("   pip install streamlit")
    
except Exception as e:
    print(f"❌ 发生未知错误: {e}") 