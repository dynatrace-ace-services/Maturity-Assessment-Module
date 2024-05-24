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
            (self.base_url, token, self.Uuid, self.file, self.sheet) = row[0:]
        self.header = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": "Api-Token {}".format(token)}
        self.logger.info("Configuration parameters are {}, {}, {}, {}".format(self.base_url, self.header, self.file, self.Uuid))

    @exec_time
    @exception_catcher   
    def maturity(self):
        self.logger.info("The main code has started its execution !!") 
        self.df = pd.read_excel('{}'.format(self.file), index_col=False, sheet_name=self.sheet).fillna('')
        #Iterate through rows in the dataframe
        for index, rows in self.df.iterrows():
            self.observability_data(index, rows)
        #print(self.df)
        Excel_Exporter(self.file, self.df, "Sample")
        self.logger.info("The main code has completed its execution !!")

    @exception_catcher
    def make_get_calls(self,*args):
        self.logger.debug("The method make_get_calls in invoked")
        # validating if the cell has api url or 0`12w`
        if args[0] != '' and args[0].startswith("/"):
            if "accountUuid" in args[0]:
                 # condition to check if the api uri contains accountid and replace with Uuid
                full_url = args[0].replace("{accountUuid}", self.Uuid )
            elif "platform" in args[0]:
                full_url = self.base_url.replace("live", "apps")+args[0]
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
                if get_response.json() == []:
                    return "Empty"
                else:
                    outcome = get_response.json()
                    if 'nextPageKey' in outcome and outcome['nextPageKey'] is not None:
                        self.next_page = outcome['nextPageKey']
                        #self.logger.info("the nextpage key is {}".format(outcome['nextPageKey']))
                    else:
                        self.next_page = ''
                        #self.logger.info("the nextpage key is not present")
                    return outcome
            elif get_response.status_code == 403:
                # condition to check if the API response is 403 and marking the cell as False
                self.logger.debug("The API response for HTTP 403 is {}".format(get_response.json()))
                return "Forbidden"
            else:
                self.logger.error(f'API call failed with {get_response.status_code} on {full_url}')
                # Marking the cell as API failed, to check on logs for details
                return "API failed"
        return "Not Available"
    
    def recurser(self, api_url, temp_list, data_key):
        self.logger.info("The nextpage key is not empty")
        while True:
            if self.next_page != '':
                #self.logger.info("The api has multiple page and the NP key of this run is {}".format(self.next_page))
                #if 'from' in api_url:
                updated_api = api_url.split("?")[0]+"?nextPageKey={}".format(self.next_page)
                #updated_api = "{}&nextPageKey={}".format(api_url,self.next_page)
                self.logger.info("The updated URL is {}".format(updated_api))
                api_out = self.make_get_calls(updated_api)
                #self.logger.info("The data key is {}".format(data_key))
                #self.logger.info("The data length is {}".format(len(api_out)))
                temp_list = temp_list + api_out[data_key]
                self.logger.info("The length from recurser is {}".format(len(temp_list)))
            else:
                self.logger.info("The code run is completed with next page keys")
                break
        #self.logger.info("Next page key is not found!!!")
        return temp_list


    def observability_data(self, index, rows):
        if True:
            #self.df.at[index, 'Total Count'] = self.make_get_calls(self.df["API Call"].values[index])
            api_output = self.make_get_calls(self.df["API Call"].values[index])
            key_list = [ "hosts", "items", "problems", "values", "metrics", "monitors", "attacks", "releases", "events", "results" ]
            if type(api_output) is dict:
                for a,b in enumerate(key_list):
                    if b in api_output:
                        data_key = b
                temp = []
                temp = api_output[data_key]
                self.logger.info("The primary length of data is {}".format(len(temp)))
                if self.next_page != "":
                    out_list = self.recurser(self.df["API Call"].values[index], temp, data_key)
                    #out_list = self.recurser(self.df["API Call"].values[index], temp)
                    self.df.at[index, 'Total Count'] = len(out_list)
                else:
                    self.df.at[index, 'Total Count'] = len(temp)
            else:
                self.logger.info("The API {} returned a reponse {}".format(self.df["API Call"].values[index], api_output))
                #self.df.at[index, 'Total Count'] = len(api_output)
                self.df.at[index, 'Total Count'] = 0



if __name__ == "__main__":
    run_job = Automation()
    run_job.maturity()

