from read import products, filename

def stringProduct(product):
    """
    Convert all items to String
    Returns: all the items in string format
    """
    return product['name'] + ", " + product['brand'] + ", " + str(product['quantity']) + ", " + str(product['costPrice']) + ", " + product['origin']

def saveGoods():
    """
    Write the new product after all the previous ones
    Returns Nothing
    """
    try:
        file = open(filename, 'w')
        for product in products:
            file.write(stringProduct(product) + "\n")
        file.close()
        print("Products has been saved.")
    except:
        print("Error has occurred while saving the file.")

def saveSalesBillAndTransaction(billID, billData, billType):
    """
    Saves bill to a file
    Parameters: billID (str), billData (list of str), billType (str)
    Returns: True if successful, False otherwise
    """
    try:
        billFile = open(billID + ".txt", 'w')
        for line in billData:
            billFile.write(line + "\n")
        billFile.close()
        return True
    except:
        print("Error saving " + billType.lower() + " bill")
        return False
