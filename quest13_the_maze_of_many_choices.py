score=int(input('Enter your score(0-100): '))
if score > 100 or score < 0:
    print("Please enter a number between 0 and 100")
elif score >= 90:
    print('A')
elif score >= 80:
    print('B')
elif score >= 70:
    print('C')
else:
    print('Needs improvement')