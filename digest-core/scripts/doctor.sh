#!/bin/bash
# ActionPulse Doctor - диагностика окружения
set -euo pipefail

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Icons
CHECK="${GREEN}✓${NC}"
CROSS="${RED}✗${NC}"
WARN="${YELLOW}⚠${NC}"
INFO="${BLUE}ℹ${NC}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DIGEST_CORE_DIR="$PROJECT_ROOT/digest-core"

echo ""
echo "======================================"
echo "  ActionPulse Environment Doctor"
echo "======================================"
echo ""

# Counters
ERRORS=0
WARNINGS=0
SUCCESS=0

# Function to print status
print_check() {
    local status=$1
    local message=$2
    if [ "$status" = "ok" ]; then
        echo -e "${CHECK} ${message}"
        ((SUCCESS++))
    elif [ "$status" = "warn" ]; then
        echo -e "${WARN} ${message}"
        ((WARNINGS++))
    else
        echo -e "${CROSS} ${message}"
        ((ERRORS++))
    fi
}

# Check 1: Python version
echo "Проверка Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
    PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 11 ]; then
        print_check "ok" "Python $PYTHON_VERSION найден"
    else
        print_check "error" "Python $PYTHON_VERSION (требуется 3.11+)"
        if command -v python3.11 &> /dev/null; then
            PY311_VERSION=$(python3.11 --version 2>&1 | awk '{print $2}')
            print_check "ok" "Python3.11 доступен: $PY311_VERSION"
            echo -e "  ${INFO} Используйте: python3.11 -m digest_core.cli ..."
        else
            echo -e "  ${INFO} Установите: brew install python@3.11 (macOS) или sudo apt install python3.11 (Linux)"
        fi
    fi
else
    print_check "error" "Python не найден"
    echo -e "  ${INFO} Установите Python 3.11+"
fi

# Check 2: Git
echo ""
echo "Проверка Git..."
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | awk '{print $3}')
    print_check "ok" "Git $GIT_VERSION найден"
else
    print_check "error" "Git не найден"
    echo -e "  ${INFO} Установите: brew install git (macOS) или sudo apt install git (Linux)"
fi

# Check 3: Virtual environment
echo ""
echo "Проверка виртуального окружения..."
if [ -d "$DIGEST_CORE_DIR/.venv" ]; then
    print_check "ok" "Виртуальное окружение найдено в digest-core/.venv"
    
    # Check if activated
    if [[ "$VIRTUAL_ENV" == *"digest-core/.venv"* ]]; then
        print_check "ok" "Виртуальное окружение активно"
    else
        print_check "warn" "Виртуальное окружение не активировано"
        echo -e "  ${INFO} Активируйте: source digest-core/.venv/bin/activate"
    fi
    
    # Check if digest_core installed
    if [ -f "$DIGEST_CORE_DIR/.venv/bin/python" ]; then
        if "$DIGEST_CORE_DIR/.venv/bin/python" -c "import digest_core" 2>/dev/null; then
            print_check "ok" "Пакет digest_core установлен"
        else
            print_check "warn" "Пакет digest_core не установлен"
            echo -e "  ${INFO} Установите: cd digest-core && .venv/bin/pip install -e ."
        fi
    fi
else
    print_check "warn" "Виртуальное окружение не найдено"
    echo -e "  ${INFO} Создайте: cd digest-core && python3.11 -m venv .venv"
fi

# Check 4: Environment variables
echo ""
echo "Проверка переменных окружения..."

check_env_var() {
    local var_name=$1
    local is_required=$2
    
    if [ -n "${!var_name:-}" ]; then
        # Mask sensitive values
        if [[ "$var_name" == *"PASSWORD"* ]] || [[ "$var_name" == *"TOKEN"* ]]; then
            print_check "ok" "$var_name установлена (***)"
        else
            print_check "ok" "$var_name = ${!var_name}"
        fi
    else
        if [ "$is_required" = "required" ]; then
            print_check "error" "$var_name не установлена (обязательная)"
        else
            print_check "warn" "$var_name не установлена (опциональная)"
        fi
    fi
}

check_env_var "EWS_ENDPOINT" "required"
check_env_var "EWS_USER_UPN" "required"
check_env_var "EWS_PASSWORD" "required"
check_env_var "LLM_ENDPOINT" "optional"
check_env_var "LLM_TOKEN" "optional"
check_env_var "OUT_DIR" "optional"
check_env_var "STATE_DIR" "optional"

# Check 5: Configuration file
echo ""
echo "Проверка конфигурационного файла..."
if [ -f "$DIGEST_CORE_DIR/configs/config.yaml" ]; then
    print_check "ok" "config.yaml найден"
    
    # Basic YAML validation
    if command -v python3 &> /dev/null; then
        if python3 -c "import yaml; yaml.safe_load(open('$DIGEST_CORE_DIR/configs/config.yaml'))" 2>/dev/null; then
            print_check "ok" "config.yaml валиден (YAML синтаксис)"
        else
            print_check "error" "config.yaml имеет ошибки синтаксиса"
        fi
    fi
else
    print_check "warn" "config.yaml не найден"
    echo -e "  ${INFO} Создайте: cp digest-core/configs/config.example.yaml digest-core/configs/config.yaml"
fi

# Check 6: Working directories
echo ""
echo "Проверка рабочих директорий..."

check_directory() {
    local dir_path=$1
    local dir_name=$2
    
    if [ -d "$dir_path" ]; then
        if [ -w "$dir_path" ]; then
            print_check "ok" "$dir_name существует и доступна для записи"
        else
            print_check "error" "$dir_name существует, но недоступна для записи"
            echo -e "  ${INFO} Исправьте: chmod 755 $dir_path"
        fi
    else
        print_check "warn" "$dir_name не существует"
        echo -e "  ${INFO} Создайте: mkdir -p $dir_path"
    fi
}

OUT_DIR="${OUT_DIR:-$HOME/.digest-out}"
STATE_DIR="${STATE_DIR:-$HOME/.digest-state}"
TMPDIR="${TMPDIR:-$HOME/.digest-temp}"
LOG_DIR="$HOME/.digest-logs"

check_directory "$OUT_DIR" "OUT_DIR ($OUT_DIR)"
check_directory "$STATE_DIR" "STATE_DIR ($STATE_DIR)"
check_directory "$TMPDIR" "TMPDIR ($TMPDIR)"
check_directory "$LOG_DIR" "LOG_DIR ($LOG_DIR)"

# Check 7: Network connectivity
echo ""
echo "Проверка сетевого подключения..."

check_connectivity() {
    local url=$1
    local name=$2
    
    if command -v curl &> /dev/null; then
        if curl -s --connect-timeout 5 -I "$url" > /dev/null 2>&1; then
            print_check "ok" "Доступ к $name ($url)"
        else
            print_check "warn" "Нет доступа к $name ($url)"
        fi
    else
        print_check "warn" "curl не установлен, пропускаем проверку подключения"
    fi
}

if [ -n "${EWS_ENDPOINT:-}" ]; then
    check_connectivity "$EWS_ENDPOINT" "EWS"
else
    print_check "warn" "EWS_ENDPOINT не установлен, пропускаем проверку"
fi

if [ -n "${LLM_ENDPOINT:-}" ]; then
    check_connectivity "$LLM_ENDPOINT" "LLM Gateway"
else
    print_check "warn" "LLM_ENDPOINT не установлен, пропускаем проверку"
fi

# Check 8: SSL certificates (if specified)
echo ""
echo "Проверка SSL сертификатов..."

if [ -f "$DIGEST_CORE_DIR/configs/config.yaml" ]; then
    # Extract verify_ca path from config (simple grep)
    CERT_PATH=$(grep -A 5 "ews:" "$DIGEST_CORE_DIR/configs/config.yaml" | grep "verify_ca:" | awk '{print $2}' | tr -d '"' | tr -d "'")
    
    if [ -n "$CERT_PATH" ]; then
        # Expand variables
        CERT_PATH=$(eval echo "$CERT_PATH")
        
        if [ -f "$CERT_PATH" ]; then
            print_check "ok" "CA сертификат найден: $CERT_PATH"
        else
            print_check "warn" "CA сертификат не найден: $CERT_PATH"
        fi
    else
        print_check "warn" "CA сертификат не указан в config.yaml (используется системный trust store)"
    fi
fi

# Check 9: Disk space
echo ""
echo "Проверка дискового пространства..."
if command -v df &> /dev/null; then
    AVAILABLE_KB=$(df -k "$HOME" | tail -1 | awk '{print $4}')
    AVAILABLE_MB=$((AVAILABLE_KB / 1024))
    
    if [ "$AVAILABLE_MB" -gt 500 ]; then
        print_check "ok" "Свободное место: ${AVAILABLE_MB} MB"
    elif [ "$AVAILABLE_MB" -gt 100 ]; then
        print_check "warn" "Свободное место: ${AVAILABLE_MB} MB (рекомендуется >500 MB)"
    else
        print_check "error" "Недостаточно места: ${AVAILABLE_MB} MB (требуется минимум 100 MB)"
    fi
fi

# Check 10: Required Python packages
echo ""
echo "Проверка Python зависимостей..."
if [ -f "$DIGEST_CORE_DIR/.venv/bin/python" ]; then
    VENV_PYTHON="$DIGEST_CORE_DIR/.venv/bin/python"
    
    check_package() {
        local package=$1
        if $VENV_PYTHON -c "import $package" 2>/dev/null; then
            print_check "ok" "Пакет $package установлен"
        else
            print_check "error" "Пакет $package не установлен"
        fi
    }
    
    check_package "pydantic"
    check_package "yaml"
    check_package "jinja2"
else
    print_check "warn" "Виртуальное окружение не найдено, пропускаем проверку пакетов"
fi

# Summary
echo ""
echo "======================================"
echo "  Итоги диагностики"
echo "======================================"
echo -e "${GREEN}✓ Успешно: $SUCCESS${NC}"
echo -e "${YELLOW}⚠ Предупреждений: $WARNINGS${NC}"
echo -e "${RED}✗ Ошибок: $ERRORS${NC}"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}🎉 Все проверки пройдены! Система готова к работе.${NC}"
    echo ""
    echo "Следующие шаги:"
    echo "  1. source .env"
    echo "  2. cd digest-core"
    echo "  3. python3.11 -m digest_core.cli run --dry-run"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ Есть предупреждения, но система должна работать.${NC}"
    echo ""
    echo "Рекомендуется устранить предупреждения перед production использованием."
    exit 0
else
    echo -e "${RED}✗ Обнаружены критические ошибки!${NC}"
    echo ""
    echo "Исправьте ошибки, затем запустите снова: ./scripts/doctor.sh"
    echo ""
    echo "Для помощи см.:"
    echo "  - docs/testing/E2E_TESTING_GUIDE.md"
    echo "  - docs/troubleshooting/TROUBLESHOOTING.md"
    exit 1
fi
