from datetime import datetime
print("Log V0")
def start_message():
    print("Select the choice for today :\n 0 -> Saving to logs\n 1 -> In the moment(no saving)\n 2 -> Accessing your saved logs\n 3 -> Saving and displaying only the current log\n 4 -> Search for specific logs \n 5 -> Clock-in log\n 6 -> Access habit log \n 9 -> Exit\n")
def save_log():
    entry = input("Enter your log entry:\n")
    now = datetime.now()
    timestamp = now.strftime("%d-%m-%y %H:%M:%S")
    file = open("log.txt" , "a")
    file.write("[" +timestamp + "]" "\t" + entry + "\n")
    file.close()
    print("Saved to logs")
def display_log():
    entry = input("we are not saving anything, let your heart out\n")
    print("You said : \n" +entry)
def access_log():
    try:
        file = open("log.txt" , "r")
        print("Here are your saved logs:\n")
        print(file.read())
        file.close()
    except:
        print("No logs found, please save some logs first.")
def save_read_log():
    entry = input("Say hi:\n")
    now = datetime.now()
    timestamp = now.strftime("%d-%m-%y %H:%M:%S")
    file = open("log.txt" , "a")
    file.write("[" +timestamp + "]" "\t" + entry + "\n")
    file.close()
    print("Saved to logs")
    print("You said : \n" +entry)
def specific_log():
    keyword = input("Enter a keyword to access logs: ")
    try:
        file = open("log.txt" , "r")
        logs = file.readlines()
        found_logs = [log for log in logs if keyword in log]
        if found_logs:
            print("Here are the logs containing your keyword:\n")
            for log in found_logs:
                print(log)
        else:
            print("No logs found with the given keyword.")
        file.close()
    except:
        print("No logs found, please save some logs first.")
def clock_log():
    habit = input("Enter the habit you are clocking in for: ").lower()
    count = input("Enter the number of times you've done this habit today: ")
    if count.strip() == "":
        count = 1
    else:
        try:
            count = int(count)
        except:
            print("Invalid number, defaulting to 1")
            count = 1
    now = datetime.now()
    timestamp = now.strftime("%d-%m-%y %H:%M:%S") 
    file = open("habits.txt", "a")
    file.write("[" + timestamp + "]" + habit + "|" + str(count) + "\n")
    file.close()
    print("Habit logged successfully.")
def habit_log():
    try:
        file = open("habits.txt" , "r")
        print("Here are your habit logs:\n")
        print(file.read())
        file.close()
    except:
        print("No habit logs found, please log some habits first.")
def main():
    while True:
        start_message()
        
        try:
            n =int(input("Enter your choice: \n"))
        except:
            print("Invalid input, try again")
            continue
        if n == 0:
           save_log()
        elif n == 1:
           display_log()
        elif n == 2:
           access_log()
        elif n == 3:
           save_read_log()
        elif n == 4:
            specific_log()
        elif n == 5:
            clock_log()
        elif n == 6:
            habit_log()
        elif n == 9:
           print("Exiting Log V0... Goodbye")
           break
        else:
           print("Invalid input, try again")

main()

