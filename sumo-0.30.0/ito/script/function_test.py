#for function test

def user_fullcheck(floor):
    for f in range(1,4):
        if f != floor:
            if f < 3:
                print(f)
                break



if __name__ == '__main__':
    user_fullcheck(1)