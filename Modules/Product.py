import sqlite3
import pandas as pd
from rich.console import Console
from rich.table import Table

console = Console()

values = ["category", "item", "variety", "kilograms", "price"]
database_name = "../Databases/store.db"
csv_filename = "./Databases/database.csv"

def displayData(cursor): # Display data from sql database
    data = cursor.execute('''SELECT * FROM Products''')
    table = Table(title="Recipe")
    for x in values:
        table.add_column(x, style="cyan")
    x = 0
    for row in data:
        table.add_row(*row)
        x += 1
    if x != 0:
        console.print(table)
        data = cursor.execute('''SELECT price FROM Products''')
        overall = 0
        for row in data:
            price = float(row[0])
            overall = overall + price
        overall = round(overall, 3)
        
        table = Table()
        table.add_column("Cart price", style="cyan")
        table.add_row(str(overall) + " $")
        console.print(table)

    return x

def saveToDatabase(rows, cursor): # Save values into database
    cursor.executemany('insert into Products values (?,?,?,?,?)', rows)

def getProductPrice(category, item, variety, unit):
    df = pd.read_csv(csv_filename)
    df = df.loc[df['category'].isin([category])]
    df = df.loc[df['item'].isin([item])]
    df = df.loc[df['variety'].isin([variety])]
    price = float(df['price'].values[0]) * float(unit)
    return price

def weightFromScale(): # Function for getting informations from external scale
    console.print("[red bold]\n This feature is currently unavailable \n")
    console.print("[green bold] Please enter weight manually \n")
    
class Product:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()
    
    def __del__(self):
        self.connection.commit()
        self.connection.close()
    
    def createProduct(self, category, item, variety, unit):
        self.category = category
        self.item = item
        self.variety = variety
        self.unit = unit
        self.price = getProductPrice(self.category, self.item, self.variety, self.unit)
        rows = [[self.category, self.item, self.variety, self.unit, self.price]]
        saveToDatabase(rows, self.cursor)
        displayData(self.cursor)
        self.connection.commit()
    
    def dropData(self):
        self.cursor.execute('DELETE FROM Products;',);
        if self.cursor.rowcount == 0:
            console.print("[red bold]\n Your recipe is empty, add some items to cart! \n")
        else:
            console.print("[green bold]\n You deleted successfully %s records from cart! \n"%self.cursor.rowcount)

    def printRecipe(self):
        if displayData(self.cursor) == 0:
            console.print("[red bold]\n Nothing to display, please add some items to cart \n")
            
