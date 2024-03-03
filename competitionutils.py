import csv
import os
import json

CSV_LOG_NAME = 'qa_log.csv' # shouldn't need to access this
JSON_FILETRACKER = os.path.join('question_bank', 'info.json') # path to dictionary that tracks the location of the line for the question file

def getLine(filename):
    '''Given the prefix of the given questions textfile, check the local database against the line number read and continue querying from there.
    Returns str value while valid.
    Returns None when file has finished iteration.'''
    if not os.path.exists(os.path.join('question_bank','info.json')):
        # create json block
        db = {}
        with open(JSON_FILETRACKER, 'w') as f:
            json.dump(db, f)

    # Read
    with open(JSON_FILETRACKER, 'r') as f:        
        db = json.load(f)
    line_number = db.get(filename, 0)

    

    filepath = os.path.join('question_bank',filename)
    with open(filepath, 'r') as f:
        questions = f.readlines()
    
    # Early termination if the end of file has been reached
    if line_number == len(questions):
        return None
    
    db[filename] = line_number+1
        

    # Save if the DB is updated
    with open(JSON_FILETRACKER, 'w') as f:
        json.dump(db, f)
    
    return questions[line_number]
    

print(getLine('questions.txt'))


