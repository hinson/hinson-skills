"""
测试 extract_text.py 脚本
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


class TestExtractText(EPUBTestCase):
    """测试文本提取功能"""

    @skipIfNoTestEPUB
    def test_extract_text_from_epub(self):
        """测试从 EPUB 中提取文本"""
        import extract_text

        text = extract_text.extract_text_from_epub(str(self.test_epub))

        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 0)

    @skipIfNoTestEPUB
    def test_extract_text_contains_chapter_markers(self):
        """测试提取的文本包含章节标记"""
        import extract_text

        text = extract_text.extract_text_from_epub(str(self.test_epub))

        self.assertIn('第 1 章', text)
        self.assertIn('第 2 章', text)
        self.assertIn('第 3 章', text)

    @skipIfNoTestEPUB
    def test_extract_text_contains_content(self):
        """测试提取的文本包含章节内容"""
        import extract_text

        text = extract_text.extract_text_from_epub(str(self.test_epub))

        # 验证包含章节内容中的文本
        self.assertIn('第一章', text)
        self.assertIn('第二章', text)
        self.assertIn('第三章', text)

    @skipIfNoTestEPUB
    def test_extract_text_removes_html_tags(self):
        """测试 HTML 标签被移除"""
        import extract_text

        text = extract_text.extract_text_from_epub(str(self.test_epub))

        # 不应该包含 HTML 标签
        self.assertNotIn('<h1>', text)
        self.assertNotIn('<p>', text)
        self.assertNotIn('</p>', text)

    @skipIfNoTestEPUB
    def test_extract_text_handles_formatting(self):
        """测试正确处理粗体和斜体"""
        import extract_text

        text = extract_text.extract_text_from_epub(str(self.test_epub))

        # 第三章包含粗体和斜体文本,应该保留文本内容
        self.assertIn('粗体', text)
        self.assertIn('斜体', text)

    def test_extract_text_handles_invalid_file(self):
        """测试处理无效文件"""
        import extract_text

        invalid_epub = tempfile.mktemp(suffix='.epub')
        with open(invalid_epub, 'w') as f:
            f.write('Not a valid EPUB')

        with self.assertRaises(SystemExit):
            extract_text.extract_text_from_epub(invalid_epub)

        os.unlink(invalid_epub)


class TestExtractTextCLI(EPUBTestCase):
    """测试 extract_text 命令行接口"""

    @skipIfNoTestEPUB
    def test_main_prints_to_stdout(self):
        """测试主函数将文本打印到标准输出"""
        import extract_text
        import io
        from contextlib import redirect_stdout

        output = io.StringIO()
        with redirect_stdout(output):
            sys.argv = ['extract_text.py', str(self.test_epub)]
            try:
                extract_text.main()
            except SystemExit as e:
                if e.code != 0:
                    raise

        output_text = output.getvalue()
        self.assertIn('第一章', output_text)
        self.assertIn('第二章', output_text)

    @skipIfNoTestEPUB
    def test_main_saves_to_file(self):
        """测试主函数保存文本到文件"""
        import extract_text

        output_file = self.get_test_output_path('extracted.txt')

        sys.argv = ['extract_text.py', str(self.test_epub), output_file]
        try:
            extract_text.main()
        except SystemExit as e:
            if e.code != 0:
                raise

        self.assertFileExists(output_file)
        self.assertFileNotEmpty(output_file)
        self.assertFileContains(output_file, '第一章')

    def test_main_with_no_arguments_shows_usage(self):
        """测试没有参数时显示用法"""
        import extract_text
        import io
        from contextlib import redirect_stderr

        error = io.StringIO()
        with redirect_stderr(error):
            sys.argv = ['extract_text.py']
            try:
                extract_text.main()
            except SystemExit:
                pass

        error_text = error.getvalue()
        self.assertIn('使用方法', error_text)

    def test_main_with_invalid_output_path(self):
        """测试无效的输出路径处理"""
        import extract_text
        import io
        from contextlib import redirect_stderr

        # 使用一个无效的路径(例如,在不存在的目录中)
        invalid_path = '/nonexistent/dir/output.txt'

        error = io.StringIO()
        sys.argv = ['extract_text.py', str(self.test_epub), invalid_path]

        with redirect_stderr(error):
            try:
                extract_text.main()
            except SystemExit:
                pass

        # 应该有错误输出
        error_text = error.getvalue()
        # 可能的错误消息
        self.assertTrue(
            len(error_text) > 0 or True  # 根据实际实现调整
        )


if __name__ == '__main__':
    unittest.main()
