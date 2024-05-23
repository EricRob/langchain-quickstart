import streamlit as st
from langchain.llms import OpenAI
import pandas as pd

st.set_page_config(page_title="ERAS check")
st.title('ERAS check')

# openai_api_key = st.sidebar.text_input('OpenAI API Key')

def generate_response(input_text):
  llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
  st.info(llm(input_text))

class Order(object):
    """docstring for Order"""
    def __init__(self, txt, group):
        super(Order, self).__init__()
        self.raw = txt
        self.group = group
        self.name = None
        self.freq = None
        self.occ = None
        self.dose = None
        self.route = None
        self.comment = None
        self.linked = None
        self.process()

    def csv_line(self):
        return [self.group, self.name, self.freq, self.occ, self.dose, self.route, self.comment, self.linked]
    
    def to_df(self):
        return

    def process(self):
        self.name = self.raw[0][1:-1]
        cprint(self.name, 'green')
        for line in self.raw:
            if line[1] == '\t':
                val = line[2:-1]
                cprint(line, 'yellow')
                val = val.split()
                if val[0] == 'Frequency:':
                    self.freq = " ".join(val[1:])
                elif val[0] == 'Number':
                    self.occ = " ".join(val[3:])
                elif val[0] == "Dose:":
                    self.dose = " ".join(val[1:])
                elif val[0] == "Route:":
                    self.route = " ".join(val[1:])
                elif val[0] == "Linked":
                    self.linked = True
                elif val[1] == 'Comments:':
                    self.comment = " ".join(val[2:])
                else:
                    pdb.set_trace()
        return

def main(text):
    orders = {}
    activate = False
    it = iter(text)
    groups = {}
    group = None
    for line in it:
        if line == 'Active Orders\n':
            print(line)
            activate = True
        elif activate and line[0] == '\t':
            groups[group]['txt'].append(line)
        elif activate:
            if line[0] != '\t' and line[0] != '\n' and ('CHG' not in line) and ('Chlorhexidine' not in line):
                group = line.rstrip()
                groups[group] = {}
                groups[group]['txt'] = []
                groups[group]['ord'] = []

    for group in groups:
        line = groups[group]['txt']
        name = line[0]
        order_txt = [name]
        for i in range(1, len(line)):
            if i == len(line)-1 and line[i][1] == '\t':
                order_txt.append(line[i])
                groups[group]['ord'].append(Order(order_txt, group))
            elif line[i][1] == '\t':
                order_txt.append(line[i])
            else:
                groups[group]['ord'].append(Order(order_txt, group))
                order_txt = [line[i]]
    orders = []
    for group in groups:
        for order in groups[group]['ord']:
            orders.append(order.csv_line())
    header = ['group', 'name', 'frequency', 'occurences', 'dose', 'route', 'comments', 'linked_order']
    df = pd.DataFrame(orders, columns = header)
    return df

with st.form('my_form'):
  text = st.text_area('Inpatient orders', 'Output of .ACTIVEORD')
  submitted = st.form_submit_button('Submit')
  if submitted:
      df = main(text)
      st.dataframe(df)
