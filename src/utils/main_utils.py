import sys  #system sathe trace.
from typing import Dict, Tuple #type hints.
import os #फाइल/डायरेक्टरी का path बनाना, फाइल चेक/बनाने में काम आता है।
import pandas as pd
import pickle #Python ऑब्जेक्ट को binary में save/load करने के लिए।
import yaml #yaml file read karava.
import boto3 #AWS SDK for Python.

from src.constant import * #प्रोजेक्ट के constants ले कर आता है
from src.exception import CustomException #कस्टम exception क्लास — आपके try/except में उसे raise किया जा रहा है।
from src.logger import logging # project logging setup.

class MainUnits:  #जहाँ file-I/O और serialization के functions rake huae he.
  def __init__(self) -> None: #constructor। अभी खाली है (pass) — यानी जब MainUnits() बनाते हैं तो कोई initialization नहीं हो रही।
    pass

  def read_yaml_file(self, filename :str) -> dict:
    try:
      with open(filename,'rb') as yaml_file: #फाइल binary मोड में खोलता है।
        return yaml.safe_load(yaml_file) #YAML parsing करके Python dict देता है।
    except Exception as e:
      raise CustomException(e,sys) from e #अगर कोई error आया तो CustomException के साथ raise करता है।
    
  def read_schema_config_file(self) ->dict:
    try:
      schema_config = self.read_yaml_file(os.path.join("config","schema.yaml")) #config/schema.yaml फाइल पढ़कर return करता है।
      return schema_config
    except Exception as e:
      raise CustomException(e, sys) from e  #यह method सीधे config/schema.yaml पढ़कर schema का dict लौटाता है।
  @staticmethod
  def save_object(file_path:str, obj:object) -> None:
    logging.info("entered the save_object method of main units class")
    try:
      with open(file_path,'wb') as file_obj:
        pickle.dump (obj, file_obj) #ऑब्जेक्ट को binary में फाइल में save करता है।
      logging.info('exited the save_object method of main utils class')
#किसी Python object को .pkl-जैसे फाइल में सुरक्षित तरीके से लिख देता है।
    except Exception as e:
      raise CustomException(e,sys) from e

  @staticmethod

  def load_object(file_path:str) ->object:
    logging.info('enteed the load_object method of MainUtils class')
    try:
      with open(file_path,'rb') as file_obj:
        obj = pickle.load(file_obj)
      logging.info("exited the load_object method of Mainutils class")
      return obj
    except Exception as e:
      raise CustomException (e, sys) from e
  @staticmethod

  def load_object(file_path):
    try:
      with open(file_path,'rb') as file_obj:
        return pickle.load(file_obj)
      
    except Exception as e:
      logging.info('exception occured in load_object function utils')
      raise CustomException(e,sys)
      
# Python में एक ही नाम की दो definitions में से आखिरी वाला ही उपयोग होगा — यानी पहला वाला ओवरराइड (replace) हो जाएगा। यह अक्सर unintended होता है और bugs पैदा करता है।