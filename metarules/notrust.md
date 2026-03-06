# notrust - Мінімізація інструментів

## ПРОБЛЕМА
Після кожного інструменту треба натискати `t` (trust), навіть якщо вже дав trust for session.

## ПРАВИЛО
**Мінімізуй кількість викликів інструментів. Роби більше за один виклик.**

## ЯК ЗАСТОСОВУВАТИ

### ❌ ПОГАНО (багато викликів):
```
1. fs_write - створити файл A
2. fs_write - створити файл B  
3. execute_bash - chmod A
4. execute_bash - chmod B
5. execute_bash - git add
6. execute_bash - git commit
```
**Результат:** 6 разів натискати `t`

### ✅ ДОБРЕ (мінімум викликів):
```
1. fs_write - створити файл A
2. fs_write - створити файл B
3. execute_bash - chmod +x A B && git add -A && git commit -m "msg"
```
**Результат:** 3 рази натискати `t`

### ✅ ІДЕАЛЬНО (один скрипт):
```
1. fs_write - створити deploy.sh з усіма командами
2. execute_bash - chmod +x deploy.sh
```
**Результат:** 2 рази натискати `t`

## ПРИКЛАДИ

### Створення багатьох файлів
❌ Погано:
- fs_write file1.py
- fs_write file2.py
- fs_write file3.py

✅ Добре:
- fs_write file1.py
- fs_write file2.py (якщо різний контент)
- АБО створити один скрипт який генерує всі файли

### Bash команди
❌ Погано:
- execute_bash "mkdir dir"
- execute_bash "cd dir"
- execute_bash "touch file"

✅ Добре:
- execute_bash "mkdir -p dir && cd dir && touch file"

### Git операції
❌ Погано:
- execute_bash "git add file1"
- execute_bash "git add file2"
- execute_bash "git commit -m 'msg'"

✅ Добре:
- execute_bash "git add -A && git commit -m 'msg'"

## ВИКЛЮЧЕННЯ

Коли ТРЕБА робити окремі виклики:
1. **Перевірка між кроками** (startcheck)
2. **Різна логіка** (if/else)
3. **Читання результату** між кроками

## КОМБІНАЦІЯ З ІНШИМИ ПРАВИЛАМИ

### + selfself
Не питай дозволу, роби пакетом.

### + noblock
Не запускай довгі інтерактивні команди.

### + scriptsmany
Якщо >3 команди → створи .sh скрипт.

## ПРИКЛАД ЗАСТОСУВАННЯ

### Завдання: Створити 3 файли, зробити executable, commit

❌ Без notrust (9 викликів):
```
fs_write file1.py
fs_write file2.py
fs_write file3.py
execute_bash chmod +x file1.py
execute_bash chmod +x file2.py
execute_bash chmod +x file3.py
execute_bash git add file1.py
execute_bash git add file2.py
execute_bash git commit -m "msg"
```

✅ З notrust (4 виклики):
```
fs_write file1.py
fs_write file2.py
fs_write file3.py
execute_bash "chmod +x *.py && git add -A && git commit -m 'msg'"
```

✅ З notrust + scriptsmany (2 виклики):
```
fs_write setup.sh (містить всі команди)
execute_bash "chmod +x setup.sh && ./setup.sh"
```

## ВИСНОВОК

**Кожен виклик інструменту = натискання `t`**

Мінімізуй виклики → менше натискань → швидша робота.
