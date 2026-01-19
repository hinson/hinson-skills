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
        # 读取 EPUB,使用 ignore_ncx 选项避免 ebooklib 的 NCX 处理 bug
        book = epub.read_epub(epub_path, options={'ignore_ncx': True})

        modified = False

        # 更新标题
        if title:
            # 先清除现有标题
            # 注意:元数据使用完整的命名空间 URL
            for ns in book.metadata:
                if 'title' in book.metadata[ns]:
                    book.metadata[ns]['title'] = []
            # 设置新标题
            book.set_title(title)
            print(f"✓ 更新标题: {title}")
            modified = True

        # 更新作者
        if author:
            # 先清除现有作者
            for ns in book.metadata:
                if 'creator' in book.metadata[ns]:
                    book.metadata[ns]['creator'] = []
            book.add_author(author)
            print(f"✓ 更新作者: {author}")
            modified = True

        # 更新语言
        if language:
            for ns in book.metadata:
                if 'language' in book.metadata[ns]:
                    book.metadata[ns]['language'] = []
            book.set_language(language)
            print(f"✓ 更新语言: {language}")
            modified = True

        # 更新出版社
        if publisher:
            # 清除现有出版社并添加新的
            for ns in book.metadata:
                if 'publisher' in book.metadata[ns]:
                    book.metadata[ns]['publisher'] = []
            book.add_metadata('DC', 'publisher', {}, publisher)
            print(f"✓ 更新出版社: {publisher}")
            modified = True

        # 更新 ISBN
        if isbn:
            # 清除现有标识符并设置新的
            for ns in book.metadata:
                if 'identifier' in book.metadata[ns]:
                    book.metadata[ns]['identifier'] = []
            book.set_unique_identifier(isbn)
            print(f"✓ 更新 ISBN: {isbn}")
            modified = True

        if not modified:
            print("没有修改任何元数据")
            return

        # 确保 TOC 中的所有项目都有 uid
        # 这是 ebooklib 的要求,否则写入时会失败
        if hasattr(book, 'toc') and book.toc:
            def ensure_uid(toc_items, counter=[0]):
                """递归地为 TOC 中的所有项目设置 uid"""
                if not toc_items:
                    return
                for item in toc_items:
                    if isinstance(item, tuple) or isinstance(item, list):
                        ensure_uid(item, counter)
                    elif hasattr(item, 'uid'):
                        if not item.uid or item.uid is None:
                            item.uid = f'uid_{counter[0]}'
                            counter[0] += 1

            # 确保 book.toc 被当作列表处理
            toc_list = list(book.toc) if hasattr(book.toc, '__iter__') else [book.toc]
            ensure_uid(toc_list)

        # 保存修改后的 EPUB
        epub.write_epub(epub_path, book, {})
        print(f"\n✓ 元数据已更新: {epub_path}")

    except Exception as e:
        # 在库函数中抛出异常而不是调用 sys.exit
        raise RuntimeError(f"无法更新 EPUB: {e}") from e


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

    try:
        update_metadata(
            args.epub_file,
            title=args.title,
            author=args.author,
            language=args.language,
            publisher=args.publisher,
            isbn=args.isbn
        )
    except RuntimeError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
