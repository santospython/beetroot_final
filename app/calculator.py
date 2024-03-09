from datetime import date
import datetime
import operator
import os

from app.models import Income
from app.store import Storage
from settings import tax_percent, app_name, app_version

import json
import matplotlib.pyplot as plt
import numpy as np


class TaxCalculator:
    def __init__(self, storage=None) -> None:
        self.storage = Storage() if storage is None else storage
        self.storage.load()

    def __str__(self) -> str:
        return f"{app_name}/{app_version}"

    def add_income(self):
        year = int(input("Year: "))
        today = date.today()
        if year > today.year:
            raise ValueError("Year should not be in the future")

        month = int(input("Month (1-12): "))
        if 1 > month > 12:
            raise ValueError("Month should be between 1 and 12")

        amount = float(input("Income amount: "))
        if amount < 0:
            raise ValueError("Income should not be negative")

        self.storage.add_income(Income(year, month, amount))
        self.storage.save()


    def reload_incomes(self):
        self.storage.load()


    def print_tax(self):
        total_income = self.get_total_income()
        tax_amount = total_income * tax_percent
        print(f"Tax to be paid: {tax_amount:0.2f}")


    def print_incomes(self):
        if not self.storage.incomes:
            print("No incomes. Please start adding a new one.")
            return

        for income in self.storage.incomes:
            print(income.present())

    def print_stats(self):
        min_income = 0 if not self.storage.incomes else self.storage.incomes[0].amount
        max_income = 0 if not self.storage.incomes else self.storage.incomes[0].amount
        avg_income = 0

        for income in self.storage.incomes:
            amount = income.amount

            if amount < min_income:
                min_income = amount

            if amount > max_income:
                max_income = amount

        total_income = self.get_total_income()    

        if self.storage.incomes:
            avg_income = total_income / len(self.storage.incomes)
        
        print(f"Minimum income: {min_income:.2f}")
        print(f"Maximum income: {max_income:.2f}")
        print(f"Average income: {avg_income:.2f}")
        print(f"Total income: {total_income:.2f}")


    def show_graphic(self):
        if not self.storage.incomes:
            print("No incomes. Please start adding a new one.")
            return
        
        labels = []
        amounts = []
        for income in self.storage.incomes:
            labels.append(income.date_label)
            amounts.append(income.amount)

        fig, ax = plt.subplots()

        x_labels = [income.date_label for income in self.storage.incomes]
        y_values = [income.amount for income in self.storage.incomes]

        lin_reg = np.polyfit(range(len(x_labels)), y_values, 1)
        trendline = lin_reg[0] * np.array(range(len(x_labels))) + lin_reg[1]

        for i, income in enumerate(self.storage.incomes):
            plt.bar(i, income.amount, color='steelblue')

            if income.amount == max(y_values):
                plt.annotate('Highest', xy=(i, income.amount), xytext=(15, 15), textcoords='offset points', color = 'green', arrowprops=dict(arrowstyle="-|>", color = 'black'))

            if income.amount == min(y_values):
                plt.annotate('Lowest', xy=(i, income.amount), xytext=(15, -15), textcoords='offset points', color = 'red', arrowprops=dict(arrowstyle="-|>", color = 'black'))

        average = sum(y_values) / len(y_values)
        x_avg = len(x_labels) + 1
        plt.plot(trendline, label='Trendline', color='orange')
        average = sum(amounts) / len(amounts)
        plt.text(0.5, average, f'Average: {average:.2f}', ha='center', va='bottom')


        plt.xticks(range(len(x_labels)), x_labels, rotation=45)
        plt.xlabel('Month and year')
        plt.ylabel('Amount (euros)')
        plt.title('Income Data')
        plt.legend(['Trendline'])
        plt.tight_layout()
        plt.show()

        for income in self.storage.incomes:
            amount = income.amount
            print(f"{income.date_label}: {'-' * int(amount // 50)}")

    def get_total_income(self):
        return sum(map(operator.attrgetter('amount'), self.storage.incomes))