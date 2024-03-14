from pymongo import MongoClient
from tqdm import tqdm
import re
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import Dataset
import json

class DLLM:
    def __init__(self):
        self.key_mapping = {
            "JudgeNames": "jdg-",
            "People": "pp-",
            "Organizations": "org-",
            "Locations": "loc-",
            "CaseNumbers": "cn-",
            "Appellants": "app-",
            "Respondents": "res-",
            "Money": "mon-",
            "FIRNumbers": "fr-",
            "ReferenceArticles": "ra-",
            "ReferredCases": "rca-",
            "ReferredCourts": "rco-",
            "AppealCaseNumbers": "acn-",
            "AppealCourtNames": "apcn-",
            "Case Approval": "capp-"
        }
        self.client = MongoClient('mongodb://localhost:27017/')

    # This function generates abstracts using a pretrained model based on the specified prefix.
    # It first checks if CUDA is available, then determines the appropriate model based on the prefix.
    # It then adds a prefix text to each article in the input array.
    # After preprocessing the articles, it loads the tokenizer for the selected model.
    # It defines a function to generate answers using the tokenizer and a dummy batch for demonstration purposes.
    # This function maps the generated abstracts to the input articles.
    # Finally, it converts the output summaries to JSON format along with information about the device used.
    # Note: The model loading part is commented out and a dummy response is returned for illustration purposes.

    def generate_abstracts(self, article_array, prefix):
        # Check if CUDA is available to select the appropriate device
        if torch.cuda.is_available():
            device = "cuda"
        else:
            device = "cpu"

        # Determine the prefix text and model based on the specified prefix
        if prefix == "Sum":
            prefix_text = "Summary : "
            model_name = "google/long-t5-tglobal-base"
        elif prefix == "IE":
            prefix_text = "Extract Crucial Information : "
            model_name = "t5-base"  # Assuming model 2 is T5-base
        else:
            raise ValueError("Invalid prefix. Choose 'Sum' for summarization or 'IE' for extraction.")
        
        # Add prefix_text to each article in article_array
        article_array = [prefix_text + article for article in article_array]
        
        my_dict = {'article': article_array}
        test_dataset = Dataset.from_dict(my_dict)
        model_directory = 'something'
        
        # Load the tokenizer for the selected model
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Define a function to generate answers using the tokenizer
        def generate_answer(batch):
            inputs_dict = tokenizer(batch["article"], padding="max_length", max_length=8192, return_tensors="pt", truncation=True)
            input_ids = inputs_dict.input_ids.to(device)
            attention_mask = inputs_dict.attention_mask.to(device)

            # Generate a dummy abstract for illustration (Replace with actual model generation)
            batch["predicted_abstract"] = tokenizer.decode([2, 11,23,11,4345,232,887], skip_special_tokens=True)
            return batch

        # Apply the function to generate abstracts for the test dataset
        test_dataset = test_dataset.map(generate_answer)




        # test dummy later to me removed 

        if prefix =='IE':
            summar ='jdg-Waheeduddin-Ahmad @ pp-Khuda-Bakhsh @ org-High-Court-of-West-Pakistan,-Lahore @ loc-Mongia-Street @ cn-Writ-Petition-No.-685/R-of-1964 @ app-Sardar-Muhammad @ mon-Rs.-W.-98.-R.-21 @ capp-Appeal-allowed. @'
            output_summaries = [{"output": summar}]

        if prefix =='Sum':
            summar = 'IN THE SUPREME COURT OF PAKISTAN (Appellate Jurisdiction) Present: Mr. Justice Qazi Faez Isa Mr. Supreme Court Sardar Tariq Masood CIVIL APPEAL NO. 472 OF 2013 (On appeal against the judgment dated 6.02.2013 passed by the Lahore High Court, Lah., in C. R. No. 489/2009) Contract Act (XXIII of 1872) Ss. 12 (2), 25 & 115 Relinquishment of right of inheritance, relied upon from the petitioner’s side, even if proved against the respondent, had to be found against public policy Dispute between two sisters was contrary to public policy and contrary to shariah Appellate Court had wrongly exercised its jurisdiction, had misread evidence, disregarded crucial evidence, relyd on the purported compromise application which Mirza Abid Baig could not establish was part of the Court record, gave credence to purported agreement without the concomitant obligation of making payment and wrongly assumed that a valuable claim was relinquished without proof and without consideration. Umar Bakhsh v Azim Khan1 and Ghulam Ali v Ghuam Sarwar Naqvi (Mst.) 4 ref. Muhammad Atif Amin, ASC Mr. M. S. Khattak, AOR Respondent Nos. 1(a) to (d) Mr. Mustafa Ramday, A SC assisted by Mr. Zaafir Khan, Ms. Zoe Khan and Mr. Akbar Khan, Advocates Syed Rifaqat Hussain Shah, Aor Respondents No. 2-5: Ex parte Dates of Hearing: 10th and 12th February 2020 JUDGMENT QAZI FAEZ ISSA, J. Mirza Sultan Baig died on 22nd March 1975 leaving behind a widow Mst Tahira Sultana, two sons, namely Mirza Abbas Baig and Mirza Imran Baig, and four daughters, Abida Azam, Zahida Sabir, Naveeda Sultan (Pasha) and Fakhira TariQ. A suit for the administration of the estate of their father and rendition of accounts'
            output_summaries = [{"output": summar}]




        # Convert the output summaries to JSON format
        #output_summaries = [{"output": summary} for summary in test_dataset["predicted_abstract"]]
        return json.dumps({"device": device, "predicted": output_summaries})

    


    def SimilarCaseRetrieval(self, text):
        # Sample dictionary mapping file names to their content
        # Extract indexes from the function's return value
        indexes = [45, 55, 65]  # Example indexes of similar cases found
        
        # Combine found_files and indexes
        result = {"indexes": indexes}  # Combining indexes into a dictionary
        
        # Convert result to JSON format
        return json.dumps(result)  # Returning the result as a JSON string

    


    def find_files_by_indexes(self, indexes):
        """
        Fetches files from MongoDB based on the given indexes.

        Args:
            indexes (list): List of indexes to search for in the database.

        Returns:
            list: List of dictionaries containing file information.
                Each dictionary contains keys: 'content', 'summary', 'filename', 'ie', 'id'.
        """
        try:
           # client = MongoClient('mongodb://localhost:27017/')  # Connect to MongoDB
            db = self.client['JudiciaryCases']  # Replace 'your_database_name' with your database name
            collection = db['files']  # Choose a collection name, e.g., 'files'
            print("connected to DB")
        except Exception as e:
            print("Error connecting to the database:", e)
            return []

        files = []
        documents = collection.find({'id': {'$in': indexes}})

        for document in documents:
            try:
                if document:
                    content = document['content']
                    summary = document['summary']
                    filename = document['filename']
                    ie = document['information']
                    id = document['id']  # You need to implement Information Extraction logic
                    files.append({
                        'content': content,
                        'summary': summary,
                        'filename': filename,
                        'ie': ie,
                        'id': id
                    })
            except Exception as e:
                print(f"Error retrieving document for index {document}: {e}")
        return  json.dumps(files, indent=4)
        #return files



    
        

    def find_matching_files_in_mongodb(self, search_string, optional_strings=None):
        """
        Search for matching files in MongoDB based on the search string and optional strings.

        Args:
            search_string (str): The main search string.
            optional_strings (list[str], optional): List of optional strings to search for in addition to the main string.

        Returns:
            list[dict]: List of dictionaries containing matching files, each dictionary containing 'id' and 'filename'.
        """
        # Remove leading/trailing whitespaces from the search string
        search_string = search_string.strip()

        # Remove leading/trailing whitespaces from optional strings if provided
        if optional_strings:
            optional_strings = [opt_string.strip() for opt_string in optional_strings]
        else:
            optional_strings = []  # Handle case where optional_strings is None

        # Connect to MongoDB
        #client = MongoClient('mongodb://localhost:27017/')
        db = self.client['JudiciaryCases']  # Replace 'your_database_name' with your database name
        collection = db['files']  # Choose a collection name, e.g., 'files'

        matching_files = []

        # Retrieve all documents from the collection
        cursor = collection.find()
        for index, document in enumerate(tqdm(cursor, desc="Searching files in MongoDB")):
            content = document['content']
            filename = document['filename']
            index = document['id']

            # Check if all optional strings are present in the content
            if optional_strings and not all(re.search(opt_string, content, re.IGNORECASE) for opt_string in optional_strings):
                continue  # Skip this file if any optional string is not found

            # Check if the search string is present in the content
            if re.search(search_string, content, re.IGNORECASE):
                matching_files.append({
                    'id': index,
                    'filename': filename
                })
 
        return json.dumps(matching_files)



    # Method to extract key-value pairs from a given text using a predefined mapping.
    # It searches for each key's corresponding prefix in the text using regular expressions,
    # and extracts the value associated with it. Returns a dictionary of extracted pairs.
    def _extract_key_value(self, text):
        pairs = {}
        text = text + ' @'  # Appending '@' to ensure all patterns are properly matched.
        for key, prefix in self.key_mapping.items():
            pattern = re.escape(prefix) + "(.*?)(?=@)"
            matches = re.findall(pattern, text)
            if matches:
                values = [match.strip() for match in matches]
                pairs[key] = values
        return pairs

    # Method to convert extracted key-value pairs from text into JSON format.
    # It utilizes _extract_key_value method to obtain the pairs, then converts them into JSON format
    # using the json.dumps() function and returns the JSON output.
    def convert_to_json(self, text):
        extracted_pairs = self._extract_key_value(text)
        json_output = json.dumps(extracted_pairs)
        return json_output


    