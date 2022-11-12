import os, socket
from simple_term_menu import TerminalMenu
import pandas as pd
from art import *
from Modules.Product import Product, weightFromScale, getProductPrice, console
from getpass import getpass
from settings import host, port

values = ["category", "item", "variety", "unit", "price"]
main_menu_options = ["Add item to cart", "Delete items from cart", "Send data to server", "Check recipe", "Quit"]
csv_filename = "./Databases/database.csv"
database_name = "./Databases/store.db"

def getColumnData(column, contains, row):
    df = pd.read_csv(csv_filename)
    if contains != "None":
        df = df[df[column].str.contains(contains) == True]
    if row == "None":
        output = df[column].tolist()
    else:
        output = df[row].tolist()
    output2 = []
    if contains != "None":
        pass
    for x in output:
        if x not in output2:
            output2.append(x)

    return output2

def main():
    tprint("Grocery Store")
    mainMenu = TerminalMenu(main_menu_options, title = "MAIN MENU")
    quiting = False

    while quiting == False:
        optionsIndex = mainMenu.show()
        optionsChoice = main_menu_options[optionsIndex]
        
        if (optionsChoice == main_menu_options[-1]):
            os.system('clear')
            quiting = True
            break
        
        if (optionsChoice == main_menu_options[0]):
            os.system('clear')
            menu_list = getColumnData("category", "None", "None")
            subMenu = TerminalMenu(menu_list, title="Select Category")
            menu_entry_index = subMenu.show()
            menu_value1 = menu_list[menu_entry_index]
            
            menu_list = getColumnData("category", menu_value1, "item")
            subMenu = TerminalMenu(menu_list, title="Select Item")
            menu_entry_index = subMenu.show()
            menu_value2 = menu_list[menu_entry_index]

            menu_list = getColumnData("item", menu_value2, "variety")
            subMenu = TerminalMenu(menu_list, title="Select Item")
            menu_entry_index = subMenu.show()
            menu_value3 = menu_list[menu_entry_index]
            
            menu_list = ["Use external electronic scale", "Select manually"]
            subMenu = TerminalMenu(menu_list, title="Choose type of receive weight")
            menu_entry_index = subMenu.show()
            unit_menu = menu_list[menu_entry_index]

            if unit_menu == "Use external electronic scale":
                weightFromScale()
            else:
                pass

            while True:
                unit = input("Enter %s weight in kilograms (%s $/kg): "%(menu_value2, getProductPrice(menu_value1, menu_value2, menu_value3, 1)))
                try:
                    val = int(unit)
                    break
                except ValueError:
                    os.system('clear')
                    try:
                        float(unit)
                        break
                    except ValueError:
                        console.print("[red bold]\n This is not a number. Please enter a valid number \n")

            ProductValues = [menu_value1, menu_value2, menu_value3, unit]
            ProductToPush = Product(database_name)
            ProductToPush.createProduct(*ProductValues)
            os.system('clear')
        if (optionsChoice == main_menu_options[1]):
            os.system('clear')
            ProductToPush = Product(database_name)
            ProductToPush.dropData()
        
        if (optionsChoice == main_menu_options[2]):
            os.system('clear')
            console.print("[yellow bold]\n Connect to: %s:%s \n"%(host, port))
            username = input("Type Username: ")
            password = getpass()
            sendToServer(username, password)
        if(optionsChoice == main_menu_options[3]):
            os.system('clear')
            ProductToPush = Product(database_name)
            ProductToPush.printRecipe()

def sendToServer(username, password):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, int(port)))
            SEPARATOR = "<SEPARATOR>"
            os.system("cp ./Databases/store.db ./Databases/store_copy.db")
            file = "./Databases/store_copy.db"
            filesize = os.path.getsize(file)
            s.send(f"{file}{SEPARATOR}{filesize}".encode())
            console.print("[green bold underline]\n Can't Connect \n")
        except:
            os.system('clear')
            console.print("[red bold underline]\n Can't connect to the server\n")
    
if __name__ == '__main__':
    os.system('clear')
    main()