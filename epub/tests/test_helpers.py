"""
测试辅助工具函数

提供创建测试 EPUB 文件和测试数据的工具函数。
这些函数是纯函数,遵循 pytest 最佳实践。
"""
import tempfile
from pathlib import Path
from ebooklib import epub


def create_simple_epub(title="测试书籍", author="测试作者", language="zh-CN",
                       chapters=None, output_path=None):
    """
    创建一个简单的测试用 EPUB 文件

    参数:
        title: 书名
        author: 作者
        language: 语言代码
        chapters: 章节内容列表,默认为示例章节
        output_path: 输出文件路径,如果为 None 则使用临时文件

    返回:
        EPUB 文件路径
    """
    if chapters is None:
        chapters = [
            {
                'title': '第一章',
                'content': '<h1>第一章</h1><p>这是第一章的内容。</p>'
            },
            {
                'title': '第二章',
                'content': '<h1>第二章</h1><p>这是第二章的内容,包含更多细节。</p>'
            },
            {
                'title': '第三章',
                'content': '<h1>第三章</h1><p>这是第三章的内容,包含一些<strong>粗体</strong>和<em>斜体</em>文本。</p>'
            }
        ]

    # 创建 EPUB 书籍
    book = epub.EpubBook()

    # 设置元数据
    book.set_identifier('test_book_id_123')
    book.set_title(title)
    book.set_language(language)
    book.add_author(author)
    # 添加出版社为元数据
    book.add_metadata('DC', 'publisher', '测试出版社')

    # 创建章节
    epub_chapters = []
    for i, chapter_data in enumerate(chapters, 1):
        chapter = epub.EpubHtml(
            title=chapter_data['title'],
            file_name=f'chapter_{i:02d}.xhtml',
            lang=language
        )
        chapter.content = chapter_data['content']
        book.add_item(chapter)
        epub_chapters.append(chapter)

    # 设置目录
    book.toc = tuple(epub_chapters)

    # 添加导航文件
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # 设置书脊
    book.spine = ['nav'] + epub_chapters

    # 写入文件
    if output_path is None:
        output_path = tempfile.mktemp(suffix='.epub')

    epub.write_epub(output_path, book, {})
    return output_path


def create_epub_with_images(output_path=None):
    """
    创建包含图片引用的测试 EPUB

    注意:此函数创建引用图片的 EPUB,但实际的图片数据需要单独添加。
    这对于测试图片提取逻辑很有用。
    """
    book = epub.EpubBook()
    book.set_identifier('test_with_images')
    book.set_title('带图片的测试书')
    book.set_language('zh-CN')
    book.add_author('测试作者')

    # 创建一个简单的章节,引用图片
    chapter = epub.EpubHtml(title='第一章', file_name='chap01.xhtml')
    chapter.content = '''
    <h1>第一章</h1>
    <p>这是一段文本。</p>
    <div style="text-align: center;">
        <img src="images/test.jpg" alt="测试图片" style="width: 200px;"/>
    </div>
    <p>图片上面的文字。</p>
    '''
    book.add_item(chapter)

    # 注意: 真实的图片需要单独添加,这里只是创建引用
    # 在实际测试中可以使用真实的图片数据

    book.toc = (chapter,)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ['nav', chapter]

    if output_path is None:
        output_path = tempfile.mktemp(suffix='.epub')

    epub.write_epub(output_path, book, {})
    return output_path


def create_large_epub(chapter_count=50, output_path=None):
    """
    创建包含多个章节的大型 EPUB,用于测试性能

    参数:
        chapter_count: 章节数量
        output_path: 输出文件路径

    返回:
        EPUB 文件路径
    """
    chapters = []
    for i in range(1, chapter_count + 1):
        chapters.append({
            'title': f'第{i}章',
            'content': f'''
                <h1>第{i}章</h1>
                <p>这是第{i}章的内容。</p>
                <p>本章包含一些测试数据:</p>
                <ul>
                    <li>项目 1</li>
                    <li>项目 2</li>
                    <li>项目 3</li>
                </ul>
                <p>更多段落内容...</p>
            '''
        })

    return create_simple_epub(
        title=f'大型测试书 ({chapter_count}章)',
        chapters=chapters,
        output_path=output_path
    )


def create_malformed_epub(output_path=None):
    """
    创建一个格式错误的 EPUB,用于测试错误处理

    返回一个无效的 ZIP 文件(不是真正的 EPUB)。
    """
    if output_path is None:
        output_path = tempfile.mktemp(suffix='.epub')

    # 创建一个无效的 ZIP 文件(不是真正的 EPUB)
    Path(output_path).write_bytes(b'This is not a valid EPUB file')

    return output_path


def setup_test_fixtures(fixture_dir):
    """
    在指定目录创建所有测试夹具文件

    参数:
        fixture_dir: 夹具目录路径 (Path 对象或字符串)

    返回:
        创建的文件列表
    """
    fixture_path = Path(fixture_dir)
    fixture_path.mkdir(parents=True, exist_ok=True)

    created_files = []

    # 创建标准测试 EPUB
    simple_epub = fixture_path / 'test_book.epub'
    create_simple_epub(output_path=str(simple_epub))
    created_files.append(simple_epub)

    # 创建大型测试 EPUB
    large_epub = fixture_path / 'large_book.epub'
    create_large_epub(chapter_count=30, output_path=str(large_epub))
    created_files.append(large_epub)

    # 创建带图片的 EPUB
    with_images_epub = fixture_path / 'book_with_images.epub'
    create_epub_with_images(output_path=str(with_images_epub))
    created_files.append(with_images_epub)

    # 创建多语言测试 EPUB
    english_epub = fixture_path / 'english_book.epub'
    create_simple_epub(
        title="Test Book",
        author="Test Author",
        language="en",
        chapters=[
            {'title': 'Chapter 1', 'content': '<h1>Chapter 1</h1><p>Content of chapter 1.</p>'},
            {'title': 'Chapter 2', 'content': '<h1>Chapter 2</h1><p>Content of chapter 2.</p>'}
        ],
        output_path=str(english_epub)
    )
    created_files.append(english_epub)

    print(f"测试夹具已创建在: {fixture_dir}")
    print(f"  - test_book.epub (标准测试书)")
    print(f"  - large_book.epub (大型测试书, 30章)")
    print(f"  - book_with_images.epub (带图片)")
    print(f"  - english_book.epub (英文)")

    return created_files


if __name__ == '__main__':
    # 当直接运行此脚本时,创建测试夹具
    import sys
    fixture_dir = sys.argv[1] if len(sys.argv) > 1 else 'fixtures'
    setup_test_fixtures(fixture_dir)
