from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class Task:
    def __init__(self, title, description, status="Pending"):
        self.title = title
        self.description = description
        self.status = status
        self.due_date = None

    def complete_task(self):
        self.status = "Completed"

    def extend_due_date(self, days):
        if self.due_date:
            self.due_date += timedelta(days=days)

    def set_due_date(self, due_date):
        try:
            self.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid due date format. Please use YYYY-MM-DD.")


class Notification:
    def __init__(self, message):
        self.message = message

    def send(self):
        print(f"Sending notification: {self.message}")


class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def display_tasks(self):
        print(f"Tasks for User: {self.name}")
        for task in self.tasks:
            print(task.title)


class TaskList:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def display_tasks(self):
        print(f"Tasks in List: {self.name}")
        for task in self.tasks:
            print(task.title)


class TaskScheduler:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def get_due_tasks(self):
        today = datetime.today().date()
        due_tasks = [task for task in self.tasks if task.due_date and task.due_date <= today]
        return due_tasks

    def display_tasks(self):
        print("Due Tasks:")
        for task in self.tasks:
            print(task.title)


class ProjectTask(Task):
    def __init__(self, title, description, status="Pending", project=None):
        super().__init__(title, description, status)
        self.project = project

    def set_project(self, project):
        self.project = project


class Project:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def display_tasks(self):
        print(f"Tasks in Project: {self.name}")
        for task in self.tasks:
            print(task.title)


class TaskManager:
    def __init__(self):
        self.users = []
        self.task_lists = []

    def add_user(self, user):
        self.users.append(user)

    def remove_user(self, user):
        self.users.remove(user)

    def create_task_list(self, name):
        task_list = TaskList(name)
        self.task_lists.append(task_list)

    def remove_task_list(self, task_list):
        self.task_lists.remove(task_list)

    def display_users(self):
        print("Users:")
        for user in self.users:
            print(user.name)

    def display_task_lists(self):
        print("Task Lists:")
        for task_list in self.task_lists:
            print(task_list.name)


class Reminder(Notification):
    def __init__(self, message, due_date):
        super().__init__(message)
        self.due_date = due_date

    def send(self):
        print(f"Sending reminder: {self.message} (Due Date: {self.due_date})")


class TaskPlanner(TaskScheduler):
    def __init__(self):
        super().__init__()

    def get_upcoming_tasks(self):
        today = datetime.today().date()
        upcoming_tasks = [task for task in self.tasks if task.due_date and task.due_date > today]
        return upcoming_tasks


class TaskExecutor(ABC):
    @abstractmethod
    def execute(self, task):
        pass


class AssigneeTaskExecutor(TaskExecutor):
    def __init__(self, assignee):
        self.assignee = assignee

    def execute(self, task):
        print(f"Executing task: {task.title} (Assignee: {self.assignee})")


class TaskAnalyzer(ABC):
    @abstractmethod
    def analyze(self, task):
        pass


class PriorityTaskAnalyzer(TaskAnalyzer):
    def analyze(self, task):
        if task.status == "Pending" and task.due_date and task.due_date <= datetime.today().date():
            print(f"Task '{task.title}' has high priority.")


def main():
    # Create objects
    task1 = Task("Task 1", "Description 1")
    task1.set_due_date("2023-04-30")

    task2 = ProjectTask("Task 2", "Description 2")
    task2.set_due_date("2023-05-15")

    user1 = User("John Doe", "john@example.com")
    user1.add_task(task1)

    task_list = TaskList("Today's Tasks")
    task_list.add_task(task2)

    project = Project("Project A")
    project.add_task(task2)

    task_scheduler = TaskScheduler()
    task_scheduler.add_task(task1)

    task_manager = TaskManager()
    task_manager.add_user(user1)
    task_manager.create_task_list("My Tasks")
    task_manager.create_task_list("Work Tasks")

    reminder = Reminder("Don't forget!", "2023-04-30")

    task_planner = TaskPlanner()
    task_planner.add_task(task1)

    assignee_task_executor = AssigneeTaskExecutor("John")
    assignee_task_executor.execute(task1)

    priority_task_analyzer = PriorityTaskAnalyzer()
    priority_task_analyzer.analyze(task1)

    # Display information
    print("--- Task Manager ---")
    task_manager.display_users()
    task_manager.display_task_lists()

    print("--- Task List ---")
    task_list.display_tasks()

    print("--- Project ---")
    project.display_tasks()

    print("--- Task Scheduler ---")
    task_scheduler.display_tasks()
    due_tasks = task_scheduler.get_due_tasks()
    print("Due Tasks:")
    for task in due_tasks:
        print(task.title)

    print("--- Task Planner ---")
    upcoming_tasks = task_planner.get_upcoming_tasks()
    print("Upcoming Tasks:")
    for task in upcoming_tasks:
        print(task.title)

    # Send notifications
    reminder.send()

    # Execute task
    assignee_task_executor.execute(task1)


if __name__ == "__main__":
    main()
