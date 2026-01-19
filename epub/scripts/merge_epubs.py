#!/usr/bin/env python3
"""
合并多个 EPUB 文件为一个
使用方法: python merge_epubs.py <输出文件.epub> <输入文件1.epub> <输入文件2.epub> ...
"""
import sys
import os
from ebooklib import epub
from ebooklib import ITEM_DOCUMENT, ITEM_IMAGE, ITEM_STYLE, ITEM_NAVIGATION


def merge_epubs(input_files, output_file):
    """合并多个 EPUB 文件

    参数:
        input_files: 输入的 EPUB 文件路径列表
        output_file: 输出的 EPUB 文件路径
    """
    try:
        merged_book = epub.EpubBook()
        merged_book.set_identifier(f'merged_{os.path.basename(output_file)}')
        merged_book.set_title('合并的电子书')
        merged_book.set_language('zh-CN')

        all_chapters = []
        all_images = set()
        all_styles = set()

        # 遍历所有输入文件
        for i, input_file in enumerate(input_files):
            if not os.path.exists(input_file):
                print(f"警告: 找不到文件 {input_file}, 跳过", file=sys.stderr)
                continue

            print(f"正在处理: {input_file}")
            # 使用 ignore_ncx 选项避免 ebooklib 的 NCX 处理 bug
            book = epub.read_epub(input_file, options={'ignore_ncx': True})

            # 获取原书名作为章节组标题
            titles = book.get_metadata('DC', 'title')
            book_title = titles[0][0] if titles else f'书{i+1}'

            # 复制所有章节
            chapter_count = 0
            for item in book.get_items():
                if item.get_type() == ITEM_DOCUMENT:
                    chapter_count += 1
                    # 创建新章节以避免文件名冲突
                    new_chapter = epub.EpubHtml(
                        title=f'{book_title} - 第{chapter_count}章',
                        file_name=f'book{i+1}_chap{chapter_count}.xhtml'
                    )
                    new_chapter.content = item.get_content()
                    merged_book.add_item(new_chapter)
                    all_chapters.append(new_chapter)

                # 复制图片
                elif item.get_type() == ITEM_IMAGE:
                    # 生成唯一的图片文件名
                    img_name = f'book{i+1}_{item.get_name()}'
                    item.file_name = img_name
                    if img_name not in all_images:
                        merged_book.add_item(item)
                        all_images.add(img_name)

                # 复制样式
                elif item.get_type() == ITEM_STYLE:
                    style_name = f'book{i+1}_{item.get_name()}'
                    item.file_name = style_name
                    if style_name not in all_styles:
                        merged_book.add_item(item)
                        all_styles.add(style_name)

            print(f"  ✓ 添加了 {chapter_count} 个章节")

        if not all_chapters:
            raise RuntimeError("没有找到任何章节")

        # 设置目录
        merged_book.toc = tuple(all_chapters)

        # 添加导航文件
        merged_book.add_item(epub.EpubNcx())
        merged_book.add_item(epub.EpubNav())

        # 设置书脊
        merged_book.spine = ['nav'] + all_chapters

        # 写入合并后的 EPUB
        epub.write_epub(output_file, merged_book, {})
        print(f"\n✓ 合并完成!")
        print(f"  输出文件: {output_file}")
        print(f"  总章节数: {len(all_chapters)}")

    except Exception as e:
        # 在库函数中抛出异常而不是调用 sys.exit
        raise RuntimeError(f"无法合并 EPUB 文件: {e}") from e


def main():
    if len(sys.argv) < 3:
        print("使用方法: python merge_epubs.py <输出文件.epub> <输入文件1.epub> <输入文件2.epub> ...", file=sys.stderr)
        print("\n示例:")
        print("  python merge_epubs.py merged.epub book1.epub book2.epub book3.epub", file=sys.stderr)
        sys.exit(1)

    output_file = sys.argv[1]
    input_files = sys.argv[2:]

    try:
        # 注意:CLI 调用时参数顺序是 output_file, input_files
        # 但库函数签名是 merge_epubs(input_files, output_file)
        merge_epubs(input_files, output_file)
    except RuntimeError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
