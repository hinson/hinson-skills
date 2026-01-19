# 开发指南

本文档面向 EPUB Skills 的开发者。

## 环境设置

### Python 版本

- **最低版本**: 3.10
- **推荐版本**: 3.10 或 3.14
- **测试覆盖**: 3.10, 3.14

### 安装依赖

```bash
# 使用 uv (推荐)
uv sync --group dev

# 或使用 pip
pip install -e ".[dev]"
```

## 开发工作流

### 1. 编写代码

```bash
# 编辑脚本
vim scripts/your_script.py
```

### 2. 代码质量检查

```bash
# 检查代码
uv run ruff check scripts/

# 自动修复问题
uv run ruff check scripts/ --fix

# 格式化代码
uv run ruff format scripts/
```

### 3. 运行测试

```bash
# 运行所有测试
uv run pytest

# 运行特定测试
uv run pytest tests/test_extract_text.py

# 运行特定测试类
uv run pytest tests/test_extract_text.py::TestExtractText

# 使用便捷脚本
./run_pytest.sh all
./run_pytest.sh quick
```

### 4. 查看覆盖率

```bash
# 生成覆盖率报告
uv run pytest --cov=scripts --cov-report=html

# 查看报告
open htmlcov/index.html
```

## 配置说明

### Ruff 配置

- **目标版本**: py310+
- **行长度**: 100 字符
- **导入排序**: 自动,导入后空 2 行
- **格式化**: 双引号,空格缩进

### Pytest 配置

- **测试路径**: tests/
- **覆盖率目标**: 80%
- **分支覆盖**: 启用
- **并行测试**: 支持

## 项目结构

```
epub/
├── scripts/              # 源代码
│   ├── extract_*.py     # 提取类脚本
│   ├── create_epub.py   # 创建 EPUB
│   ├── merge_epubs.py   # 合并 EPUB
│   ├── split_epub.py    # 分割 EPUB
│   └── ...
├── tests/               # 测试套件
│   ├── fixtures/        # 测试数据
│   ├── conftest.py      # 测试配置
│   └── test_*.py        # 测试文件
├── pyproject.toml       # 项目配置
├── pytest.ini           # pytest 配置
├── run_pytest.sh        # 测试运行脚本
└── .gitignore           # Git 忽略规则
```

## 测试指南

### 编写测试

```python
import unittest
from .conftest import EPUBTestCase

class TestMyFeature(EPUBTestCase):
    def test_basic_functionality(self):
        """测试基本功能"""
        result = my_function()
        self.assertIsNotNone(result)

    def test_with_fixture(self):
        """使用测试夹具"""
        epub_path = self.test_epub
        result = process(epub_path)
        self.assertTrue(result)
```

### 测试标记

```python
import pytest

@pytest.mark.unit
def test_unit_test():
    """单元测试"""
    assert True

@pytest.mark.integration
def test_integration_test():
    """集成测试"""
    assert True

@pytest.mark.slow
def test_slow_test():
    """慢速测试"""
    assert True
```

### 运行特定标记的测试

```bash
# 单元测试
uv run pytest -m unit

# 集成测试
uv run pytest -m integration

# 排除慢速测试
uv run pytest -m "not slow"
```

## 代码覆盖率

### 当前状态

- **总体覆盖率**: 52.12%
- **目标**: 80%
- **差距**: -27.88%

### 高覆盖率文件

- ✅ `extract_text.py` - 100%
- ✅ `extract_metadata.py` - 83%
- ✅ `extract_chapters.py` - 83%

### 需改进的文件

- ⚠️ `split_epub.py` - 21% (有 bug)
- ⚠️ `merge_epubs.py` - 16% (有 bug)
- ⚠️ `update_metadata.py` - 44% (API 问题)

## 常见任务

### 添加新脚本

1. 在 `scripts/` 创建新文件
2. 添加文档字符串和类型提示
3. 编写测试
4. 更新 README.md
5. 运行 `uv run ruff check . --fix`
6. 运行 `uv run ruff format .`
7. 运行 `uv run pytest`

### 修复 bug

1. 识别问题
2. 编写失败测试
3. 修复代码
4. 运行测试验证
5. 更新文档

### 添加功能

1. 设计 API
2. 实现功能
3. 编写测试
4. 检查覆盖率
5. 更新文档

## 持续集成

推荐使用 GitHub Actions:

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
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      - name: Install dependencies
        run: uv sync --group dev
      - name: Run tests
        run: uv run pytest
```

## 性能优化

### 当前性能

- **文本提取**: 50章 / 0.02秒
- **章节抽取**: 50章 / 0.03秒
- **批量处理**: 20个 / 0.001秒每个

### 优化建议

1. 使用 lxml 解析器
2. 批量处理操作
3. 避免重复读取
4. 使用生成器处理大文件

## 文档

### 更新文档

添加功能时请更新:

- `README.md` - 用户文档
- `DEVELOPMENT.md` - 开发文档
- `SKILL.md` - Claude 技能文档
- 代码注释 - 技术细节

### 文档风格

- 使用中文
- 清晰的示例
- 完整的参数说明
- 错误处理示例

## 发布流程

1. 更新版本号 (pyproject.toml)
2. 更新 CHANGELOG
3. 运行完整测试套件
4. 生成覆盖率报告
5. 创建 Git tag
6. 推送到远程

## 资源链接

- [Pytest 文档](https://docs.pytest.org/)
- [Ruff 文档](https://docs.astral.sh/ruff/)
- [Coverage.py 文档](https://coverage.readthedocs.io/)
- [ebooklib 文档](https://ebooklib.readthedocs.io/)

---

**最后更新**: 2025-01-19
**维护者**: Claude Code & Community
