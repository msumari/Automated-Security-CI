import os
import sys


def main():

    aws_key = "AKIA1234567890EXAMPLE"

    if len(sys.argv) > 1:
        user_input = sys.argv[1]
        os.system("ping " + user_input)


if __name__ == "__main__":
    main()
