from random import randint

print("Welcome to the Odd or Even game!")
score = 0
while True:
    rand = randint(0, 6)
    user = int(input("Enter a number between 0 and 6: "))
    if user == rand:
        print("AHHH,you failed")
        break
    if user == 0:
        score += rand
    score += user
    print(f"Your score is: {score}")
print(f"Your score is: {score}")    