#!/usr/bin/env python3
"""
EPUB 技能测试运行器

使用方法:
  python -m tests                    # 运行所有测试
  python -m tests -v                 # 详细输出
  python -m tests TestExtractText    # 运行特定测试类
  python -m tests -k "metadata"      # 运行匹配的测试
"""
import unittest
import sys

# 添加父目录到路径以导入脚本
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


def run_tests(verbosity=2):
    """运行所有测试"""
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)

    # 输出摘要
    print("\n" + "="*70)
    print(f"测试总数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print(f"跳过: {len(result.skipped)}")
    print("="*70)

    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    verbosity = 2 if '-v' in sys.argv or '--verbose' in sys.argv else 1
    sys.exit(run_tests(verbosity))
