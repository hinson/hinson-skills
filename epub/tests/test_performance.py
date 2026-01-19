"""
性能和压力测试

使用 pytest 风格的测试,测试 EPUB 技能脚本在处理大型文件和批量操作时的性能表现。
"""
import sys
import os
import time
from pathlib import Path

from ebooklib import epub

from .test_helpers import create_large_epub, create_simple_epub


def get_test_output_path(output_dir, filename):
    """获取测试输出文件路径"""
    return str(Path(output_dir) / filename)


def count_files_in_dir(directory, pattern='*.txt'):
    """计算目录中匹配模式的文件数量

    参数:
        directory: 目录路径
        pattern: 文件匹配模式,默认为 *.txt
    """
    dir_path = Path(directory)
    return len([f for f in dir_path.glob(pattern) if f.is_file()])


class TestPerformance:
    """性能测试"""

    def test_extract_text_performance_large_epub(self, output_dir):
        """测试从大型 EPUB 中提取文本的性能"""
        import extract_text

        # 创建包含 50 章的大型 EPUB
        large_epub = create_large_epub(chapter_count=50, output_path=get_test_output_path(output_dir, 'large.epub'))

        start_time = time.time()
        text = extract_text.extract_text_from_epub(large_epub)
        elapsed_time = time.time() - start_time

        # 验证结果
        assert len(text) > 0

        # 性能断言: 50 章应该在合理时间内完成(例如 10 秒)
        # 这是性能基准测试,实际阈值可以根据系统性能调整
        assert elapsed_time < 10.0, \
            f"提取文本耗时 {elapsed_time:.2f}秒,超过性能阈值 10秒"

        print(f"\n✓ 性能测试: 提取 50 章 EPUB 耗时 {elapsed_time:.2f}秒")

    def test_extract_chapters_performance(self, output_dir):
        """测试章节抽取的性能"""
        import extract_chapters

        # 创建包含 50 章的大型 EPUB
        large_epub = create_large_epub(chapter_count=50, output_path=get_test_output_path(output_dir, 'large_chapters.epub'))

        start_time = time.time()
        extract_chapters.extract_chapters(
            large_epub,
            output_dir,
            output_format='txt',
            separate=True
        )
        elapsed_time = time.time() - start_time

        # 验证文件已生成 - 统计 chapter_*.txt 文件
        file_count = count_files_in_dir(output_dir, 'chapter_*.txt')
        # 现在应该正好是 50 个章节文件(已排除 nav.xhtml)
        assert file_count == 50, f"期望 50 个章节文件,实际 {file_count} 个"

        # 性能断言
        assert elapsed_time < 15.0, \
            f"抽取 50 章耗时 {elapsed_time:.2f}秒,超过性能阈值 15秒"

        print(f"\n✓ 性能测试: 抽取 {file_count} 章为单独文件耗时 {elapsed_time:.2f}秒")

    def test_merge_performance(self, output_dir):
        """测试合并多个 EPUB 的性能"""
        import merge_epubs

        # 创建 10 个测试 EPUB
        epub_files = []
        for i in range(10):
            epub_path = get_test_output_path(output_dir, f'book_{i}.epub')
            create_simple_epub(
                title=f'Book {i}',
                chapters=[
                    {'title': f'Chapter {i}', 'content': f'<p>Content {i}</p>'}
                ],
                output_path=epub_path
            )
            epub_files.append(epub_path)

        output_epub = get_test_output_path(output_dir, 'merged.epub')

        start_time = time.time()
        merge_epubs.merge_epubs(epub_files, output_epub)
        elapsed_time = time.time() - start_time

        # 验证合并成功
        assert Path(output_epub).exists()

        # 性能断言
        assert elapsed_time < 5.0, \
            f"合并 10 个 EPUB 耗时 {elapsed_time:.2f}秒,超过性能阈值 5秒"

        print(f"\n✓ 性能测试: 合并 10 个 EPUB 耗时 {elapsed_time:.2f}秒")

    def test_metadata_extraction_performance(self, output_dir):
        """测试元数据提取的性能"""
        import extract_metadata

        # 创建大型 EPUB
        large_epub = create_large_epub(chapter_count=100, output_path=get_test_output_path(output_dir, 'large_meta.epub'))

        start_time = time.time()
        metadata = extract_metadata.extract_metadata(large_epub)
        elapsed_time = time.time() - start_time

        # 验证结果 - 章节数应该至少为 100 (可能包含导航文件)
        assert metadata['chapters_count'] >= 100

        # 性能断言
        assert elapsed_time < 5.0, \
            f"提取元数据耗时 {elapsed_time:.2f}秒,超过性能阈值 5秒"

        print(f"\n✓ 性能测试: 提取元数据({metadata['chapters_count']}章)耗时 {elapsed_time:.2f}秒")


class TestStress:
    """压力测试 - 测试极限情况"""

    def test_very_large_epub(self, output_dir):
        """测试处理非常大的 EPUB"""
        import extract_text

        # 创建包含 100 章的超大 EPUB
        huge_epub = create_large_epub(chapter_count=100, output_path=get_test_output_path(output_dir, 'huge.epub'))

        # 应该能够成功处理而不崩溃
        text = extract_text.extract_text_from_epub(huge_epub)
        assert len(text) > 0

        print(f"\n✓ 压力测试: 成功处理 100 章的 EPUB")

    def test_batch_process(self, output_dir):
        """测试批量处理多个 EPUB"""
        import extract_metadata

        # 创建 20 个测试 EPUB
        epub_files = []
        for i in range(20):
            epub_path = get_test_output_path(output_dir, f'batch_{i}.epub')
            create_simple_epub(
                title=f'Batch Book {i}',
                output_path=epub_path
            )
            epub_files.append(epub_path)

        # 批量处理
        start_time = time.time()
        results = []
        for epub_file in epub_files:
            metadata = extract_metadata.extract_metadata(epub_file)
            results.append(metadata)
        elapsed_time = time.time() - start_time

        # 验证所有处理成功
        assert len(results) == 20

        print(f"\n✓ 压力测试: 批量处理 20 个 EPUB,平均每个耗时 {elapsed_time/20:.3f}秒")

    def test_rapid_sequential_operations(self, output_dir):
        """测试快速连续操作"""
        import extract_chapters

        # 创建测试 EPUB
        test_epub = get_test_output_path(output_dir, 'rapid.epub')
        create_simple_epub(output_path=test_epub)

        # 快速连续执行多次操作
        iterations = 10
        start_time = time.time()

        for i in range(iterations):
            output_subdir = Path(output_dir) / f'rapid_{i}'
            output_subdir.mkdir(parents=True, exist_ok=True)
            extract_chapters.extract_chapters(
                test_epub,
                str(output_subdir),
                output_format='txt'
            )

        elapsed_time = time.time() - start_time

        # 验证所有操作都成功完成
        for i in range(iterations):
            output_subdir = Path(output_dir) / f'rapid_{i}'
            output_file = output_subdir / 'chapters.txt'
            assert output_file.exists()

        print(f"\n✓ 压力测试: 快速连续执行 {iterations} 次操作,总耗时 {elapsed_time:.2f}秒")

    def test_memory_efficiency(self, output_dir):
        """测试内存效率"""
        import extract_text
        import tracemalloc

        # 创建大型 EPUB
        large_epub = create_large_epub(chapter_count=50, output_path=get_test_output_path(output_dir, 'memory.epub'))

        # 开始内存跟踪
        tracemalloc.start()

        # 执行操作
        text = extract_text.extract_text_from_epub(large_epub)

        # 获取内存使用
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # 验证结果
        assert len(text) > 0

        # 内存使用应该在合理范围内(例如 100MB)
        peak_mb = peak / 1024 / 1024
        assert peak_mb < 100, \
            f"内存使用峰值 {peak_mb:.1f}MB,超过阈值 100MB"

        print(f"\n✓ 内存测试: 处理 50 章使用峰值内存 {peak_mb:.1f}MB")


class TestEdgeCases:
    """边缘情况测试"""

    def test_empty_epub(self, output_dir):
        """测试处理空 EPUB"""
        empty_epub = Path(output_dir) / 'empty.epub'
        book = epub.EpubBook()
        book.set_identifier('empty')
        book.set_title('Empty Book')
        book.set_language('en')

        # 添加必要的导航文件,即使没有内容
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # 设置空的 spine
        book.spine = ['nav']

        epub.write_epub(str(empty_epub), book)

        # 应该能够处理而不崩溃
        import extract_metadata
        metadata = extract_metadata.extract_metadata(str(empty_epub))
        assert metadata['title'] == 'Empty Book'
        # 空书可能有 1 个 nav.xhtml 文件被计数为章节,这是正常的
        assert metadata['chapters_count'] <= 1

    def test_special_characters_in_metadata(self, output_dir):
        """测试元数据中的特殊字符"""
        special_epub = create_simple_epub(
            title='《测试》"特殊" & <字符> [书籍]',
            author='作者©™®',
            output_path=get_test_output_path(output_dir, 'special.epub')
        )

        import extract_metadata
        metadata = extract_metadata.extract_metadata(special_epub)

        assert '《测试》' in metadata['title']
        assert '作者' in metadata['authors'][0]

    def test_very_long_chapter_content(self, output_dir):
        """测试处理非常长的章节"""
        # 创建包含大量内容的章节
        long_content = '<p>' + '测试内容 ' * 10000 + '</p>'

        long_epub = create_simple_epub(
            chapters=[
                {'title': '长章节', 'content': long_content}
            ],
            output_path=get_test_output_path(output_dir, 'long.epub')
        )

        import extract_text
        text = extract_text.extract_text_from_epub(long_epub)

        assert len(text) > 50000  # 应该非常长

    def test_unicode_content(self, output_dir):
        """测试处理 Unicode 内容"""
        unicode_epub = create_simple_epub(
            chapters=[
                {
                    'title': 'Unicode 测试',
                    'content': '''
                        <h1>多种语言</h1>
                        <p>English: Hello World</p>
                        <p>中文: 你好世界</p>
                        <p>日本語: こんにちは</p>
                        <p>한국어: 안녕하세요</p>
                        <p>Русский: Привет мир</p>
                        <p>العربية: مرحبا بالعالم</p>
                        <p>Emoji: 😀🎉🚀💻</p>
                    '''
                }
            ],
            output_path=get_test_output_path(output_dir, 'unicode.epub')
        )

        import extract_text
        text = extract_text.extract_text_from_epub(unicode_epub)

        # 验证各种语言都被正确提取
        assert '你好世界' in text
        assert 'こんにちは' in text
        assert '안녕하세요' in text
        assert '😀' in text
