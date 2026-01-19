#!/usr/bin/env python3
"""
将 EPUB 的每一章保存为单独的 EPUB 文件
使用方法: python split_epub.py <输入epub> <输出目录>
"""
import sys
import os
from ebooklib import epub
from ebooklib import ITEM_DOCUMENT, ITEM_IMAGE, ITEM_STYLE, ITEM_NAVIGATION


def split_epub(input_file, output_dir):
    """将 EPUB 的每一章保存为单独的 EPUB"""
    try:
        book = epub.read_epub(input_file)

        # 获取标题作为基础名称
        titles = book.get_metadata('DC', 'title')
        base_name = titles[0][0] if titles else 'chapter'
        base_name = base_name.replace(' ', '_').replace('/', '_')

        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)

        # 获取所有元数据
        all_metadata = {}
        for metadata_type in ['DC', 'OPF']:
            for item in book.get_metadata(metadata_type, []):
                if metadata_type not in all_metadata:
                    all_metadata[metadata_type] = []
                all_metadata[metadata_type].append(item)

        chapter_num = 0
        image_items = [item for item in book.get_items()
                      if item.get_type() == ITEM_IMAGE]
        style_items = [item for item in book.get_items()
                      if item.get_type() == ITEM_STYLE]

        # 遍历所有章节
        for item in book.get_items():
            if item.get_type() == ITEM_DOCUMENT:
                chapter_num += 1

                # 为每个章节创建新的 EPUB
                chapter_book = epub.EpubBook()

                # 设置唯一标识符
                chapter_id = f'{base_name}_chapter_{chapter_num}'
                chapter_book.set_identifier(chapter_id)

                # 设置标题
                chapter_title = f'{base_name} - 第{chapter_num}章'
                chapter_book.set_title(chapter_title)

                # 复制语言设置
                languages = book.get_metadata('DC', 'language')
                if languages:
                    chapter_book.set_language(languages[0][0])

                # 复制作者
                authors = book.get_metadata('DC', 'creator')
                for author in authors:
                    chapter_book.add_author(author[0])

                # 复制其他元数据
                for metadata_type, items in all_metadata.items():
                    for metadata_item in items:
                        if metadata_type not in ['DC', 'creator']:
                            chapter_book.add_metadata(
                                metadata_type,
                                metadata_item[0],
                                metadata_item[1]
                            )

                # 添加当前章节
                chapter_book.add_item(item)

                # 复制所有图片
                for img_item in image_items:
                    chapter_book.add_item(img_item)

                # 复制所有样式
                for style_item in style_items:
                    chapter_book.add_item(style_item)

                # 添加必要的导航文件
                chapter_book.add_item(epub.EpubNcx())
                chapter_book.add_item(epub.EpubNav())
                chapter_book.spine = ['nav', item]

                # 保存章节 EPUB
                output_filename = f'chapter_{chapter_num:03d}.epub'
                output_path = os.path.join(output_dir, output_filename)

                epub.write_epub(output_path, chapter_book, {})
                print(f"✓ 已保存: {output_filename}")

        print(f"\n完成!")
        print(f"  总章节数: {chapter_num}")
        print(f"  保存位置: {output_dir}")

    except Exception as e:
        print(f"错误: 无法分割 EPUB - {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    if len(sys.argv) != 3:
        print("使用方法: python split_epub.py <输入epub> <输出目录>", file=sys.stderr)
        print("\n示例:")
        print("  python split_epub.py large_book.epub chapters/", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"错误: 找不到文件 {input_file}", file=sys.stderr)
        sys.exit(1)

    split_epub(input_file, output_dir)


if __name__ == "__main__":
    main()
