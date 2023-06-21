from datetime import datetime

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
	
	st.subheader('infrastructure changes - New stations on the São Paulo Subway System - timeline')

	fig, ax = plt.subplots(figsize=(16, 8), layout="constrained")
	ax.set_title('New stations on São Paulo Subway System - Timeline', fontsize=25)

	ax.vlines(list(df.inauguration), 0, levels, color="tab:red")  # The vertical stems.
	ax.plot(list(df.inauguration), np.zeros_like(list(df.inauguration)), "-o",
        color="k", markerfacecolor="w")  # Baseline and markers on it.

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

	#st.markdown('Questions:')
	#st.markdown('**A.** Are there significant changes in the infrastructure of the subway (new station or lines)?')
    
	#st.markdown('**R.** infrastructure changes - New stations in the subway')

	#st.markdown('**B.** Are there significant changes in the infrastructure in the metropolitan transport network?')
        
	#st.markdown('**R.** -------')

	#st.markdown('**C.** What\'s the reason for the increasing in passenger transported demand in lines 5 and 15?')
        
	#st.markdown('**R.** There are a big number of inaugurations of new stations for these lines, it can be a good reason.')
        
	#st.markdown('**D.** What can be caused by participation decreases of demand in lines 1 and 3 ?')
        
	#st.markdown('**R.** -------')

	#st.markdown('**E.** If the main lines are decreasing the demand, is there the possibility ' 
    #     'of other lines taking these positions in the next years?')

	#st.markdown('**R.** Modelling task.')
        
	#st.markdown('**F.** Is this a new pattern or when the subway rescues the level of ' 
    #     'passenger demand near of previous COVID pandemic the old pattern will return?')
        
	#st.markdown('**R.** Modelling task.')
	
