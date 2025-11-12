#Python का built-in logging मॉड्यूल। यह console या file में संदेश (info, error आदि) लिखने के लिए होता है।
import logging
import os
#अभी का समय लेने के लिए (datetime.now()), ताकि logfile का नाम टाइमस्टैम्प के साथ बना सकें।
from datetime import datetime

#सेकण्ड के लिए %S use करें, मिलिसेकंड/माइक्रोसेकंड चाहिए तो %f।
#यह line एक unique log file name बनाती है,
#जिसमें current date और time शामिल है।
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%s')}.log"
#यहाँ यह 'logs' नाम का folder बनाकर उसके अंदर log file रखना चाहता है।
logs_path = os.path.join(os.getcwd(),'logs')

os.makedirs(logs_path,exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
  filename=LOG_FILE_PATH, #जहाँ logs save होंगे
  #%(asctime)s ->Time जब log लिखा गया
  #%(lineno)d -> Line number जहाँ से log आया
  #%(name)s  -> Logger का नाम
  #%(levelname)s -> Log का level (INFO, ERROR, WARNING आदि)
  #%(message)s  -> Actual log message
  format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s", # किस format में message लिखना है
  level=logging.INFO #कौनसे level के logs लिखने हैं (INFO, WARNING, ERROR आदि)
)