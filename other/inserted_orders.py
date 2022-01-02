def inserted_orders(root):
    if (root.left == None and root.right == None):
        return [[root]]
    elif (root.left == None):
        return [[root] + order for order in inserted_orders(root.right)]
    elif (root.right == None):
        return [[root] + order for order in inserted_orders(root.left)]
    else:
        new_orders = []
        left_orders = inserted_orders(root.left)
        right_orders = inserted_orders(root.right)
        for order1 in left_orders:
            for order2 in right_orders:
                number_of_buckets = len(order1)+1
                number_of_permutations = number_of_buckets**len(order2)
                ways_to_fill_buckets = []
                for i in range(number_of_permutations):
                    buckets = [0]*number_of_buckets
                    while (i>0):
                        digit = i%number_of_buckets
                        buckets[digit] += 1
                        i //= number_of_buckets
                new_order = [root]
                for buckets in ways_to_fill_buckets[:-1]:
                    for bucket in buckets:
                        for i in range(bucket):
                            new_order.append(order2.pop())
                    new_order.append(order1.pop())
                for i in range(buckets[-1]):
                    new_order.append(order2.pop())
                new_orders.append(new_order)
        return new_orders
                
                        
                    
