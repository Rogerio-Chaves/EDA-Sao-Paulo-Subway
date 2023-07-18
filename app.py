from datetime import datetime
from Graphics import Graphics

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


@st.cache_data
def load_data(PATH):
	data = pd.read_csv(PATH, index_col='year_month')
	return data	

if __name__ == '__main__':
	st.title('Passanger transported demand by lines - São Paulo Subway')
	st.text('From January 2017 to April 2023')

	DATA_PATH = 'ptl_complete.csv'

	data_load_state = st.text('Loading data...')
	df = load_data(DATA_PATH)
	data_load_state.text('Done! (using st.cache_data)')

	graphics = Graphics(df)

	st.subheader('Passengers transforted by line - Metrics')
	option_graph_01 = st.selectbox(label='Metric', options=df.columns[1:], index=0)
	color_lines = ['yellow', 'blue', 'green', 'red', 'purple', 'silver']
	graphics.metrics_graph(option_graph_01, color_lines)
	st.markdown('We can see the impact of COVID pandemic for passenger transported demand in the subway.')

	st.subheader('Lines 1 and 3 monthly participation in total of demand (in %) - Passenger transported demand by line')
	graphics.most_participation()

	st.markdown('#### Question:')
	st.markdown('If the monthly share of the two lines with the highest passenger demand is decreasing over time, is there any possibility that other lines are growing?')
	st.markdown('Below we can verify the share of each line.')

	st.subheader('Monthly participation in total of demand (in %) by line')
	option_graph_02 = st.selectbox(label='Line', options=[1, 2, 3, 4, 5, 15], index=0)
	graphics.participation_measurement(option_graph_02)

	st.markdown('As we can see, '
		'**Line 1 - blue** has kept the same participation after the COVID period. Although, it has decreased in the previous period. '
		'**Line 2 - green**, after the fall caused by the COVID pandemic, recovered the participation level previous. '
		'**Line 3 - red** is decreasing, inclusive with this pattern before of COVID pandemic. '
		'**Line 4 - yellow**, after the COVID period shows a growing pattern in demand for passengers in your line. '
		'**Line 5 - lilac** kept a growing pattern until the begun 2021, next it has slowly decreasing. '
		'Finally, **line 15 - silver** has a growing pattern in this period. Although, the participation of this line is small yet.')
        
	line_04 = {'station': ['São Paulo - Morumbi', 'Higienópolis - Mackenzie', 'Oscar Freire', 'Vila Sônia'],
            'inauguration': ['2018-12-27', '2018-01-23', '2018-04-04', '2021-12-17'],
            'line': [4, 4, 4, 4]}
	line_04['inauguration'] = [datetime.strptime(d, "%Y-%m-%d") for d in line_04['inauguration']]
        
	line_05 = {'station':['Alto da Boa Vista', 'Borba Gato', 'Brooklin', 'Eucaliptos', 'Moema', 'Hospital São Paulo', 'Santa Cruz', 'Chácara Kablin', 'AACD - Servidor', 'Campo Belo'], 
           'inauguration': ['2017-09-06', '2017-09-06', '2017-09-06', '2018-03-02', '2018-04-05', '2018-09-28', '2018-09-28', '2018-09-28', '2018-08-31', '2019-04-08'],
          'line': [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]}
	line_05['inauguration'] = [datetime.strptime(d, "%Y-%m-%d") for d in line_05['inauguration']]
        
	line_15 = {'station':['São Lucas', 'Camilo Haddad', 'Vila Tolstói', 'Vila União', 'jardim Planalto', 'Sapopemba', 'Fazenda da Juta', 'São Mateus', 'jardim Colonial'], 
           'inauguration':['2018-04-06', '2018-04-06', '2018-04-06', '2018-04-06', '2019-08-26', '2019-12-16', '2019-12-16', '2019-12-16', '2021-12-16'],
          'line': [15, 15, 15, 15, 15, 15, 15, 15, 15]}
	line_15['inauguration'] = [datetime.strptime(d, "%Y-%m-%d") for d in line_15['inauguration']]

	line_04_df = pd.DataFrame(line_04)
	line_05_df = pd.DataFrame(line_05)
	line_15_df = pd.DataFrame(line_15)
    
	df = pd.concat([line_04_df, line_05_df, line_15_df], axis=0)
	df.sort_values(by='inauguration', inplace=True)

	line_colors = {4: 'yellow', 5: 'purple', 15: 'silver'}
	levels = np.tile([-9, 9, -7, 7 -5, 5, -3, 3, -1, 1],
                 int(np.ceil(df.shape[0]/6)))[:df.shape[0]]
	
	
	st.subheader('Infrastructure changes - New stations on the São Paulo Subway System - timeline')

	fig, ax = plt.subplots(figsize=(16, 8), layout="constrained")
	ax.set_title('New stations on São Paulo Subway System - Timeline', fontsize=25)

	ax.vlines(list(df.inauguration), 0, levels, color="tab:red")
	ax.plot(list(df.inauguration), np.zeros_like(list(df.inauguration)), "-o",
        color="k", markerfacecolor="w")

	for d, l, r, line in zip(list(df.inauguration), levels, list(df.station), list(df.line)):
		ax.annotate(r, xy=(d, l),
                xytext=(-3, np.sign(l)*3), textcoords="offset points", size='large',
                horizontalalignment="right",
                verticalalignment="bottom" if l > 0 else "top", bbox={'facecolor': line_colors[line], 'alpha': 0.75, 'pad': 10})

	ax.annotate('Line 4 - Yellow', xy=(datetime.strptime('2022-01-01', "%Y-%m-%d"), -5),
                xytext=(-3, np.sign(l)*3), textcoords="offset points", size='large',
                horizontalalignment="right",
                verticalalignment="bottom" if l > 0 else "top", bbox={'facecolor': 'yellow', 'alpha': 0.75, 'pad': 2})

	ax.annotate('Line 5 - Lilac', xy=(datetime.strptime('2022-01-01', "%Y-%m-%d"), -6),
                xytext=(-3, np.sign(l)*3), textcoords="offset points", size='large',
                horizontalalignment="right",
                verticalalignment="bottom" if l > 0 else "top", bbox={'facecolor': 'purple', 'alpha': 0.75, 'pad': 2})

	ax.annotate('Line 15 - Silver', xy=(datetime.strptime('2022-01-01', "%Y-%m-%d"), -7),
                xytext=(-3, np.sign(l)*3), textcoords="offset points", size='large',
                horizontalalignment="right",
                verticalalignment="bottom" if l > 0 else "top", bbox={'facecolor': 'silver', 'alpha': 0.75, 'pad': 2})
    
	plt.setp(ax.get_xticklabels(), rotation=30, ha="right",fontsize=20)
	ax.yaxis.set_visible(False)
	ax.spines[["left", "top", "right"]].set_visible(False)
	ax.margins(y=0.1)
	st.pyplot(fig)
   