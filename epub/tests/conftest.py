"""
Pytest 配置和共享 fixtures

提供测试所需的共享资源、临时文件管理和测试数据。
"""
import pytest
import tempfile
import shutil
from pathlib import Path


# 添加脚本目录到 Python 路径
SCRIPTS_DIR = Path(__file__).parent.parent / 'scripts'
import sys
sys.path.insert(0, str(SCRIPTS_DIR))


@pytest.fixture
def temp_dir():
    """创建临时目录,测试后自动清理"""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    # 清理
    if Path(temp_path).exists():
        shutil.rmtree(temp_path)


@pytest.fixture
def output_dir(temp_dir):
    """创建输出目录,测试后自动清理"""
    output_path = Path(temp_dir) / 'output'
    output_path.mkdir(parents=True, exist_ok=True)
    return str(output_path)


@pytest.fixture
def test_epub():
    """获取测试 EPUB 文件路径"""
    fixture_dir = Path(__file__).parent / 'fixtures'
    epub_path = fixture_dir / 'test_book.epub'

    if not epub_path.exists():
        pytest.skip(f"测试 EPUB 文件不存在: {epub_path}")

    return epub_path


@pytest.fixture
def fixture_dir():
    """获取测试夹具目录"""
    return Path(__file__).parent / 'fixtures'


# pytest 断言辅助函数 - 通过 conftest.py 暴露到全局
@pytest.fixture
def file_helpers():
    """提供文件断言辅助函数"""
    class FileHelpers:
        @staticmethod
        def assert_exists(path, msg=None):
            """断言文件存在"""
            path_obj = Path(path)
            if not path_obj.exists():
                if msg is None:
                    msg = f"文件不存在: {path}"
                pytest.fail(msg)

        @staticmethod
        def assert_not_empty(path, msg=None):
            """断言文件非空"""
            FileHelpers.assert_exists(path)
            if path_obj := Path(path):
                if path_obj.stat().st_size == 0:
                    if msg is None:
                        msg = f"文件为空: {path}"
                    pytest.fail(msg)

        @staticmethod
        def assert_contains(path, text, msg=None):
            """断言文件包含指定文本"""
            FileHelpers.assert_exists(path)
            content = Path(path).read_text(encoding='utf-8')
            if text not in content:
                if msg is None:
                    msg = f"文件 {path} 不包含文本: {text}"
                pytest.fail(msg)

    return FileHelpers


# 便捷的全局辅助函数(可从 conftest 导入)
def get_test_output_path(output_dir, filename):
    """获取测试输出文件路径"""
    return str(Path(output_dir) / filename)


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


# pytest 配置钩子
def pytest_configure(config):
    """在 pytest 启动时配置自定义标记"""
    config.addinivalue_line(
        "markers", "slow: 标记运行较慢的测试"
    )
    config.addinivalue_line(
        "markers", "integration: 集成测试"
    )
    config.addinivalue_line(
        "markers", "performance: 性能测试"
    )
    config.addinivalue_line(
        "markers", "stress: 压力测试"
    )
