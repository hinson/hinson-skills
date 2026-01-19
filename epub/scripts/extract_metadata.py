#!/usr/bin/env python3
"""
提取 EPUB 电子书的元数据信息
使用方法: python extract_metadata.py <epub文件路径>
"""
import sys
import json
from ebooklib import epub
from ebooklib import ITEM_DOCUMENT, ITEM_IMAGE, ITEM_STYLE, ITEM_NAVIGATION


def extract_metadata(epub_path):
    """提取并返回 EPUB 的元数据"""
    try:
        # 使用 ignore_ncx 选项避免 ebooklib 的 NCX 处理 bug
        book = epub.read_epub(epub_path, options={'ignore_ncx': True})

        metadata = {
            'file': epub_path,
            'title': None,
            'authors': [],
            'language': None,
            'publisher': None,
            'publish_date': None,
            'isbn': None,
            'description': None,
            'chapters_count': 0,
            'images_count': 0
        }

        # 提取标题
        titles = book.get_metadata('DC', 'title')
        if titles:
            metadata['title'] = titles[0][0]

        # 提取作者
        creators = book.get_metadata('DC', 'creator')
        metadata['authors'] = [creator[0] for creator in creators]

        # 提取语言
        languages = book.get_metadata('DC', 'language')
        if languages:
            metadata['language'] = languages[0][0]

        # 提取出版社
        publishers = book.get_metadata('DC', 'publisher')
        if publishers:
            metadata['publisher'] = publishers[0][0]

        # 提取出版日期
        dates = book.get_metadata('DC', 'date')
        if dates:
            metadata['publish_date'] = dates[0][0]

        # 提取 ISBN
        identifiers = book.get_metadata('DC', 'identifier')
        for identifier in identifiers:
            if 'isbn' in str(identifier[1]).lower():
                metadata['isbn'] = identifier[0]
                break
            if not metadata['isbn']:
                metadata['isbn'] = identifier[0]

        # 提取描述
        descriptions = book.get_metadata('DC', 'description')
        if descriptions:
            metadata['description'] = descriptions[0][0]

        # 统计章节和图片
        for item in book.get_items():
            if item.get_type() == ITEM_DOCUMENT:
                metadata['chapters_count'] += 1
            elif item.get_type() == ITEM_IMAGE:
                metadata['images_count'] += 1

        return metadata

    except Exception as e:
        # 在库函数中抛出异常而不是调用 sys.exit
        # 这样测试代码可以捕获异常
        raise RuntimeError(f"无法读取 EPUB 文件: {e}") from e


def main():
    if len(sys.argv) != 2:
        print("使用方法: python extract_metadata.py <epub文件路径>", file=sys.stderr)
        sys.exit(1)

    epub_path = sys.argv[1]

    try:
        metadata = extract_metadata(epub_path)
    except RuntimeError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

    # 格式化输出
    print("=" * 50)
    print(f"文件: {metadata['file']}")
    print("=" * 50)
    print(f"书名: {metadata['title'] or '未知'}")
    print(f"作者: {', '.join(metadata['authors']) if metadata['authors'] else '未知'}")
    print(f"语言: {metadata['language'] or '未知'}")
    print(f"出版社: {metadata['publisher'] or '未知'}")
    print(f"出版日期: {metadata['publish_date'] or '未知'}")
    print(f"ISBN: {metadata['isbn'] or '未知'}")
    print(f"章节数: {metadata['chapters_count']}")
    print(f"图片数: {metadata['images_count']}")
    if metadata['description']:
        print(f"\n简介:\n{metadata['description']}")
    print("=" * 50)

    # 同时输出 JSON 格式便于程序处理
    print("\nJSON 格式:")
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
