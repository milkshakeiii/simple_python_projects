T = int(input())

for i in range(T):
    N = int(input())
    array = list(map(int,input().split()))
    alex_owns = list(map(lambda x: x%2, array))
    alex_books = [book for book in array if book%2 == 1]
    bob_books = [book for book in array if book%2 == 0]
    alex_books = list(reversed(sorted(alex_books)))
    bob_books = list(sorted(bob_books))
    result = []
    for alex_own in alex_owns:
        if alex_own:
            result.append(alex_books.pop())
        else:
            result.append(bob_books.pop())
    print("Case #" + str(i+1) + ": " + ' '.join(map(str,result)))
