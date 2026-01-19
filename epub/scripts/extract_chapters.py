#!/usr/bin/env python3
"""
从 EPUB 文件中抽取章节内容,支持多种输出格式
使用方法: python extract_chapters.py <epub文件路径> <输出目录> [选项]

选项:
  --format txt|md|html    输出格式 (默认: txt)
  --separate               将每章保存为单独文件
  --toc                    生成目录索引文件
  --metadata               在输出中包含元数据
"""
import sys
import os
import argparse
from ebooklib import epub
from ebooklib import ITEM_DOCUMENT, ITEM_IMAGE, ITEM_STYLE
from bs4 import BeautifulSoup


def extract_chapter_title(content, default_title):
    """从章节 HTML 内容中提取标题"""
    try:
        soup = BeautifulSoup(content, 'html.parser')

        # 尝试查找 h1-h3 标题
        for tag_name in ['h1', 'h2', 'h3']:
            title_tag = soup.find(tag_name)
            if title_tag:
                title = title_tag.get_text(strip=True)
                if title:
                    return title

        # 如果没有找到标题,使用默认标题
        return default_title
    except:
        return default_title


def clean_html_content(content):
    """清理 HTML 内容,移除脚本和样式"""
    soup = BeautifulSoup(content, 'html.parser')

    # 移除不需要的标签
    for tag in soup(['script', 'style', 'nav', 'noscript']):
        tag.decompose()

    return soup


def html_to_text(soup, preserve_structure=True):
    """将 HTML 转换为纯文本,可选择保留结构"""
    if preserve_structure:
        # 保留标题和段落结构
        text_parts = []
        for elem in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'br']):
            text = elem.get_text(strip=True)
            if text:
                if elem.name.startswith('h'):
                    # 标题添加前缀
                    level = int(elem.name[1])
                    prefix = '#' * level
                    text_parts.append(f"\n{prefix} {text}\n")
                elif elem.name == 'br':
                    text_parts.append('\n')
                else:
                    text_parts.append(f"\n{text}\n")

        return '\n'.join(text_parts)
    else:
        return soup.get_text(separator='\n', strip=True)


def html_to_markdown(soup):
    """将 HTML 转换为 Markdown 格式"""
    markdown_lines = []

    for elem in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'strong', 'em', 'br', 'a', 'img']):
        if elem.name.startswith('h'):
            level = int(elem.name[1])
            text = elem.get_text(strip=True)
            markdown_lines.append(f"\n{'#' * level} {text}\n")

        elif elem.name == 'p':
            text = elem.get_text(strip=True)
            if text:
                # 处理段落内的格式
                for strong in elem.find_all('strong'):
                    strong.replace_with(f"**{strong.get_text()}**")
                for em in elem.find_all('em'):
                    em.replace_with(f"*{em.get_text()}*")
                text = elem.get_text(strip=True)
                markdown_lines.append(f"\n{text}\n")

        elif elem.name == 'strong':
            text = elem.get_text(strip=True)
            markdown_lines.append(f"**{text}**")

        elif elem.name == 'em':
            text = elem.get_text(strip=True)
            markdown_lines.append(f"*{text}*")

        elif elem.name == 'br':
            markdown_lines.append('\n')

        elif elem.name == 'a':
            text = elem.get_text(strip=True)
            href = elem.get('href', '')
            if text and href:
                markdown_lines.append(f"[{text}]({href})")

        elif elem.name == 'img':
            alt = elem.get('alt', '')
            src = elem.get('src', '')
            markdown_lines.append(f"![{alt}]({src})")

    return '\n'.join(markdown_lines)


def format_chapter_as_text(content, title, metadata=None):
    """将章节内容格式化为纯文本"""
    soup = clean_html_content(content)
    text = html_to_text(soup, preserve_structure=True)

    output = []
    output.append("=" * 70)
    output.append(f"章节: {title}")
    output.append("=" * 70)

    if metadata:
        output.append(f"\n元数据:")
        for key, value in metadata.items():
            if value:
                output.append(f"  {key}: {value}")
        output.append("\n")

    output.append(text)
    output.append("\n")

    return '\n'.join(output)


def format_chapter_as_markdown(content, title, metadata=None):
    """将章节内容格式化为 Markdown"""
    soup = clean_html_content(content)
    markdown = html_to_markdown(soup)

    output = []
    output.append(f"# {title}\n")

    if metadata:
        output.append("## 元数据\n")
        for key, value in metadata.items():
            if value:
                output.append(f"- **{key}**: {value}")
        output.append("\n")

    output.append(markdown)
    output.append("\n")

    return '\n'.join(output)


def format_chapter_as_html(content, title, metadata=None):
    """将章节内容格式化为 HTML"""
    soup = clean_html_content(content)

    # 构建 HTML 文档
    html_parts = []
    html_parts.append("<!DOCTYPE html>")
    html_parts.append("<html lang=\"zh-CN\">")
    html_parts.append("<head>")
    html_parts.append("  <meta charset=\"UTF-8\">")
    html_parts.append(f"  <title>{title}</title>")
    html_parts.append("  <style>")
    html_parts.append("    body { font-family: 'Georgia', serif; line-height: 1.6; margin: 2em; }")
    html_parts.append("    h1, h2, h3 { color: #333; }")
    html_parts.append("    p { text-align: justify; }")
    html_parts.append("    .metadata { background: #f5f5f5; padding: 1em; margin-bottom: 2em; }")
    html_parts.append("  </style>")
    html_parts.append("</head>")
    html_parts.append("<body>")

    # 标题
    html_parts.append(f"  <h1>{title}</h1>")

    # 元数据
    if metadata:
        html_parts.append("  <div class=\"metadata\">")
        html_parts.append("    <h2>元数据</h2>")
        html_parts.append("    <ul>")
        for key, value in metadata.items():
            if value:
                html_parts.append(f"      <li><strong>{key}:</strong> {value}</li>")
        html_parts.append("    </ul>")
        html_parts.append("  </div>")

    # 内容
    html_parts.append("  <div class=\"content\">")
    html_parts.append(str(soup))
    html_parts.append("  </div>")

    html_parts.append("</body>")
    html_parts.append("</html>")

    return '\n'.join(html_parts)


def extract_chapters(epub_path, output_dir, output_format='txt', separate=False,
                     include_metadata=False, generate_toc=False):
    """从 EPUB 中抽取章节"""
    try:
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)

        # 读取 EPUB
        book = epub.read_epub(epub_path)

        # 提取元数据
        metadata = {}
        if include_metadata:
            titles = book.get_metadata('DC', 'title')
            metadata['书名'] = titles[0][0] if titles else None

            authors = book.get_metadata('DC', 'creator')
            metadata['作者'] = ', '.join([a[0] for a in authors]) if authors else None

            languages = book.get_metadata('DC', 'language')
            metadata['语言'] = languages[0][0] if languages else None

            publishers = book.get_metadata('DC', 'publisher')
            metadata['出版社'] = publishers[0][0] if publishers else None

        # 抽取章节
        chapters = []
        chapter_num = 0

        for item in book.get_items():
            # 跳过导航文件(nav.xhtml),只处理真正的章节内容
            if item.get_type() == ITEM_DOCUMENT:
                file_name = item.get_name()

                # 跳过导航文件
                if file_name == 'nav.xhtml':
                    continue

                chapter_num += 1
                content = item.get_content()

                # 提取章节标题
                default_title = f"第 {chapter_num} 章"
                chapter_title = extract_chapter_title(content, default_title)

                # 格式化内容
                if output_format == 'txt':
                    formatted_content = format_chapter_as_text(content, chapter_title, metadata)
                elif output_format == 'md':
                    formatted_content = format_chapter_as_markdown(content, chapter_title, metadata)
                elif output_format == 'html':
                    formatted_content = format_chapter_as_html(content, chapter_title, metadata)
                else:
                    raise ValueError(f"不支持的输出格式: {output_format}")

                chapters.append({
                    'num': chapter_num,
                    'title': chapter_title,
                    'content': formatted_content,
                    'filename': file_name
                })

        # 输出结果
        if separate:
            # 每章保存为单独文件
            for chapter in chapters:
                ext = output_format
                filename = f"chapter_{chapter['num']:03d}.{ext}"
                filepath = os.path.join(output_dir, filename)

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(chapter['content'])

                print(f"✓ 已保存: {filename}")

        else:
            # 合并保存到单个文件
            ext = output_format
            filename = f"chapters.{ext}"
            filepath = os.path.join(output_dir, filename)

            all_content = []
            for chapter in chapters:
                all_content.append(chapter['content'])

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(all_content))

            print(f"✓ 已保存所有章节到: {filename}")

        # 生成目录
        if generate_toc:
            toc_filename = "TOC.txt"
            toc_path = os.path.join(output_dir, toc_filename)

            with open(toc_path, 'w', encoding='utf-8') as f:
                f.write("目录\n")
                f.write("=" * 50 + "\n\n")

                for chapter in chapters:
                    f.write(f"{chapter['num']}. {chapter['title']}\n")
                    if separate:
                        ext = output_format
                        f.write(f"   文件: chapter_{chapter['num']:03d}.{ext}\n")
                    f.write("\n")

            print(f"✓ 已生成目录: {toc_filename}")

        # 输出统计信息
        print(f"\n完成!")
        print(f"  总章节数: {chapter_num}")
        print(f"  输出格式: {output_format}")
        print(f"  保存位置: {output_dir}")

    except Exception as e:
        print(f"错误: 无法抽取章节 - {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='从 EPUB 文件中抽取章节内容',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 抽取所有章节到单个文本文件
  python extract_chapters.py book.epub output/

  # 每章保存为单独的 Markdown 文件
  python extract_chapters.py book.epub output/ --format md --separate

  # 生成带元数据和目录的 HTML 文件
  python extract_chapters.py book.epub output/ --format html --metadata --toc
        """
    )

    parser.add_argument('epub_path', help='EPUB 文件路径')
    parser.add_argument('output_dir', help='输出目录')
    parser.add_argument('--format', choices=['txt', 'md', 'html'], default='txt',
                      help='输出格式 (默认: txt)')
    parser.add_argument('--separate', action='store_true',
                      help='将每章保存为单独文件')
    parser.add_argument('--toc', action='store_true',
                      help='生成目录索引文件')
    parser.add_argument('--metadata', action='store_true',
                      help='在输出中包含元数据')

    args = parser.parse_args()

    if not os.path.exists(args.epub_path):
        print(f"错误: 找不到文件 {args.epub_path}", file=sys.stderr)
        sys.exit(1)

    extract_chapters(
        args.epub_path,
        args.output_dir,
        output_format=args.format,
        separate=args.separate,
        include_metadata=args.metadata,
        generate_toc=args.toc
    )


if __name__ == "__main__":
    main()
