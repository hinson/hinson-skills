#!/usr/bin/env python3
from ebooklib import ITEM_IMAGE
"""
从 EPUB 文件中提取所有图片
使用方法: python extract_images.py <epub文件路径> [输出目录]
"""
import sys
import os
from ebooklib import epub


def extract_images(epub_path, output_dir=None):
    """提取 EPUB 中的所有图片"""
    try:
        book = epub.read_epub(epub_path)

        # 默认输出目录
        if output_dir is None:
            base_name = os.path.splitext(os.path.basename(epub_path))[0]
            output_dir = f'{base_name}_images'

        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)

        image_count = 0
        skipped_count = 0

        for item in book.get_items():
            if item.get_type() == ITEM_IMAGE:
                # 获取图片文件名
                image_name = item.get_name()

                # 替换路径中的目录,确保所有图片在同一目录
                image_name = os.path.basename(image_name)

                # 如果文件名冲突,添加数字后缀
                base, ext = os.path.splitext(image_name)
                counter = 1
                while os.path.exists(os.path.join(output_dir, image_name)):
                    image_name = f"{base}_{counter}{ext}"
                    counter += 1

                # 保存图片
                image_path = os.path.join(output_dir, image_name)

                try:
                    with open(image_path, 'wb') as f:
                        f.write(item.get_content())
                    image_count += 1
                    print(f"✓ 提取: {image_name}")
                except Exception as e:
                    print(f"✗ 跳过: {item.get_name()} ({e})", file=sys.stderr)
                    skipped_count += 1

        print(f"\n完成!")
        print(f"  提取图片: {image_count} 张")
        if skipped_count > 0:
            print(f"  跳过图片: {skipped_count} 张")
        print(f"  保存位置: {output_dir}")

    except Exception as e:
        print(f"错误: 无法读取 EPUB 文件 - {e}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("使用方法: python extract_images.py <epub文件路径> [输出目录]", file=sys.stderr)
        print("\n示例:")
        print("  python extract_images.py book.epub")
        print("  python extract_images.py book.epub my_images/", file=sys.stderr)
        sys.exit(1)

    epub_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) >= 3 else None

    if not os.path.exists(epub_path):
        print(f"错误: 找不到文件 {epub_path}", file=sys.stderr)
        sys.exit(1)

    extract_images(epub_path, output_dir)


if __name__ == "__main__":
    main()
