import os
import csv
from datetime import datetime
from constants import EMBEDDING_MODEL_NAME
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from pathlib import Path


def log_to_csv(question, answer, filename):

    log_dir, log_file = "local_chat_history", f"{Path(filename).stem}_log.csv"
    # Ensure log directory exists, create if not
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Construct the full file path
    log_path = os.path.join(log_dir, log_file)

    # Check if file exists, if not create and write headers
    if not os.path.isfile(log_path):
        with open(log_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "question", "answer"])

    # Append the log entry
    with open(log_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, question, answer])


def get_embeddings(device_type="cuda"):
    if "instructor" in EMBEDDING_MODEL_NAME:
        return HuggingFaceInstructEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            model_kwargs={"device": device_type},
            embed_instruction="Represent the document for retrieval:",
            query_instruction="Represent the question for retrieving supporting documents:",
        )

    elif "bge" in EMBEDDING_MODEL_NAME:
        return HuggingFaceBgeEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            model_kwargs={"device": device_type},
            query_instruction="Represent this sentence for searching relevant passages:",
        )

    else:
        return HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            model_kwargs={"device": device_type},
        )

## NOT USED
def run_question_file(directory):
    """
    Opens a directory and gets the path of a text file if it exists.
    
    Parameters:
        directory (str): The path of the directory to search.
    
    Returns:
        str: The path of the text file if found, otherwise returns None.
    """
    # Check if the directory exists
    if os.path.exists(directory) and os.path.isdir(directory):

        # List all files in the directory
        files = os.listdir(directory)
        query_number, query_array = 0,[]

         # Flag to indicate if CSV file is found
        csv_found = False

        # Iterate through the files
        for file in files:
            file_path = os.path.join(directory, file)  # Construct the full file path

            # Check if the file has a csv file (ends with .csv)
            print(file_path)
            if file.endswith(".csv"):
                #return number in file
                csv_found = True
                with open(file_path, "r") as f:
                    query_number = f.readline()
            else:
                #return question array
                with open(file_path, "r") as f:
                    query_array = f.readlines()

        # If no CSV file is found, create one with integer 0
        if not csv_found:
            csv_file_path = os.path.join(directory, "question_number.csv")
            try:
                with open(csv_file_path, "w") as f:
                    f.write("0\n")
                query_number = 0
            except Exception as e:
                print(f"Error creating CSV file: {e}")

        return [query_array, query_number]

    else:
        print("Invalid directory path.")
        return []
