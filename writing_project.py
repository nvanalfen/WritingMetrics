from enum import Enum
from datetime import datetime, timedelta

class GoalFrequency(Enum):
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3
    YEARLY = 4

class Project:
    def __init__(self, name, goal=None, start=None, end=None):
        self.name = name
        self.goal = goal
        self.start=start
        self.end=end
        self.hiatus = set()            # Set of dates to ignore (Long spans of no activity with an explanation)

    def set_goal(self, amount, frequency=GoalFrequency.DAILY):
        self.goal = ProjectGoal(amount, frequency)

    def set_hiatus(self, start, end):
        delta = end - start
        
        for i in range(delta.days + 1):
            self.hiatus.add(start + timedelta(days=i))

class ProjectGoal:
    def __init__(self, amount, frequency=GoalFrequency.DAILY):
        self.amount = amount
        self.frequency = frequency