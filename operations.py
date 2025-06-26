import datetime
from read import products
from write import saveGoods

def sellPrice(costPrice):
    """
    Multiplies cost price by 2 to get selling price
    Returns in float
    """
    return costPrice * 2

def display():
    """
    display()
    Display all the data of the products
    Returns Nothing
    """
    if not products:
        print("There is no product in the store.")
        return

    print("\n" "*" * 106)

    # Prints title
    print("ID\tProduct Name\t\tBrand\t\t\tQuantity\tSelling Price\tOrigin")
    print("*" * 106)

    i = 1
    for product in products:
        sellingPrice = sellPrice(product['costPrice'])

        idString = str(i)
        name = product['name']
        brand = product['brand']
        quantity = str(product['quantity'])
        price = "$" + str(sellingPrice)
        origin = product['origin']

        # Adds space
        if len(name) < 8:
            nameSpace = "\t\t\t"
        elif len(name) < 16:
            nameSpace = "\t\t"
        else:
            nameSpace = "\t"

        if len(brand) < 8:
            brandSpace = "\t\t\t"
        elif len(brand) < 16:
            brandSpace = "\t\t"
        else:
            brandSpace = "\t"

        quantitySpace = "\t\t"
        priceSpace = "\t\t"
        originSpace = "\t"

        # Print in proper format using spaces
        print(idString + "\t" + name + nameSpace + brand + brandSpace +
              quantity + quantitySpace + price + priceSpace + origin + originSpace)

        i += 1

    print("*" * 106)
    print("Buy 3 Get 1 Free on all products in the store.")
    print("*" * 106)


def addGoods():
    """
    Ask users the product details, store them, and generate a bill
    Returns Nothing
    """
    from write import saveSalesBillAndTransaction

    try:
        name = input("Enter product name: ")
        if name=="":
            print("Product name was not entered.")
            return
        
        brand = input("Enter brand name: ")
        if brand=="":
            print("Brand name was not entered.")
            return
        
        addGoodsString = input("Enter quantity you want to add: ")
        if not addGoodsString.isdigit():
            print("Please enter a number.")
            return
        addQuantity = int(addGoodsString)
        if addQuantity < 0:
            print("Quantity value cannot be negative")
            return
        
        costPriceString = input("Enter cost price: ")
        try:
            costPrice = float(costPriceString)
            if costPrice <= 0:
                print("Cost price cannot be negative.")
                return
        except:
            print("Please enter value in number.")
            return
        
        origin = input("Enter country of origin: ")
        if origin=="":
            print("Country of origin should be entered.")
            return
        
        newGoods = {'name': name, 'brand': brand, 'quantity': addQuantity, 'costPrice': costPrice, 'origin': origin}
        products.append(newGoods)
        saveGoods()
        print("Product '" + name + "' has been added successfully.")

        # Generate bill for new item
        dateTimeStr, year, month, day, hour, minute, second = formatDateTime()
        billID = hour + minute + second + hour + minute + second
        totalCost = addQuantity * costPrice

        billData = []
        billData.append("-" * 74)
        billData.append("                        New Item Bill                               ")
        billData.append("-" * 74)
        billData.append("Bill ID: " + billID)
        billData.append("Date: " + dateTimeStr)
        billData.append("-" * 74)
        billData.append("Item\t\tBrand\t\tQty\tCost Price\tTotal")
        billData.append("-" * 74)
        if len(name) < 8:
            nameSpace = "\t\t"
        else:
            nameSpace ="\t"
        if len(brand) < 8:
            brandSpace = "\t\t"
        else:
            brandSpace ="\t"
        itemLine = name + nameSpace + brand + brandSpace + str(addQuantity) + "\t$" + str(costPrice) + "\t\t$" + str(totalCost)
        billData.append(itemLine)
        
        billData.append("-" * 74)
        billData.append("Total:" + "\t" * 4 + "$" + str(totalCost))
        billData.append("-" * 74)
        billData.append("New item has been added.")
        billData.append("-" * 74)

        print("\n")
        for line in billData:
            print(line)

        billSaved = saveSalesBillAndTransaction(billID, billData, "New Item")
        if billSaved:
            print("\nNew item bill has been saved to file: " + billID + ".txt")
        else:
            print("\nFailed to save new item bill.")

    except:
        print("Error adding new product")

def fillGoods():
    """
    Adds quantity to the previous quantity for multiple products and generates a combined bill when done.
    Returns Nothing
    """
    from write import saveSalesBillAndTransaction

    display()
    if not products:
        return

    reFills = []
    continue_restocking = True
    while continue_restocking:
        try:
            goodsIdStr = input("Enter the ID of the product to restock: ")
            if not goodsIdStr.isdigit():
                print("Please enter a valid number.")
                continue

            goodsId = int(goodsIdStr)
            if goodsId < 1 or goodsId > len(products):
                print("Please choose number from 1 to 5.")
                continue

            product = products[goodsId - 1]
            print("Current quantity of '" + product['name'] + "': " + str(product['quantity']))

            addGoodsString = input("Enter quantity to add: ")
            if not addGoodsString.isdigit():
                print("Please enter a valid number.")
                continue

            addQuantity = int(addGoodsString)
            if addQuantity < 0:
                print("Quantity cannot be negative.")
                continue

            product['quantity'] = product['quantity'] + addQuantity
            saveGoods()
            print("Updated quantity of '" + product['name'] + "': " + str(product['quantity']))

            # Log the restock
            reFills.append({'name': product['name'], 'quantity': product['quantity']})

            # Ask if the user wants to continue restocking
            while True:
                continue_choice = input("\nDo you want to continue restocking? (y/n): ").lower()
                if continue_choice in ['y', 'n']:
                    break
                print("Please enter 'y' for yes or 'n' for no.")
            
            if continue_choice != 'y':
                continue_restocking = False
                break

            # Generate individual bill for saving (but don't print)
            dateTimeStr, year, month, day, hour, minute, second = formatDateTime()
            billID = hour + minute + second + hour + minute + second
            costPrice = product['costPrice']
            totalCost = addQuantity * costPrice

            billData = []
            billData.append("-" * 74)
            billData.append("                              Refill Bill                               ")
            billData.append("-" * 74)
            billData.append("Bill ID: " + billID)
            billData.append("Date: " + dateTimeStr)
            billData.append("-" * 74)
            billData.append("Item\t\t\tBrand\tQty\tCost Price\tTotal")
            billData.append("-" * 74)
            
            name = product['name']
            brand = product['brand']
            
            if len(name) < 8:
                nameSpace = "\t\t"
            else:
                nameSpace ="\t"
            if len(brand) < 8:
                brandSpace = "\t\t"
            else:
                brandSpace ="\t"
            itemLine = name + nameSpace + brand + brandSpace + str(addQuantity) + "\t$" + str(costPrice) + "\t\t$" + str(totalCost)
            billData.append(itemLine)
            
            billData.append("-" * 74)
            billData.append("Total:" + "\t" * 4 + "$" + str(totalCost))
            billData.append("Total quantity:" + str(product['quantity']))
            billData.append("-" * 74)
            billData.append("Items have been refilled.")
            billData.append("-" * 74)

            billSaved = saveSalesBillAndTransaction(billID, billData, "Restock")
            if billSaved:
                print("\nRefill bill has been saved to file: " + billID + ".txt")
            else:
                print("\nFailed to save refill bill.")

        except:
            print("Error restocking product")
            continue

    # Generate combined bill if restocks occurred
    if reFills:
        dateTimeStr, year, month, day, hour, minute, second = formatDateTime()
        billID = hour + minute + second + hour + minute + second

        billData = []
        billData.append("-" * 74)
        billData.append("                        Combined Restock Bill                       ")
        billData.append("-" * 74)
        billData.append("Bill ID: " + billID)
        billData.append("Date: " + dateTimeStr)
        billData.append("-" * 74)
        billData.append("Item\t\tQuantity")
        billData.append("-" * 74)
        
        for restock in reFills:
            name = restock['name']
            quantity = str(restock['quantity'])
            
            itemLine = name + "\t"+ quantity
            billData.append(itemLine)
        
        billData.append("-" * 74)
        billData.append("Restocking completed.")
        billData.append("-" * 74)

        print("\n")
        for line in billData:
            print(line)

def formatDateTime():
    """
    Returns formatted date and time strings
    Returns tuple of (dateTimeStr, year, month, day, hour, minute, second)
    """
    now = datetime.datetime.now()
    year = str(now.year)
    month = str(now.month)
    if len(month) == 1:
        month = "0" + month
    day = str(now.day)
    if len(day) == 1:
        day = "0" + day
    hour = str(now.hour)
    if len(hour) == 1:
        hour = "0" + hour
    minute = str(now.minute)
    if len(minute) == 1:
        minute = "0" + minute
    second = str(now.second)
    if len(second) == 1:
        second = "0" + second
    dateTimeStr = year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second
    return (dateTimeStr, year, month, day, hour, minute, second)

def buyGoods():
    """
    Allows the user to buy multiple products and generates a combined bill
    Returns Nothing
    """
    from write import saveSalesBillAndTransaction

    display()
    if not products:
        return
    
    cart = []
    totalBill = 0
    totalFreeItems = 0
    
    dateTimeStr, year, month, day, hour, minute, second = formatDateTime()
    billID = hour + minute + second + hour + minute + second
    
    shopping = True
    while shopping:
        goodsId = input("Enter the product ID you want to buy seeing in the inventory. (0 for checkout): ")
        
        if goodsId == '0':
            if not cart:
                print("You have not bought anything.")
                return
            break
            
        if not goodsId.isdigit():
            print("Please enter a valid number.")
            continue

        goodsId = int(goodsId)
        
        try:
            if goodsId < 1 or goodsId > len(products):
                print("Provide ID seeing on the inventory.")
                continue
                
            product = products[goodsId - 1]
            if product['quantity'] <= 0:
                print("Sorry, we are out of stock for this product.")
                continue
                
            sellingPrice = sellPrice(product['costPrice'])
            print("Available quantity: " + str(product['quantity']))
            buyQuantityString = input("Enter quantity to buy: ")
            
            if not buyQuantityString.isdigit() or int(buyQuantityString) <= 0:
                print("Please enter a positive number.")
                continue
                
            buyQuantity = int(buyQuantityString)
            if buyQuantity > product['quantity']:
                print("Sorry, we only have " + str(product['quantity']) + " number of stocks available.")
                continue
                
            freeGoods = buyQuantity // 3
            paidItems = buyQuantity - freeGoods
            itemCost = paidItems * sellingPrice
            
            cartItem = {
                'name': product['name'],
                'brand': product['brand'], 
                'quantity': buyQuantity,
                'freeItems': freeGoods,
                'paidItems': paidItems,
                'price': sellingPrice,
                'totalCost': itemCost,
                'productIndex': goodsId - 1
            }
            
            cart.append(cartItem)
            print("Added " + str(buyQuantity) + " " + product['name'] + " to cart.")
            
            addMore = input("Would you like to add more products? (y/n): ").lower()
            if addMore != 'y':
                break
                
        except:
            print("Error has been occured while adding product.")
    
    if not cart:
        return
        
    totalBill = 0
    totalFreeItems = 0
    for item in cart:
        totalBill = totalBill + item['totalCost']
        totalFreeItems = totalFreeItems + item['freeItems']
    
    shippingChoice = input("\nWould you like your items to be shipped? (y/n): ").lower()
    shippingCost = 0
    if shippingChoice == 'y':
        shippingCost = 20
        totalBill = totalBill + shippingCost
    
    billData = []
    billData.append("-" * 74)
    billData.append("                        Purchase Bill                               ")
    billData.append("-" * 74)
    billData.append("Bill ID: " + billID)
    billData.append("Date: " + dateTimeStr)
    billData.append("-" * 74)
    billData.append("Item\t\tBrand\t\tQty\tPrice\t\tTotal")
    billData.append("-" * 74)
    
    for item in cart:
        name = item['name']
        brand = item['brand']
        qty = str(item['quantity'])
        price = "$" + str(item['price'])
        total = "$" + str(item['totalCost'])
        if len(name) < 8:
            nameSpace = "\t\t"
        else:
            nameSpace ="\t"
        if len(brand) < 8:
            brandSpace = "\t\t"
        else:
            brandSpace = "\t"
        itemLine = name + nameSpace + brand + brandSpace + qty + "\t" + price + "\t\t" + total
        billData.append(itemLine)
    
    billData.append("-" * 74)
    if shippingChoice == 'y':
        billData.append("Shipping Cost:" + "\t" * 3 + "$" + str(shippingCost))
    billData.append("Total:" + "\t" * 4 + "$" + str(totalBill))
    billData.append("Total Free Items:" + "\t" * 2 + str(totalFreeItems))
    
    billData.append("-" * 74)
    billData.append("Thank you. Hope you have a wonderful day ahead.")
    billData.append("-" * 74)
    
    print("\n")
    for line in billData:
        print(line)
    
    confirm = input("\nDo you want to confirm the purchase? (y/n): ").lower()
    if confirm == 'y':
        billSaved = saveSalesBillAndTransaction(billID, billData, "Purchase")
        
        if billSaved:
            for item in cart:
                product = products[item['productIndex']]
                product['quantity'] = product['quantity'] - item['quantity']
            billData.append("Total products:" + "\t" * 3 + str(sum(product['quantity'] for product in products)))
            billData.append("-" * 74)
            billData.append("Thank you. Hope you have a wonderful day ahead.")
            billData.append("-" * 74)
            saveGoods()
            
            print("\nUpdated Bill with Total Products Left:")
            for line in billData:
                print(line)
            
            if shippingChoice == 'y':
                print("\nPurchase has been completed along with shipping.")
            else:
                print("\nPurchase has been completed!")
            print("Your Bill ID: " + billID)
    else:
        billData.append("Total products:" + "\t" * 3 + str(sum(product['quantity'] for product in products)))
        billData.append("-" * 74)
        billData.append("Thank you. Hope you have a wonderful day ahead.")
        billData.append("-" * 74)
        
        print("\nUpdated Bill with Total Products Left:")
        for line in billData:
            print(line)
        print("Purchase cancelled.")
    
    print("Hope you have a wonderful day ahead.")


