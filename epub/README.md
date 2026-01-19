# EPUB Skill - 完整文档

这是一个用于处理 EPUB 电子书的完整工具集,包含操作指南和可执行脚本。

## 📁 目录结构

```
epub/
├── SKILL.md           # 主要使用指南(理论文档)
└── scripts/           # 可执行脚本工具
    ├── README.md      # 脚本使用说明
    ├── check_env.py   # 环境检查
    ├── install.sh     # 依赖安装脚本
    ├── extract_metadata.py   # 提取元数据
    ├── extract_text.py       # 提取纯文本
    ├── extract_images.py     # 提取图片
    ├── create_epub.py        # 创建 EPUB
    ├── merge_epubs.py        # 合并 EPUB
    ├── split_epub.py         # 分割 EPUB
    ├── update_metadata.py    # 更新元数据
    └── validate_epub.py      # 验证结构
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd scripts/
bash install.sh
```

或手动安装:

```bash
pip install ebooklib beautifulsoup4 lxml
```

### 2. 检查环境

```bash
python3 check_env.py
```

### 3. 使用脚本

```bash
# 查看元数据
python3 extract_metadata.py book.epub

# 验证结构
python3 validate_epub.py book.epub

# 提取文本
python3 extract_text.py book.epub output.txt
```

## 📚 主要功能

### 📖 读取与解析
- **extract_metadata.py** - 提取标题、作者、ISBN 等元数据
- **extract_text.py** - 提取所有纯文本内容
- **extract_images.py** - 提取所有图片资源

### ✏️ 创建与编辑
- **create_epub.py** - 从 Markdown 创建 EPUB
- **update_metadata.py** - 修改元数据(标题、作者等)
- **validate_epub.py** - 验证 EPUB 结构完整性

### 🔧 高级操作
- **merge_epubs.py** - 合并多个 EPUB 为一个
- **split_epub.py** - 将 EPUB 按章分割为多个文件

## 📖 使用示例

### 场景 1: 查看 EPUB 信息

```bash
# 检查文件是否有效
python3 validate_epub.py book.epub

# 查看完整元数据
python3 extract_metadata.py book.epub
```

### 场景 2: 提取内容

```bash
# 提取所有文本
python3 extract_text.py book.epub text.txt

# 提取所有图片
python3 extract_images.py book.epub images/
```

### 场景 3: 创建电子书

```bash
# 从 Markdown 创建 EPUB
python3 create_epub.py my_novel.md my_novel.epub "我的小说" "张三"

# 验证创建的文件
python3 validate_epub.py my_novel.epub
```

### 场景 4: 批量处理

```bash
# 合并系列书籍
python3 merge_epubs.py complete.epub vol1.epub vol2.epub vol3.epub

# 分割大书
python3 split_epub.py large_book.epub chapters/
```

### 场景 5: 修正元数据

```bash
# 修正标题和作者
python3 update_metadata.py book.epub --title "正确标题" --author "真实作者"

# 添加 ISBN
python3 update_metadata.py book.epub --isbn "978-7-xxx-xxxx-x"
```

## 🛠️ 技术细节

### 支持的操作

| 操作 | 脚本 | 输入 | 输出 |
|------|------|------|------|
| 提取元数据 | extract_metadata.py | EPUB | 屏幕输出 + JSON |
| 提取文本 | extract_text.py | EPUB | TXT 文件 |
| 提取图片 | extract_images.py | EPUB | 图片文件夹 |
| 创建 EPUB | create_epub.py | Markdown | EPUB |
| 合并 EPUB | merge_epubs.py | 多个 EPUB | 单个 EPUB |
| 分割 EPUB | split_epub.py | 单个 EPUB | 多个 EPUB |
| 更新元数据 | update_metadata.py | EPUB | 原文件覆盖 |
| 验证结构 | validate_epub.py | EPUB | 验证报告 |

### 依赖库

- **ebooklib** - EPUB 文件读写核心库
- **BeautifulSoup4** - HTML 解析和内容提取
- **lxml** - 高性能 XML/HTML 解析器

### 字符编码

所有脚本使用 UTF-8 编码,支持中英文混合内容。

## 📋 脚本特性

### 错误处理
- 文件不存在时给出明确提示
- 无效 EPUB 文件显示详细错误
- 使用非零退出码便于脚本中使用

### 用户友好
- 清晰的进度提示
- 详细的帮助信息
- 彩色输出(成功 ✓, 警告 ⚠, 错误 ✗)

### 批量处理支持
- 所有脚本支持在 shell 循环中使用
- 标准错误输出便于日志记录

## 📖 完整文档

- **[SKILL.md](SKILL.md)** - 完整的操作指南和代码示例
- **[scripts/README.md](scripts/README.md)** - 脚本详细使用说明

## 🔍 故障排除

### 问题: ModuleNotFoundError

```bash
# 解决方法: 重新安装依赖
pip install --upgrade ebooklib beautifulsoup4 lxml
```

### 问题: 脚本没有执行权限

```bash
# 解决方法: 添加执行权限
chmod +x scripts/*.py
```

### 问题: 中文乱码

```bash
# 确保使用 UTF-8 编码
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8
```

## 📝 许可证

MIT License

## 🤝 贡献

欢迎贡献!请遵循以下步骤:

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 🧪 开发

### 环境要求

- Python >= 3.10
- uv (推荐) 或 pip

### 安装开发依赖

```bash
# 使用 uv
uv sync --group dev

# 使用 pip
pip install -e ".[dev]"
```

### 代码质量

```bash
# 代码检查
uv run ruff check .

# 自动修复
uv run ruff check . --fix

# 格式化
uv run ruff format .
```

### 测试

```bash
# 运行所有测试
uv run pytest

# 使用便捷脚本
./run_pytest.sh all          # 所有测试
./run_pytest.sh quick        # 快速测试
./run_pytest.sh unit         # 单元测试
```

### 覆盖率

当前覆盖率: **52.12%** (目标: 80%)

```bash
# 查看覆盖率报告
uv run pytest --cov=scripts --cov-report=html
open htmlcov/index.html
```

### 测试状态

```
总测试数: 58
通过: 47 (81%)
失败: 11 (19%)
```

详见 [tests/TEST_SUMMARY.md](tests/TEST_SUMMARY.md)

## 📚 更多文档

- [DEVELOPMENT.md](DEVELOPMENT.md) - 开发指南
- [pyproject.toml](pyproject.toml) - 项目配置
- [pytest.ini](pytest.ini) - 测试配置

---

**最后更新**: 2025-01-19
**Python 版本**: 3.10+
**状态**: ✅ 活跃开发
