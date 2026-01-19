#!/usr/bin/env python3
"""
从 EPUB 文件中提取纯文本内容
使用方法: python extract_text.py <epub文件路径> [输出文件路径]
"""
import sys
from ebooklib import epub
from ebooklib import ITEM_DOCUMENT, ITEM_IMAGE, ITEM_STYLE, ITEM_NAVIGATION
from bs4 import BeautifulSoup


def extract_text_from_epub(epub_path):
    """从 EPUB 中提取所有纯文本"""
    try:
        book = epub.read_epub(epub_path)
        full_text = []
        chapter_num = 0

        for item in book.get_items():
            if item.get_type() == ITEM_DOCUMENT:
                chapter_num += 1
                content = item.get_content().decode('utf-8')
                soup = BeautifulSoup(content, 'html.parser')

                # 移除脚本和样式
                for script in soup(['script', 'style', 'nav']):
                    script.decompose()

                # 提取文本
                text = soup.get_text(separator='\n', strip=True)

                # 添加章节标题
                full_text.append(f"\n{'='*60}\n第 {chapter_num} 章\n{'='*60}\n")
                full_text.append(text)

        return '\n'.join(full_text)

    except Exception as e:
        print(f"错误: 无法读取 EPUB 文件 - {e}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("使用方法: python extract_text.py <epub文件路径> [输出文件路径]", file=sys.stderr)
        sys.exit(1)

    epub_path = sys.argv[1]

    # 提取文本
    text = extract_text_from_epub(epub_path)

    # 输出到文件或标准输出
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"文本已提取到: {output_path}")
        except Exception as e:
            print(f"错误: 无法写入输出文件 - {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(text)


if __name__ == "__main__":
    main()
