
## For using sleep function because selenium 
## works only when the all the elements of the 
## page is loaded.
import time 
import requests
import threading
import pandas as pd
import tkinter
from tkinter import filedialog

class WhatsAppBulk:
    def __init__(self, APIkey:str) -> None:
        """
        APIkey -> Your TextMeBot API key
        """
        self.API_KEY = APIkey
        return None
    
    def ReadExcelFile(self)-> None:
        """
        Opens a 'Open File' window to read Excel File"""
        root = tkinter.Tk()
        root.withdraw()
        try:
            self.file_path = filedialog.askopenfilename()

        except FileNotFoundError:
            print("File Not found at ", self.file_path)

    def WnoLabel(self, label:str = None, CountryCode:str = None, getLabels:bool = False):
        #Check if  
        """
        label  -> Excel Column'label' having WhatsAPP Number.
        
        CountryCode  -> Country Code WhatsAPP numbers. Eg. India : '+91'
        
        getLabels  -> If True: return all labels in ExcelFile""" 
        try:
                file = pd.read_excel(self.file_path)
                df = pd.DataFrame(file)

        except ValueError:
            print("Select Excel File (.xl)")
            return None

        except:
            print("File Not found. Use ( .ReadExcelFile) method to read excel file")
            return None
        
        #If getLabels is False
        if not getLabels:

            self.CntryCode = CountryCode
            self.WtsAppNumList = [] 
                
            try:
                #While getLabels is False, check if certain WhatsApp column exists in DataFrame
                number = df[label]
                for n in number:
                    "WhatsApp Numbers are being appended to WtsNumList."
                    self.WtsAppNumList.append(self.CntryCode+str(n))
                
            except KeyError:
                print("Label dosen't exist in document.")
        #If getLabels is True,  Return Column Labels -> list
        elif getLabels:
            return df.columns
    
    def Start(self, message:str, ImageURL:str = None, maxlimit:int = 1000, wait:int=8.1):
        """
        message:str -> Enter your message which you want to be sent.

        ImageURL    -> Image URL should be publicaly hosted on Internet.

        maxlimit    -> WhatsApp messaging limit of your WhatsApp Account.

        wait        -> Sleep time, to make your WhatsApp messaging genuine to WhatsApp."""

        def Run(num):
            txtBotURL = f'http://api.textmebot.com/send.php?recipient={num}&apikey={self.API_KEY}&text='+message
            if ImageURL:
                txtBotURL+='&file='+ImageURL
            r = requests.get(txtBotURL)
            print(r.text)

        def Multhread():
            limit = 0
            try:
                for n in range(len(self.WtsAppNumList)):
                    if limit < maxlimit:
                        if self.WtsAppNumList:
                            thread = threading.Thread(target=Run, args=(self.WtsAppNumList[0], ), name='t'+str(n))
                            thread.start()
                            self.WtsAppNumList.pop(0)
                            limit+=1
                            if wait:
                                time.sleep(wait)
                    else:
                        print("Max Limit Reached. Numbers left to be Whatsapped->\n", self.WtsAppNumList)
            except AttributeError:
                print("\nWhatsApp number list empty. Use .ReadExcelFile method to read from Excel file or <obj>.WtsAppNumList to enter number in list.")
        return Multhread()

api = "Your TextMeBot API_KEY"
send = WhatsAppBulk(api)
send.ReadExcelFile()
send.WnoLabel(label='Name', CountryCode='+91')
msg = "Hello World"
send.Start(message=msg, maxlimit=501, ImageURL="https://i.pinimg.com/564x/31/7f/c9/317fc98d6a0e8bdce3d48f827e93890d.jpg")



