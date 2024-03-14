
import os
from pymongo import MongoClient
from tqdm import tqdm

def store_files_in_mongodb(content_directory, summary_directory, information_directory):
    client = MongoClient('mongodb+srv://Alucard008:UiIhOdwPy1xuM8jy@judiciarycluster.4jhslpg.mongodb.net/Judiciary_Database?retryWrites=true&w=majority')
    db = client['Judiciary_Database']  # Use a valid database name without spaces
    collection = db['files']  # Choose a collection name, e.g., 'files'
    Start_ID = 0
    
    content_files = [filename for filename in os.listdir(content_directory) if filename.endswith('.txt')]
    summary_files = [filename for filename in os.listdir(summary_directory) if filename.endswith('.txt')]
    information_files = [filename for filename in os.listdir(information_directory) if filename.endswith('.txt')]
    
    # Ensure each directory has the same number of files
    assert len(content_files) == len(summary_files) == len(information_files), "Each directory must have the same number of files"
    
    for content_filename, summary_filename, information_filename in tqdm(zip(content_files, summary_files, information_files), desc="Storing files in MongoDB"):
        content_file_path = os.path.join(content_directory, content_filename)
        summary_file_path = os.path.join(summary_directory, summary_filename)
        information_file_path = os.path.join(information_directory, information_filename)
        
        with open(content_file_path, 'r', encoding='utf-8') as content_file, open(summary_file_path, 'r', encoding='utf-8') as summary_file, open(information_file_path, 'r', encoding='utf-8') as information_file:
            content = content_file.read()
            summary = summary_file.read()
            information = information_file.read()
            
            # Insert the file content into MongoDB
            collection.insert_one({
                'filename': content_filename,
                'content': content,
                'summary': summary,
                'information': information,
                'id': Start_ID
            })
            Start_ID += 1

# Example usage:
content_dir = 'files/Civil Cases Together'
summary_dir = 'files/generated_summaries'
information_dir = 'files/generated_Information'
store_files_in_mongodb(content_dir, summary_dir, information_dir)