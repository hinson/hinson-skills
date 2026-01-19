#!/usr/bin/env python3
"""
从 Markdown 文件创建 EPUB 电子书
使用方法: python create_epub.py <markdown文件> <输出epub> [标题] [作者]
"""
import sys
import os
from ebooklib import epub
from bs4 import BeautifulSoup
import re


def markdown_to_html(md_content):
    """简单的 Markdown 转 HTML"""
    html = md_content

    # 标题
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

    # 粗体和斜体
    html = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # 代码块
    html = re.sub(r'```(.+?)```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)

    # 链接
    html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)

    # 图片
    html = re.sub(r'!\[(.+?)\]\((.+?)\)', r'<img src="\2" alt="\1" />', html)

    # 段落
    paragraphs = html.split('\n\n')
    html_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<h') and not p.startswith('<pre') and not p.startswith('<img'):
            html_paragraphs.append(f'<p>{p}</p>')
        elif p:
            html_paragraphs.append(p)

    return '\n'.join(html_paragraphs)


def create_epub_from_markdown(md_file, output_epub, title=None, author=None):
    """从 Markdown 文件创建 EPUB"""
    try:
        # 读取 Markdown
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # 如果没有指定标题和作者,尝试从 Markdown 中提取
        if not title:
            title_match = re.search(r'^# (.+)$', md_content, re.MULTILINE)
            title = title_match.group(1) if title_match else os.path.basename(md_file)

        if not author:
            author = "未知作者"

        # 转换为 HTML
        html_content = markdown_to_html(md_content)

        # 创建 EPUB
        book = epub.EpubBook()
        book.set_identifier(os.path.basename(md_file))
        book.set_title(title)
        book.set_language('zh-CN')
        book.add_author(author)

        # 创建章节
        chapter = epub.EpubHtml(title=title, file_name='chapter_01.xhtml', lang='zh-CN')
        chapter.content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>{title}</title>
    <link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
    <h1>{title}</h1>
    {html_content}
</body>
</html>'''
        book.add_item(chapter)

        # 添加样式
        style = '''
body {
    font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
    line-height: 1.8;
    margin: 2em;
}
h1, h2, h3 {
    color: #333;
    margin-top: 1.5em;
    margin-bottom: 0.8em;
}
p {
    text-indent: 2em;
    margin: 0.5em 0;
}
code {
    background-color: #f4f4f4;
    padding: 0.2em 0.4em;
    border-radius: 3px;
}
pre {
    background-color: #f4f4f4;
    padding: 1em;
    border-radius: 5px;
    overflow-x: auto;
}
a {
    color: #0066cc;
}
'''
        nav_css = epub.EpubItem(
            uid="style_nav",
            file_name="style.css",
            media_type="text/css",
            content=style
        )
        book.add_item(nav_css)

        # 设置目录和书脊
        book.toc = (chapter,)
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        book.spine = ['nav', chapter]

        # 写入 EPUB
        epub.write_epub(output_epub, book, {})
        print(f"✓ EPUB 创建成功: {output_epub}")
        print(f"  标题: {title}")
        print(f"  作者: {author}")

    except Exception as e:
        print(f"错误: 无法创建 EPUB - {e}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 3:
        print("使用方法: python create_epub.py <markdown文件> <输出epub> [标题] [作者]", file=sys.stderr)
        print("\n示例:")
        print("  python create_epub.py my_book.md my_book.epub")
        print("  python create_epub.py my_book.md my_book.epub '我的书' '张三'", file=sys.stderr)
        sys.exit(1)

    md_file = sys.argv[1]
    output_epub = sys.argv[2]
    title = sys.argv[3] if len(sys.argv) >= 4 else None
    author = sys.argv[4] if len(sys.argv) >= 5 else None

    if not os.path.exists(md_file):
        print(f"错误: 找不到文件 {md_file}", file=sys.stderr)
        sys.exit(1)

    create_epub_from_markdown(md_file, output_epub, title, author)


if __name__ == "__main__":
    main()
