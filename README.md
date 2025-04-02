# Лабораторная работа №2: Разработка 2D-игры "Crimsonland"

В рамках лабораторной работы №2 была разработана игра в стиле top-down шутера с использованием библиотеки PyGame. Проект реализует основные механики survival-жанра с динамическим геймплеем и системой прогрессии.

## Описание функционала

### Главное меню и интерфейс
- Экран старта игры с возможностью выбора: 
  - Начать новую игру
  - Просмотреть рекорды
  - Ознакомиться с правилами
  - Выйти из приложения
- Интерактивный HUD с отображением:
  - Здоровья игрока
  - Текущего боезапаса
  - Номера волны
  - Статуса перка
- Адаптивная камера, следящая за перемещением персонажа

### Управление игровым процессом
- Перемещение персонажа с помощью WASD
- Стрельба в направлении курсора мыши
- Система перезарядки оружия (пробел)
- Активация специального умения (Enter)
- Пауза и возобновление игры

### Система оружия и боевая механика
- 3 типа вооружения с уникальными характеристиками:
  - Пистолет (базовый урон, средняя перезарядка)
  - Автомат (высокая скорострельность)
  - Дробовик (зонный урон с разбросом)
- Реалистичная баллистика пуль
- Система подбора оружия с земли
- Визуализация траектории выстрелов

### Генерация врагов и волн
- Прогрессивная система волн (20 уровней сложности)
- Несколько типов противников с уникальным поведением:
  - Стандартные мобы
  - Тяжелые танки
  - Скоростные юниты
  - Дальнобойные стрелки
- Динамический спавн врагов на границах карты
- Автоматическое увеличение характеристик противников с каждой волной

### Сохранение и анализ статистики
- Запись рекордов в JSON-файл:
  - Максимальное время выживания
  - Общее количество убийств
  - Средний показатель сессий
- Система достижений:
  - "Сурвивалист" (преодоление 10 волн)
  - "Охотник за головами" (100 убийств)
  - "Неуязвимый" (завершение без потери здоровья)

### Обработка игровых событий
- Реалистичная система столкновений:
  - Пули ↔ враги
  - Персонаж ↔ препятствия
  - Спецэффекты ↔ окружение
- Разрушаемые объекты окружения (деревья, камни)
- Интерактивные зоны (замедляющие болота)

### Аудиовизуальное сопровождение
- 3 оригинальных саундтрека:
  - Меню
  - Игровой процесс
  - Финальный босс
- Система позиционного звука:
  - Выстрелы
  - Крики врагов
  - Предупреждения об атаках
- Частицы и эффекты:
  - Кровь при попадании

## Заключение

Разработанная игра демонстрирует комплексный подход к созданию 2D-экшена с использованием парадигм ООП. Реализованы ключевые механики современных survival-игр, включая прогрессивную систему сложности, разнообразие вооружения и детальную статистику.

