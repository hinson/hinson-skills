#!/bin/bash
# Pytest 运行脚本 (epub 技能目录专用)

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}EPUB Skills Pytest 测试套件${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 解析命令行参数
TEST_TYPE="${1:-all}"
COVERAGE="${COVERAGE:-true}"
PARALLEL="${PARALLEL:-false}"
VERBOSE="${VERBOSE:-false}"

# 检查 pytest 是否安装
if ! uv run pytest --version >/dev/null 2>&1; then
    echo -e "${RED}❌ pytest 未安装${NC}"
    echo "运行: uv add --dev pytest pytest-cov pytest-html pytest-xdist"
    exit 1
fi

# 构建 pytest 命令
PYTEST_CMD="uv run pytest"

# 添加覆盖率和报告选项
if [ "$COVERAGE" = "true" ]; then
    PYTEST_CMD="$PYTEST_CMD --cov=scripts --cov-report=term-missing --cov-report=html --cov-report=xml"
fi

# 添加并行选项
if [ "$PARALLEL" = "true" ]; then
    PYTEST_CMD="$PYTEST_CMD -n auto"
fi

# 添加详细输出
if [ "$VERBOSE" = "true" ]; then
    PYTEST_CMD="$PYTEST_CMD -vv"
fi

# 添加 HTML 报告
PYTEST_CMD="$PYTEST_CMD --html=pytest_report.html --self-contained-html"

# 执行测试
case $TEST_TYPE in
    all)
        echo -e "${GREEN}运行所有测试(带覆盖率)...${NC}"
        $PYTEST_CMD tests
        ;;
    unit)
        echo -e "${GREEN}运行单元测试...${NC}"
        $PYTEST_CMD -m unit tests
        ;;
    integration)
        echo -e "${GREEN}运行集成测试...${NC}"
        $PYTEST_CMD -m integration tests
        ;;
    performance)
        echo -e "${GREEN}运行性能测试...${NC}"
        $PYTEST_CMD -m performance tests
        ;;
    quick)
        echo -e "${GREEN}运行快速测试(排除慢速测试)...${NC}"
        $PYTEST_CMD -m "not slow" tests
        ;;
    no-cov)
        echo -e "${GREEN}运行测试(无覆盖率检查)...${NC}"
        uv run pytest tests --html=pytest_report.html --self-contained-html
        ;;
    parallel)
        echo -e "${GREEN}并行运行测试...${NC}"
        $PYTEST_CMD -n auto tests
        ;;
    report)
        echo -e "${GREEN}仅生成覆盖率报告...${NC}"
        uv run pytest --cov=scripts --cov-report=html --cov-report=term tests -q
        ;;
    -h|--help|help)
        echo "用法: run_pytest.sh [选项] [标志]"
        echo ""
        echo "选项:"
        echo "  all         运行所有测试(默认)"
        echo "  unit        运行单元测试"
        echo "  integration 运行集成测试"
        echo "  performance 运行性能测试"
        echo "  quick       运行快速测试(排除慢速测试)"
        echo "  no-cov      运行测试(无覆盖率检查)"
        echo "  parallel    并行运行测试"
        echo "  report      仅生成覆盖率报告"
        echo "  help        显示此帮助信息"
        echo ""
        echo "环境变量:"
        echo "  COVERAGE=false      禁用覆盖率检查"
        echo "  PARALLEL=true       启用并行测试"
        echo "  VERBOSE=true        启用详细输出"
        echo ""
        echo "示例:"
        echo "  ./run_pytest.sh all"
        echo "  ./run_pytest.sh unit"
        echo "  ./run_pytest.sh quick"
        echo "  COVERAGE=false ./run_pytest.sh all"
        echo "  PARALLEL=true ./run_pytest.sh all"
        echo "  VERBOSE=true ./run_pytest.sh all"
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
    echo -e "${GREEN}✓ 测试完成!${NC}"

    # 显示覆盖率报告位置
    if [ "$COVERAGE" = "true" ]; then
        echo ""
        echo -e "${BLUE}📊 覆盖率报告:${NC}"
        echo "  终端: 已在上方显示"
        echo "  HTML: htmlcov/index.html"
        echo "  XML:  coverage.xml"
        echo ""
        echo "查看 HTML 报告:"
        echo "  open htmlcov/index.html"
    fi

    echo ""
    echo -e "${BLUE}📈 测试报告:${NC}"
    echo "  HTML: pytest_report.html"

    exit 0
else
    echo ""
    echo -e "${RED}✗ 测试失败${NC}"
    exit 1
fi
