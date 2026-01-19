# EPUB Skills 测试文档

## 概述

本测试套件为 EPUB 技能的所有脚本提供全面的单元测试、集成测试和性能测试。

## 测试结构

```
tests/
├── __init__.py              # 测试包初始化
├── __main__.py              # 测试运行器
├── conftest.py              # 测试配置和基类
├── test_helpers.py          # 测试辅助工具
├── test_extract_metadata.py # 元数据提取测试
├── test_extract_text.py     # 文本提取测试
├── test_extract_chapters.py # 章节抽取测试
├── test_other_scripts.py    # 其他脚本测试
├── test_performance.py      # 性能和压力测试
└── fixtures/                # 测试夹具
    ├── test_book.epub       # 标准测试 EPUB
    ├── large_book.epub      # 大型测试 EPUB (30章)
    ├── book_with_images.epub # 带图片的 EPUB
    └── english_book.epub    # 英文 EPUB
```

## 运行测试

### 运行所有测试

```bash
# 方法 1: 使用 Python 模块方式
cd .claude/skills/epub/tests
uv run python -m tests

# 方法 2: 直接运行测试运行器
uv run python __main__.py

# 方法 3: 使用 unittest
uv run unittest discover -s tests -p 'test_*.py'
```

### 运行特定测试文件

```bash
# 运行元数据提取测试
uv run python -m unittest test_extract_metadata -v

# 运行章节抽取测试
uv run python -m unittest test_extract_chapters -v
```

### 运行特定测试类或方法

```bash
# 运行特定测试类
uv run python -m unittest test_extract_text.TestExtractText -v

# 运行特定测试方法
uv run python -m unittest test_extract_text.TestExtractText.test_extract_text_from_epub -v
```

### 运行性能测试

```bash
# 运行性能测试套件
uv run python -m unittest test_performance -v

# 运行特定性能测试
uv run python -m unittest test_performance.TestPerformance.test_extract_text_performance_large_epub -v
```

## 测试类型

### 1. 单元测试

测试单个函数和方法的功能:

- ✅ 函数输入输出验证
- ✅ 边界条件测试
- ✅ 错误处理测试
- ✅ 数据格式验证

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

- ✅ 空文件处理
- ✅ 特殊字符和 Unicode
- ✅ 超长内容
- ✅ 无效文件格式

## 测试夹具

测试夹具是预先准备好的测试数据,位于 `fixtures/` 目录:

### test_book.epub
标准测试 EPUB,包含:
- 3 个章节
- 完整的元数据
- 中文内容

### large_book.epub
大型测试 EPUB,包含:
- 30 个章节
- 用于性能测试

### book_with_images.epub
包含图片引用的 EPUB,用于测试:
- 图片提取
- 资源处理

### english_book.epub
英文 EPUB,用于测试:
- 多语言支持
- 字符编码

## 创建测试夹具

如果需要重新生成测试夹具:

```bash
cd tests
uv run python test_helpers.py fixtures
```

## 编写新测试

### 基本模板

```python
import unittest
import sys
from pathlib import Path

# 添加脚本目录
SCRIPTS_DIR = Path(__file__).parent.parent / 'scripts'
sys.path.insert(0, str(SCRIPTS_DIR))

from conftest import EPUBTestCase, skipIfNoTestEPUB


class TestYourScript(EPUBTestCase):
    """测试你的脚本"""

    @skipIfNoTestEPUB
    def test_basic_functionality(self):
        """测试基本功能"""
        import your_script

        result = your_script.your_function(str(self.test_epub))

        self.assertIsNotNone(result)

    def test_edge_case(self):
        """测试边缘情况"""
        import your_script

        # 测试代码
        pass


if __name__ == '__main__':
    unittest.main()
```

### 测试最佳实践

1. **使用继承**: 继承 `EPUBTestCase` 以获得共享的测试工具
2. **清理资源**: 使用 `setUp()` 和 `tearDown()` 管理测试资源
3. **使用装饰器**: 使用 `@skipIfNoTestEPUB` 跳过需要测试文件的测试
4. **断言方法**: 使用自定义断言方法如 `assertFileExists()`
5. **独立测试**: 确保每个测试相互独立,不依赖执行顺序

## 自定义断言

`EPUBTestCase` 提供以下自定义断言方法:

```python
self.assertFileExists(path, msg=None)
self.assertFileNotEmpty(path, msg=None)
self.assertFileContains(path, text, msg=None)
self.count_files_in_dir(directory)
```

## 性能基准

当前性能基准(根据系统性能可能有所不同):

| 操作 | 数据量 | 预期时间 |
|------|--------|----------|
| 提取文本 | 50章 | < 10秒 |
| 抽取章节 | 50章 | < 15秒 |
| 合并 EPUB | 10个 | < 5秒 |
| 提取元数据 | 100章 | < 5秒 |
| 内存使用 | 50章 | < 100MB |

## 持续集成

测试可以集成到 CI/CD 流程中:

```bash
# 在 CI 环境中运行测试
cd .claude/skills/epub/tests
uv run python -m tests -v

# 检查测试结果
echo $?
```

## 故障排除

### 测试失败

1. **缺少测试夹具**:
   ```bash
   cd tests
   uv run python test_helpers.py fixtures
   ```

2. **依赖问题**:
   ```bash
   cd ../scripts
   bash install.sh
   ```

3. **权限问题**:
   ```bash
   chmod +x scripts/*.py
   ```

### 调试测试

启用详细输出:

```bash
uv run python -m tests -v
```

运行单个测试并打印详细信息:

```bash
uv run python -m unittest test_extract_text.TestExtractText.test_extract_text_from_epub -v
```

## 贡献

添加新测试时:

1. 在适当的测试文件中添加测试类或方法
2. 使用清晰的测试名称和文档字符串
3. 确保测试独立且可重复
4. 更新此文档以反映新的测试覆盖

## 许可

与 EPUB 技能项目相同。

## 联系

有问题或建议请查看项目文档或联系维护人员。
