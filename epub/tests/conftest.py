"""
测试配置和共享夹具

提供测试所需的共享资源、临时文件管理和测试数据。
"""
import unittest
import tempfile
import shutil
import os
import sys
from pathlib import Path

# 添加脚本目录到路径
SCRIPTS_DIR = Path(__file__).parent.parent / 'scripts'
sys.path.insert(0, str(SCRIPTS_DIR))


class EPUBTestCase(unittest.TestCase):
    """EPUB 测试基类,提供共享的测试工具"""

    def setUp(self):
        """每个测试前的设置"""
        # 创建临时目录
        self.test_dir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.test_dir, 'output')
        os.makedirs(self.output_dir)

        # 测试 EPUB 路径
        self.fixture_dir = Path(__file__).parent / 'fixtures'
        self.test_epub = self.fixture_dir / 'test_book.epub'

    def tearDown(self):
        """每个测试后的清理"""
        # 删除临时目录
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def get_test_output_path(self, filename):
        """获取测试输出文件路径"""
        return os.path.join(self.output_dir, filename)

    def assertFileExists(self, path, msg=None):
        """断言文件存在"""
        if not os.path.exists(path):
            if msg is None:
                msg = f"文件不存在: {path}"
            self.fail(msg)

    def assertFileNotEmpty(self, path, msg=None):
        """断言文件非空"""
        self.assertFileExists(path)
        if os.path.getsize(path) == 0:
            if msg is None:
                msg = f"文件为空: {path}"
            self.fail(msg)

    def assertFileContains(self, path, text, msg=None):
        """断言文件包含指定文本"""
        self.assertFileExists(path)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if text not in content:
            if msg is None:
                msg = f"文件 {path} 不包含文本: {text}"
            self.fail(msg)

    def count_files_in_dir(self, directory):
        """计算目录中的文件数量"""
        return len([f for f in os.listdir(directory)
                   if os.path.isfile(os.path.join(directory, f))])


def skipIfNoTestEPUB(func):
    """如果没有测试 EPUB 文件则跳过测试"""
    def wrapper(self, *args, **kwargs):
        test_epub = Path(__file__).parent / 'fixtures' / 'test_book.epub'
        if not test_epub.exists():
            self.skipTest(f"测试 EPUB 文件不存在: {test_epub}")
        return func(self, *args, **kwargs)
    return wrapper
