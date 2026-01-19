#!/bin/bash
# EPUB 脚本使用示例集

echo "========================================="
echo "  EPUB 处理工具 - 使用示例"
echo "========================================="
echo ""

# 示例 1: 环境检查
echo "示例 1: 检查运行环境"
echo "命令: python3 check_env.py"
echo ""

# 示例 2: 验证 EPUB
echo "示例 2: 验证 EPUB 文件"
echo "命令: python3 validate_epub.py book.epub"
echo ""

# 示例 3: 提取元数据
echo "示例 3: 提取 EPUB 元数据"
echo "命令: python3 extract_metadata.py book.epub"
echo ""

# 示例 4: 提取文本
echo "示例 4: 提取 EPUB 文本内容"
echo "命令: python3 extract_text.py book.epub output.txt"
echo ""

# 示例 5: 提取图片
echo "示例 5: 提取 EPUB 中的所有图片"
echo "命令: python3 extract_images.py book.epub images/"
echo ""

# 示例 6: 更新元数据
echo "示例 6: 更新 EPUB 元数据"
echo "命令: python3 update_metadata.py book.epub --title '新书名' --author '新作者'"
echo ""

# 示例 7: 创建 EPUB
echo "示例 7: 从 Markdown 创建 EPUB"
echo "命令: python3 create_epub.py novel.md novel.epub '我的小说' '张三'"
echo ""

# 示例 8: 合并 EPUB
echo "示例 8: 合并多个 EPUB"
echo "命令: python3 merge_epubs.py merged.epub book1.epub book2.epub book3.epub"
echo ""

# 示例 9: 分割 EPUB
echo "示例 9: 分割 EPUB 为多个文件"
echo "命令: python3 split_epub.py large_book.epub chapters/"
echo ""

# 示例 10: 批量处理
echo "示例 10: 批量验证目录中的所有 EPUB"
echo '命令: for file in *.epub; do python3 validate_epub.py "$file"; done'
echo ""

# 示例 11: 批量提取文本
echo "示例 11: 批量提取所有 EPUB 的文本"
echo '命令: mkdir -p texts && for file in *.epub; do base=$(basename "$file" .epub); python3 extract_text.py "$file" "texts/${base}.txt"; done'
echo ""

echo "========================================="
echo "  完整工作流示例"
echo "========================================="
echo ""
echo "# 1. 检查环境"
echo "python3 check_env.py"
echo ""
echo "# 2. 验证 EPUB 文件"
echo "python3 validate_epub.py book.epub"
echo ""
echo "# 3. 查看元数据"
echo "python3 extract_metadata.py book.epub"
echo ""
echo "# 4. 提取内容"
echo "python3 extract_text.py book.epub text.txt"
echo "python3 extract_images.py book.epub images/"
echo ""
echo "# 5. 创建新 EPUB"
echo "python3 create_epub.md novel.md novel.epub"
echo ""
echo "# 6. 合并系列书籍"
echo "python3 merge_epubs.py complete.epub vol1.epub vol2.epub"
echo ""
echo "========================================="
echo ""
echo "查看详细文档:"
echo "  - scripts/README.md: 脚本详细说明"
echo "  - SKILL.md: 完整操作指南"
echo ""
