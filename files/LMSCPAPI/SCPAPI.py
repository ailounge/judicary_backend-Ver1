from DLLM import DLLM
import json
# Search Keyword
def SearchKeyWord(Main_Search,CheckBox,dllm):
    '''
    Main_Search -> String
    CheckBox-> List of Strings
    dllm -> DLLM object

    returns
    [{
                'filename': ...,
                'content': ...,
                'id':  ...,
                'summary' : ... '
                'ie':  ... 

            }...] , totalnumber

    '''
    
    indexes  = json.loads(dllm.find_matching_files_in_mongodb( Main_Search, CheckBox))
    ids = [entry['id'] for entry in indexes]
    data = json.loads(dllm.find_files_by_indexes(ids))
    for entry in data:
        entry['ie'] = dllm.convert_to_json(entry['ie'])
    return [json.dumps(data) ,  len(data)]

    




def OnDetail(id,dllm):

    '''
    id -> String/ID # dummy for now
    dllm -> DLLM object

    returns
    [{
                'filename': ...,
                'content': ...,
                'id':  ...,
                'summary' : ... '
                'ie':  ... 

            }...] , totalnumber

    '''
    ids = json.loads(dllm.SimilarCaseRetrieval(id))['indexes']
    data = json.loads(dllm.find_files_by_indexes(ids))
    #print(data)
    for entry in data:
        entry['ie'] = dllm.convert_to_json(entry['ie'])
    #print(data)
    #data = [entry for entry in data]
    return [json.dumps(data), len(data)]




Sum='both'
def GenerateSumIE(doc,dllm,Sum='both'):
    '''
    doc -> string # dummy for now
    dllm -> DLLM object

    returns sum,ie
    # Sample Summary output {"device": "cuda", "predicted": [{"output": "Summary"}]}
    # Sample IE Output     {"device": "cuda", "predicted": [{"output": Json format}]}

    '''

    if Sum == 'sum'  or Sum == 'Sum':
        data = dllm.generate_abstracts( doc ,"Sum")
        return data
    elif Sum == 'ie'  or Sum == 'IE':
        data = dllm.generate_abstracts( doc ,"IE")
        return data
    elif Sum == "Both" or Sum == "both":
        print('Generating summary')
        sum = dllm.generate_abstracts( doc ,"Sum")
        print('Generating Information')
        ie = dllm.generate_abstracts( doc ,"IE")

        ie = json.loads(ie)
        ie['predicted'][0]['output'] = dllm.convert_to_json(ie['predicted'][0]['output'] )
        return sum,ie


    
        












# Example usage:
if __name__ == "__main__":
    dllm = DLLM()

    '''
    #Test Search by keyword
    indexes,total = SearchKeyWord("Crime ",["Qazi Faez","Islamabad"],dllm)
    print(indexes, total)
    '''



    '''
    #Test  When Click on Detail:  Since this is yet to be completed in module 3. this will return 3 files as dummy
    indexes,total = OnDetail("Test or number",dllm)
    print(indexes,total)

    '''



    SearchKeyWord('Hello',"hello",dllm)

    '''  '''
    # Test function when  document is uploaded .  for now it only accepts Text and returns dummy text 
    # sum,ie = GenerateSumIE(["Document1 is very good document"],dllm)
    # print(sum,ie)


  

