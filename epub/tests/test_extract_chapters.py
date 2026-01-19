"""
测试 extract_chapters.py 脚本

使用 pytest 风格的测试,测试章节抽取功能。
"""
import sys
import pytest
from pathlib import Path
from io import StringIO
from contextlib import redirect_stdout

import extract_chapters


def assert_file_exists(path, msg=None):
    """断言文件存在"""
    path_obj = Path(path)
    if not path_obj.exists():
        if msg is None:
            msg = f"文件不存在: {path}"
        pytest.fail(msg)


def assert_file_not_empty(path, msg=None):
    """断言文件非空"""
    assert_file_exists(path)
    if path_obj := Path(path):
        if path_obj.stat().st_size == 0:
            if msg is None:
                msg = f"文件为空: {path}"
            pytest.fail(msg)


def assert_file_contains(path, text, msg=None):
    """断言文件包含指定文本"""
    assert_file_exists(path)
    content = Path(path).read_text(encoding='utf-8')
    if text not in content:
        if msg is None:
            msg = f"文件 {path} 不包含文本: {text}"
        pytest.fail(msg)


def count_files_in_dir(directory):
    """计算目录中的文件数量"""
    dir_path = Path(directory)
    return len([f for f in dir_path.iterdir() if f.is_file()])


class TestExtractChapters:
    """测试章节抽取功能"""

    def test_extract_chapters_txt_format(self, test_epub, output_dir):
        """测试提取为文本格式"""
        extract_chapters.extract_chapters(
            str(test_epub),
            output_dir,
            output_format='txt'
        )

        # 应该生成单个文件
        output_file = Path(output_dir) / 'chapters.txt'
        assert_file_exists(output_file)
        assert_file_not_empty(output_file)

    def test_extract_chapters_md_format(self, test_epub, output_dir):
        """测试提取为 Markdown 格式"""
        extract_chapters.extract_chapters(
            str(test_epub),
            output_dir,
            output_format='md'
        )

        output_file = Path(output_dir) / 'chapters.md'
        assert_file_exists(output_file)
        assert_file_not_empty(output_file)
        assert_file_contains(output_file, '#')

    def test_extract_chapters_html_format(self, test_epub, output_dir):
        """测试提取为 HTML 格式"""
        extract_chapters.extract_chapters(
            str(test_epub),
            output_dir,
            output_format='html'
        )

        output_file = Path(output_dir) / 'chapters.html'
        assert_file_exists(output_file)
        assert_file_not_empty(output_file)
        assert_file_contains(output_file, '<!DOCTYPE html>')

    def test_extract_chapters_separate_files(self, test_epub, output_dir):
        """测试提取为单独文件"""
        extract_chapters.extract_chapters(
            str(test_epub),
            output_dir,
            output_format='txt',
            separate=True
        )

        # 应该生成章节文件
        assert_file_exists(Path(output_dir) / 'chapter_001.txt')
        assert_file_exists(Path(output_dir) / 'chapter_002.txt')
        assert_file_exists(Path(output_dir) / 'chapter_003.txt')

        file_count = count_files_in_dir(output_dir)
        assert file_count > 0

    def test_extract_chapters_with_metadata(self, test_epub, output_dir):
        """测试包含元数据的提取"""
        extract_chapters.extract_chapters(
            str(test_epub),
            output_dir,
            output_format='txt',
            include_metadata=True
        )

        output_file = Path(output_dir) / 'chapters.txt'
        assert_file_contains(output_file, '书名:')
        assert_file_contains(output_file, '测试书籍')
        assert_file_contains(output_file, '作者:')
        assert_file_contains(output_file, '测试作者')

    def test_extract_chapters_with_toc(self, test_epub, output_dir):
        """测试生成目录"""
        extract_chapters.extract_chapters(
            str(test_epub),
            output_dir,
            output_format='txt',
            generate_toc=True
        )

        toc_file = Path(output_dir) / 'TOC.txt'
        assert_file_exists(toc_file)
        assert_file_not_empty(toc_file)
        assert_file_contains(toc_file, '目录')

    def test_extract_chapters_preserves_chapter_content(self, test_epub, output_dir):
        """测试保留章节内容"""
        extract_chapters.extract_chapters(
            str(test_epub),
            output_dir,
            output_format='md',
            separate=True
        )

        # 检查第一章内容
        chapter_01 = Path(output_dir) / 'chapter_001.md'
        assert_file_contains(chapter_01, '第一章')

    def test_extract_chapters_title_extraction(self):
        """测试标题提取功能"""
        # 测试从 HTML 中提取标题
        html_content = '<h1>测试标题</h1><p>内容</p>'
        title = extract_chapters.extract_chapter_title(html_content, '默认标题')

        assert title == '测试标题'

    def test_extract_chapters_title_extraction_with_fallback(self):
        """测试标题提取回退到默认值"""
        # 测试没有标题标签的 HTML
        html_content = '<p>只有内容,没有标题</p>'
        title = extract_chapters.extract_chapter_title(html_content, '默认标题')

        assert title == '默认标题'


class TestExtractChaptersCLI:
    """测试 extract_chapters 命令行接口"""

    def test_main_basic_usage(self, test_epub, output_dir):
        """测试基本命令行用法"""
        output = StringIO()
        with redirect_stdout(output):
            sys.argv = ['extract_chapters.py', str(test_epub), output_dir]
            try:
                extract_chapters.main()
            except SystemExit as e:
                if e.code != 0:
                    raise

        output_text = output.getvalue()
        assert '完成!' in output_text
        assert '总章节数:' in output_text

    def test_main_with_format_option(self, test_epub, output_dir):
        """测试 --format 选项"""
        output = StringIO()
        with redirect_stdout(output):
            sys.argv = [
                'extract_chapters.py',
                str(test_epub),
                output_dir,
                '--format', 'md'
            ]
            try:
                extract_chapters.main()
            except SystemExit as e:
                if e.code != 0:
                    raise

        output_file = Path(output_dir) / 'chapters.md'
        assert_file_exists(output_file)

    def test_main_with_separate_option(self, test_epub, output_dir):
        """测试 --separate 选项"""
        output = StringIO()
        with redirect_stdout(output):
            sys.argv = [
                'extract_chapters.py',
                str(test_epub),
                output_dir,
                '--separate'
            ]
            try:
                extract_chapters.main()
            except SystemExit as e:
                if e.code != 0:
                    raise

        # 应该有多个章节文件
        file_count = count_files_in_dir(output_dir)
        assert file_count > 0

    def test_main_with_multiple_options(self, test_epub, output_dir):
        """测试多个选项组合"""
        output = StringIO()
        with redirect_stdout(output):
            sys.argv = [
                'extract_chapters.py',
                str(test_epub),
                output_dir,
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
        assert_file_exists(Path(output_dir) / 'chapter_001.html')
        assert_file_exists(Path(output_dir) / 'TOC.txt')

    def test_main_shows_help(self):
        """测试显示帮助信息"""
        output = StringIO()
        with redirect_stdout(output):
            sys.argv = ['extract_chapters.py', '--help']
            try:
                extract_chapters.main()
            except SystemExit:
                # 帮助信息会退出
                pass

        output_text = output.getvalue()
        assert 'usage:' in output_text
        assert '--format' in output_text
        assert '--separate' in output_text
