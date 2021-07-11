T = int(input())
for i in range(T):
    N, M = map(int,input().split())
    
    problem_sets = []
    for j in range(N):
        A, B = map(int,input().split())
        problem_sets.append([A, B])
    problem_sets = sorted(problem_sets)
    
    students = list(map(int,input().split()))
    best_problems = []
    for student in students:
        left_index = 0
        right_index = len(problem_sets)-1
        print(problem_sets)
        while left_index <= right_index:
            center = (left_index + right_index) // 2
            center_set = problem_sets[center]
            if center_set[0] > student:
                right_index = center-1
            elif center_set[0] < student:
                left_index = center+1
            else:
                left_index = center
                break
        best_problem = -1
        if left_index == 0:
            best_problem = problem_sets[left_index][0]
            problem_sets[left_index][0] += 1
            if problem_sets[left_index][1] < problem_sets[left_index][0]:
                problem_sets = problem_sets[1:]
        elif left_index == len(problem_sets) and problem_sets[-1][1] < student:
            best_problem = problem_sets[-1][1]
            problem_sets[-1][1] -=1
            if problem_sets[-1][1] < problem_sets[-1][0]:
                problem_sets = problem_sets[:-1]
        elif left_index == len(problem_sets):
            best_problem = student
            new1 = [[problem_sets[-1][0], student-1]]
            new2 = [[student+1, problem_sets[-1][1]]]
            if new1[0][1] < new1[0][0]:
                new1 = []
            if new2[0][1] < new2[0][0]:
                new2 = []
            problem_sets.append(new1[0])
            problem_sets.append(new2[0])
        else:
            easy_set = problem_sets[left_index-1]
            hard_set = problem_sets[left_index]
            if easy_set[1] >= student:
                best_problem = student
                new1 = [[easy_set[0], student-1]]
                new2 = [[student+1, easy_set[1]]]
                if new1[0][1] < new1[0][0]:
                    new1 = []
                if new2[0][1] < new2[0][0]:
                    new2 = []
                problem_sets = problem_sets[:left_index-1] + new1 + new2 + problem_sets[left_index:]
            else:
                hard_gap = abs(hard_set[0] - student)
                easy_gap = abs(easy_set[1] - student)
                if hard_gap < easy_gap:
                    best_problem = hard_set[0]
                    problem_sets[left_index][0] += 1
                    if problem_sets[left_index][1] < problem_sets[left_index][0]:
                        problem_sets = problem_sets[:left_index] + problem_sets[left_index+1:]
                else:
                    best_problem = easy_set[1]
                    problem_sets[left_index-1][1] -= 1
                    if problem_sets[left_index-1][1] < problem_sets[left_index-1][0]:
                        problem_sets = problem_sets[:left_index-1] + problem_sets[left_index:]

        best_problems.append(str(best_problem))

    print("Case #" + str(i+1) + ": " + ' '.join(best_problems))

            
