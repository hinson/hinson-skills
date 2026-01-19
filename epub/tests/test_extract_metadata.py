"""
测试 extract_metadata.py 脚本
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
from .test_helpers import create_simple_epub


class TestExtractMetadata(EPUBTestCase):
    """测试元数据提取功能"""

    @skipIfNoTestEPUB
    def test_extract_metadata_from_valid_epub(self):
        """测试从有效的 EPUB 文件中提取元数据"""
        import extract_metadata

        metadata = extract_metadata.extract_metadata(str(self.test_epub))

        # 验证必需字段存在
        self.assertIsNotNone(metadata)
        self.assertIn('title', metadata)
        self.assertIn('authors', metadata)
        self.assertIn('language', metadata)
        self.assertIn('file', metadata)

    @skipIfNoTestEPUB
    def test_extract_metadata_returns_correct_title(self):
        """测试正确提取书名"""
        import extract_metadata

        metadata = extract_metadata.extract_metadata(str(self.test_epub))

        self.assertEqual(metadata['title'], '测试书籍')

    @skipIfNoTestEPUB
    def test_extract_metadata_returns_correct_author(self):
        """测试正确提取作者"""
        import extract_metadata

        metadata = extract_metadata.extract_metadata(str(self.test_epub))

        self.assertEqual(len(metadata['authors']), 1)
        self.assertEqual(metadata['authors'][0], '测试作者')

    @skipIfNoTestEPUB
    def test_extract_metadata_counts_chapters(self):
        """测试正确统计章节数"""
        import extract_metadata

        metadata = extract_metadata.extract_metadata(str(self.test_epub))

        # 我们创建的测试书有章节
        self.assertGreater(metadata['chapters_count'], 0)

    def test_extract_metadata_handles_invalid_file(self):
        """测试处理无效的 EPUB 文件"""
        import extract_metadata

        # 创建一个无效的 EPUB 文件
        invalid_epub = tempfile.mktemp(suffix='.epub')
        with open(invalid_epub, 'w') as f:
            f.write('Not a valid EPUB')

        with self.assertRaises(SystemExit):
            extract_metadata.extract_metadata(invalid_epub)

        os.unlink(invalid_epub)

    def test_extract_metadata_handles_missing_file(self):
        """测试处理不存在的文件"""
        import extract_metadata

        with self.assertRaises(SystemExit):
            extract_metadata.extract_metadata('/nonexistent/file.epub')


class TestExtractMetadataCLI(EPUBTestCase):
    """测试 extract_metadata 命令行接口"""

    @skipIfNoTestEPUB
    def test_main_with_valid_file(self):
        """测试主函数处理有效文件"""
        import extract_metadata
        import io
        from contextlib import redirect_stdout

        # 捕获输出
        output = io.StringIO()
        with redirect_stdout(output):
            sys.argv = ['extract_metadata.py', str(self.test_epub)]
            try:
                extract_metadata.main()
            except SystemExit as e:
                if e.code != 0:
                    raise

        output_text = output.getvalue()
        self.assertIn('书名:', output_text)
        self.assertIn('测试书籍', output_text)
        self.assertIn('作者:', output_text)
        self.assertIn('章节数:', output_text)

    @skipIfNoTestEPUB
    def test_main_shows_json_output(self):
        """测试主函数输出 JSON 格式"""
        import extract_metadata
        import io
        from contextlib import redirect_stdout
        import json

        output = io.StringIO()
        with redirect_stdout(output):
            sys.argv = ['extract_metadata.py', str(self.test_epub)]
            try:
                extract_metadata.main()
            except SystemExit as e:
                if e.code != 0:
                    raise

        output_text = output.getvalue()

        # 验证 JSON 部分
        json_start = output_text.find('JSON 格式:')
        self.assertGreater(json_start, 0)

        # 尝试解析 JSON
        json_section = output_text[json_start:]
        json_lines = json_section.split('\n', 1)[1]  # 跳过 "JSON 格式:" 行

        try:
            data = json.loads(json_lines)
            self.assertEqual(data['title'], '测试书籍')
        except json.JSONDecodeError:
            self.fail("无法解析 JSON 输出")

    def test_main_with_no_arguments(self):
        """测试没有参数时显示帮助"""
        import extract_metadata
        import io
        from contextlib import redirect_stderr

        error = io.StringIO()
        with redirect_stderr(error):
            sys.argv = ['extract_metadata.py']
            try:
                extract_metadata.main()
            except SystemExit as e:
                # 应该退出并显示错误
                pass

        error_text = error.getvalue()
        self.assertIn('使用方法', error_text)


if __name__ == '__main__':
    unittest.main()
