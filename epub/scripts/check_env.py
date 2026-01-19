#!/usr/bin/env python3
"""
检查 EPUB 脚本的运行环境
使用方法: python check_env.py
"""
import sys


def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✓ Python 版本: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python 版本过低: {version.major}.{version.minor}.{version.micro}")
        print("  需要 Python 3.7 或更高版本")
        return False


def check_module(module_name, package_name=None):
    """检查模块是否已安装"""
    if package_name is None:
        package_name = module_name

    try:
        __import__(module_name)
        print(f"✓ {package_name} 已安装")
        return True
    except ImportError:
        print(f"✗ {package_name} 未安装")
        return False


def main():
    print("=" * 50)
    print("EPUB 工具环境检查")
    print("=" * 50)
    print()

    all_ok = True

    # 检查 Python 版本
    if not check_python_version():
        all_ok = False
    print()

    # 检查依赖模块
    print("依赖模块:")
    if not check_module('ebooklib', 'ebooklib'):
        all_ok = False
    if not check_module('bs4', 'beautifulsoup4'):
        all_ok = False
    if not check_module('lxml', 'lxml'):
        all_ok = False

    print()
    print("=" * 50)

    if all_ok:
        print("✓ 环境检查通过!")
        print()
        print("可以开始使用 EPUB 处理脚本:")
        print("  python extract_metadata.py book.epub")
        print("  python validate_epub.py book.epub")
        return 0
    else:
        print("✗ 环境检查失败!")
        print()
        print("请运行以下命令安装依赖:")
        print("  pip install ebooklib beautifulsoup4 lxml")
        print()
        print("或使用安装脚本:")
        print("  bash install.sh")
        return 1


if __name__ == "__main__":
    sys.exit(main())
