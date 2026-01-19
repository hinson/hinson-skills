---
name: epub
description: Comprehensive EPUB ebook manipulation toolkit for reading, creating, editing, merging, and converting EPUB documents. When Claude needs to parse EPUB structure, extract metadata/content, create ebooks from scratch, or convert between ebook formats.
license: Proprietary
---

# EPUB 电子书操作指南

## 概述

EPUB 是基于 HTML/XML 的开放电子书格式。本指南涵盖使用 Python 的 ebooklib 库处理 EPUB 的核心操作。

**快速开始**: 使用 `scripts/` 目录下的现成脚本处理常见任务。

## 快速开始

### 使用脚本(推荐)

```bash
# 提取元数据
python scripts/extract_metadata.py book.epub

# 提取所有文本
python scripts/extract_text.py book.epub output.txt

# 抽取章节为 Markdown
python scripts/extract_chapters.py book.epub output/ --format md --separate

# 验证 EPUB
python scripts/validate_epub.py book.epub
```

### 使用 Python API

```python
from ebooklib import epub
from ebooklib import ITEM_DOCUMENT

# 读取 EPUB
book = epub.read_epub('book.epub')
print(f"书名: {book.get_metadata('DC', 'title')}")

# 遍历章节
for item in book.get_items():
    if item.get_type() == ITEM_DOCUMENT:
        print(f"章节: {item.get_name()}")
```

## 核心概念

### ebooklib 常量(重要!)

**当前版本使用以下常量:**

```python
from ebooklib import ITEM_DOCUMENT, ITEM_IMAGE, ITEM_STYLE, ITEM_NAVIGATION

# ITEM_DOCUMENT = 9   # 文档/章节内容
# ITEM_IMAGE = 1      # 图片
# ITEM_STYLE = 2      # 样式表
# ITEM_NAVIGATION = 4 # 导航文件

# ⚠️ 注意: 不存在 ITEM_CHAPTER,必须使用 ITEM_DOCUMENT
```

### EPUB 结构

```
EPUB 文件 (ZIP 格式)
├── mimetype           # 文件类型声明
├── META-INF/          # 元数据
│   └── container.xml  # 根文件位置
├── OEBPS/             # 内容目录
│   ├── content.opf    # 包描述(元数据)
│   ├── toc.ncx        # 目录
│   ├── Text/          # 章节内容(ITEM_DOCUMENT)
│   └── Styles/        # 样式文件(ITEM_STYLE)
└── Images/            # 图片(ITEM_IMAGE)
```

## 常用 API

### 读取操作

```python
from ebooklib import epub
from ebooklib import ITEM_DOCUMENT

book = epub.read_epub('book.epub')

# 获取元数据
title = book.get_metadata('DC', 'title')[0][0]
author = book.get_metadata('DC', 'creator')[0][0]

# 遍历项目
for item in book.get_items():
    if item.get_type() == ITEM_DOCUMENT:
        content = item.get_content()  # bytes
        html = content.decode('utf-8')
```

### 写入操作

```python
from ebooklib import epub

# 创建新 EPUB
book = epub.EpubBook()
book.set_identifier('id123')
book.set_title('书名')
book.set_language('zh-CN')
book.add_author('作者')

# 添加章节
chapter = epub.EpubHtml(title='第一章', file_name='chap01.xhtml')
chapter.content = '<h1>第一章</h1><p>内容</p>'
book.add_item(chapter)

# 设置导航
book.toc = (chapter,)
book.add_item(epub.EpubNcx())
book.spine = ['nav', chapter]

# 保存
epub.write_epub('output.epub', book)
```

## 脚本工具

### extract_metadata.py - 提取元数据

```bash
python scripts/extract_metadata.py book.epub
```

**输出:**
- 书名、作者、语言
- 出版社、出版日期、ISBN
- 章节数、图片数
- JSON 格式便于程序处理

### extract_text.py - 提取文本

```bash
# 输出到文件
python scripts/extract_text.py book.epub text.txt

# 输出到终端
python scripts/extract_text.py book.epub
```

**功能:**
- 提取所有纯文本
- 移除 HTML 标签
- 按章节分隔
- UTF-8 编码

### extract_chapters.py - 抽取章节 ⭐

```bash
# 单个文件
python scripts/extract_chapters.py book.epub output/

# 分离章节
python scripts/extract_chapters.py book.epub output/ --separate

# Markdown 格式
python scripts/extract_chapters.py book.epub output/ --format md --separate

# 包含元数据和目录
python scripts/extract_chapters.py book.epub output/ --format html --metadata --toc
```

**选项:**
- `--format txt|md|html` - 输出格式
- `--separate` - 每章单独保存
- `--toc` - 生成目录索引
- `--metadata` - 包含书籍元数据

### validate_epub.py - 验证结构

```bash
python scripts/validate_epub.py book.epub
```

**检查项:**
- 文件可读性
- 必需元数据
- 章节数量
- 导航文件
- 结构完整性

### split_epub.py - 分割 EPUB

```bash
python scripts/split_epub.py large_book.epub chapters/
```

**功能:**
- 每章保存为独立 EPUB
- 保留原始元数据
- 自动编号

### merge_epubs.py - 合并 EPUB

```bash
python scripts/merge_epubs.py merged.epub book1.epub book2.epub book3.epub
```

**功能:**
- 合并多个 EPUB
- 避免文件名冲突
- 保留所有章节

### extract_images.py - 提取图片

```bash
python scripts/extract_images.py book.epub images/
```

**功能:**
- 提取所有图片
- 保留目录结构
- 自动创建目录

### update_metadata.py - 更新元数据

```bash
# 更新书名
python scripts/update_metadata.py book.epub --title "新书名"

# 更新作者
python scripts/update_metadata.py book.epub --author "新作者"

# 更新多个字段
python scripts/update_metadata.py book.epub --title "书名" --author "作者" --language "en"
```

## 命令行工具

### pandoc - 格式转换

```bash
# Markdown → EPUB
pandoc book.md -o book.epub --toc

# EPUB → PDF (需要 LaTeX)
pandoc book.epub -o book.pdf --pdf-engine=xelatex -V CJKmainfont="SimSun"

# EPUB → DOCX
pandoc book.epub -o book.docx
```

### unzip - 查看结构

```bash
# 查看内容列表
unzip -l book.epub

# 解压查看
unzip book.epub -d extracted/

# 提取特定文件
unzip book.epub "OEBPS/content.opf"
```

## 典型工作流

### 1. 提取内容

```bash
# 查看信息
python scripts/extract_metadata.py book.epub

# 提取文本
python scripts/extract_text.py book.epub book.txt

# 抽取章节
python scripts/extract_chapters.py book.epub chapters/ --format md --separate
```

### 2. 编辑 EPUB

```python
from ebooklib import epub

# 读取
book = epub.read_epub('book.epub')

# 修改
book.set_title('新标题')

# 保存
epub.write_epub('book_modified.epub', book)
```

### 3. 批量处理

```bash
# 批量验证
for file in *.epub; do
    python scripts/validate_epub.py "$file"
done

# 批量提取
for file in *.epub; do
    python scripts/extract_text.py "$file" "${file%.epub}.txt"
done
```

### 4. 格式转换

```bash
# EPUB → PDF (用于打印)
pandoc book.epub -o book.pdf --pdf-engine=xelatex

# EPUB → DOCX (用于编辑)
pandoc book.epub -o book.docx

# Markdown → EPUB (用于发布)
pandoc book.md -o book.epub --toc --toc-depth=2
```

## 快速参考

| 需求 | 工具 | 命令 |
|------|------|------|
| 查看元数据 | extract_metadata.py | `python scripts/extract_metadata.py book.epub` |
| 提取文本 | extract_text.py | `python scripts/extract_text.py book.epub text.txt` |
| 抽取章节 | extract_chapters.py | `--format md --separate` |
| 验证文件 | validate_epub.py | `python scripts/validate_epub.py book.epub` |
| 分割 EPUB | split_epub.py | `python scripts/split_epub.py book.epub output/` |
| 合并 EPUB | merge_epubs.py | `python scripts/merge_epubs.py out.epub in1.epub in2.epub` |
| 提取图片 | extract_images.py | `python scripts/extract_images.py book.epub img/` |
| 更新元数据 | update_metadata.py | `--title "新书名"` |
| 格式转换 | pandoc | `pandoc book.epub -o book.pdf` |

## 依赖安装

```bash
# Python 库
pip install ebooklib beautifulsoup4 lxml

# Pandoc (推荐安装)
brew install pandoc  # macOS
sudo apt-get install pandoc  # Ubuntu

# Calibre (可选)
brew install --cask calibre  # macOS
```

## 最佳实践

1. **使用脚本优先**: 对于常见任务,优先使用 `scripts/` 下的现成脚本
2. **常量导入**: 始终使用 `from ebooklib import ITEM_DOCUMENT` 导入常量
3. **元数据完整**: 为 EPUB 设置完整的元数据(标题、作者、语言、ISBN)
4. **UTF-8 编码**: 所有文本内容使用 UTF-8 编码
5. **验证文件**: 修改或创建后使用 validate_epub.py 验证
6. **备份原文件**: 修改 EPUB 前创建备份副本

## 故障排除

### 常见错误

**NameError: name 'ebooklib' is not defined**
```python
# 错误
if item.get_type() == ebooklib.ITEM_DOCUMENT:

# 正确
from ebooklib import ITEM_DOCUMENT
if item.get_type() == ITEM_DOCUMENT:
```

**章节没有提取到**
- 确认使用 `ITEM_DOCUMENT` 而非 `ITEM_CHAPTER`
- 检查 EPUB 是否使用非标准的章节结构

**中文乱码**
- 确保使用 UTF-8 编码
- 检查终端/编辑器编码设置

## 进阶主题

### 程序化处理

```python
from ebooklib import epub
from ebooklib import ITEM_DOCUMENT
from bs4 import BeautifulSoup

# 读取并处理
book = epub.read_epub('book.epub')

for item in book.get_items():
    if item.get_type() == ITEM_DOCUMENT:
        content = item.get_content().decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')

        # 自定义处理
        title = soup.find('h1').get_text()
        text = soup.get_text()

        print(f"处理章节: {title}")
```

### 创建自定义 EPUB

```python
from ebooklib import epub

book = epub.EpubBook()
book.set_title('自定义书籍')
book.set_language('zh-CN')

# 添加多个章节
for i in range(1, 6):
    chapter = epub.EpubHtml(
        title=f'第{i}章',
        file_name=f'chap{i:02d}.xhtml'
    )
    chapter.content = f'<h1>第{i}章</h1><p>内容...</p>'
    book.add_item(chapter)

# 设置导航
chapters = [item for item in book.get_items()
            if isinstance(item, epub.EpubHtml)]
book.toc = tuple(chapters)
book.add_item(epub.EpubNcx())
book.spine = ['nav'] + chapters

epub.write_epub('custom.epub', book)
```

## 参考资源

- **scripts/** - 可执行脚本
- **tests/** - 测试套件和示例
- ebooklib 官方文档: https://ebooklib.readthedocs.io/
- EPUB 3.0 规范: https://www.w3.org/publishing/epub32/
