# Тестирование ActionPulse

Добро пожаловать в раздел тестирования! Здесь собрана вся документация для тестирования ActionPulse на различных платформах.

---

## 🎯 Быстрая навигация

### Для тестировщиков

**Вы впервые устанавливаете проект?**
→ Начните с **[E2E Testing Guide](./E2E_TESTING_GUIDE.md)**

**Уже установили и нужен детальный чек-лист?**
→ См. **[Manual Testing Checklist](../../docs/testing/MANUAL_TESTING_CHECKLIST.md)**

**Готовы отправить результаты?**
→ См. **[Send Results Guide](../../docs/testing/SEND_RESULTS.md)**

### Для разработчиков

**Нужно проверить документацию?**
→ См. **[Documentation Validation](./DOCUMENTATION_VALIDATION.md)**

**Добавляете новые фичи?**
→ См. **[Testing Strategy](../development/TESTING.md)**

---

## 📚 Доступные документы

### Основные гайды

#### [E2E Testing Guide](./E2E_TESTING_GUIDE.md) ⭐
**Для кого:** Тестировщики, QA, новые пользователи  
**Что включает:**
- Пошаговая установка с нуля
- Настройка на корпоративных ноутбуках
- Smoke-тестирование и полный цикл
- Сбор диагностики
- Отправка результатов
- Troubleshooting

**Время:** ~30 минут

---

#### [Manual Testing Checklist](../../docs/testing/MANUAL_TESTING_CHECKLIST.md)
**Для кого:** Опытные тестировщики, детальное тестирование  
**Что включает:**
- Детальный чек-лист по этапам
- Проверка граничных случаев
- Проверка качества (PII, точность, производительность)
- Специфичные проверки для корпоративных сред

**Время:** 1-2 часа

---

#### [Send Results Guide](../../docs/testing/SEND_RESULTS.md)
**Для кого:** Все тестировщики  
**Что включает:**
- Чек-лист перед отправкой
- Шаблоны отчетов
- Примеры (успешный/с проблемами)
- Проверка безопасности
- Альтернативные способы передачи

---

### Примеры и референсы

#### [Примеры отчетов](./examples/)

**[Успешный отчет](./examples/successful_test_report.md)**
- Пример полного успешного тестирования
- Все метрики и результаты
- Формат email

**[Отчет с проблемами](./examples/failed_test_report.md)**
- Детальное описание ошибок
- Workarounds и решения
- Рекомендации по исправлению

**[Corporate Laptop Setup](./examples/corporate_laptop_setup.md)**
- Специфика корпоративных ноутбуков
- Типичные ограничения и решения
- Конфигурация для разных ОС
- Работа с прокси, SSL, NTLM

---

### Для разработчиков

#### [Documentation Validation](./DOCUMENTATION_VALIDATION.md)
**Для кого:** Разработчики документации, контрибьюторы  
**Что включает:**
- Чек-листы проверки документации
- Процедура валидации на чистой машине
- Автоматические проверки
- Шаблон отчета о валидации

---

## 🚀 Быстрый старт

### Сценарий 1: Первая установка и тестирование

```bash
# 1. Прочитайте E2E Testing Guide
# 2. Запустите диагностику
./digest-core/scripts/doctor.sh

# 3. Следуйте гайду пошагово
# 4. Соберите результаты
cd digest-core && ./digest-core/scripts/collect_diagnostics.sh

# 5. Отправьте отчет (см. Send Results Guide)
```

### Сценарий 2: Детальное тестирование существующей установки

```bash
# 1. Убедитесь, что система настроена
./digest-core/scripts/doctor.sh

# 2. Следуйте Manual Testing Checklist
# 3. Отмечайте выполненные пункты
# 4. Соберите диагностику при проблемах
```

### Сценарий 3: Тестирование на корпоративном ноутбуке

```bash
# 1. Прочитайте Corporate Laptop Setup Guide
# 2. Примените workarounds для вашей ОС
# 3. Следуйте E2E Testing Guide
# 4. Используйте Failed Test Report template при проблемах
```

---

## 🛠️ Инструменты

### Скрипты для тестирования

**`digest-core/scripts/doctor.sh`** - Комплексная диагностика окружения
```bash
./digest-core/scripts/doctor.sh
# Проверяет: Python, Git, venv, env vars, config, directories, network
```

**`digest-core/scripts/test_run.sh`** - Автоматический тестовый запуск
```bash
cd digest-core
./digest-core/scripts/test_run.sh
# Запускает полный цикл + автоматический сбор диагностики
```

**`digest-core/scripts/collect_diagnostics.sh`** - Сбор диагностики
```bash
cd digest-core
./digest-core/scripts/collect_diagnostics.sh
# Создает архив: logs, metrics, config, system info
```

---

## 📋 Чек-лист перед началом тестирования

### Подготовка

- [ ] Прочитали [E2E Testing Guide](./E2E_TESTING_GUIDE.md)
- [ ] Есть доступ к учетным данным EWS
- [ ] Есть токен LLM Gateway (опционально для dry-run)
- [ ] Машина соответствует минимальным требованиям
- [ ] Есть права на создание файлов в `$HOME`

### Корпоративный ноутбук (дополнительно)

- [ ] Прочитали [Corporate Laptop Setup](./examples/corporate_laptop_setup.md)
- [ ] Получили корпоративный CA сертификат (если нужен)
- [ ] Знаете адрес прокси сервера (если есть)
- [ ] Подтвердили доступ к EWS и LLM endpoints

### После тестирования

- [ ] Выполнили все необходимые тесты
- [ ] Собрали архив диагностики
- [ ] Заполнили шаблон отчета
- [ ] Проверили, что архив не содержит секреты
- [ ] Готовы отправить результаты

---

## 🆘 Нужна помощь?

### Проблемы при установке
→ См. [E2E Testing Guide - Troubleshooting](./E2E_TESTING_GUIDE.md#troubleshooting)

### Проблемы на корпоративном ноутбуке
→ См. [Corporate Laptop Setup](./examples/corporate_laptop_setup.md)

### Общие проблемы
→ См. [Global Troubleshooting Guide](../troubleshooting/TROUBLESHOOTING.md)

### Диагностика
→ Запустите `./digest-core/scripts/doctor.sh`

---

## 🔗 Связанная документация

### Installation
- [Quick Start](../installation/QUICK_START.md) - Быстрый старт за 5 минут
- [Installation Guide](../installation/INSTALL.md) - Подробное руководство

### Operations
- [Deployment](../operations/DEPLOYMENT.md) - Production развертывание
- [Automation](../operations/AUTOMATION.md) - Автоматизация запусков
- [Monitoring](../operations/MONITORING.md) - Мониторинг и метрики

### Development
- [Architecture](../development/ARCHITECTURE.md) - Архитектура системы
- [Testing Strategy](../development/TESTING.md) - Стратегия тестирования для разработчиков
- [Contributing](../../CONTRIBUTING.md) - Как контрибьютить

### Troubleshooting
- [Main Troubleshooting](../troubleshooting/TROUBLESHOOTING.md) - Решение проблем
- [EWS Connection](../troubleshooting/EWS_CONNECTION.md) - Проблемы с EWS

---

## 📝 Обратная связь

Если нашли ошибки в документации или есть предложения:

1. Создайте issue с тегом `documentation`
2. Опишите проблему или предложение
3. Укажите, какой документ затронут
4. Предложите исправление (опционально)

Или следуйте [Documentation Validation](./DOCUMENTATION_VALIDATION.md) для систематической проверки.

---

## 📊 Метрики качества документации

Цели для документации:
- ✅ E2E тестирование завершается за < 30 минут
- ✅ 95%+ успешных первых запусков на чистых машинах
- ✅ Все типичные проблемы покрыты в troubleshooting
- ✅ Документация валидируется на 3+ ОС (macOS, Linux, Windows/WSL)

---

**Спасибо за тестирование ActionPulse!** 🎉

Ваша обратная связь помогает улучшить проект.


