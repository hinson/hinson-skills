#!/bin/bash
# EPUB Skills 测试运行脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TESTS_DIR="$SCRIPT_DIR"

echo "======================================"
echo "EPUB Skills 测试套件"
echo "======================================"
echo ""

# 检查测试夹具是否存在
if [ ! -f "$TESTS_DIR/fixtures/test_book.epub" ]; then
    echo -e "${YELLOW}⚠️  测试夹具不存在,正在生成...${NC}"
    cd "$TESTS_DIR"
    uv run python test_helpers.py fixtures
    echo ""
fi

# 解析命令行参数
TEST_TYPE="${1:-all}"
VERBOSE="${VERBOSE:-}"

case $TEST_TYPE in
    all)
        echo -e "${GREEN}运行所有测试...${NC}"
        cd "$TESTS_DIR"
        uv run python -m tests $VERBOSE
        ;;
    unit)
        echo -e "${GREEN}运行单元测试...${NC}"
        cd "$TESTS_DIR"
        uv run python -m unittest test_extract_metadata test_extract_text test_extract_chapters $VERBOSE
        ;;
    integration)
        echo -e "${GREEN}运行集成测试...${NC}"
        cd "$TESTS_DIR"
        uv run python -m unittest test_other_scripts.TestIntegration $VERBOSE
        ;;
    performance)
        echo -e "${GREEN}运行性能测试...${NC}"
        cd "$TESTS_DIR"
        uv run python -m unittest test_performance $VERBOSE
        ;;
    other)
        echo -e "${GREEN}运行其他脚本测试...${NC}"
        cd "$TESTS_DIR"
        uv run python -m unittest test_other_scripts $VERBOSE
        ;;
    metadata)
        echo -e "${GREEN}运行元数据提取测试...${NC}"
        cd "$TESTS_DIR"
        uv run python -m unittest test_extract_metadata $VERBOSE
        ;;
    text)
        echo -e "${GREEN}运行文本提取测试...${NC}"
        cd "$TESTS_DIR"
        uv run python -m unittest test_extract_text $VERBOSE
        ;;
    chapters)
        echo -e "${GREEN}运行章节抽取测试...${NC}"
        cd "$TESTS_DIR"
        uv run python -m unittest test_extract_chapters $VERBOSE
        ;;
    quick)
        echo -e "${GREEN}运行快速测试(跳过性能测试)...${NC}"
        cd "$TESTS_DIR"
        uv run python -m unittest test_extract_metadata test_extract_text test_extract_chapters test_other_scripts.TestCreateEpub test_other_scripts.TestValidateEpub $VERBOSE
        ;;
    -h|--help|help)
        echo "用法: run_tests.sh [选项] [verbose]"
        echo ""
        echo "选项:"
        echo "  all         运行所有测试(默认)"
        echo "  unit        运行单元测试"
        echo "  integration 运行集成测试"
        echo "  performance 运行性能测试"
        echo "  other       运行其他脚本测试"
        echo "  metadata    运行元数据提取测试"
        echo "  text        运行文本提取测试"
        echo "  chapters    运行章节抽取测试"
        echo "  quick       运行快速测试(跳过性能测试)"
        echo "  help        显示此帮助信息"
        echo ""
        echo "参数:"
        echo "  verbose     启用详细输出"
        echo ""
        echo "示例:"
        echo "  ./run_tests.sh all"
        echo "  ./run_tests.sh unit verbose"
        echo "  ./run_tests.sh quick"
        exit 0
        ;;
    *)
        echo -e "${RED}❌ 未知选项: $TEST_TYPE${NC}"
        echo "使用 'help' 查看可用选项"
        exit 1
        ;;
esac

# 检查测试结果
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ 所有测试通过!${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}✗ 测试失败${NC}"
    exit 1
fi
