import statistics
students = [
    {
        "name": "Matt",
        "homework": [90.0, 97.0, 75.0, 92.0],
        "quizzes": [88.0, 40.0, 94.0],
        "tests": [75.0, 90.0],
    },
    {
        "name": "Mich",
        "homework": [100.0, 92.0, 98.0, 100.0],
        "quizzes": [82.0, 83.0, 91.0],
        "tests": [89.0, 97.0],
    },
{
        "name": "Mark",
        "homework": [0.0, 87.0, 75.0, 22.0],
        "quizzes": [0.0, 75.0, 78.0],
        "tests": [100.0, 100.0],
    }
]

if __name__ == '__main__':
    total_hw = 0
    total_quiz= 0
    total_tests = 0
    for x in students:
        ave_hw = statistics.mean(x['homework'])
        ave_quiz = statistics.mean(x['quizzes'])
        ave_tests = statistics.mean(x['tests'])
        total_hw += ave_hw
        total_quiz += ave_quiz
        total_tests += ave_tests
    average_hw = total_hw / len(students)
    average_quiz = total_quiz / len(students)
    average_tests = total_tests/ len(students)
        #print(f"average is {average}. total is {total}")


    print(f"Average homework mark: {average_hw}")
    print(f"Average quiz mark: {average_quiz}")
    print(f"Average test mark: {average_tests}")