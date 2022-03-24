# Python imports
import copy
import shutil
from typing import Dict, List

#External libraries import
from fpdf import FPDF
from libs.pdf_table import create_table #Also a local import but is a external code

#Local imports
from commands.utils.report import wrapper_image
from config import IMAGE_FOLDER

A4_SIZE=(210,297) #(Width,Height)

def format_to_list(info:List[Dict[str,str]])->List[List[str]]:
  """ Transform the Dict info into a list format"""

  info = copy.deepcopy(info)

  #Delete keys we won't use
  [[i.pop('id'),i.pop('reference'),i.pop('extra_data')] for i in info]
  
  #First element will be a keys list
  headers = [[i.capitalize() for i in info[0].keys() ]] 
  
  #Convert the dicts into a list and format the values
  body  = [ 
      [ str(values) for values in i.values() ] for i in info
  ]
  data = headers+body
  
  #Parse the empty data into a white space
  for i in data:
      for j in range(len(i)):
          if(i[j]==''):
              i[j]=' '
  return data

def insert_text_into_pdf(pdf:FPDF,texts:List[str])->None:
  """Set text into the pdf and"""
  pdf.set_font('helvetica', '', 24)
  pdf.ln(30)
  for text in texts:
    pdf.write(8,text)
    pdf.ln(12)

  #Insert the content divider 
  pdf.image("./.images/image1.png", 50, 80, A4_SIZE[0]//2)

def create_pdf(filename:str,info:List[Dict[str,str]],extra_info:List[str])->None:
  """Create the movements report in a pdf format"""
  pdf = FPDF()
  pdf.add_page()

  #Format the data
  data = format_to_list(info)

  #Execute all the images related functions
  wrapper_image(data)

  #Prometeo's logo
  pdf.image(f"{IMAGE_FOLDER}/image0.png", 50, 8, A4_SIZE[0]//2)

  #Titles
  insert_text_into_pdf(pdf,extra_info)
  pdf.set_font("Times", size=8)
  pdf.ln()
  
  #Create the data table
  create_table(table_data = data,pdf=pdf, cell_width=[20,120,20,20])
  pdf.ln()

  #Inser the charts images into the pdf
  pdf.add_page()
  pdf.image(f"{IMAGE_FOLDER}/image1.png", 50, 8, A4_SIZE[0]//2)
  pdf.image(f"{IMAGE_FOLDER}/pie_chart.png", 50, 20, A4_SIZE[0]//2)
  pdf.image(f"{IMAGE_FOLDER}/total_balance.png", 40, 100, (A4_SIZE[0]//2)+25)
  pdf.image(f"{IMAGE_FOLDER}/credit_bar.png", 40, 200, (A4_SIZE[0]//2)+25)
  
  #Remove the images folder
  shutil.rmtree(IMAGE_FOLDER,ignore_errors=True)
  
  #Save the file
  pdf.output(filename, 'F')