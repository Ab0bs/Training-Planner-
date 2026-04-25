from datetime import datetime

class DataValidator:
    @staticmethod
    def validate_date(date_str):
        try:
            datetime.strptime(date_str, '%d.%m.%Y')
            return True, None
        except ValueError:
            return False, "Дата должна быть в формате ДД.ММ.ГГГГ"

    @staticmethod
    def validate_duration(duration_str):
        try:
            duration = float(duration_str)
            if duration <= 0:
                return False, "Длительность должна быть положительным числом"
            return True, None
        except ValueError:
            return False, "Длительность должна быть числом"
