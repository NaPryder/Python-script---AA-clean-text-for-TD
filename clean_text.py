import re
import os

class RawData:

    def __init__(self, raw_file) -> None:
        self.raw_file = raw_file
        self.source_text = ""
        self.cleaned_text = ""
        self.pattern = r"^[1-9]+"
    
    def clean_raw_file(self):
        """Read raw file 
            Split text with {start_splitter_txt} and {end_splitter_txt}
            get source file

        Args:
            raw_file (str): read from raw file .txt

        Returns:
            bool: if found source text return true
        """

        with open(self.raw_file, 'r', encoding='utf8') as rawtxt:
            txt = rawtxt.read()

            start_splitter_txt = "FlowListDual\nStart"
            end_splitter_txt = "Action details\nSelect an action in the flow or list view to view details"

            if end_splitter_txt in txt:
                txt = txt.split(end_splitter_txt)[0]
                txt = "Start" + txt.split(start_splitter_txt)[1]
                # print('txt:', txt)
                self.source_text = txt
                # print("source text: " ,self.source_text)
                return True

            else:
                print(f'Raw file:{self.raw_file} not found end_splitter_txt: {end_splitter_txt}')
                return False

    def read_source_text(self):
        data = ""
        for line in self.source_text.split('\n'):

            if re.match(self.pattern, line.strip()):
                line = line.replace('\n','')
                # print(line, type(line))
                data += line + " "
            else:

                data += line + "\n"
            
        self.add_cleaned_text(data=data.strip())
        # print(' source data ', data)
        
    def add_cleaned_text(self, data:str):

        print(' len source data:', len(data.split('\n')))
        for line in data.split('\n'):
            # print(" scr data:", line)
            if str(line).strip().lower() == "start":
                continue

            elif str(line).strip().lower() == "end":
                continue

            elif str(line).strip().lower() == "":
                print(f"line = blank >> '{line}'")
                continue

            else:
                #Other text
                #replace some text
                line = self.replacing_text(text=line)
                if not re.match(self.pattern, line.strip()):
                    self.cleaned_text += f" {line}"

                else:
                    self.cleaned_text += f"\n{line}"

    @staticmethod
    def replacing_text(text:str):
        d_replacer = {
            "Iffile": "If file",
            "Ifstring": "If string",
            "Ifnumber" : "If number",
            "Iffolder" : "If folder",
            "If$" : "If $",
            "Ifboolean" : "If boolean",
            "Ifwindow": "If window",
            'If“TEXTBOX”': 'If “TEXTBOX”',
            'Ifchecks': 'If checks',
            "If(": "If (",
            'If“': 'If “',
            "❪":" ( ",
            "❫":" ) ",
            " Sendan ": " Send an ",
            'stringconvert': 'string convert',
            'Replace“': 'Replace “',
            'Trim$': 'Trim $',
            'Delete“': 'Delete “',
            'Step“':'Step “',
            'Run“': 'Run “',
            "Assign": "Assign ",
            "Increment$": "Increment $",
            "Decrement$": "Decrement $",
            'Comment“' : 'Comment “',
            "PutVariable": "Put Variable",
            'Log to file“': 'Log to file “',
            "Getvalue": "Get value",
            "windowto": "window to",
            'condition“': 'condition “',
            'text$': 'text $',
            'CaptureSelect': 'Capture Select',
            'Split$': 'Split $',
            'CaptureGet': 'Capture Get',
            'CaptureSelect': 'Capture Select',
            'Maximizethe': 'Maximize the',
            'keystrokes“': 'keystrokes “',
            'Copy“': 'Copy “',
            'textSource': 'text Source',
            'item$': 'item $',
            'rowFrom': 'row From',
            'namesfrom': 'names from',
            'cellvalue': 'cell value',
            'combobox': 'combo box',
            "sErrorMess…": "$sErrorMessage$",
            "nErrorLi…": "nErrorLineNumber$",
            'EndTask': "End Task",
            "fomula": "formula",
            "sheetby": "sheet by",
            "numberConvert": "number Convert",
            "itemfrom": "item from",
            "conditionfile": "condition file",
            "stringConvert": "string Convert",
            "Connectas": "Connect as",
            "Disconnectas": "Disconnect as",
            "Closethe": "Close the",
            "Clickon": "Click on",
            "CaptureSet": "Capture Set",
            "CaptureClick": "Capture Click",
            'CaptureCheck': 'Capture Check',
            'CaptureExpand' : 'Capture Expand',
            'CaptureLeft': 'Capture Left',
            'listview': 'list view',
            "Openspreadsheet": "Open spreadsheet",
            "Sizeof": "Size of",
            'Clearall': "Clear all",
            "Loopfor": "Loop for",
            'Connectto': 'Connect to',
            'Deleteusing': 'Delete using',
            'Activatethe': 'Activate the',
            'rowsfrom' :'rows from',
            'desktopscreenshot': 'desktop screenshot',
            'windowapplication': 'window application',
            'Open$': 'Open $',
            'Loopwhile':'Loop while',
            "ThrowAllErrors": "Throw All Errors",
            "CatchAllErrors": "Catch All Errors"

        }

        for findText, replaceWith in d_replacer.items():
            if findText in text:
                text = text.replace(findText, replaceWith)
        return text

class DataOutput:

    def __init__(self) -> None:
        self.d_data = {}
        self.d_sorted_data = {}
        self.d_output = {}
        pass
    
    def cut_invicible_line(self, cleaned_text): 

        for line in cleaned_text.split('\n'):

            pattern_cut = r"^[1-9]+\d+ [1-9]+\d+"
            if not re.match(pattern_cut, line.strip()):
                # print(line)

                if line.lower().strip() == 'start':
                    continue
                elif line.lower().strip() == 'end':
                    continue
                elif line.lower().strip() == '':
                    #skip blank line
                    continue

                key = line.split(' ')[0].strip()
                value = line.replace(key, '').strip()

                # try convert key to int
                try:
                    key = int(key)
                    # print(f"key: {key} line:{value}")
                except:
                    print(f'key: {key} is error {value}')
                    pass

                if key not in self.d_data:
                    self.d_data[key] = [value]
                else:
                    self.d_data[key].append(value)

            else:
                print('not match', line)
    
    def select_line_detail(self):
        """
        Select first item in list of line detail
        """

        for key, listOfvalue in self.d_data.items():
            if len(listOfvalue) >= 2:

                if listOfvalue[0] == listOfvalue[1]:
                    self.d_data[key] = listOfvalue[0]
                else:
                    self.d_data[key] = listOfvalue[0]
                    # self.d_data[key] = listOfvalue[0] + " " + listOfvalue[1]
            else:
                self.d_data[key] = listOfvalue[0]

    def add_head_tail_to_output(self):
        #Add head
        self.d_output = {'Start': ''}

        #sorting
        self.sorting_line_number()

        #Add details
        for key, value in self.d_data.items():
            self.d_output[key] = value

        #Add tail
        self.d_output['End'] = ""

    def sorting_line_number(self):
        key_sorted = sorted(self.d_data)
        print(key_sorted)
        
        for key in key_sorted:
            self.d_sorted_data[key] = self.d_data.get(key)

    def write_data(self, output_file):
        """Save dictionary (self.d_output) to output file

        Args:
            output_file (str): save to output file .txt
        """

        with open(output_file, 'w', encoding='utf8') as txtf:
            for k, v in self.d_output.items():
                line = f"{k} {v}\n"
                txtf.write(str(line))

    def show_result(self):

        print('--- show result ---')
        for k, v in self.d_output.items():
            print(f'key: {k} {v}')
        print(f"len d_output = {len(self.d_output)}")

def create_folder(folder:str):
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"create folder: {folder}")

def main_clean_text(output_filename:str, is_del_file=False):

    """
    Process
        1. Get Raw file from Website as .txt file (must named like 01.txt, 02.txt, ...) saved in folder 'raw files'
        2. Loop over source folder and process on each raw file
        3. Clean raw file and get 'source text'
        4. Clean 'source text' and get 'cleaned text'
        5. Read 'cleaned text' and stored in dictionary with key= line numnber, value=line detail
        6. Add each dictionary 
        7. Add head and tail to dictionary
        8. clean dictionary and write .txt file name 'output file'

    """

    #check output filename contains .txt
    if not '.txt' in output_filename.lower():
        print(f'output_filename:{output_filename} is not .txt file')
        return 

    folder_source = os.path.join(os.path.dirname(__file__), 'raw files')
    folder_result = os.path.join(os.path.dirname(__file__), 'result')
    
    #create result folder
    create_folder(folder_result)
        
    #assign output file
    output_file = os.path.join(folder_result, output_filename)

    Data = DataOutput()
    list_del = []

    print(f"Source folder: {folder_source}")
    for file in os.listdir(folder_source):

        if re.match(r"^\d+.*.txt", file):
            print(file)

            raw_file = os.path.join(folder_source, file)
            list_del.append(raw_file)

            rawData = RawData(raw_file)

            #Read raw file
            rawData.clean_raw_file()
            
            #Read source text
            rawData.read_source_text()

            #Read cleaned text
            Data.cut_invicible_line(cleaned_text=rawData.cleaned_text)
        # break
    
    # #select line detail data
    Data.select_line_detail()

    # #merge all data with head and tail
    Data.add_head_tail_to_output()

    # #save data to output file
    Data.write_data(output_file=output_file)

    #show result
    Data.show_result()
    
    #delete raw files
    if is_del_file:
        delete_file(list_file=list_del)


def delete_file(list_file:list):
    for file in list_file:
        try:
            os.remove(file)
        except:
            pass

if __name__ == '__main__':

    #assign output filename

    output_filename = r"AR003-000-Receive_Waste_scrap - Main Task.txt"
    deletingFile = False

    main_clean_text(output_filename=output_filename, is_del_file=deletingFile)