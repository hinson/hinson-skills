#!/usr/bin/env python3
"""
验证 EPUB 文件的结构完整性
使用方法: python validate_epub.py <epub文件路径>
"""
import sys
from ebooklib import epub
from ebooklib import ITEM_DOCUMENT, ITEM_IMAGE, ITEM_STYLE, ITEM_NAVIGATION


def validate_epub(epub_path):
    """验证 EPUB 文件结构"""
    print(f"验证 EPUB 文件: {epub_path}")
    print("=" * 60)

    has_errors = False
    has_warnings = False

    try:
        book = epub.read_epub(epub_path)
        print("✓ 文件可以正常读取\n")

        # 检查元数据
        print("元数据检查:")
        titles = book.get_metadata('DC', 'title')
        if not titles:
            print("  ✗ 错误: 缺少标题")
            has_errors = True
        else:
            print(f"  ✓ 标题: {titles[0][0]}")

        authors = book.get_metadata('DC', 'creator')
        if not authors:
            print("  ⚠ 警告: 缺少作者信息")
            has_warnings = True
        else:
            author_list = [a[0] for a in authors]
            print(f"  ✓ 作者: {', '.join(author_list)}")

        language = book.get_metadata('DC', 'language')
        if not language:
            print("  ⚠ 警告: 缺少语言设置")
            has_warnings = True
        else:
            print(f"  ✓ 语言: {language[0][0]}")

        identifiers = book.get_metadata('DC', 'identifier')
        if not identifiers:
            print("  ⚠ 警告: 缺少唯一标识符")
            has_warnings = True
        else:
            print(f"  ✓ 标识符: {identifiers[0][0]}")

        print()

        # 检查内容
        print("内容检查:")

        chapters = [item for item in book.get_items()
                   if item.get_type() == ITEM_DOCUMENT]
        if not chapters:
            print("  ✗ 错误: 没有找到任何章节")
            has_errors = True
        else:
            print(f"  ✓ 找到 {len(chapters)} 个章节")

            # 检查章节内容是否为空
            empty_chapters = []
            for i, chapter in enumerate(chapters):
                content = chapter.get_content().decode('utf-8', errors='ignore')
                if not content or len(content.strip()) < 10:
                    empty_chapters.append(chapter.get_name())

            if empty_chapters:
                print(f"  ⚠ 警告: {len(empty_chapters)} 个章节内容为空或过短")
                has_warnings = True

        images = [item for item in book.get_items()
                 if item.get_type() == ITEM_IMAGE]
        if images:
            print(f"  ✓ 找到 {len(images)} 张图片")
        else:
            print("  ℹ 没有")

        styles = [item for item in book.get_items()
                 if item.get_type() == ITEM_STYLE]
        if styles:
            print(f"  ✓ 找到 {len(styles)} 个样式文件")
        else:
            print("  ℹ 没有样式文件")

        print()

        # 检查导航结构
        print("导航结构检查:")

        has_ncx = any(item.get_type() == ITEM_NAVIGATION
                     for item in book.get_items())
        if not has_ncx:
            print("  ✗ 错误: 缺少导航文件 (NCX)")
            has_errors = True
        else:
            print("  ✓ 导航文件存在")

        if book.toc:
            print(f"  ✓ 目录包含 {len(list(book.toc))} 个项目")
        else:
            print("  ⚠ 警告: 目录为空")
            has_warnings = True

        if book.spine:
            print(f"  ✓ 书脊包含 {len(book.spine)} 个项目")
        else:
            print("  ✗ 错误: 书脊为空")
            has_errors = True

        print()

        # 总结
        print("=" * 60)
        if has_errors:
            print("❌ 验证失败: 发现错误")
            return 1
        elif has_warnings:
            print("⚠️  验证通过: 但有警告")
            return 0
        else:
            print("✅ 验证通过: 文件结构完整")
            return 0

    except Exception as e:
        print(f"\n✗ 致命错误: {e}")
        import traceback
        traceback.print_exc()
        return 2


def main():
    if len(sys.argv) != 2:
        print("使用方法: python validate_epub.py <epub文件路径>", file=sys.stderr)
        sys.exit(1)

    epub_path = sys.argv[1]
    exit_code = validate_epub(epub_path)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
