#यह Python का OS (Operating System) module import करता है।
#इसका उपयोग files और folders के path को handle करने के लिए किया जाता है।
import os 


#S3 bucket का उपयोग डेटा या मॉडल को cloud storage में सेव करने के लिए होता है।
#यहाँ यह नाम सिर्फ एक constant के रूप में रखा गया है।
AWS_S3_BUCKET_NAME = "wafer-fault"
#यह बताता है कि प्रोजेक्ट MongoDB database में "pwskills" नाम का database इस्तेमाल करेगा।
MONGO_DATABASE_NAME = 'pwskills'
#यह बताता है कि इस database में "waferfault" नाम की collection इस्तेमाल की जाएगी।
MONGO_COLLECTION_NAME = 'waferfault'


#यह उस column का नाम है जिसे predict या classify किया जाएगा।
#यानी dataset में "quality" नाम का column target variable (output) है।
TARGET_COLUMN = 'quality'
#इस URL के ज़रिए Python प्रोग्राम MongoDB Cloud से कनेक्ट होगा।
#यहाँ snshrivas:Snshrivas username और password हैं।
#imp: यह sensitive information (password) है, इसे public कोड में नहीं रखना चाहिए।
#अच्छा तरीका है कि इसे .env फाइल या environment variable में रखें।
MONGO_DB_URL = 'mongodb+srv://yesha:yesha123@wafercluster.u5q3zia.mongodb.net/'

#यह उस फाइल का बेस नाम है जिसमें trained machine learning model को सेव किया जाएगा।
MODEL_FILE_NAME = 'model'
#यह Python का binary format होता है जिससे object (जैसे trained model) को सेव और लोड किया जा सकता है।
MODEL_FILE_EXTENSION = '.pkl'

artifact_folder = 'artifacts'