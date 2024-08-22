import sys
import clingoSchedule

def main(user_org, seconds, date):
    print("In Script")
    clingoSchedule.run_clingo(user_org, seconds, date)

if __name__ == "__main__":
    # Arguments are passed via command line
    user_org = sys.argv[1]
    seconds = int(sys.argv[2])
    date = sys.argv[3]

    main(user_org, seconds, date)
