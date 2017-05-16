# -*- coding: utf-8 -*-

from csv import DictReader

import matplotlib.pyplot as plt

from stats import correlation # I am stats.py from the book.


def parse_gun_law_score_file():
    """Parse the gun law score.txt file. Returns a list of tuple, where each
    tuple contains the state's name and grade."""
    
    with open('gun law score.txt', 'r') as f:
        data = []
        append = data.append
        for line in f:
            try:
                _, state, grade, _ = line.split()
            except ValueError:
                # A ValueError is raised for state that contain a whitespace in
                # their name such as New York, New Jersey, and etc. The two
                # parts of the name must be put back together
                _, state_pt1, state_pt2, grade, _ = line.split()
                state = state_pt1 + ' ' + state_pt2
            
            append((state.strip(), grade.strip()))
        
        return data
    
    
def parse_violent_crime_rates_file():
    """Parses the 'violent crime rates 2014.csv' file. Returns a list of 
    tuples, where each tuple contains the state's name and the total number of
    violent crimes per 100,000 people in that state."""
    
    with open('violent crime rates 2014.csv', 'r') as f:
        data = []
        append = data.append
        
        reader = DictReader(f)
        for row in reader:
            append((row['State'], float(row['Violent Crime rate'])))
            
        return data

    
def parse_property_crime_rates_file():
    """Parses the 'property crime rates 2014.csv' file. Returns a list of 
    tuples, where each tuple contains the state's name and the total number of
    property crimes per 100,000 people in that state."""
    
    with open('property crime rates 2014.csv', 'r') as f:
        data = []
        append = data.append
        
        reader = DictReader(f)
        for row in reader:
            append((row['State'], float(row['Property crime rate'])))
            
        return data


def total_crime_rates(v, p):
    """Given that v and p are the list of violent crime rate and property crime
    rate repectively, this function return a list of tuples containing the name 
    of the state and the total crime rate for that state. 
    """
    totals = []
    append = totals.append
    for i in range(len(v)):
        v_state, v_rate = v[i]
        p_state, p_rate = p[i]
        
        if v_state == p_state:
            append((v_state, v_rate + p_rate))
        else:
            print(v_state, p_state)
            
    return totals 


def show_graph_of_average_crime_rates(grades, rates):
    
    #We start by calculation the averages based on grades
    
    avg = [0.0, 0.0, 0.0, 0.0, 0.0]
    
    a_cnt = 0
    b_cnt = 0
    c_cnt = 0
    d_cnt = 0
    f_cnt = 0
    
    rates = dict(rates)
    for state, grade in grades:
        if grade[0] == 'A':
            avg[4] += rates[state] 
            a_cnt += 1
        if grade[0] == 'B':
            avg[3] += rates[state] 
            b_cnt += 1
        if grade[0] == 'C':
            avg[2] += rates[state] 
            c_cnt += 1
        if grade[0] == 'D':
            avg[1] += rates[state] 
            d_cnt += 1
        if grade[0] == 'F':
            avg[0] += rates[state] 
            f_cnt += 1
            
    avg[4] /= a_cnt
    avg[3] /= b_cnt
    avg[2] /= c_cnt
    avg[1] /= d_cnt
    avg[0] /= f_cnt
    
    plt.title("Average Crime Rate Vs Gun Law Grades, 2014")
    plt.plot([0.0, 1.0, 2.0, 3.0, 4.0], avg)
    plt.xlabel('Grade')
    plt.ylabel('Total crime rate(per 100,000)')
    plt.xticks(range(0, 5))
    plt.show()


table = {
    'A' : 4.0,
    'A-': 3.7,
    'B+': 3.3,
    'B' : 3.0,
    'B-': 2.7,
    'C+': 2.3,
    'C' : 2.0,
    'C-': 1.7,
    'D+': 1.3,
    'D' : 1.0,
    'D-': 0.7,
    'F' : 0
    }
    

def calculate_correlation(grades, rates):
    
    number_grades = []
    crime_rates = []
    
    rates = dict(rates)
    for state, grade in grades:
        number_grades.append(table[grade])
        crime_rates.append(rates[state])
        
    return correlation(number_grades, crime_rates)
        

def show_scatter_plot(grades, rates):
    num_grades = []
    crime_rates = []
    
    rates = dict(rates)
    for state, grade in grades:
        num_grades.append(table[grade])
        crime_rates.append(rates[state])
    
    plt.title("Gun Law vs Crime Rate, 2014")
    plt.scatter(num_grades, crime_rates)
    plt.xlabel('Grade')
    plt.ylabel('Total crime rate(per 100,000)')
    plt.show()
    

if __name__ == '__main__':
    grades = parse_gun_law_score_file()
    
    v = parse_violent_crime_rates_file()
    p = parse_property_crime_rates_file()
    totals = total_crime_rates(v, p)
    
    show_graph_of_average_crime_rates(grades, totals)
    
    show_scatter_plot(grades, totals)
    
    print(calculate_correlation(grades, totals))