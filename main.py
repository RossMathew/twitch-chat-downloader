from app import CLI, Config


def main():
    print(Config().filename)
    #print(CLI().arguments)


if __name__ == '__main__':
    main()
