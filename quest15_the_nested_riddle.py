print('Welcome to the Mini Adventure!')
direction= input('Which direction are you taking (left or right): ').lower()
if direction == 'left':
    choice=input('Do you swim or wait: ').lower()

    if choice == 'swim':
        print('You have found the treasure!')
    elif choice == 'wait':
        print('Just a moment...')
    else:
        print('Invalid choice')
elif direction == 'right':
    print('Treasure lost!')
else:
    print('Invalid choice')
git add