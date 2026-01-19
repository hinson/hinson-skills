# EPUB Skills 测试文档

## 概述

本测试套件为 EPUB 技能的所有脚本提供全面的单元测试、集成测试和性能测试。

**测试状态**: ✅ 全部 58 个测试通过

## 测试结构

```
tests/
├── __init__.py              # 测试包初始化
├── conftest.py              # pytest 配置和夹具
├── test_helpers.py          # 测试辅助工具
├── test_extract_metadata.py # 元数据提取测试
├── test_extract_text.py     # 文本提取测试
├── test_extract_chapters.py # 章节抽取测试
├── test_other_scripts.py    # 其他脚本测试(分割、合并、更新元数据等)
└── test_performance.py      # 性能和压力测试
```

## 运行测试

### 运行所有测试

```bash
# 从项目根目录运行
cd .claude/skills/epub
uv run pytest

# 运行测试并显示详细输出
uv run pytest -v

# 运行测试并显示覆盖率报告
uv run pytest --cov=scripts --cov-report=html
```

### 运行特定测试文件

```bash
# 运行元数据提取测试
uv run pytest tests/test_extract_metadata.py -v

# 运行章节抽取测试
uv run pytest tests/test_extract_chapters.py -v

# 运行其他脚本测试
uv run pytest tests/test_other_scripts.py -v

# 运行性能测试
uv run pytest tests/test_performance.py -v
```

### 运行特定测试类或方法

```bash
# 运行特定测试类
uv run pytest tests/test_extract_text.py::TestExtractText -v

# 运行特定测试方法
uv run pytest tests/test_extract_text.py::TestExtractText::test_extract_text_from_epub -v

# 运行性能测试
uv run pytest tests/test_performance.py::TestPerformance::test_extract_text_performance_large_epub -v
```

### 运行标记的测试

```bash
# 运行所有单元测试
uv run pytest -m unit -v

# 运行所有集成测试
uv run pytest -m integration -v

# 运行所有性能测试
uv run pytest -m performance -v

# 跳过慢速测试
uv run pytest -m "not slow" -v
```

## 测试覆盖

### 测试文件映射

| 脚本文件 | 测试文件 | 测试数量 | 状态 |
|---------|---------|---------|------|
| extract_metadata.py | test_extract_metadata.py | 8 | ✅ |
| extract_text.py | test_extract_text.py | 9 | ✅ |
| extract_chapters.py | test_extract_chapters.py | 13 | ✅ |
| split_epub.py | test_other_scripts.py::TestSplitEpub | 2 | ✅ |
| update_metadata.py | test_other_scripts.py::TestUpdateMetadata | 2 | ✅ |
| merge_epubs.py | test_other_scripts.py::TestMergeEpubs | 1 | ✅ |
| 所有脚本集成 | test_other_scripts.py::TestIntegration | 2 | ✅ |
| 性能测试 | test_performance.py | 21 | ✅ |
| **总计** | | **58** | **✅** |

## 测试类型

### 1. 单元测试

测试单个函数和方法的功能:

- ✅ 函数输入输出验证
- ✅ 边界条件测试
- ✅ 错误处理测试
- ✅ 数据格式验证
- ✅ CLI 参数解析

### 2. 集成测试

测试多个脚本协同工作:

- ✅ 提取元数据 → 提取文本
- ✅ 分割 EPUB → 合并 EPUB
- ✅ 创建 EPUB → 验证 → 提取内容

### 3. 性能测试

验证脚本在处理大型文件时的性能:

- ✅ 大型 EPUB (50-100章) 处理时间
- ✅ 批量操作性能
- ✅ 内存使用效率
- ✅ 并发操作压力测试

### 4. 边缘情况测试

测试特殊和极端情况:

- ✅ 空 EPUB 处理
- ✅ 特殊字符和 Unicode
- ✅ 超长内容
- ✅ 无效文件格式
- ✅ 缺失文件处理

## 重要修复和改进

### 修复 1: ebooklib NCX Bug

**问题**: `ebooklib` 库在处理 NCX 导航文件时会抛出 `AttributeError`

**解决方案**: 所有脚本现在使用 `options={'ignore_ncx': True}` 选项

**影响的脚本**:
- `extract_metadata.py`
- `split_epub.py`
- `update_metadata.py`
- `merge_epubs.py`

### 修复 2: 错误处理改进

**问题**: 核心函数直接调用 `sys.exit(1)`,导致无法在测试中捕获错误

**解决方案**:
- 核心函数抛出 `RuntimeError` 异常
- CLI 入口点(`main()` 函数)捕获异常并转换为 `sys.exit(1)`

**好处**:
- 函数可以被其他代码导入和重用
- 测试可以捕获和验证错误
- 保持 CLI 的友好性

### 修复 3: 元数据更新

**问题**: `set_title()` 等方法会追加而不是替换元数据

**解决方案**: 在设置新值前清除现有元数据,遍历所有命名空间

**修复的脚本**:
- `update_metadata.py`: 正确清除和设置元数据
- 添加 TOC uid 设置逻辑,避免写入失败

### 修复 4: 章节提取过滤

**问题**: `extract_chapters.py` 将 `nav.xhtml` 导航文件也当作章节提取

**解决方案**: 跳过文件名为 `nav.xhtml` 的文档项

**结果**: 现在 50 章的 EPUB 正好生成 50 个章节文件,而不是 51 个

### 修复 5: 函数签名一致性

**问题**: `merge_epubs()` 函数签名与 CLI 使用不一致

**解决方案**: 统一函数签名为 `merge_epubs(input_files, output_file)`

## 测试辅助工具

### create_simple_epub()

创建包含指定章节的测试 EPUB:

```python
epub_path = create_simple_epub(
    title='测试书籍',
    author='测试作者',
    language='zh-CN',
    chapters=[
        {'title': '第一章', 'content': '<h1>第一章</h1><p>内容</p>'},
        {'title': '第二章', 'content': '<h1>第二章</h1><p>内容</p>'}
    ],
    output_path='test.epub'
)
```

### create_large_epub()

创建大型 EPUB 用于性能测试:

```python
large_epub = create_large_epub(
    chapter_count=50,
    output_path='large.epub'
)
```

## pytest 配置

### 夹具 (Fixtures)

**test_epub**: 提供标准测试 EPUB 文件路径
**output_dir**: 提供临时输出目录

### 标记 (Markers)

- `unit`: 单元测试
- `integration`: 集成测试
- `performance`: 性能测试
- `slow`: 慢速测试

### 覆盖率配置

```ini
[tool.pytest.ini_options]
minversion = "8.0"
addopts = [
    "--strict-markers",
    "--strict-config",
    "--verbose",
    "--tb=short",
    "--cov=scripts",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=80"
]
```

## 性能基准

当前性能基准(根据系统性能可能有所不同):

| 操作 | 数据量 | 预期时间 | 状态 |
|------|--------|----------|------|
| 提取文本 | 50章 | < 10秒 | ✅ |
| 抽取章节 | 50章 | < 15秒 | ✅ |
| 合并 EPUB | 10个 | < 5秒 | ✅ |
| 提取元数据 | 100章 | < 5秒 | ✅ |
| 内存使用 | 50章 | < 100MB | ✅ |

**注意**: 这些基准在普通硬件上测试。CI 环境可能需要更宽松的限制。

## 编写新测试

### 基本模板

```python
def test_your_function(test_epub, output_dir):
    """测试你的函数"""
    import your_script

    # 执行测试
    result = your_script.your_function(str(test_epub))

    # 验证结果
    assert result is not None
    assert len(result) > 0
```

### CLI 测试模板

```python
def test_your_script_cli(test_epub, output_dir):
    """测试脚本的 CLI 接口"""
    import your_script
    import sys

    # 设置命令行参数
    sys.argv = [
        'your_script.py',
        str(test_epub),
        '--option', 'value'
    ]

    try:
        your_script.main()
    except SystemExit as e:
        # 预期的退出
        assert e.code == 0
```

### 测试最佳实践

1. **使用夹具**: 使用 `test_epub` 和 `output_dir` 夹具而不是自己创建
2. **独立测试**: 确保每个测试相互独立,不依赖执行顺序
3. **清理资源**: 临时文件会在测试后自动清理
4. **明确断言**: 使用清晰的消息说明断言失败的原因
5. **测试边界**: 不仅测试正常情况,还要测试错误情况

## 持续集成

测试可以集成到 CI/CD 流程中:

```bash
# 运行所有测试
uv run pytest

# 检查退出码
if [ $? -eq 0 ]; then
    echo "✅ 所有测试通过"
else
    echo "❌ 测试失败"
    exit 1
fi
```

### GitHub Actions 示例

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install uv
      run: |
        curl -LsSf https://astral.sh/uv/install.sh | sh
        source $HOME/.cargo/env

    - name: Run tests
      run: |
        uv run pytest --cov=scripts --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## 故障排除

### 测试失败

1. **依赖问题**:
   ```bash
   uv sync
   ```

2. **权限问题**:
   ```bash
   chmod +x scripts/*.py
   ```

3. **清理缓存**:
   ```bash
   uv run pytest --cache-clear
   ```

### 调试测试

启用详细输出:

```bash
uv run pytest -v -s
```

运行单个测试并打印详细信息:

```bash
uv run pytest tests/test_extract_text.py::TestExtractText::test_extract_text_from_epub -vvs
```

进入调试器:

```bash
uv run pytest --pdb
```

## 已知问题

### 1. Duplicate nav.xhtml 警告

某些测试会产生警告:
```
UserWarning: Duplicate name: 'EPUB/nav.xhtml'
```

这是 `ebooklib` 的已知问题,不影响功能。我们在 `split_epub.py` 中已经处理了这个问题。

### 2. 性能测试时间

性能测试可能需要较长时间,可以通过跳过慢速测试来加速:

```bash
uv run pytest -m "not slow"
```

## 更新日志

### v1.0.0 (当前版本)

- ✅ 修复所有 11 个失败的测试
- ✅ 改进错误处理机制
- ✅ 添加对 ebooklib NCX bug 的处理
- ✅ 修复元数据更新逻辑
- ✅ 修复章节提取(排除 nav.xhtml)
- ✅ 统一函数签名
- ✅ 100% 测试通过率(58/58)

## 贡献

添加新测试时:

1. 在适当的测试文件中添加测试类或方法
2. 使用清晰的测试名称和文档字符串
3. 确保测试独立且可重复
4. 更新此文档以反映新的测试覆盖
5. 确保所有测试通过后再提交

## 许可

与 EPUB 技能项目相同。
