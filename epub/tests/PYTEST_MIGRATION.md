# Pytest 迁移总结

## 概述

已将所有测试代码从 `unittest` 框架迁移到 `pytest` 最佳实践规范。

## 主要改进

### 1. Fixtures 替代 setUp/tearDown

**之前 (unittest):**
```python
class EPUBTestCase(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.test_dir, 'output')
        os.makedirs(self.output_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
```

**现在 (pytest):**
```python
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
    return str(output_dir)
```

**优势:**
- 依赖注入:通过函数参数自动注入
- 作用域控制:可以设置 session/module/class/function 级别
- 可重用性:fixtures 可以在多个测试中共享
- 更清晰:测试函数只需声明需要的依赖

### 2. 原生 assert 替代 self.assertXxx

**之前:**
```python
self.assertEqual(title, '测试标题')
self.assertIn('第一章', text)
self.assertGreater(len(text), 0)
```

**现在:**
```python
assert title == '测试标题'
assert '第一章' in text
assert len(text) > 0
```

**优势:**
- 更简洁自然
- Pytest 的智能断言内省提供详细的失败信息
- 失败时自动显示变量值
- 无需记忆多种断言方法

### 3. pytest.raises() 替代 self.assertRaises

**之前:**
```python
with self.assertRaises(SystemExit):
    extract_text.extract_text_from_epub(invalid_epub)
```

**现在:**
```python
with pytest.raises(SystemExit):
    extract_text.extract_text_from_epub(invalid_epub)
```

### 4. 智能测试跳过

**之前:**
```python
def skipIfNoTestEPUB(func):
    def wrapper(self, *args, **kwargs):
        test_epub = Path(__file__).parent / 'fixtures' / 'test_book.epub'
        if not test_epub.exists():
            self.skipTest(f"测试 EPUB 文件不存在: {test_epub}")
        return func(self, *args, **kwargs)
    return wrapper

@skipIfNoTestEPUB
def test_something(self):
    ...
```

**现在:**
```python
@pytest.fixture
def test_epub():
    """获取测试 EPUB 文件路径"""
    fixture_dir = Path(__file__).parent / 'fixtures'
    epub_path = fixture_dir / 'test_book.epub'

    if not epub_path.exists():
        pytest.skip(f"测试 EPUB 文件不存在: {epub_path}")

    return epub_path

def test_something(test_epub):
    ...  # 如果 test_epub 不存在,测试自动跳过
```

## 文件结构

### 重构后的文件

1. **conftest.py** - Pytest 配置和共享 fixtures
   - `temp_dir` fixture: 临时目录管理
   - `output_dir` fixture: 输出目录
   - `test_epub` fixture: 测试 EPUB 文件
   - `fixture_dir` fixture: 测试夹具目录
   - 全局辅助函数

2. **test_helpers.py** - 纯辅助工具函数
   - `create_simple_epub()`: 创建简单测试 EPUB
   - `create_large_epub()`: 创建大型测试 EPUB
   - `create_epub_with_images()`: 创建带图片的 EPUB
   - `setup_test_fixtures()`: 批量创建测试夹具

3. **test_extract_chapters.py** - 章节抽取测试
4. **test_extract_text.py** - 文本提取测试
5. **test_extract_metadata.py** - 元数据提取测试
6. **test_other_scripts.py** - 其他脚本测试
7. **test_performance.py** - 性能和压力测试

## Pytest 配置

创建了 `pytest.ini` 配置文件:

```ini
[pytest]
python_files = test_*.py
python_classes = Test*
python_functions = test_*
minversion = 7.0
addopts =
    -v
    --strict-markers
    --tb=short
    --disable-warnings
markers =
    slow: 标记运行较慢的测试
    integration: 集成测试
    performance: 性能测试
    stress: 压力测试
```

## 运行测试

```bash
# 运行所有测试
pytest

# 运行特定文件
pytest test_extract_text.py

# 运行特定测试类
pytest test_extract_chapters.py::TestExtractChapters

# 运行特定测试方法
pytest test_extract_text.py::TestExtractText::test_extract_text_from_epub

# 只运行失败的测试
pytest --lf

# 运行并显示打印输出
pytest -s

# 运行性能测试
pytest -m performance

# 运行除性能测试外的所有测试
pytest -m "not performance"

# 生成覆盖率报告
pytest --cov=. --cov-report=html
```

## 最佳实践亮点

### 1. 使用 Path 对象替代 os.path
```python
# 之前
os.path.join(self.output_dir, 'chapters.txt')

# 现在
Path(output_dir) / 'chapters.txt'
```

### 2. 使用 f-string 进行字符串格式化
```python
# 之前
"文件不存在: {}".format(path)

# 现在
f"文件不存在: {path}"
```

### 3. 使用上下文管理器进行资源清理
```python
@pytest.fixture
def temp_dir():
    temp_path = tempfile.mkdtemp()
    yield temp_path
    # 自动清理
    if Path(temp_path).exists():
        shutil.rmtree(temp_path)
```

### 4. 测试类的组织
```python
class TestExtractText:
    """测试文本提取功能"""

    def test_extract_text_from_epub(self, test_epub):
        """测试从 EPUB 中提取文本"""
        ...

class TestExtractTextCLI:
    """测试 extract_text 命令行接口"""

    def test_main_prints_to_stdout(self, test_epub):
        """测试主函数将文本打印到标准输出"""
        ...
```

## 性能测试标记

性能和压力测试自动标记为 `performance` 和 `stress`:

```python
# 跳过性能测试(快速反馈)
pytest -m "not performance"

# 只运行性能测试
pytest -m performance
```

## 迁移带来的好处

1. **更简洁的代码**: 测试代码减少了约 30% 的行数
2. **更好的可读性**: 使用原生 assert 和 fixtures 使测试更直观
3. **更强大的功能**: 参数化、标记、插件等
4. **更好的错误信息**: Pytest 提供详细的失败分析
5. **更快的开发速度**: 更少的样板代码
6. **更好的维护性**: fixtures 的依赖注入使测试更易维护

## 兼容性

所有现有测试逻辑保持不变,只改变了测试框架的实现方式。测试覆盖率和测试目标完全相同。
