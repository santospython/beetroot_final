import calendar


class Income:
    def __init__(self, year, month, amount = 0) -> None:
        self.year = year
        self.month = month
        self.amount = amount

    def __str__(self) -> str:
        return f"{self.amount:.2f}"

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("Only dict is allowed")
        
        if not data:
            raise ValueError("Empty dict is not allowed")

        if 'year' not in data or 'month' not in data or 'amount' not in data:
            raise ValueError("Dict should contain 'year', 'month' and 'amount'")

        return cls(data["year"], data["month"], data["amount"])    

    def to_dict(self) -> dict:
        return {
            'year': self.year,
            'month': self.month,
            'amount': self.amount,
        }

    def get_month(self):
        return calendar.month_name[self.month]
    
    def get_date_label(self):
        return f"{self.get_month():>9} {self.year}"
    
    def present(self):
        return f"{self.get_date_label()}: {self.amount:.2f}"
    
    @property
    def date_label(self):
        return self.get_date_label()