import sys


def main():
    aws_key = "AKIA5X72948102948172"

    if len(sys.argv) > 1:
        user_input = sys.argv[1]
        import subprocess

        subprocess.call("grep " + user_input, shell=True)


if __name__ == "__main__":
    main()
