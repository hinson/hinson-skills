#!/bin/bash
# EPUB 工具安装脚本

set -e

echo "========================================="
echo "  EPUB 处理工具 - 依赖安装"
echo "========================================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3"
    echo "   请先安装 Python 3.7 或更高版本"
    exit 1
fi

echo "✓ Python: $(python3 --version)"
echo ""

# 检查 pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ 错误: 未找到 pip3"
    exit 1
fi

echo "✓ pip: $(pip3 --version)"
echo ""

# 安装依赖
echo "正在安装 Python 依赖..."
echo "  - ebooklib"
echo "  - beautifulsoup4"
echo "  - lxml"
echo ""

pip3 install ebooklib beautifulsoup4 lxml

echo ""
echo "========================================="
echo "✓ 安装完成!"
echo "========================================="
echo ""
echo "可用脚本:"
echo "  extract_metadata.py  - 提取元数据"
echo "  extract_text.py      - 提取文本"
echo "  extract_images.py    - 提取图片"
echo "  create_epub.py       - 创建 EPUB"
echo "  merge_epubs.py       - 合并 EPUB"
echo "  split_epub.py        - 分割 EPUB"
echo "  update_metadata.py   - 更新元数据"
echo "  validate_epub.py     - 验证结构"
echo ""
echo "使用示例:"
echo "  python extract_metadata.py book.epub"
echo "  python validate_epub.py book.epub"
echo ""
echo "查看完整文档: README.md"
