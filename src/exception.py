# इसका उपयोग error की technical details निकालने के लिए किया गया है, जैसे:
#error कहाँ हुआ,कौन सी file में,कौन सी line number पर
import sys

#यह function error की पूरी जानकारी निकालने के लिए बनाया गया है
#error: जो actual error हुई है (जैसे ValueError, ZeroDivisionError आदि)
#error_details: sys module ताकि error traceback मिल सके
def error_message_detail(error,error_details:sys):
  print(error)
  print(error_details)
  print(error_details.exc_info) #एक function है जो error की तीन जानकारी देता है:type, value, traceback.
  _,_,exe_tb= error_details.exc_info() #इसका मतलब है कि हम sys.exc_info() से सिर्फ तीसरा हिस्सा traceback (exe_tb) निकाल रहे हैं।
  print(exe_tb)

  file_name = exe_tb.tb_frame.f_code.co_filename #यह बताता है कि error कौन सी Python file में हुआ है।

#यह एक formatted string है जो बताती है:
#File name,Line number,Error message
#उदाहरण के लिए output ऐसा दिखेगा
  error_message="error occurred python script name {0} line number [{1}] error mrssage [{2}]".format(
    file_name,exe_tb.tb_lineno,str(error)
  )

  return error_message

class CustomException(Exception):
#जब भी कोई error होगी, यह class उस error को error_message_detail() function को भेज देगी ताकि पूरी detail निकाली जा सके।  
  def __init__(self,error_message,error_details: sys):
    super().__init__(error_message)
    self.error_message= error_message_detail(
      error_message,error_details=error_details
    )
#इसका मतलब है — जब भी हम print(e) करेंगे (जहाँ e एक exception object है),
#तो हमें वही formatted message दिखेगा जो function ने बनाया था।
  def __str__(self):
    return self.error_message  