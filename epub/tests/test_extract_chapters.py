"""
测试 extract_chapters.py 脚本
"""
import unittest
import sys
import os
from pathlib import Path
import tempfile

# 添加脚本目录到路径
SCRIPTS_DIR = Path(__file__).parent.parent / 'scripts'
sys.path.insert(0, str(SCRIPTS_DIR))

from .conftest import EPUBTestCase, skipIfNoTestEPUB


class TestExtractChapters(EPUBTestCase):
    """测试章节抽取功能"""

    @skipIfNoTestEPUB
    def test_extract_chapters_txt_format(self):
        """测试提取为文本格式"""
        import extract_chapters

        extract_chapters.extract_chapters(
            str(self.test_epub),
            self.output_dir,
            output_format='txt'
        )

        # 应该生成单个文件
        output_file = os.path.join(self.output_dir, 'chapters.txt')
        self.assertFileExists(output_file)
        self.assertFileNotEmpty(output_file)

    @skipIfNoTestEPUB
    def test_extract_chapters_md_format(self):
        """测试提取为 Markdown 格式"""
        import extract_chapters

        extract_chapters.extract_chapters(
            str(self.test_epub),
            self.output_dir,
            output_format='md'
        )

        output_file = os.path.join(self.output_dir, 'chapters.md')
        self.assertFileExists(output_file)
        self.assertFileNotEmpty(output_file)
        self.assertFileContains(output_file, '#')

    @skipIfNoTestEPUB
    def test_extract_chapters_html_format(self):
        """测试提取为 HTML 格式"""
        import extract_chapters

        extract_chapters.extract_chapters(
            str(self.test_epub),
            self.output_dir,
            output_format='html'
        )

        output_file = os.path.join(self.output_dir, 'chapters.html')
        self.assertFileExists(output_file)
        self.assertFileNotEmpty(output_file)
        self.assertFileContains(output_file, '<!DOCTYPE html>')

    @skipIfNoTestEPUB
    def test_extract_chapters_separate_files(self):
        """测试提取为单独文件"""
        import extract_chapters

        extract_chapters.extract_chapters(
            str(self.test_epub),
            self.output_dir,
            output_format='txt',
            separate=True
        )

        # 应该生成章节文件
        self.assertFileExists(os.path.join(self.output_dir, 'chapter_001.txt'))
        self.assertFileExists(os.path.join(self.output_dir, 'chapter_002.txt'))
        self.assertFileExists(os.path.join(self.output_dir, 'chapter_003.txt'))

        file_count = self.count_files_in_dir(self.output_dir)
        self.assertGreater(file_count, 0)

    @skipIfNoTestEPUB
    def test_extract_chapters_with_metadata(self):
        """测试包含元数据的提取"""
        import extract_chapters

        extract_chapters.extract_chapters(
            str(self.test_epub),
            self.output_dir,
            output_format='txt',
            include_metadata=True
        )

        output_file = os.path.join(self.output_dir, 'chapters.txt')
        self.assertFileContains(output_file, '书名:')
        self.assertFileContains(output_file, '测试书籍')
        self.assertFileContains(output_file, '作者:')
        self.assertFileContains(output_file, '测试作者')

    @skipIfNoTestEPUB
    def test_extract_chapters_with_toc(self):
        """测试生成目录"""
        import extract_chapters

        extract_chapters.extract_chapters(
            str(self.test_epub),
            self.output_dir,
            output_format='txt',
            generate_toc=True
        )

        toc_file = os.path.join(self.output_dir, 'TOC.txt')
        self.assertFileExists(toc_file)
        self.assertFileNotEmpty(toc_file)
        self.assertFileContains(toc_file, '目录')

    @skipIfNoTestEPUB
    def test_extract_chapters_preserves_chapter_content(self):
        """测试保留章节内容"""
        import extract_chapters

        extract_chapters.extract_chapters(
            str(self.test_epub),
            self.output_dir,
            output_format='md',
            separate=True
        )

        # 检查第一章内容
        chapter_01 = os.path.join(self.output_dir, 'chapter_001.md')
        self.assertFileContains(chapter_01, '第一章')

    @skipIfNoTestEPUB
    def test_extract_chapters_title_extraction(self):
        """测试标题提取功能"""
        import extract_chapters

        # 测试从 HTML 中提取标题
        html_content = '<h1>测试标题</h1><p>内容</p>'
        title = extract_chapters.extract_chapter_title(html_content, '默认标题')

        self.assertEqual(title, '测试标题')

    @skipIfNoTestEPUB
    def test_extract_chapters_title_extraction_with_fallback(self):
        """测试标题提取回退到默认值"""
        import extract_chapters

        # 测试没有标题标签的 HTML
        html_content = '<p>只有内容,没有标题</p>'
        title = extract_chapters.extract_chapter_title(html_content, '默认标题')

        self.assertEqual(title, '默认标题')


class TestExtractChaptersCLI(EPUBTestCase):
    """测试 extract_chapters 命令行接口"""

    @skipIfNoTestEPUB
    def test_main_basic_usage(self):
        """测试基本命令行用法"""
        import extract_chapters
        import io
        from contextlib import redirect_stdout

        output = io.StringIO()
        with redirect_stdout(output):
            sys.argv = ['extract_chapters.py', str(self.test_epub), self.output_dir]
            try:
                extract_chapters.main()
            except SystemExit as e:
                if e.code != 0:
                    raise

        output_text = output.getvalue()
        self.assertIn('完成!', output_text)
        self.assertIn('总章节数:', output_text)

    @skipIfNoTestEPUB
    def test_main_with_format_option(self):
        """测试 --format 选项"""
        import extract_chapters
        import io
        from contextlib import redirect_stdout

        output = io.StringIO()
        with redirect_stdout(output):
            sys.argv = [
                'extract_chapters.py',
                str(self.test_epub),
                self.output_dir,
                '--format', 'md'
            ]
            try:
                extract_chapters.main()
            except SystemExit as e:
                if e.code != 0:
                    raise

        output_file = os.path.join(self.output_dir, 'chapters.md')
        self.assertFileExists(output_file)

    @skipIfNoTestEPUB
    def test_main_with_separate_option(self):
        """测试 --separate 选项"""
        import extract_chapters
        import io
        from contextlib import redirect_stdout

        output = io.StringIO()
        with redirect_stdout(output):
            sys.argv = [
                'extract_chapters.py',
                str(self.test_epub),
                self.output_dir,
                '--separate'
            ]
            try:
                extract_chapters.main()
            except SystemExit as e:
                if e.code != 0:
                    raise

        # 应该有多个章节文件
        file_count = self.count_files_in_dir(self.output_dir)
        self.assertGreater(file_count, 0)

    @skipIfNoTestEPUB
    def test_main_with_multiple_options(self):
        """测试多个选项组合"""
        import extract_chapters
        import io
        from contextlib import redirect_stdout

        output = io.StringIO()
        with redirect_stdout(output):
            sys.argv = [
                'extract_chapters.py',
                str(self.test_epub),
                self.output_dir,
                '--format', 'html',
                '--separate',
                '--toc',
                '--metadata'
            ]
            try:
                extract_chapters.main()
            except SystemExit as e:
                if e.code != 0:
                    raise

        # 验证生成的文件
        self.assertFileExists(os.path.join(self.output_dir, 'chapter_001.html'))
        self.assertFileExists(os.path.join(self.output_dir, 'TOC.txt'))

    def test_main_shows_help(self):
        """测试显示帮助信息"""
        import extract_chapters
        import io
        from contextlib import redirect_stdout

        output = io.StringIO()
        with redirect_stdout(output):
            sys.argv = ['extract_chapters.py', '--help']
            try:
                extract_chapters.main()
            except SystemExit as e:
                # 帮助信息会退出
                pass

        output_text = output.getvalue()
        self.assertIn('usage:', output_text)
        self.assertIn('--format', output_text)
        self.assertIn('--separate', output_text)


if __name__ == '__main__':
    unittest.main()
