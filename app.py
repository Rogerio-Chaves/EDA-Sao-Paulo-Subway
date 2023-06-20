from matplotlib.style import use

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

use('seaborn-v0_8')


@st.cache_data
def load_data(PATH):
	data = pd.read_csv(PATH, index_col='year_month')
	return data	


def participation_measurement(line, df, totals):
    line_sum = df[df.loc[:,'line'] == line].loc[:,'total']
    participation_line = (line_sum / totals) * 100
    return st.plotly_chart(px.line({'Date': participation_line.index,'%': participation_line}, x='Date', y='%', title=f'Monthly participation in total of demand (in %) - Line {line}'))


def most_participation(df, totals):
    line_01_sum = df[df.loc[:,'line'] == 1].loc[:,'total']
    line_03_sum = df[df.loc[:,'line'] == 3].loc[:,'total']
    participation_line1_line2 = ((line_01_sum + line_03_sum) / totals) * 100

    return st.plotly_chart(px.line({'Date':participation_line1_line2.index, '%':participation_line1_line2}, x='Date', y='%'))

if __name__ == '__main__':
	st.title('Passanger transported demand by lines - São Paulo Subway')
	st.text('From January 2017 to April 2023')

	DATA_PATH = 'ptl_complete.csv'

	data_load_state = st.text('Loading data...')
	df = load_data(DATA_PATH)
	data_load_state.text('Done! (using st.cache_data)')

	totals = df.groupby(by='year_month').sum().drop(labels='line', axis=1).loc[:,'total']

	st.subheader('Passengers transforted by line - Metrics')
	option_graph_01 = st.selectbox(label='Metric', options=df.columns[1:], index=0)
	color_lines = ['yellow', 'blue', 'green', 'red', 'purple', 'silver']
	st.plotly_chart(px.line(df.reset_index(), x='year_month', y=option_graph_01, color='line', color_discrete_sequence=color_lines, title=f'Passengers transforted by line - {option_graph_01.capitalize()}'))

	st.markdown('We can see the impact of COVID pandemic for passenger transported demand in the subway.')

	st.subheader('Lines 1 and 3 monthly participation in total of demand (in %) - Passenger transported demand by line')
	most_participation(df, totals)
	st.markdown('Question:')
	st.markdown('If the monthly share of the two lines with the highest passenger demand is decreasing over time, is there any possibility that other lines are growing?')
	st.markdown('Below we can verify the share of each line.')

	st.subheader('Monthly participation in total of demand (in %) by line')
	option_graph_02 = st.selectbox(label='Line', options=[1, 2, 3, 4, 5, 15], index=0)
	participation_measurement(option_graph_02, df, totals)

	st.markdown('Questions:')
	st.markdown('**A.** What can be caused by participation decreases of demand in lines 1 and 3, ' 
         	'are there significant changes in the infrastructure of the subway ' 
             '(new station or lines)?')
    
	st.markdown('**R.** infrastructure changes - New stations in the subway')
        
	st.markdown('Line 1 - No changes')

	st.markdown('Line 2 - No changes')

	st.markdown('Line 3 - No changes')
	
	st.markdown('Line 4 - 4 new stations')
	line_04 = {'Station': ['São Paulo - Morumbi', 'Higienópolis - Mackenzie', 'Oscar Freire', 'Vila Sônia'], 'Inauguration': ['December 27, 2018', 'January 23, 2018', 'April 4, 2018', 'December 17, 2021']}
	line_04_df = pd.DataFrame(line_04)
	st.write(line_04_df)
	
	st.markdown('Line 5 - 10 new stations')
	line_05 = {'Station':['Alto da Boa Vista', 'Borba Gato', 'Brooklin', 'Eucaliptos', 'Moema', 'Hospital São Paulo', 'Santa Cruz', 'Chácara Kablin', 'AACD - Servidor', 'Campo Belo'], 'Inauguration': ['September 6, 2017', 'September 6, 2017', 'September 6, 2017', 'March 2, 2018', 'April 5, 2018', 'September 28, 2018', 'September 28, 2018', 'September 28, 2018', 'August 31, 2018', 'April 8, 2019']}
	line_05_df = pd.DataFrame(line_05)
	st.write(line_05_df)
	
	st.markdown('Line 15 - 9 new stations')
	line_15 = {'Station':['São Lucas', 'Camilo Haddad', 'Vila Tolstói', 'Vila União', 'jardim Planalto', 'Sapopemba', 'Fazenda da Juta', 'São Mateus', 'jardim Colonial'], 'Inauguration':['April 6, 2018', 'April 6, 2018', 'April 6, 2018', 'April 6, 2018 ', 'August 26, 2019', 'December 16, 2019', 'December 16, 2019', 'December 16, 2019', 'December 16, 2021']}
	line_15_df = pd.DataFrame(line_15)
	st.write(line_15_df)
        
	st.markdown('**B.** What\'s the reason for the increasing in passenger transported demand ' 
         'in lines 5 and 15?')

	st.markdown('**C.** If the main lines are decreasing the demand, is there the possibility ' 
         'of other lines taking these positions in the next years?')
        
	st.markdown('**D.** Is this a new pattern or when the subway rescues the level of ' 
         'passenger demand near of previous COVID pandemic the old pattern will return?')
	
