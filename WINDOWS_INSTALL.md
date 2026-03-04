# 🪟 Запуск Worker в Windows (не WSL!)

## ❌ Проблема
**pynput не ловить hotkeys з WSL!** Треба запускати в Windows.

## ✅ Рішення

### 1. Встанови Python в Windows
Завантаж: https://www.python.org/downloads/
- ✅ Поставь галочку "Add Python to PATH"

### 2. Скопіюй файли в Windows
```bash
# З WSL скопіюй в Windows
cp /home/butenhome/aiwork/worker.py /mnt/c/Users/Lenovo/Desktop/
cp /home/butenhome/aiwork/requirements.txt /mnt/c/Users/Lenovo/Desktop/
```

### 3. Встанови залежності (Windows PowerShell)
```powershell
cd C:\Users\Lenovo\Desktop
pip install -r requirements.txt
```

### 4. Запусти worker (Windows PowerShell)
```powershell
python worker.py
```

## 🎮 Hotkeys працюватимуть!
- **Alt+Shift+1** = ✅ Добре
- **Alt+Shift+2** = ⚠️ Є проблеми
- **Alt+Shift+3** = ❌ Критичні помилки
- **Alt+Shift+0** = 🚫 Пропустити

---

## 🔧 Альтернатива: keyboard замість pynput

Можна спробувати бібліотеку `keyboard` - вона краще працює з WSL:
```bash
pip install keyboard
```

Але треба запускати з `sudo`:
```bash
sudo python3 worker.py
```
