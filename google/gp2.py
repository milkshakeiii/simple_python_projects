from math import asin, pi

T = int(input())
for i in range(T):
    V, D = map(int,input().split())
    answer = asin(9.8*D/(V**2))/2
    answer_in_degrees = answer * 180/pi
    print("Case #" + str(i+1) + ": " + str(answer_in_degrees))

###include <math.h>
###include <iostream>
###include <string>
##
##int main() {
##    int T;
##    std::cin >> T;
##    for (int i = 0; i < T; i++) {
##        int V, D;
##        std::cin >> V;
##        std::cin >> D;
##        float answer = asin(9.8*D/(V*V))/2;
##        float answer_in_degs = answer * 180 / 3.14159265358979;
##        std::cout << std::string("Case #") + std::to_string(i) + ": " + std::to_string(answer_in_degs) << std::endl;
##    }
##}
