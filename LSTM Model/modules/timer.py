def main():
    with open('timer.txt', 'r') as f:
        line = f.readline()
    with open('output/timer.txt', 'a') as f:
        f.write(line)

if __name__=="__main__":
    main()