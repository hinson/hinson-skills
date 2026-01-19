# Git 仓库设置指南

本指南帮助你将 EPUB Skills 目录设置为一个独立的 Git 仓库。

## 📋 前提条件

- ✅ Python 3.10+ 已安装
- ✅ uv 已安装
- ✅ Git 已安装

## 🚀 快速开始

### 1. 初始化 Git 仓库

```bash
cd /Users/hinson/Skills/epub/.claude/skills/epub

# 初始化 Git
git init

# 添加所有文件
git add .

# 检查状态
git status
```

### 2. 创建首次提交

```bash
git commit -m "feat: initial commit

- Add EPUB manipulation scripts
- Add comprehensive test suite (58 tests)
- Configure pytest and ruff
- Add development documentation
- Code coverage: 52.12%
"
```

### 3. 创建 GitHub 仓库

```bash
# 在 GitHub 上创建新仓库 (名为 epub-skills)
# 然后关联远程仓库

git remote add origin git@github.com:YOUR_USERNAME/epub-skills.git

# 推送到远程
git branch -M main
git push -u origin main
```

## 📁 项目结构

```
epub-skills/
├── .gitignore              # Git 忽略规则
├── pyproject.toml          # 项目配置
├── pytest.ini              # pytest 配置
├── run_pytest.sh           # 测试运行脚本
├── README.md               # 项目文档
├── DEVELOPMENT.md          # 开发指南
├── SKILL.md                # Claude 技能定义
├── QUICKREF.md             # 快速参考
├── SUMMARY.md              # 功能摘要
├── PROJECT_INFO.txt        # 项目信息
├── scripts/                # 源代码目录
│   ├── README.md
│   ├── check_env.py
│   ├── install.sh
│   ├── create_epub.py
│   ├── extract_chapters.py
│   ├── extract_images.py
│   ├── extract_metadata.py
│   ├── extract_text.py
│   ├── merge_epubs.py
│   ├── split_epub.py
│   ├── update_metadata.py
│   └── validate_epub.py
└── tests/                   # 测试目录
    ├── __init__.py
    ├── __main__.py
    ├── conftest.py
    ├── run_tests.sh
    ├── README.md
    ├── TEST_SUMMARY.md
    ├── TESTING_COMPLETE.md
    ├── fixtures/            # 测试数据
    │   ├── test_book.epub
    │   ├── large_book.epub
    │   └── ...
    └── test_*.py            # 测试文件
```

## 🔧 配置文件说明

### pyproject.toml

- **项目元数据**: 名称、版本、描述
- **依赖管理**: 生产依赖和开发依赖
- **Ruff 配置**: 代码质量工具
- **Pytest 配置**: 测试框架
- **Coverage 配置**: 代码覆盖率

### pytest.ini

- pytest 基本配置
- 测试路径和模式
- 标记定义
- 日志配置

### .gitignore

排除以下内容:
- Python 缓存
- 虚拟环境
- 测试产物
- IDE 配置
- 临时文件

## 📊 项目状态

### 代码统计

```
语言: Python
文件数: 20+ (脚本) + 6 (测试)
代码行数: ~2000 行
测试数: 58
覆盖率: 52.12%
```

### 依赖

**核心依赖**:
- ebooklib>=0.18
- beautifulsoup4>=4.12
- lxml>=5.0

**开发依赖**:
- ruff>=0.8.0
- pytest>=8.0
- pytest-cov>=6.0
- pytest-html>=4.0
- pytest-xdist>=3.0

## 🎯 里程碑

### Phase 1: 基础功能 ✅

- ✅ 元数据提取
- ✅ 文本提取
- ✅ 图片提取
- ✅ 章节抽取
- ✅ EPUB 创建
- ✅ EPUB 验证

### Phase 2: 高级功能 ⚠️

- ⚠️ 分割 EPUB (需要修复)
- ⚠️ 合并 EPUB (需要修复)
- ⚠️ 更新元数据 (需要修复)

### Phase 3: 改进 📋

- 📋 提升覆盖率到 80%
- 📋 添加更多测试
- 📋 性能优化
- 📋 文档完善

## 🔄 CI/CD 集成

### GitHub Actions 示例

创建 `.github/workflows/test.yml`:

```yaml
name: Tests
on:
  push:
    branches: [ main, dev ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
        python-version: ['3.10', '3.14']

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install uv
      run: |
        curl -LsSf https://astral.sh/uv/install.sh | sh
        echo "$HOME/.local/bin" >> $GITHUB_PATH

    - name: Install dependencies
      run: uv sync --group dev

    - name: Run tests
      run: uv run pytest --cov=scripts --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml
```

## 📝 许可证

MIT License - 自由使用、修改和分发

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📚 相关资源

- [Claude Code](https://claude.ai/code)
- [ebooklib 文档](https://ebooklib.readthedocs.io/)
- [Pytest 文档](https://docs.pytest.org/)
- [Ruff 文档](https://docs.astral.sh/ruff/)

## 🐛 已知问题

### 需要修复的问题

1. **split_epub.py** - 数据结构错误
2. **merge_epubs.py** - 数据结构问题
3. **update_metadata.py** - API 不匹配

详见 [tests/TEST_SUMMARY.md](tests/TEST_SUMMARY.md)

## 📈 下一步

1. ✅ 设置 Git 仓库
2. ⏳ 修复失败的测试
3. ⏳ 提升覆盖率到 80%
4. ⏳ 添加 CI/CD
5. ⏳ 发布 v1.0.0

---

**创建时间**: 2025-01-19
**维护者**: Claude Code & Community
**状态**: ✅ 准备就绪,可以初始化 Git 仓库
