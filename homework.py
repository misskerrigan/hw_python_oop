import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        return sum(record.amount
                   for record in self.records
                   if record.date == today)

    def get_week_stats(self):
        today = dt.date.today()
        return sum(record.amount
                   for record in self.records
                   if today - dt.timedelta(days=6) <= record.date <= today)

    def today_balance(self):
        day_balance = self.limit - self.get_today_stats()
        return day_balance


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()

    def show(self):
        return self.amount, self.comment, self.date


class CashCalculator(Calculator):
    EURO_RATE = 90.5
    USD_RATE = 70.5

    def get_today_cash_remained(self, currency):
        course = {
            'rub': (1, 'руб'),
            'usd': (CashCalculator.USD_RATE, 'USD'),
            'eur': (CashCalculator.EURO_RATE, 'Euro')
        }
        if currency not in course:
            return 'Неподдерживаемая валюта'
        if self.today_balance() == 0:
            return f'Денег нет, держись'
        rate, currency_name = course[currency]
        balance = round(self.today_balance() / rate, 2)
        if balance > 0:
            return f'На сегодня осталось {balance} {currency_name}'
        balance = abs(balance)
        return f'Денег нет, держись: твой долг - {balance} {currency_name}'


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        if self.today_balance() > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {self.today_balance()} кКал')
        return f'Хватит есть!'
