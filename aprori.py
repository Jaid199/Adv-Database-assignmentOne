import csv
from gettext import translation
from os import startfile
import time
from collections import defaultdict
from itertools import combinations

from assignemtOne import apriori, generate_rules

def load_dataset(fileName):
    transactions = []
    with open(fileName, 'r') as file:
        firstLine = file.readline()
        if 'items' in firstLine:  # <-- FIXED HERE
            file.seek(0)
            reader = csv.DictReader(file)
            for row in reader:
                items = row['items'].strip().split(',')
                transactions.append([item.strip() for item in items])
        else:
            file.seek(0)
            reader = csv.reader(file)
            for row in reader:
                if row[0].isdigit():
                    row = row[1:]
                transactions.append([item.strip() for item in row if item.strip()])
    return transactions

def aprioriAlg(transactions, minSupport):
    itemSet = [] # to add all the frequent items
    supportData = {} # a dictionary will map each frequent items to its support value
    
    def getFrequentItems(nonFreqItems, k):
        # take a list of candidate items of size k
        # checks how many transections contain them
        # filter out those who dont meet min support
        counts = defaultdict(int)
        for transaction in transactions: # loop through each transactions
            for nonFreqItem in nonFreqItems:
                if set(nonFreqItem).issubset(set(transaction)):
                    counts[nonFreqItem] += 1
        numItems = len(transactions) # total num of transec
        freItems = [] # list freq itemset that meet supports

        for itemSet, count in counts.items():
            support = count / numItems
            if support >= minSupport:
                freItems.append(itemSet)
                supportData[itemSet] = support
        return freItems

    
    def generateCandidates(prevFreqSets, k):
        # This function generates candidate itemsets of size k, based on previous frequent (k-1)-itemsets
        candidates = []
        lenPrev = len(prevFreqSets)
        for i in range(lenPrev): # Loop through all previous frequent sets
            for j in range(i + 1, lenPrev):
                l1 = list(prevFreqSets[i])
                l2 = list(prevFreqSets[j])
                l1.sort(), l2.sort()
                if l1[:k-2] == l2[:k-2]:
                    candidates.append(tuple(sorted(set(prevFreqSets[i]) | set(prevFreqSets[j]))))
        return list(set(candidates))
    singleItems = set(item for transaction in transactions for item in transaction)
    candidateOne = [(item,) for item in singleItems]
    L1 = getFrequentItems(candidateOne, 1)
    itemSet.extend(L1)

    k = 2
    Lk = L1
    while Lk:
        Ck = generateCandidates(Lk, k)
        Lk = getFrequentItems(Ck, k)
        itemSet.extend(Lk)
        k += 1

    return itemSet, supportData
    

if __name__ == "__main__":
    min_support = 0.02
    min_confidence = 0.5

    print("Loading dataset...")
    transactions = load_dataset('grocery_transactions.csv')

    print("\nRunning Apriori...")
    start_time = time.time()
    apriori_itemsets, apriori_support = apriori(transactions, min_support)
    apriori_rules = generate_rules(apriori_itemsets, apriori_support, min_confidence)
    apriori_time = time.time() - start_time
    print(f"Apriori finished in {apriori_time:.2f} seconds")
    print(f"Frequent itemsets found: {len(apriori_itemsets)}")

    print("\n--- Summary ---")
    print(f"Apriori Time: {apriori_time:.2f} sec, Itemsets: {len(apriori_itemsets)}, Rules: {len(apriori_rules)}")

    # summary of products 
    print("\n--- Summary of all frequent products ---")
    apriori_products = set()
    for itemset in apriori_itemsets:
        apriori_products.update(itemset)

    print("\nFrequent products by algorithm:")
    for item in sorted(apriori_products):
        print(f"  - {item} (found in: Apriori)")
