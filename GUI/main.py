import os
from login import login_page
import inspect

global page_stack
page_stack = ["login_win"]

login_page()
#current_filename = os.path.basename(__file__)
#print("Current filename:", current_filename)


