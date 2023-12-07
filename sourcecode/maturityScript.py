import requests
import pandas as pd
import logging
from utils import exception_catcher, exec_time, Excel_Exporter

logger = logging.basicConfig(filename="output.log", filemode='a',\
                                 format="%(asctime)s %(name)s %(levelname)s %(message)s",\
                                    datefmt="%H:%M:%S",\
                                        level=logging.INFO)

class Automation():
    def __init__(self) -> None:
        self.logger = logging.getLogger()
        config_data = pd.read_json('config.json')
        conf_df = pd.DataFrame(config_data)
        for i,row in conf_df.iterrows():
            (self.base_url, token, self.file, self.Uuid) = row[0:]
        self.header = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": "Api-Token {}".format(token)}
        self.logger.info("Configuration parameters are {}, {}, {}, {}".format(self.base_url, self.header, self.file, self.Uuid))

    @exec_time
    @exception_catcher   
    def maturity(self):
        self.logger.info("The main code has started its execution !!") 
        #Load the excel as DF, skipping first row and replace Nan cells with value 0
        df = pd.read_excel('{}'.format(self.file), index_col=False, skiprows=1).fillna(0)
        #To remove Unnamed columns 
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        Objectives = []
        #Objectives list to capture the required columns 
        [Objectives.append(cols) for cols in df.iloc[:,3:]]
        
        #Iterate through rows in the dataframe
        for index, rows in df.iterrows():
            # Iterate for each objective and modify the cell based on the outcome
            for object in Objectives:
                df.at[index, object] = self.make_get_calls(df[object].values[index])
        
        # Export the dataframe to excel, format as a table
        Excel_Exporter(self.file, df)
        self.logger.info("The main code has completed its execution !!")

    @exception_catcher
    def make_get_calls(self,*args):
        self.logger.debug("The method make_get_calls in invoked")
        # validating if the cell has api url or 0
        if args[0] != 0:
            if "accountUuid" in args[0]:
                 # condition to check if the api uri contains accountid and replace with Uuid
                 full_url = args[0].replace("{accountUuid}", self.Uuid )
            else:
                # form the complete url using the tenant adress + api Uri
                full_url = self.base_url + args[0]
            self.logger.debug("The complete URL is {}".format(full_url))
            
            # Perform get calls for the API  
            get_response = requests.get(url=full_url, headers=self.header, timeout=10)
            #get_response.raise_for_status()
            if get_response.status_code == 200:
                self.logger.debug("The API response is {}".format(get_response.json()))
                # return False if the received json is empty else mark the cell as True
                return False if get_response.json() == [] else True
            elif get_response.status_code == 403:
                # condition to check if the API response is 403 and marking the cell as False
                self.logger.debug("The API response for HTTP 403 is {}".format(get_response.json()))
                return False
            else:
                self.logger.error(f'API call failed with {get_response.status_code} on {full_url}')
                # Marking the cell as API failed, to check on logs for details
                return "API failed"
        return "Not Available"
    
if __name__ == "__main__":
    run_job = Automation()
    run_job.maturity()

