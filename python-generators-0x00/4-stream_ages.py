#!/usr/bin/python3
"""Module for calculating average age using generators"""
import csv
import os
from typing import Generator


def stream_user_ages() -> Generator[int, None, None]:
    """Generator that yields user ages one by one"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "user_data.csv")
    
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield int(row['age'])


def average_age() -> float:
    """Calculate average age using the generator"""
    total_age = 0
    count = 0
    
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    return total_age / count if count > 0 else 0


if __name__ == "__main__":
    avg = average_age()
    print(f"Average age of users: {avg:.2f}")
