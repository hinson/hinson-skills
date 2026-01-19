#!/usr/bin/env python3
"""
修改 EPUB 文件的元数据
使用方法: python update_metadata.py <epub文件> [--title "标题"] [--author "作者"] [--language "语言"]
"""
import sys
from ebooklib import epub
import argparse


def update_metadata(epub_path, title=None, author=None, language=None,
                   publisher=None, isbn=None):
    """更新 EPUB 的元数据"""
    try:
        # 读取 EPUB
        book = epub.read_epub(epub_path)

        modified = False

        # 更新标题
        if title:
            # 清除现有标题
            book.set_metadata('DC', 'title', [])
            book.set_title(title)
            print(f"✓ 更新标题: {title}")
            modified = True

        # 更新作者
        if author:
            # 清除现有作者
            book.set_metadata('DC', 'creator', [])
            book.add_author(author)
            print(f"✓ 更新作者: {author}")
            modified = True

        # 更新语言
        if language:
            book.set_metadata('DC', 'language', [])
            book.set_language(language)
            print(f"✓ 更新语言: {language}")
            modified = True

        # 更新出版社
        if publisher:
            book.set_metadata('DC', 'publisher', [])
            book.add_metadata('DC', 'publisher', {}, publisher)
            print(f"✓ 更新出版社: {publisher}")
            modified = True

        # 更新 ISBN
        if isbn:
            book.set_metadata('DC', 'identifier', [])
            book.set_unique_identifier(isbn)
            print(f"✓ 更新 ISBN: {isbn}")
            modified = True

        if not modified:
            print("没有修改任何元数据")
            return

        # 保存修改后的 EPUB
        epub.write_epub(epub_path, book, {})
        print(f"\n✓ 元数据已更新: {epub_path}")

    except Exception as e:
        print(f"错误: 无法更新 EPUB - {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='修改 EPUB 电子书的元数据',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s book.epub --title "新书名"
  %(prog)s book.epub --author "张三" --language "zh-CN"
  %(prog)s book.epub --title "新书名" --author "李四" --publisher "某某出版社"
        '''
    )

    parser.add_argument('epub_file', help='EPUB 文件路径')
    parser.add_argument('--title', help='设置标题')
    parser.add_argument('--author', help='设置作者')
    parser.add_argument('--language', help='设置语言代码 (如: zh-CN, en)')
    parser.add_argument('--publisher', help='设置出版社')
    parser.add_argument('--isbn', help='设置 ISBN')

    args = parser.parse_args()

    if not any([args.title, args.author, args.language,
               args.publisher, args.isbn]):
        parser.print_help()
        print("\n错误: 至少需要指定一个要更新的字段", file=sys.stderr)
        sys.exit(1)

    update_metadata(
        args.epub_file,
        title=args.title,
        author=args.author,
        language=args.language,
        publisher=args.publisher,
        isbn=args.isbn
    )


if __name__ == "__main__":
    main()
