import plotly.express as px
import streamlit as st

class Graphics():
    def __init__(self, df):
        self.df = df
        self.totals = df.groupby(by='year_month').sum().drop(labels='line', axis=1).loc[:,'total']

    def metrics_graph(self, metric, colors):
        return st.plotly_chart(px.line(self.df.reset_index(), x='year_month', y=metric, color='line', color_discrete_sequence=colors, title=f'Passengers transforted by line - {metric.capitalize()}'))


    def participation_measurement(self, line):
        line_sum = self.df[self.df.loc[:,'line'] == line].loc[:,'total']
        participation_line = (line_sum / self.totals) * 100
        
        return st.plotly_chart(px.line({'Date': participation_line.index,'%': participation_line}, x='Date', y='%', title=f'Monthly participation in total of demand (in %) - Line {line}'))

    def most_participation(self):
        line_01_sum = self.df[self.df.loc[:,'line'] == 1].loc[:,'total']
        line_03_sum = self.df[self.df.loc[:,'line'] == 3].loc[:,'total']
        participation_line1_line2 = ((line_01_sum + line_03_sum) / self.totals) * 100

        return st.plotly_chart(px.line({'Date':participation_line1_line2.index, '%':participation_line1_line2}, x='Date', y='%'))
