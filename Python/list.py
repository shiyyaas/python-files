#shopping list 

shoppinglist = []
while True:
    item = input(f"Shopping items {shoppinglist}\nEnter item to add to list (or Q to exit):")
    if item == "Q":
        break
    else:
        shoppinglist.append(item)
print("List adding mode exited.\n\n")

while True:
    item = input(f"Shopping items {shoppinglist}\nEnter item to add to list (or Q to exit):")
    if item == "Q":
        break
    if item not in shoppinglist:
        print(f"{item} is not in the list.")
        continue
    shoppinglist.remove(item)
print("List removing mode exited.\n\n")

print(f"Final shopping list:{shoppinglist}")