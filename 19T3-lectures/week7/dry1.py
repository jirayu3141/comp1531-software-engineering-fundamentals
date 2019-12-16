import sys

if len(sys.argv) != 2:
    sys.exit(1)

num = int(sys.argv[1])

if num != 3 and num != 4:
    sys.exit(1)

LST = {
    "2": "squared",
    "3": "cubed",
}
for i in range(10, 20):
    result = i ** num
    print(f"{i} {LST[str(num)]} = {result}")
