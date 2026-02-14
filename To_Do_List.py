# importing necessary libraries
import json
import datetime
from colorama import Fore, Style, init
init()

# Define the filename for storing tasks
FILENAME = 'tasks.json'

# Initialize the task list
task_list = []

# save and load functions to handle task persistence
def save_tasks():
    try:
        tasks_to_save = []
        for task in task_list:
            task_copy = task.copy()
            task_copy['due_date'] = task_copy['due_date'].isoformat()
            tasks_to_save.append(task_copy)

        with open(FILENAME, 'w') as f:
            json.dump(tasks_to_save, f, indent=2)
            print(Fore.GREEN + 'Tasks saved successfully!' + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error saving tasks: {e}" + Style.RESET_ALL)


def load_tasks():
    global task_list
    try:
        task_list = []
        with open(FILENAME, 'r') as f:
            tasks_loaded = json.load(f)
            for task in tasks_loaded:
                task['due_date'] = datetime.datetime.fromisoformat(task['due_date']).date()
                task_list.append(task)
    except FileNotFoundError:
        print(Fore.YELLOW + 'No existing task file found. Starting with an empty list.' + Style.RESET_ALL)
        task_list = []
    except Exception as e:
        print(Fore.RED + f"Error loading tasks: {e}" + Style.RESET_ALL)
        task_list = []
            

# welcome message and main loop for user interaction
print('==' * 20)
print(Fore.GREEN + 'Welcome to your To-Do List!'+ Style.RESET_ALL)
print('==' * 20)
load_tasks()

# Main loop for user interaction
while True:
    print('Please select an option:')
    print('1. Add a task')
    print('2. View tasks')
    print('3. Mark a task as completed')
    print('4. Delete a task')
    print("5. Sort tasks by due date")
    print('6. Exit')
    # Get user input and handle choices
    choice = input(Fore.BLUE + 'Enter your choice (1-6): ' + Style.RESET_ALL)
    # use if-elif statements to handle each choice and perform corresponding actions
    if choice == '1': # choice 1 is to add a task, we will ask the user for task description and due date
        task = input('Enter the task description:')
        date_due = input('Enter the due date (DD-MM-YYYY): ')
        # use try-except to handle date parsing and ensure correct format
        try:
            date_due = datetime.datetime.strptime(date_due, '%d-%m-%Y').date()
            task_list.append({'task': task, 'due_date': date_due, 'completed': False})
            print('Task added successfully!')
            save_tasks()
            
        except ValueError:
            print('Invalid date format. Please enter the date in DD-MM-YYYY format.')
    elif choice == '2': # choice 2 is to view tasks, we will display the list of tasks with their descriptions, due dates, and completion status
        if not task_list:
            print('No tasks in the list.')
        else:
            for idx, task in enumerate(task_list):
                status = 'Completed' if task['completed'] else 'Pending'
                print(f"{idx + 1}. {task['task']} (Due: {task['due_date']}) - {status}")
    elif choice == '3': # choice 3 is to mark a task as completed, we will ask the user for the task number and update the completion status of that task
        task_num = int(input('Enter the number of the task to mark as completed: '))
        if 1 <= task_num <= len(task_list):
            task_list[task_num - 1]['completed'] = True
            print('Task marked as completed.')
            save_tasks()
        else:
            print('Invalid task number.')
    elif choice == '4': # choice 4 asks the user for the task number to delete and removes that task from the list
        task_num = int(input('Enter the number from the list to delete: '))
        if 1 <= task_num <= len(task_list):
            del task_list[task_num - 1]
            print('Task deleted successfully.')
            save_tasks()
        else:
            print('Invalid task number.')
    elif choice == '5': # choice 5 sorts the tasks by their due date and displays them in order, 
                        # we will use the sorted function with a lambda function to sort the tasks based on their due date
        if not task_list:
            print('No tasks to sort.')
        else:
            sorted_tasks = sorted(task_list, key=lambda x: x['due_date'])
            print(Fore.CYAN + "\n📅 Tasks sorted by due date (earliest first):" + Style.RESET_ALL)
            print('==' * 20)
            for idx, task in enumerate(sorted_tasks):
                status = '✅' if task['completed'] else '🚫'
                print(f"{idx + 1}. {task['task']} (Due: {task['due_date']}) - {status}")
                print('==' * 20)
    elif choice == '6': # choice 6 is to exit the program, we will break the loop and print a goodbye message
        print('Exiting the To-Do List. Goodbye!')
        break
    else:  # everything else is an invalid choice, we will print an error message and prompt the user to enter a valid choice
        print('Invalid choice. Please enter a number between 1 and 6.')
