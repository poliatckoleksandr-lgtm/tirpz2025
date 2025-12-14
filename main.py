import tkinter as tk
from tkinter import messagebox, ttk
from abc import ABC, abstractmethod
import time
import threading
import math
import re # Для аналізу тексту (імітація AI)

# ==========================================
# 1. ІНТЕРФЕЙСИ (Архітектура)
# ==========================================

class ICalcModule(ABC):
    """
    Інтерфейс для модулів. Забезпечує гнучкість системи (DCF 02).
    """
    @abstractmethod
    def calculate(self, data: str) -> str:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

# ==========================================
# 2. МОДУЛІ (Бізнес-логіка)
# ==========================================

class FinanceModule(ICalcModule):
    """
    Фінансовий модуль: Складні відсотки.
    """
    def get_name(self) -> str:
        return "Фінансовий"

    def calculate(self, data: str) -> str:
        try:
            # Очікуємо: Сума, Ставка, Роки
            parts = data.split(',')
            if len(parts) != 3:
                return "Помилка: Введіть 'P, r, t' (Сума, %, Роки)"
            
            p = float(parts[0])
            r = float(parts[1])
            t = float(parts[2])
            
            # Формула: A = P(1 + r/100)^t
            result = p * (math.pow((1 + r / 100), t))
            return f"Кінцева сума: {result:.2f} грн"
        except ValueError:
            return "Помилка: Некоректні числа"

class EngineeringModule(ICalcModule):
    """
    Інженерний модуль: Балістика.
    """
    def get_name(self) -> str:
        return "Інженерний (Балістика)"

    def calculate(self, data: str) -> str:
        try:
            # Очікуємо: Швидкість, Кут
            parts = data.split(',')
            if len(parts) != 2:
                return "Помилка: Введіть 'V, Angle' (напр. 50, 45)"
            
            v0 = float(parts[0])
            angle_deg = float(parts[1])
            g = 9.81
            
            if angle_deg < 0 or angle_deg > 90:
                return "Помилка: Кут має бути 0-90°"
            if v0 < 0:
                return "Помилка: Швидкість > 0"

            # Конвертація в радіани для формул
            angle_rad = math.radians(angle_deg)
            
            # Дальність: L = (v^2 * sin(2a)) / g
            distance = (v0**2 * math.sin(2 * angle_rad)) / g
            
            # Висота: H = (v^2 * sin(a)^2) / 2g
            height = (v0**2 * (math.sin(angle_rad)**2)) / (2 * g)
            
            return f"Дальність: {distance:.1f} м | Висота: {height:.1f} м"
        except ValueError:
            return "Помилка: Некоректні дані"

class BasicModule(ICalcModule):
    """
    Базовий модуль: Арифметика.
    """
    def get_name(self) -> str:
        return "Базовий"
    
    def calculate(self, data: str) -> str:
        try:
            # Проста перевірка на допустимі символи для безпеки
            allowed_chars = set("0123456789+-*/(). ")
            if not set(data).issubset(allowed_chars):
                return "Помилка: Недопустимі символи"
            
            # У навчальних цілях використовуємо eval
            result = eval(data) 
            return f"{result}"
        except ZeroDivisionError:
            return "Помилка: Ділення на нуль"
        except Exception:
            return "Помилка виразу"

# ==========================================
# 3. СЕРВІСИ (AI та Історія)
# ==========================================

class HistoryLog:
    """Сервіс для збереження історії операцій."""
    def __init__(self):
        self._records = []

    def add_record(self, record: str):
        timestamp = time.strftime("%H:%M:%S")
        entry = f"[{timestamp}] {record}"
        self._records.append(entry)

    def get_history(self):
        return self._records

class SmartAIAssistant:
    """
    Локальний AI-асистент (без API ключа).
    Використовує евристичні правила для імітації "розумних" підказок.
    """
    def explain_formula(self, formula: str, current_module_name: str, callback):
        """
        Імітує асинхронний запит до сервера.
        """
        def thread_target():
            # 1. Імітація затримки мережі ("думки" AI)
            time.sleep(1.5) 
            
            # 2. Локальний аналіз (Heuristic Logic)
            explanation = self._analyze_logic(formula, current_module_name)
            
            # 3. Повернення результату
            callback(explanation)

        threading.Thread(target=thread_target, daemon=True).start()

    def _analyze_logic(self, formula: str, context: str) -> str:
        """Внутрішній 'мозок' помічника"""
        
        # --- Аналіз порожнього вводу ---
        if not formula.strip():
            return "AI: Введіть дані для аналізу."

        # --- Аналіз помилок ---
        if "/0" in formula:
            return "⚠️ Увага! Спроба ділення на нуль. Це математично неможливо."

        # --- Контекст: ФІНАНСИ ---
        if "Фінансовий" in context:
            parts = formula.split(',')
            if len(parts) == 3:
                return (f"AI Фінанси:\n"
                        f"Ви розраховуєте депозит. Формула: A = P(1 + r/100)^t.\n"
                        f"Це покаже, скільки грошей ви отримаєте з урахуванням капіталізації.")
            return "AI Підказка: Для фінансів введіть 3 числа через кому: 'Сума, Ставка, Роки'."

        # --- Контекст: ІНЖЕНЕРІЯ ---
        if "Інженерний" in context:
            if "," in formula:
                return ("AI Балістика:\n"
                        "Ви розраховуєте політ снаряда.\n"
                        "Я використовую фізичні формули руху під кутом до горизонту (g=9.81 м/с²).")
            return "AI Підказка: Введіть 'Швидкість, Кут' для розрахунку траєкторії."

        # --- Контекст: БАЗОВИЙ ---
        explanation = []
        if "**" in formula:
            explanation.append("• Використано піднесення до степеня.")
        if "%" in formula:
            explanation.append("• Використано оператор залишку від ділення.")
        if "*" in formula:
            explanation.append("• Виконується множення.")
        
        if explanation:
            return "AI Аналіз синтаксису:\n" + "\n".join(explanation)
        
        try:
            # Спроба передбачити результат
            res = eval(formula)
            return f"AI Прогноз: Вираз коректний. Орієнтовний результат ≈ {res}"
        except:
            return "AI: Вираз виглядає незавершеним або містить помилку."

# ==========================================
# 4. ГОЛОВНИЙ КЛАС (GUI)
# ==========================================

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Calc (Local AI)")
        self.root.geometry("550x550")

        # Ініціалізація сервісів
        self.history = HistoryLog()
        self.ai = SmartAIAssistant() # Використовуємо локальний клас
        
        # Реєстрація модулів
        self.modules = {
            "Базовий": BasicModule(),
            "Фінансовий": FinanceModule(),
            "Інженерний": EngineeringModule()
        }
        self.current_module = self.modules["Базовий"]

        self._setup_ui()

    def _setup_ui(self):
        # Панель вибору модуля
        frame_top = tk.Frame(self.root, pady=10)
        frame_top.pack()
        
        tk.Label(frame_top, text="Активний модуль:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.module_var = tk.StringVar(value="Базовий")
        module_selector = ttk.OptionMenu(frame_top, self.module_var, "Базовий", *self.modules.keys(), command=self.load_module)
        module_selector.pack(side=tk.LEFT, padx=10)

        # Інструкція та ввід
        self.lbl_instruction = tk.Label(self.root, text="Введіть вираз (напр. 2+2):", fg="gray")
        self.lbl_instruction.pack(pady=5)

        self.entry_input = tk.Entry(self.root, font=("Consolas", 14), width=40)
        self.entry_input.pack(pady=5)

        # Кнопки
        frame_btns = tk.Frame(self.root)
        frame_btns.pack(pady=15)

        btn_calc = tk.Button(frame_btns, text="ОБЧИСЛИТИ", command=self.perform_calculation, bg="#4CAF50", fg="white", width=15)
        btn_calc.pack(side=tk.LEFT, padx=10)

        btn_ai = tk.Button(frame_btns, text="AI Допомога", command=self.request_ai_help, bg="#2196F3", fg="white", width=15)
        btn_ai.pack(side=tk.LEFT, padx=10)

        # Результат
        self.lbl_result = tk.Label(self.root, text="Результат: ...", font=("Arial", 12), bg="#f0f0f0", width=50, height=2)
        self.lbl_result.pack(pady=10)

        # Історія
        tk.Label(self.root, text="Журнал операцій:", font=("Arial", 10, "bold")).pack(pady=(20, 0))
        
        frame_hist = tk.Frame(self.root)
        frame_hist.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(frame_hist)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox_history = tk.Listbox(frame_hist, height=8, yscrollcommand=scrollbar.set, font=("Consolas", 9))
        self.listbox_history.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.listbox_history.yview)

    def load_module(self, module_name):
        self.current_module = self.modules[module_name]
        hints = {
            "Фінансовий": "Формат: Сума, Ставка, Роки (напр. 1000, 10, 5)",
            "Інженерний": "Формат: Швидкість, Кут (напр. 50, 45)",
            "Базовий": "Введіть вираз (напр. 2+2*2)"
        }
        self.lbl_instruction.config(text=hints.get(module_name, ""))
        self.entry_input.delete(0, tk.END)

    def perform_calculation(self):
        data = self.entry_input.get()
        if not data: return
        
        result = self.current_module.calculate(data)
        
        self.lbl_result.config(text=result)
        self.history.add_record(f"[{self.current_module.get_name()}] {data} -> {result}")
        self._update_history_ui()

    def _update_history_ui(self):
        self.listbox_history.delete(0, tk.END)
        for rec in reversed(self.history.get_history()):
            self.listbox_history.insert(tk.END, rec)

    def request_ai_help(self):
        formula = self.entry_input.get()
        if not formula:
            messagebox.showwarning("AI", "Введіть дані для аналізу")
            return
        
        # Контекст передається для "розумної" відповіді
        self.lbl_result.config(text="AI аналізує...", fg="blue")
        self.ai.explain_formula(formula, self.current_module.get_name(), self._show_ai_response)

    def _show_ai_response(self, text):
        self.lbl_result.config(text="Готово", fg="black")
        messagebox.showinfo("AI Асистент", text)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()