# EPUB 处理脚本工具集

这是一组实用的 Python 脚本,用于处理 EPUB 电子书文件。

## 依赖安装

```bash
pip install ebooklib beautifulsoup4 lxml
```

## 可用脚本

### 1. extract_metadata.py - 提取元数据
提取 EPUB 文件的元数据信息(标题、作者、ISBN 等)

```bash
python extract_metadata.py book.epub
```

**输出示例:**
```
==================================================
文件: book.epub
==================================================
书名: 三体
作者: 刘慈欣
语言: zh-CN
出版社: 重庆出版社
出版日期: 2008-01
ISBN: 9787536692930
章节数: 73
图片数: 12
```

### 2. extract_text.py - 提取纯文本
从 EPUB 中提取所有文本内容

```bash
# 输出到终端
python extract_text.py book.epub

# 保存到文件
python extract_text.py book.epub output.txt
```

### 3. create_epub.py - 创建 EPUB
从 Markdown 文件创建 EPUB 电子书

```bash
# 基础用法
python create_epub.py my_book.md my_book.epub

# 指定标题和作者
python create_epub.py my_book.md my_book.epub "我的书" "张三"
```

### 4. merge_epubs.py - 合并 EPUB
将多个 EPUB 文件合并为一个

```bash
python merge_epubs.py merged.epub book1.epub book2.epub book3.epub
```

**功能特点:**
- 自动处理文件名冲突
- 保留所有章节、图片和样式
- 显示每个文件的处理进度

### 5. extract_images.py - 提取图片
从 EPUB 中提取所有图片

```bash
# 提取到默认目录 (bookname_images/)
python extract_images.py book.epub

# 指定输出目录
python extract_images.py book.epub my_images/
```

### 6. update_metadata.py - 更新元数据
修改 EPUB 的元数据

```bash
# 更新标题
python update_metadata.py book.epub --title "新书名"

# 更新作者和语言
python update_metadata.py book.epub --author "李四" --language "zh-CN"

# 更新多个字段
python update_metadata.py book.epub \
  --title "新书名" \
  --author "王五" \
  --publisher "某某出版社" \
  --isbn "978-7-xxx-xxxx-x"
```

### 7. validate_epub.py - 验证结构
检查 EPUB 文件的结构完整性

```bash
python validate_epub.py book.epub
```

**检查项:**
- ✓ 文件可读性
- ✓ 元数据完整性(标题、作者、语言等)
- ✓ 内容完整性(章节、图片、样式)
- ✓ 导航结构(NCX、目录、书脊)

**退出码:**
- 0: 验证通过(可能有警告)
- 1: 验证失败(发现错误)
- 2: 致命错误(无法读取文件)

### 8. split_epub.py - 分割 EPUB
将 EPUB 的每一章保存为单独的文件

```bash
python split_epub.py large_book.epub chapters/
```

**功能特点:**
- 每章生成独立的 EPUB 文件
- 保留原始元数据
- 自动编号(chapter_001.epub, chapter_002.epub, ...)

## 使用示例

### 完整工作流

```bash
# 1. 检查 EPUB 文件是否有效
python validate_epub.py book.epub

# 2. 查看元数据
python extract_metadata.py book.epub

# 3. 提取文本内容
python extract_text.py book.epub text.txt

# 4. 提取图片
python extract_images.py book.epub images/

# 5. 更新元数据
python update_metadata.py book.epub --title "修正标题" --author "正确作者"

# 6. 合并多本书
python merge_epubs.py collection.epub book1.epub book2.epub

# 7. 分割大书
python split_epub.py large_book.epub chapters/
```

### 创建新的电子书

```bash
# 从 Markdown 创建 EPUB
python create_epub.py my_novel.md my_novel.epub "我的小说" "张三"

# 验证创建的 EPUB
python validate_epub.py my_novel.epub

# 查看元数据
python extract_metadata.py my_novel.epub
```

## 批量处理

### 批量更新目录中所有 EPUB 的作者

```bash
for file in *.epub; do
    python update_metadata.py "$file" --author "统一作者"
done
```

### 批量提取文本

```bash
mkdir -p texts
for file in *.epub; do
    base=$(basename "$file" .epub)
    python extract_text.py "$file" "texts/${base}.txt"
done
```

### 批量验证

```bash
#!/bin/bash
failed=0
for file in *.epub; do
    echo "检查: $file"
    python validate_epub.py "$file"
    if [ $? -ne 0 ]; then
        ((failed++))
    fi
done
echo "失败数量: $failed"
```

## 技术细节

### 支持的 EPUB 版本
- EPUB 2.0.1 (主要支持)
- EPUB 3.0 (基础支持)

### 依赖库
- **ebooklib**: EPUB 文件读写
- **BeautifulSoup4**: HTML 解析和清理
- **lxml**: XML/HTML 解析器

### 字符编码
所有脚本使用 UTF-8 编码处理文本。

## 错误处理

所有脚本都包含错误处理机制:
- 文件不存在时给出明确提示
- 无效的 EPUB 文件会显示详细错误信息
- 使用非零退出码表示错误(便于脚本中使用)

## 许可证

Proprietary

## 贡献

如有问题或建议,请创建 Issue。
