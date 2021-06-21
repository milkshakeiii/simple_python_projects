count_words = ["",
               "",
               "double",
               "triple",
               "quadruple",
               "quintuple",
               "sextuple",
               "septuple",
               "octuple",
               "nonuple",
               "decuple"]
               
number_words = ["zero",
                "one",
                "two",
                "three",
                "four",
                "five",
                "six",
                "seven",
                "eight",
                "nine"]

T = int(input())
for i in range(T):
    result = []
    number, shape = input().split(' ')
    number = [int(c) for c in number]
    shape = map(int,shape.split('-'))
    endpoint = 0
    for next_shape in shape:
        endpoint += next_shape
        subnumber = number[endpoint-next_shape:endpoint]
        subnumber = list(reversed(subnumber))
        while len(subnumber)>0:
            spoken_digit = subnumber[-1]
            count = 0
            while len(subnumber)>0 and subnumber[-1] == spoken_digit:
                count += 1
                subnumber.pop()
            if (count >= 2 and count <= 10):
                result.append(count_words[count])
                result.append(number_words[spoken_digit])
            elif count > 10:
                result += [number_words[spoken_digit]]*count
            else:
                result.append(number_words[spoken_digit])
            
    print("Case #" + str(i+1) + ": " + ' '.join(result))
