import sys
from dataclasses import dataclass


def error_message(ex):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print('Fail in line:', exc_tb.tb_lineno, "\n",
          "Where:", exc_tb.tb_frame, "\n",
          "Error:", exc_obj)


@dataclass
class Contact:
    name: str
    phone: None
    email: str
    day: None
    time: None
    visit_location: str
