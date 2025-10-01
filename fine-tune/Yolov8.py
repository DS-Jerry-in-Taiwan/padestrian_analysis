import json
import json
import os
import csv
import argparse
from pathlib import Path
from PIL import Image

def parse_odgt(odgt_path):
    """
    Parse the odgt file and return a list of dictionaries.
    
    Args:
        odgt_path (str): The path to the odgt file.
    Returns:
        list: A list of dictionaries parsed from the odgt file.
    """
    with open(odgt_path, 'r', encoding="utf8") as f:
        for line in f:
            if not line.strip():
                continue
            yield json.loads(line)
def ensure_dir(file_path):
    """
    Ensure that the directory for the given file path exists. If it doesn't exist, create it.
    """
    directory = os.path.direname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory, parents=True, exist_ok=True)

def save_to_csv(data, csv_path):
    """
    Args:
        data (list): List of dictionaries to save.
        csv_path (str): Path to the output CSV file.
    """
    ensure_dir(csv_path)
    if not data:
        print("No data to save.")
        return
    
    keys = data[0].keys()
    with open(csv_path, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"Data saved to {csv_path}")

            
if __name__ == "__main__":
    odgt_path = "/home/ubuntu/projects/pedestrian_attribute_recognition_30%/data/CrowdHuman/crowdhuman/annotation_train.odgt"  # Replace with your odgt file path
    n = 0
    for item in parse_odgt(odgt_path):
        if n >= 1:
            break
        print(item)  # Process each item as needed
        n+=1