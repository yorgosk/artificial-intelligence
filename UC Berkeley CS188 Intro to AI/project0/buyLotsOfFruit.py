# buyLotsOfFruit.py
# -----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
To run this script, type

  python buyLotsOfFruit.py

Once you have correctly implemented the buyLotsOfFruit function,
the script should produce the output:

Cost of [('apples', 2.0), ('pears', 3.0), ('limes', 4.0)] is 12.25
"""

fruitPrices = {'apples':2.00, 'oranges': 1.50, 'pears': 1.75,
              'limes':0.75, 'strawberries':1.00}

def buyLotsOfFruit(orderList):
    """
        orderList: List of (fruit, numPounds) tuples

    Returns cost of order
    """
    totalCost = 0.0
    "*** YOUR CODE HERE ***"
    for fruit, numPounds in orderList:  # for each entry inside the given order list
        if fruit not in fruitPrices:    # if a fruit is not registered
            print "ERROR. We don't have %s" %(fruit)    # error message
            return None                 # there's nothing to do with this order list
        totalCost += numPounds*fruitPrices[fruit]   # calculate the order list's total cost and...

    return totalCost    # ...return it

# Main Method
if __name__ == '__main__':
    "This code runs when you invoke the script from the command line"
    orderList = [ ('apples', 2.0), ('pears', 3.0), ('limes', 4.0) ]
    print 'Cost of', orderList, 'is', buyLotsOfFruit(orderList)
