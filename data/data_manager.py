import json
import os

class WorkoutDataManager:
    DATA_FILE = "data/workouts.json"

    @staticmethod
    def load_workouts():
        if os.path.exists(WorkoutDataManager.DATA_FILE):
            with open(WorkoutDataManager.DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    @staticmethod
    def save_workouts(workouts):
        with open(WorkoutDataManager.DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(workouts, f, ensure_ascii=False, indent=2)

    @staticmethod
    def filter_workouts(workouts, workout_type=None, date=None):
        filtered = workouts
        if workout_type and workout_type != "Все":
            filtered = [w for w in filtered if w['type'] == workout_type]
        if date:
            filtered = [w for w in filtered if w['date'] == date]
        return filtered
