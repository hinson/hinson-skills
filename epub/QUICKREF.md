# EPUB Skill 快速参考卡

## 一分钟上手

```bash
# 1. 安装依赖
cd scripts/
bash install.sh

# 2. 验证环境
python3 check_env.py

# 3. 开始使用
python3 extract_metadata.py book.epub
```

## 常用命令速查

| 需求 | 命令 |
|------|------|
| 查看信息 | `python3 extract_metadata.py book.epub` |
| 验证文件 | `python3 validate_epub.py book.epub` |
| 提取文本 | `python3 extract_text.py book.epub text.txt` |
| 提取图片 | `python3 extract_images.py book.epub images/` |
| 创建 EPUB | `python3 create_epub.md novel.md novel.epub` |
| 更新元数据 | `python3 update_metadata.py book.epub --title "新书名"` |
| 合并 EPUB | `python3 merge_epubs.py merged.epub book1.epub book2.epub` |
| 分割 EPUB | `python3 split_epub.py large_book.epub chapters/` |

## 典型工作流

```bash
# 准备阶段
python3 check_env.py        # 检查环境
python3 validate_epub.py book.epub   # 验证文件

# 信息提取
python3 extract_metadata.py book.epub      # 查看元数据
python3 extract_text.py book.epub text.txt # 提取文本
python3 extract_images.py book.epub imgs/  # 提取图片

# 编辑修改
python3 update_metadata.py book.epub --title "正确标题" --author "真实作者"

# 批量操作
python3 merge_epubs.py complete.epub vol1.epub vol2.epub vol3.epub
python3 split_epub.py large_book.epub chapters/
```

## 文件结构

```
epub/
├── SKILL.md              # 📖 完整操作指南
├── README.md             # 📚 项目说明
├── SUMMARY.md            # 📊 创建总结
└── scripts/              # 🔧 可执行脚本
    ├── check_env.py      #   环境检查
    ├── install.sh        #   依赖安装
    ├── examples.sh       #   使用示例
    ├── README.md         #   脚本说明
    ├── extract_metadata.py  # 提取元数据
    ├── extract_text.py      # 提取文本
    ├── extract_images.py    # 提取图片
    ├── create_epub.py       # 创建 EPUB
    ├── update_metadata.py   # 更新元数据
    ├── validate_epub.py     # 验证结构
    ├── merge_epubs.py       # 合并 EPUB
    └── split_epub.py        # 分割 EPUB
```

## 依赖项

```
必需:
  ebooklib          # EPUB 读写
  beautifulsoup4    # HTML 解析
  lxml              # XML 解析器

可选:
  pandoc            # 格式转换
  calibre           # ebook-convert
```

## 退出码

```
0  - 成功
1  - 错误
2  - 致命错误
```

## 获取帮助

```bash
# 查看脚本帮助
python3 extract_metadata.py        # 显示用法
python3 update_metadata.py --help  # 显示参数说明

# 查看文档
cat scripts/README.md      # 脚本详细说明
cat SKILL.md               # 完整操作指南
bash examples.sh           # 查看所有示例
```

## 常见问题

**Q: 提示找不到模块?**
```bash
A: pip install ebooklib beautifulsoup4 lxml
```

**Q: 中文乱码?**
```bash
A: 确保使用 UTF-8: export LANG=zh_CN.UTF-8
```

**Q: 脚本没有执行权限?**
```bash
A: chmod +x scripts/*.py
```

**Q: 如何批量处理?**
```bash
A: for file in *.epub; do python3 validate_epub.py "$file"; done
```

## 完整文档

- 📖 [SKILL.md](SKILL.md) - 完整操作指南
- 📚 [README.md](README.md) - 项目说明
- 🔧 [scripts/README.md](scripts/README.md) - 脚本详细说明
- 📊 [SUMMARY.md](SUMMARY.md) - 创建总结

## 联系与反馈

有问题请查看文档或联系维护人员。
