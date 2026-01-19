"""
测试 extract_metadata.py 脚本

使用 pytest 风格的测试,测试元数据提取功能。
"""
import sys
import tempfile
import json
import pytest
from pathlib import Path
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

import extract_metadata
from .test_helpers import create_simple_epub


class TestExtractMetadata:
    """测试元数据提取功能"""

    def test_extract_metadata_from_valid_epub(self, test_epub):
        """测试从有效的 EPUB 文件中提取元数据"""
        metadata = extract_metadata.extract_metadata(str(test_epub))

        # 验证必需字段存在
        assert metadata is not None
        assert 'title' in metadata
        assert 'authors' in metadata
        assert 'language' in metadata
        assert 'file' in metadata

    def test_extract_metadata_returns_correct_title(self, test_epub):
        """测试正确提取书名"""
        metadata = extract_metadata.extract_metadata(str(test_epub))

        assert metadata['title'] == '测试书籍'

    def test_extract_metadata_returns_correct_author(self, test_epub):
        """测试正确提取作者"""
        metadata = extract_metadata.extract_metadata(str(test_epub))

        assert len(metadata['authors']) == 1
        assert metadata['authors'][0] == '测试作者'

    def test_extract_metadata_counts_chapters(self, test_epub):
        """测试正确统计章节数"""
        metadata = extract_metadata.extract_metadata(str(test_epub))

        # 我们创建的测试书有章节
        assert metadata['chapters_count'] > 0

    def test_extract_metadata_handles_invalid_file(self):
        """测试处理无效的 EPUB 文件"""
        # 创建一个无效的 EPUB 文件
        invalid_epub = tempfile.mktemp(suffix='.epub')
        Path(invalid_epub).write_text('Not a valid EPUB')

        # 核心函数现在抛出 RuntimeError 而不是 SystemExit
        with pytest.raises(RuntimeError, match="无法读取 EPUB 文件"):
            extract_metadata.extract_metadata(invalid_epub)

        Path(invalid_epub).unlink()

    def test_extract_metadata_handles_missing_file(self):
        """测试处理不存在的文件"""
        # 核心函数现在抛出 RuntimeError 而不是 SystemExit
        with pytest.raises(RuntimeError, match="无法读取 EPUB 文件"):
            extract_metadata.extract_metadata('/nonexistent/file.epub')


class TestExtractMetadataCLI:
    """测试 extract_metadata 命令行接口"""

    def test_main_with_valid_file(self, test_epub):
        """测试主函数处理有效文件"""
        # 捕获输出
        output = StringIO()
        with redirect_stdout(output):
            sys.argv = ['extract_metadata.py', str(test_epub)]
            try:
                extract_metadata.main()
            except SystemExit as e:
                if e.code != 0:
                    raise

        output_text = output.getvalue()
        assert '书名:' in output_text
        assert '测试书籍' in output_text
        assert '作者:' in output_text
        assert '章节数:' in output_text

    def test_main_shows_json_output(self, test_epub):
        """测试主函数输出 JSON 格式"""
        output = StringIO()
        with redirect_stdout(output):
            sys.argv = ['extract_metadata.py', str(test_epub)]
            try:
                extract_metadata.main()
            except SystemExit as e:
                if e.code != 0:
                    raise

        output_text = output.getvalue()

        # 验证 JSON 部分
        json_start = output_text.find('JSON 格式:')
        assert json_start > 0

        # 尝试解析 JSON
        json_section = output_text[json_start:]
        json_lines = json_section.split('\n', 1)[1]  # 跳过 "JSON 格式:" 行

        try:
            data = json.loads(json_lines)
            assert data['title'] == '测试书籍'
        except json.JSONDecodeError as e:
            pytest.fail(f"无法解析 JSON 输出: {e}")

    def test_main_with_no_arguments(self):
        """测试没有参数时显示帮助"""
        error = StringIO()
        with redirect_stderr(error):
            sys.argv = ['extract_metadata.py']
            try:
                extract_metadata.main()
            except SystemExit:
                # 应该退出并显示错误
                pass

        error_text = error.getvalue()
        assert '使用方法' in error_text
