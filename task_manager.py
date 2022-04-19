"""Capstone template project for FCS Task 19 Compulsory task 1.
This template provides a skeleton code to start compulsory task 1 only.
Once you have successfully implemented compulsory task 1 it will be easier to
add a code for compulsory task 2 to complete this capstone"""
# =====importing libraries===========
from os import path
from datetime import datetime
from typing import List, Tuple, Optional

# ====Login Section====
''' Declare file paths in the global scope so that they can be referred to more easily later.
    Use the path.join(__file__, file) pattern so that the program runs even if the working directory 
    is different from the file directory.
'''
# ====Global Declarations====
User = Tuple[str, str]
user_txt = path.join(path.dirname(__file__), "user.txt")
task_txt = path.join(path.dirname(__file__), "tasks.txt")
task_overview_txt = path.join(path.dirname(__file__), "task_overview.txt")
user_overview_txt = path.join(path.dirname(__file__), "user_overview.txt")
user_index = 0
due_date_index = 4
completed_index = 5
# ====Templates=====
entry_template = "{assign_to}, {task}, {description}, {date_created}, {due_date}, {completed}"


def task_report_template(
        total_generated: int,
        total_completed: int,
        total_incomplete: int,
        percentage_incomplete: float,
        total_overdue: int,
        percentage_overdue: float
):
    return '''
[Task Overview]
Total tasks generated:          {0: >30}
Total tasks completed:          {1: >30}
Total tasks incomplete:         {2: >30}
Percentage tasks incomplete:    {3: >30.2f}%
Total tasks overdue:            {4: >30}
Percentage tasks overdue:       {5: >30.2f}%
'''.format(total_generated,
           total_completed,
           total_incomplete,
           percentage_incomplete,
           total_overdue,
           percentage_overdue
           )


def user_report_template(
        username: str,
        percentage_of_total: float,
        total: int,
        percentage_completed: float,
        percentage_incomplete: float,
        percentage_overdue: float):
    # This function generates a user report according to the user report template.
    return '''
    [{0}]
        Tasks assigned to user:                     {1: >20}
        Percentage of all tasks assigned to user:   {2: >20.2f}%
        Percentage of assigned tasks completed:     {3: >20.2f}%
        Percentage of assigned tasks incomplete:    {4: >20.2f}%
        Percentage of assigned tasks overdue:       {5: >20.2f}%
'''.format(
        username, total,
        percentage_of_total, percentage_completed,
        percentage_incomplete,
        percentage_overdue
    )


def user_overview_template(total_users: int, total_tasks: int, user_reports: List[str]) -> str:
    # This function generates the User Overview
    return '''
[User Overview]
    Total users registered:                         {0: >20}
    Total tasks generated:                          {1: >20}
[User Reports]
{2}'''.format(total_users, total_tasks, '\n'.join(user_reports))


def task_template(
        task_id: int, task_title: str,
        assigned_to: str, date_assigned: str,
        due_date: str, task_description: str,
        task_complete: str):
    # This function generates a task sheet.
    return '''
Task ID:                            {0}
Task:                               {1}
Assigned to:                        {2}
Date assigned:                      {3}
Due date:                           {4}
Task complete?                      {5}
Task description:
 {6}
-------------------------------------------\
'''.format(
        task_id, task_title,
        assigned_to, date_assigned,
        due_date, task_description,
        task_complete
    )


# =====Functions=====
def percentage(numerator: float, denominator: int) -> float:
    # This function accepts a numerator and denominator
    if denominator != 0:
        return numerator * 100 / denominator
    return 0


def set_date() -> Optional[str]:
    # This function generates a date string if the details
    day = int(input("Day of the month (dd): "))
    month = int(input("Month (mm): "))
    year = int(input("Year (yyyy): "))
    # Make sure that a value greater than 0 was provided for each part of the date.
    if day and month and year:
        return datetime(day=day, month=month, year=year).strftime("%d %b %Y")
    return None


def find_task(given_id: int) -> Optional[str]:
    # This function finds a task using its id
    with open(task_txt, 'r') as tasks:
        for task_id, task in enumerate(tasks):
            if task_id == given_id:
                assigned_to, task_title, task_description, date_assigned, task_due_date, completed = task.split(', ')
                return task_template(
                    task_id, task_title,
                    assigned_to, date_assigned,
                    task_due_date, task_description,
                    completed
                )
    return None


def find_user(given_user: str) -> Optional[User]:
    # This function returns a user's (username, password) pair if the user exists.
    with open(user_txt, 'r') as users:
        for line in users:
            username, password = line.strip().split(', ')
            credentials = (username, password)
            if credentials[0] == given_user:
                return credentials
    return None  # No user was found


def reg_user(new_username: str) -> bool:
    # This function registers a new user to user.txt if the user does not exist.
    alert_template = '''\
===============================================
{0:^45}
===============================================
'''
    if find_user(new_username):
        print(alert_template.format(f"The user {new_username} already exists!"))
        return False
    with open(user_txt, 'a') as userdata:
        password = input("password: ")
        if input("confirm password: ") != password:  # Password confirmation doesn't need to be stored, just tested.
            print(alert_template.format("'password' must match 'confirm password'"))
            return False
        else:
            userdata.write('\n')  # Avoid adding an unnecessary newline to users.txt
            userdata.write(", ".join([new_username, password]))
            print(alert_template.format(f"User '{new_username}' created successfully!"))
            return True


def add_task(
        assign_to: str, task: str,
        description: str, due_date: str,
        completed: str = "No"):
    # This function adds a task to tasks.txt
    date_created = datetime.now().strftime("%d %b %Y")
    task_entry: str = entry_template.format(
        assign_to=assign_to, task=task,
        description=description, date_created=date_created,
        due_date=due_date, completed=completed
    )
    # Only open tasks.txt once all the variables have been set.
    with open(task_txt, 'a') as tasks:
        tasks.write('\n' + task_entry)
        print(f"Task created successfully (due: {due_date})")


def view_all():
    # This function lists all tasks in tasks.txt
    with open(task_txt, 'r') as tasks:
        total_tasks = len(tasks.readlines())
        tasks.seek(0)
    for t in range(1, total_tasks):
        # Use find_task() to avoid rewriting the task template.
        print(find_task(t))


def view_mine(username: str):
    # This function views a specific user's tasks.
    with open(task_txt, 'r') as tasks:
        print("-------------------------------------------")
        for task_id, line in enumerate(tasks):
            assigned_to = line.split(', ')[0]
            if assigned_to == username:
                print(find_task(task_id))


def show_stats(border_length: int = 80):
    # This function prints out user and task statistics
    border = '-' * border_length
    if not (path.exists(user_overview_txt) and path.exists(task_overview_txt)):
        generate_reports()

    with open(user_overview_txt, 'r+') as user_overview, open(task_overview_txt, 'r+') as task_overview:
        print(border)
        for line in user_overview:
            print(line, end='')
        print(border)
        for line in task_overview:
            print(line, end='')
        print(border)


def generate_reports():
    # This function generates user_overview.txt and task_overview.txt
    with open(task_txt, "r") as tasks, open(user_txt, "r") as users:
        user_reports: List[str] = []
        total_assigned_tasks = len(tasks.readlines())
        total_users = len(users.readlines())
        # These will be updated as user.txt and tasks.txt are read.
        total_complete_tasks = 0
        total_incomplete_tasks = 0
        total_overdue_tasks = 0
        ''' Since the amount of lines in user.txt counted using readlines()
            the pointer needs to be set back to the start of the file.
            https://stackoverflow.com/questions/64385399/file-readline-returns-nothing-even-though-know-there-are-lines-of-content
        '''
        users.seek(0)
        for user_line in users:
            username = user_line.strip().split(', ')[user_index]
            # Reset all stats to 0 for each user
            user_overdue = 0
            user_assigned = 0
            user_incomplete = 0

            # Reset the pointer for tasks.txt each time we go through all tasks.
            tasks.seek(0)
            for task_line in tasks:
                task = task_line.strip().split(", ")
                if task[user_index] == username:
                    user_assigned += 1
                    if task[completed_index] == "No":
                        user_incomplete += 1
                        total_incomplete_tasks += 1
                        if datetime.strptime(task[due_date_index], "%d %b %Y") < datetime.now():
                            user_overdue += 1
                            total_overdue_tasks += 1
            # These variables are just used to make the call to user_report_template() look nicer.
            total_complete_tasks = total_assigned_tasks - total_incomplete_tasks
            complete = user_assigned - user_incomplete

            user_percentage_of_total = percentage(user_assigned, total_assigned_tasks)
            user_percentage_completed = percentage(complete, user_assigned)

            user_percentage_incomplete = percentage(user_assigned - complete, user_assigned)
            user_percentage_overdue = percentage(user_overdue, user_assigned)
            # Generate and append a user_report to the user_reports list.
            user_report = user_report_template(
                username, user_percentage_of_total,
                user_assigned, user_percentage_completed,
                user_percentage_incomplete, user_percentage_overdue
            )

            user_reports.append(user_report)
        # Update
        total_incomplete_tasks = total_assigned_tasks - total_complete_tasks
        percentage_total_incomplete = percentage(
            total_incomplete_tasks,
            total_assigned_tasks
        )

        # Write to user_overview.txt
        with open(user_overview_txt, "w+") as user_overview:
            user_overview.write(user_overview_template(total_users, total_assigned_tasks, user_reports))
            print("user_overview.txt generated")

        # Write to task_overview.txt
        with open(task_overview_txt, "w+") as task_overview:
            task_overview.write(
                task_report_template(
                    total_assigned_tasks,
                    total_complete_tasks,
                    total_incomplete_tasks,
                    percentage_total_incomplete,
                    total_overdue_tasks,
                    percentage(total_overdue_tasks, total_assigned_tasks)
                )
            )
            print("task_overview.txt generated")


def choose_from_menu(username: str):
    """This function prints out the options available to the current user."""
    all_options = '''\
a - adding a task
va - view all tasks
vm - view my task
e - exit'''
    admin_options = '''\
r - registering a user
ds - display statistics
gr - generate reports'''

    print("Select one of the following options:")
    if username == 'admin':
        print(admin_options)
    # Presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print(all_options)
    return input(": ").lower()


def edit_task(
        given_id: int, assigned_to: Optional[str] = None,
        due_date: str = "", completed: Optional[bool] = None) -> str:
    """This function is used to edit tasks in task.txt"""
    result = ""
    # Keep track of each line since they all need to be written back to the file.
    lines: List[str] = []
    with open(task_txt, 'r') as tasks:
        for task_index, line in enumerate(tasks):
            if task_index == given_id:
                task = line.strip().split(', ')
                task_completed = task[completed_index]
                # Only allow tasks to be edited if they are incomplete.
                if task_completed == "No":
                    if completed:
                        task[completed_index] = "Yes"
                        result = "Task has been marked complete."
                        # Continue the loop if the task is remarked as complete.
                        continue
                    if assigned_to:
                        task[user_index] = assigned_to
                        print(task)
                    if due_date:
                        new_date = set_date()
                        if new_date:
                            task[due_date_index] = new_date
                    lines.append(', '.join(task))
                    result = "Task details edited successfully."
                else:
                    lines.append(line)
                    result = "The task is 'complete' and may not be edited"
            else:
                lines.append(line)
    # Reopen tasks.txt for writing
    with open(task_txt, 'w') as tasks:
        tasks.write('\n'.join(lines))
    return result


def display_tasks(username: str):
    selected = None
    view_mine(username)
    while selected != '-1':
        selected = input("Select a task (Enter -1 to go back):")
        if selected.isdigit():
            selected = int(selected)
            print("Select Task: ", selected)
            print("Please select an option below to continue:")
            print("r: Return to the previous menu")
            print("c: Mark as complete")
            print("e: Edit this task")
            print("b: Back to main menu")
            choice = input(": ")
            operation = ""
            if choice == 'c':
                operation = edit_task(selected, completed=True)
                print(operation)
            elif choice == 'e':
                username = input("username (leave empty to skip): ")
                due_date = input("due date (leave empty to skip): ")
                if username or due_date:
                    operation = edit_task(selected, username, due_date)
            elif choice == 'b':
                break
            elif choice == 'c':
                continue
            print(operation)
        else:
            print("Please enter a number (or -1 to go back)")


def assign_task():
    # This option is used by the 'admin' user to assign a task to a user
    assign_to = input("Assign task to (username): ")
    task = input(f"What should {assign_to} do? ")
    description = input(f"How should {assign_to} complete this task? ")
    print("By when should this task be completed? (dd-mm-YYYY)")
    # Use the `datetime` module so that the date can be validated with minimal effort.
    print("When is the task due? ")
    due_date = set_date()
    if due_date:
        add_task(assign_to, task, description, due_date)


# ====Logic====
def main():
    """ This function runs until 'e' is entered by the user"""
    credentials = None
    logged_in = False

    while True:
        if not credentials:
            credentials = find_user(input("username: "))
        elif not logged_in:
            logged_in = input("password: ") == credentials[1]
        else:
            menu = choose_from_menu(credentials[0])
            if menu == 'r' and credentials[0] == 'admin':
                """ This option is used by 'admin' to register new users.
                    Any other user will not be given an indication that it exists.
                """
                new_username = input("username: ")
                reg_user(new_username)

            elif menu == 'ds' and credentials[0] == 'admin':
                """ This option is used by 'admin' user to show program statistics 
                    (total amount of users, total amount of tasks given)
                    Any other user will not be given an indication that it exists.
                """
                show_stats()

            elif menu == 'a':
                # This option is used to assign a task to a user
                assign_task()

            elif menu == 'va':
                # This option is used to view all tasks assigned to all users.
                view_all()

            elif menu == 'vm':
                # This option is used to display all tasks assigned to the current user.
                display_tasks(credentials[0])
            elif menu == "gr" and credentials[0] == 'admin':
                # This option allows the admin to generate a user_overview.txt and task_overview.txt
                generate_reports()

            elif menu == 'e':
                # This option is used to exit the program.
                print('Goodbye!!!')
                exit()

            else:
                print("You have made a wrong choice, Please Try again")


main()
