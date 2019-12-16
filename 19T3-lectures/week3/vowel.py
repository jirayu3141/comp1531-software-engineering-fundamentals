import sys

if __name__ == '__main__':
    vowels = {}
    for character in 'aeiou':
        vowels[character] = 0
    words = sys.stdin.readline().split(' ')
    print(words)
    for word in words:
        for character in word:
            if character in 'aeiou':
                vowels[character] += 1
    for character in 'aeiou':
        print(f"{character}: {vowels[character]}")
