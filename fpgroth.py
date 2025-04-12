import csv
import time
from collections import defaultdict
from itertools import combinations

def load_dataset(fileName):
    transactions = []
    with open(fileName, 'r') as file:
        firstLine = file.readline()
        if 'items' in firstLine:
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

class FPTreeNode:
    def __init__(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.link = None

def build_fp_tree(transactions, min_support):
    item_count = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            item_count[item] += 1

    # Filter items by min_support
    item_count = {item: count for item, count in item_count.items()
                  if count / len(transactions) >= min_support}

    if len(item_count) == 0:
        return None, None

    # Header table
    header_table = {item: [count, None] for item, count in item_count.items()}

    # Build tree
    root = FPTreeNode(None, 1, None)
    for transaction in transactions:
        filtered = [item for item in transaction if item in item_count]
        filtered.sort(key=lambda x: item_count[x], reverse=True)
        current = root
        for item in filtered:
            if item in current.children:
                current.children[item].count += 1
            else:
                new_node = FPTreeNode(item, 1, current)
                current.children[item] = new_node
                if header_table[item][1] is None:
                    header_table[item][1] = new_node
                else:
                    node = header_table[item][1]
                    while node.link is not None:
                        node = node.link
                    node.link = new_node
            current = current.children[item]

    return root, header_table

def ascend_fp_tree(node):
    path = []
    while node and node.parent.item is not None:
        node = node.parent
        path.append(node.item)
    return path

def find_prefix_paths(base_pat, node):
    cond_pats = []
    while node is not None:
        path = ascend_fp_tree(node)
        if path:
            cond_pats.append((path, node.count))
        node = node.link
    return cond_pats

def mine_fp_tree(header_table, min_support, prefix, freq_items):
    for item, (support, node) in sorted(header_table.items(), key=lambda x: x[1][0]):
        new_freq_set = prefix.copy()
        new_freq_set.add(item)
        freq_items[frozenset(new_freq_set)] = support / total_transactions
        cond_patt_bases = find_prefix_paths(item, node)

        cond_transactions = []
        for path, count in cond_patt_bases:
            cond_transactions.extend([path] * count)

        cond_tree, cond_header = build_fp_tree(cond_transactions, min_support)
        if cond_header:
            mine_fp_tree(cond_header, min_support, new_freq_set, freq_items)

def fp_growth(transactions, min_support):
    tree, header_table = build_fp_tree(transactions, min_support)
    freq_items = {}
    global total_transactions
    total_transactions = len(transactions)
    if header_table:
        mine_fp_tree(header_table, min_support, set(), freq_items)
    return freq_items

# -------------------------------
# Association Rule Generation
# -------------------------------

def generate_rules(frequent_itemsets, support_data, min_confidence):
    rules = []
    for itemset in frequent_itemsets:
        if len(itemset) >= 2:
            subsets = list(combinations(itemset, len(itemset) - 1))
            for antecedent in subsets:
                consequent = tuple(set(itemset) - set(antecedent))
                if consequent:
                    antecedent = tuple(sorted(antecedent))
                    itemset_sorted = tuple(sorted(itemset))
                    if antecedent in support_data:
                        conf = support_data[itemset_sorted] / support_data[antecedent]
                        if conf >= min_confidence:
                            rules.append((antecedent, consequent, conf))
    return rules

# -------------------------------
# Run Everything
# -------------------------------

if __name__ == "__main__":
    min_support = 0.02
    min_confidence = 0.5

    print("Loading dataset...")
    transactions = load_dataset('grocery_transactions.csv')

    # FP-Growth
    print("\nRunning FP-Growth...")
    start_time = time.time()
    fp_itemsets = fp_growth(transactions, min_support)
    fp_rules = generate_rules(list(fp_itemsets.keys()), fp_itemsets, min_confidence)
    fp_time = time.time() - start_time
    print(f"FP-Growth finished in {fp_time:.2f} seconds")
    print(f"Frequent itemsets found: {len(fp_itemsets)}")

    # Summary
    print("\n--- Summary ---")
    print(f"FP-Growth Time: {fp_time:.2f} sec, Itemsets: {len(fp_itemsets)}, Rules: {len(fp_rules)}")

    # summary of products 
    print("\n--- Summary of all frequent products products ---")
    fp_growth_products = set()
    for itemset in fp_itemsets.keys():
        fp_growth_products.update(itemset)
    
    all_products = fp_growth_products

    print("\nFrequent products by algorithm:")
    for item in sorted(fp_growth_products):
        print(f"  - {item} (found in: FpGroth)")