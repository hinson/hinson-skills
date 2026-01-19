"""
性能和压力测试

测试 EPUB 技能脚本在处理大型文件和批量操作时的性能表现。
"""
import unittest
import sys
import os
import time
from pathlib import Path

# 添加脚本目录到路径
SCRIPTS_DIR = Path(__file__).parent.parent / 'scripts'
sys.path.insert(0, str(SCRIPTS_DIR))

from .conftest import EPUBTestCase
from .test_helpers import create_large_epub


class TestPerformance(EPUBTestCase):
    """性能测试"""

    def test_extract_text_performance_large_epub(self):
        """测试从大型 EPUB 中提取文本的性能"""
        import extract_text

        # 创建包含 50 章的大型 EPUB
        large_epub = create_large_epub(chapter_count=50, output_path=self.get_test_output_path('large.epub'))

        start_time = time.time()
        text = extract_text.extract_text_from_epub(large_epub)
        elapsed_time = time.time() - start_time

        # 验证结果
        self.assertGreater(len(text), 0)

        # 性能断言: 50 章应该在合理时间内完成(例如 10 秒)
        # 这是性能基准测试,实际阈值可以根据系统性能调整
        self.assertLess(elapsed_time, 10.0,
                       f"提取文本耗时 {elapsed_time:.2f}秒,超过性能阈值 10秒")

        print(f"\n✓ 性能测试: 提取 50 章 EPUB 耗时 {elapsed_time:.2f}秒")

    def test_extract_chapters_performance(self):
        """测试章节抽取的性能"""
        import extract_chapters

        # 创建包含 50 章的大型 EPUB
        large_epub = create_large_epub(chapter_count=50, output_path=self.get_test_output_path('large_chapters.epub'))

        start_time = time.time()
        extract_chapters.extract_chapters(
            large_epub,
            self.output_dir,
            output_format='txt',
            separate=True
        )
        elapsed_time = time.time() - start_time

        # 验证文件已生成
        file_count = self.count_files_in_dir(self.output_dir)
        self.assertEqual(file_count, 50)

        # 性能断言
        self.assertLess(elapsed_time, 15.0,
                       f"抽取 50 章耗时 {elapsed_time:.2f}秒,超过性能阈值 15秒")

        print(f"\n✓ 性能测试: 抽取 50 章为单独文件耗时 {elapsed_time:.2f}秒")

    def test_merge_performance(self):
        """测试合并多个 EPUB 的性能"""
        import merge_epubs

        # 创建 10 个测试 EPUB
        epub_files = []
        for i in range(10):
            epub_path = self.get_test_output_path(f'book_{i}.epub')
            from .test_helpers import create_simple_epub
            create_simple_epub(
                title=f'Book {i}',
                chapters=[
                    {'title': f'Chapter {i}', 'content': f'<p>Content {i}</p>'}
                ],
                output_path=epub_path
            )
            epub_files.append(epub_path)

        output_epub = self.get_test_output_path('merged.epub')

        start_time = time.time()
        merge_epubs.merge_epubs(epub_files, output_epub)
        elapsed_time = time.time() - start_time

        # 验证合并成功
        self.assertFileExists(output_epub)

        # 性能断言
        self.assertLess(elapsed_time, 5.0,
                       f"合并 10 个 EPUB 耗时 {elapsed_time:.2f}秒,超过性能阈值 5秒")

        print(f"\n✓ 性能测试: 合并 10 个 EPUB 耗时 {elapsed_time:.2f}秒")

    def test_metadata_extraction_performance(self):
        """测试元数据提取的性能"""
        import extract_metadata

        # 创建大型 EPUB
        large_epub = create_large_epub(chapter_count=100, output_path=self.get_test_output_path('large_meta.epub'))

        start_time = time.time()
        metadata = extract_metadata.extract_metadata(large_epub)
        elapsed_time = time.time() - start_time

        # 验证结果
        self.assertEqual(metadata['chapters_count'], 100)

        # 性能断言
        self.assertLess(elapsed_time, 5.0,
                       f"提取元数据耗时 {elapsed_time:.2f}秒,超过性能阈值 5秒")

        print(f"\n✓ 性能测试: 提取元数据(100章)耗时 {elapsed_time:.2f}秒")


class TestStress(EPUBTestCase):
    """压力测试 - 测试极限情况"""

    def test_very_large_epub(self):
        """测试处理非常大的 EPUB"""
        import extract_text

        # 创建包含 100 章的超大 EPUB
        huge_epub = create_large_epub(chapter_count=100, output_path=self.get_test_output_path('huge.epub'))

        # 应该能够成功处理而不崩溃
        text = extract_text.extract_text_from_epub(huge_epub)
        self.assertGreater(len(text), 0)

        print(f"\n✓ 压力测试: 成功处理 100 章的 EPUB")

    def test_batch_process(self):
        """测试批量处理多个 EPUB"""
        import extract_metadata

        # 创建 20 个测试 EPUB
        epub_files = []
        for i in range(20):
            epub_path = self.get_test_output_path(f'batch_{i}.epub')
            from .test_helpers import create_simple_epub
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
        self.assertEqual(len(results), 20)

        print(f"\n✓ 压力测试: 批量处理 20 个 EPUB,平均每个耗时 {elapsed_time/20:.3f}秒")

    def test_rapid_sequential_operations(self):
        """测试快速连续操作"""
        import extract_chapters

        # 创建测试 EPUB
        test_epub = self.get_test_output_path('rapid.epub')
        from .test_helpers import create_simple_epub
        create_simple_epub(output_path=test_epub)

        # 快速连续执行多次操作
        iterations = 10
        start_time = time.time()

        for i in range(iterations):
            output_dir = self.get_test_output_path(f'rapid_{i}')
            os.makedirs(output_dir)
            extract_chapters.extract_chapters(
                test_epub,
                output_dir,
                output_format='txt'
            )

        elapsed_time = time.time() - start_time

        # 验证所有操作都成功完成
        for i in range(iterations):
            output_dir = self.get_test_output_path(f'rapid_{i}')
            output_file = os.path.join(output_dir, 'chapters.txt')
            self.assertFileExists(output_file)

        print(f"\n✓ 压力测试: 快速连续执行 {iterations} 次操作,总耗时 {elapsed_time:.2f}秒")

    def test_memory_efficiency(self):
        """测试内存效率"""
        import extract_text
        import tracemalloc

        # 创建大型 EPUB
        large_epub = create_large_epub(chapter_count=50, output_path=self.get_test_output_path('memory.epub'))

        # 开始内存跟踪
        tracemalloc.start()

        # 执行操作
        text = extract_text.extract_text_from_epub(large_epub)

        # 获取内存使用
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # 验证结果
        self.assertGreater(len(text), 0)

        # 内存使用应该在合理范围内(例如 100MB)
        peak_mb = peak / 1024 / 1024
        self.assertLess(peak_mb, 100,
                       f"内存使用峰值 {peak_mb:.1f}MB,超过阈值 100MB")

        print(f"\n✓ 内存测试: 处理 50 章使用峰值内存 {peak_mb:.1f}MB")


class TestEdgeCases(EPUBTestCase):
    """边缘情况测试"""

    def test_empty_epub(self):
        """测试处理空 EPUB"""
        from ebooklib import epub

        empty_epub = self.get_test_output_path('empty.epub')
        book = epub.EpubBook()
        book.set_identifier('empty')
        book.set_title('Empty Book')
        book.set_language('en')
        epub.write_epub(empty_epub, book)

        # 应该能够处理而不崩溃
        import extract_metadata
        metadata = extract_metadata.extract_metadata(empty_epub)
        self.assertEqual(metadata['title'], 'Empty Book')

    def test_special_characters_in_metadata(self):
        """测试元数据中的特殊字符"""
        from .test_helpers import create_simple_epub

        special_epub = create_simple_epub(
            title='《测试》"特殊" & <字符> [书籍]',
            author='作者©™®',
            output_path=self.get_test_output_path('special.epub')
        )

        import extract_metadata
        metadata = extract_metadata.extract_metadata(special_epub)

        self.assertIn('《测试》', metadata['title'])
        self.assertIn('作者', metadata['authors'][0])

    def test_very_long_chapter_content(self):
        """测试处理非常长的章节"""
        from .test_helpers import create_simple_epub

        # 创建包含大量内容的章节
        long_content = '<p>' + '测试内容 ' * 10000 + '</p>'

        long_epub = create_simple_epub(
            chapters=[
                {'title': '长章节', 'content': long_content}
            ],
            output_path=self.get_test_output_path('long.epub')
        )

        import extract_text
        text = extract_text.extract_text_from_epub(long_epub)

        self.assertGreater(len(text), 50000)  # 应该非常长

    def test_unicode_content(self):
        """测试处理 Unicode 内容"""
        from .test_helpers import create_simple_epub

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
            output_path=self.get_test_output_path('unicode.epub')
        )

        import extract_text
        text = extract_text.extract_text_from_epub(unicode_epub)

        # 验证各种语言都被正确提取
        self.assertIn('你好世界', text)
        self.assertIn('こんにちは', text)
        self.assertIn('안녕하세요', text)
        self.assertIn('😀', text)


if __name__ == '__main__':
    unittest.main()
