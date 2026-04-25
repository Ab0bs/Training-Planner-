import tkinter as tk
from tkinter import ttk, messagebox
from data_manager import WorkoutDataManager
from validator import DataValidator

class TrainingPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.root.geometry("800x600")
        self.workouts = WorkoutDataManager.load_workouts()
        self.setup_ui()

    def setup_ui(self):
        # Форма ввода
        input_frame = ttk.LabelFrame(self.root, text="Добавить тренировку")
        input_frame.pack(pady=10, padx=20, fill='x')

        # Дата
        ttk.Label(input_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.date_entry = ttk.Entry(input_frame, width=15)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        # Тип тренировки
        ttk.Label(input_frame, text="Тип тренировки:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.type_var = tk.StringVar()
        types = ["Все", "Кардио", "Силовая", "Йога", "Растяжка", "Функциональная"]
        self.type_combo = ttk.Combobox(input_frame, textvariable=self.type_var, values=types, state="readonly", width=15)
        self.type_combo.grid(row=1, column=1, padx=5, pady=5)
        self.type_combo.set("Кардио")

        # Длительность
        ttk.Label(input_frame, text="Длительность (мин):").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.duration_entry = ttk.Entry(input_frame, width=15)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка добавления
        ttk.Button(input_frame, text="Добавить тренировку", command=self.add_workout).grid(row=3, column=0, columnspan=2, pady=10)

        # Таблица тренировок
        table_frame = ttk.LabelFrame(self.root, text="Тренировки")
        table_frame.pack(pady=10, padx=20, fill='both', expand=True)

        columns = ('date', 'type', 'duration')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)

        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=150)
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Фильтры
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(pady=5, padx=20, fill='x')

        ttk.Label(filter_frame, text="Фильтр по типу:").pack(side='left', padx=5)
        self.filter_type_var = tk.StringVar(value="Все")
        filter_type = ttk.Combobox(filter_frame, textvariable=self.filter_type_var, values=["Все", "Кардио", "Силовая", "Йога", "Растяжка", "Функциональная"], state="readonly", width=15)
        filter_type.pack(side='left', padx=5)

        ttk.Label(filter_frame, text="Дата:").pack(side='left', padx=5)
        self.filter_date_entry = ttk.Entry(filter_frame, width=15)
        self.filter_date_entry.pack(side='left', padx=5)

        ttk.Button(filter_frame, text="Применить фильтры", command=self.apply_filters).pack(side='left', padx=10)
        ttk.Button(filter_frame, text="Сбросить фильтры", command=self.reset_filters).pack(side='left')

        self.display_workouts()

    def add_workout(self):
        date = self.date_entry.get().strip()
        workout_type = self.type_var.get()
        duration = self.duration_entry.get().strip()

        # Валидация
        is_valid_date, date_error = DataValidator.validate_date(date)
        if not is_valid_date:
            messagebox.showerror("Ошибка", date_error)
            return

        is_valid_duration, duration_error = DataValidator.validate_duration(duration)
        if not is_valid_duration:
            messagebox.showerror("Ошибка", duration_error)
            return

        # Добавление тренировки
        workout = {
            'date': date,
            'type': workout_type,
            'duration': float(duration)
        }
        self.workouts.append(workout)
        WorkoutDataManager.save_workouts(self.workouts)
        self.display_workouts()
        messagebox.showinfo("Успех", "Тренировка добавлена!")

        # Очистка полей
        self.date_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

    def display_workouts(self, workouts=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        display_list = workouts if workouts is not None else self.workouts
        for workout in display_list:
            self.tree.insert('', 'end', values=(
                workout['date'],
                workout['type'],
                f"{workout['duration']} мин"
            ))

    def apply_filters(self):
        workout_type = self.filter_type
