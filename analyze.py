import transform
import numpy as np
import matplotlib.pyplot as plt  #
from scipy.stats import norm

def calculate_mean(grades: List[float]) -> float:
    """ calculating the means of grades """
    if not grades:
        return 0.0
    return sum(grades)/ len(grades) 
def calculate_std(grades: List[float]) -> float:
    """ calcuating the standard deviation of grades"""
    if len(grades) < 2:
        return 0.0
    mean = calculate_mean(grades)
    variance = sum((x - mean) ** 2 for x in grades / len(grades) - 1) 
    return variance ** 0.5


def calculate_percentile(grades: List[float], percentile: int) -> float:
     if not grades:
        return 0.0
    sorted_grades = sorted(grades)
    index = (percentile / 100) * (len(sorted_grades) - 1)
    lower = int(index)
    upper = lower + 1
    
    if upper >= len(sorted_grades):
        return sorted_grades[-1]
    
    weight = index - lower
    return sorted_grades[lower] * (1 - weight) + sorted_grades[upper] * weight


"""
def find_outliers

def calculate_distribution_stats

def plot_grade_distribution

def plot_box_pilot

def identify_improvements
    
    Identify students showing improvement across quizzes
    quiz_grades: list of grade lists [quiz1_grades, quiz2_grades, ...]
    Returns list of improvement metrics
    
"""


x = np.linspace(mean - 4 * std, mean + 4 * std, 1000)  
y = norm(loc=mean, scale=std).pdf(x)

plt.plot(x, y, c="blue")  
plt.show()