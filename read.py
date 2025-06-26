products = []
filename = "StoreFile.txt"

def loadGoods():
    """
    Takes all the data from file and stores in local dictionary
    Returns Nothing
    """
    try:
        file = open(filename, 'r')
        lines = file.readlines()
        file.close()
        localGoods = []
        for line in lines:
            parts = line.replace("\n", "").split(",")
            name = parts[0]
            brand = parts[1]
            quantityString = parts[2]
            costPriceString = parts[3]
            origin = parts[4]
            try:
                quantity = int(quantityString)
                costPrice = float(costPriceString)
                product = {'name': name, 'brand': brand, 'quantity': quantity, 'costPrice': costPrice, 'origin': origin}
                localGoods.append(product)
            except:
                print("Error parsing line: " + line)
        products.clear()
        products.extend(localGoods)
        print("Goods have been successfully loaded with " + str(len(products)) + " products.")
    except FileNotFoundError:
        print("Cannot find the file")
    except:
        print("Error has occurred in file")
