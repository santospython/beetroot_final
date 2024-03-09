from settings import app_name, app_version
from app.calculator import TaxCalculator


def main():
    calculator = TaxCalculator()

    print(f"Welcome to {app_name}/{app_version}!")

    print("""
Please select action.
a - add a new income
p - to show all incomes
s - to stats
t - to print tax amount
c - to show graphic with all incomes and informations
r - reload incomes from database (file)
q - to quit from application""")

    while True:
        try:
            action = input("\nYour action: ")

            if action == 'q':
                print("See you soon!")
                break

            elif action == 'a':
                calculator.add_income()

            elif action == 'p':
                calculator.print_incomes()

            elif action == 's':
                calculator.print_stats()
            
            elif action == 't':
                calculator.print_tax()
            
            elif action == 'c':
                calculator.show_graphic()
            
            elif action == 'r':
                calculator.reload_incomes()
            
        except:
         print("Unexpected error! Please check your input or values.")


if __name__ == "__main__":
    main()