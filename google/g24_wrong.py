import math

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

T = int(input())
for i in range(T):
    B = int(input())
    answer_xy = (None, None)
    answer_d = 0
    centerweights = []
    rectanges = []
    numerator = (0, 0)
    denominator = 0
    for j in range(B):
        x1, x2, y1, y2 = map(int,input().split())
        rectanges.append((x1, x2, y1, y2))
        center = (x1+y1)/2, (x2+y2)/2
        weight = (y2-x2+1)*(y1-x1+1)
        centerweights.append((center, weight))
        numerator = (numerator[0] + center[0] * weight,
                     numerator[1] + center[1] * weight)
        denominator += weight
        
    barycenter = (numerator[0]/denominator, numerator[1]/denominator)
    corners = []
    for rectangle in rectanges:
        x1, x2, y1, y2 = rectangle
        if x1 <= barycenter[0] <= y1 and x2 <= barycenter[1] <= y2:
            answer_x = None
            if center[0]%1 == 0.5:
                answer_x = int(center[0])
            else:
                answer_x = round(center[0])
            answer_y = None
            if center[1]%1 == 0.5:
                answer_y = int(center[1])
            else:
                answer_y = round(center[1])
            answer_xy = (answer_x, answer_y)
        corners.append((x1, x2))
        corners.append((y1, y2))
        corners.append((x1, y2))
        corners.append((x2, y1))

    if answer_xy == (None, None):
        closest_corners = []
        closest_corner_distance = float('inf')
        for corner in corners:
            distance = manhattan_distance(corner, barycenter)
            if distance < closest_corner_distance:
                closest_corners = [corner]
                closest_corner_distance = distance
            elif distance == closest_corner_distance:
                closest_corners.append(corner)

        answer_xy = min(closest_corners)

    answer_d = 0
    for centerweight in centerweights:
        position, weight = centerweight
        answer_d += weight*manhattan_distance(position, answer_xy)
          
    print("Case #" + str(i+1) + ": " + ' '.join(map(str,[answer_xy[0], answer_xy[1], int(answer_d)])))
