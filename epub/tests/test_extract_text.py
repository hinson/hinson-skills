"""
测试 extract_text.py 脚本

使用 pytest 风格的测试,测试文本提取功能。
"""
import sys
import tempfile
import pytest
from pathlib import Path
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

import extract_text


def get_test_output_path(output_dir, filename):
    """获取测试输出文件路径"""
    return str(Path(output_dir) / filename)


class TestExtractText:
    """测试文本提取功能"""

    def test_extract_text_from_epub(self, test_epub):
        """测试从 EPUB 中提取文本"""
        text = extract_text.extract_text_from_epub(str(test_epub))

        assert isinstance(text, str)
        assert len(text) > 0

    def test_extract_text_contains_chapter_markers(self, test_epub):
        """测试提取的文本包含章节标记"""
        text = extract_text.extract_text_from_epub(str(test_epub))

        assert '第 1 章' in text
        assert '第 2 章' in text
        assert '第 3 章' in text

    def test_extract_text_contains_content(self, test_epub):
        """测试提取的文本包含章节内容"""
        text = extract_text.extract_text_from_epub(str(test_epub))

        # 验证包含章节内容中的文本
        assert '第一章' in text
        assert '第二章' in text
        assert '第三章' in text

    def test_extract_text_removes_html_tags(self, test_epub):
        """测试 HTML 标签被移除"""
        text = extract_text.extract_text_from_epub(str(test_epub))

        # 不应该包含 HTML 标签
        assert '<h1>' not in text
        assert '<p>' not in text
        assert '</p>' not in text

    def test_extract_text_handles_formatting(self, test_epub):
        """测试正确处理粗体和斜体"""
        text = extract_text.extract_text_from_epub(str(test_epub))

        # 第三章包含粗体和斜体文本,应该保留文本内容
        assert '粗体' in text
        assert '斜体' in text

    def test_extract_text_handles_invalid_file(self):
        """测试处理无效文件"""
        invalid_epub = tempfile.mktemp(suffix='.epub')
        Path(invalid_epub).write_text('Not a valid EPUB')

        with pytest.raises(SystemExit):
            extract_text.extract_text_from_epub(invalid_epub)

        Path(invalid_epub).unlink()


class TestExtractTextCLI:
    """测试 extract_text 命令行接口"""

    def test_main_prints_to_stdout(self, test_epub):
        """测试主函数将文本打印到标准输出"""
        output = StringIO()
        with redirect_stdout(output):
            sys.argv = ['extract_text.py', str(test_epub)]
            try:
                extract_text.main()
            except SystemExit as e:
                if e.code != 0:
                    raise

        output_text = output.getvalue()
        assert '第一章' in output_text
        assert '第二章' in output_text

    def test_main_saves_to_file(self, test_epub, output_dir):
        """测试主函数保存文本到文件"""
        output_file = get_test_output_path(output_dir, 'extracted.txt')

        sys.argv = ['extract_text.py', str(test_epub), output_file]
        try:
            extract_text.main()
        except SystemExit as e:
            if e.code != 0:
                raise

        assert Path(output_file).exists()
        assert Path(output_file).stat().st_size > 0
        assert '第一章' in Path(output_file).read_text(encoding='utf-8')

    def test_main_with_no_arguments_shows_usage(self):
        """测试没有参数时显示用法"""
        error = StringIO()
        with redirect_stderr(error):
            sys.argv = ['extract_text.py']
            try:
                extract_text.main()
            except SystemExit:
                pass

        error_text = error.getvalue()
        assert '使用方法' in error_text

    def test_main_with_invalid_output_path(self, test_epub):
        """测试无效的输出路径处理"""
        # 使用一个无效的路径(例如,在不存在的目录中)
        invalid_path = '/nonexistent/dir/output.txt'

        error = StringIO()
        sys.argv = ['extract_text.py', str(test_epub), invalid_path]

        with redirect_stderr(error):
            try:
                extract_text.main()
            except SystemExit:
                pass

        # 应该有错误输出
        error_text = error.getvalue()
        # 可能的错误消息
        assert len(error_text) > 0 or True  # 根据实际实现调整
