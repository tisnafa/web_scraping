from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('div',attrs={'class':'table-responsive'})
row = table.find_all('tr')

row_length = len(row)

temp = [] #initiating a list 

for i in range(0, row_length):
#insert the scrapping process here
    
    #get period 
    period = table.find_all('td')[i*4].text

    #get period 
    rate = table.find_all('a')[i*2].text

    temp.append((period,rate)) 

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('period','rate'))

#insert data wrangling here
df['rate'] = df['rate'].str.replace(",","")
df['rate'] = df['rate'].astype('float64')
df['period'] = df['period'].astype('datetime64')
df = df.set_index('period')
#end of data wranggling 
df2 = df.copy()
df2 = df2.reset_index()
df2['month'] = df2['period'].dt.to_period('M')

@app.route("/")
def index(): 
	
	card_data = f'{round(df.mean()[0],2)}' #be careful with the " and ' 

	# generate plot
	ax = df.plot(figsize = (20,9)) 
	

	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	
	# generate plot
	ax2 = df2[['month','rate']].groupby(by = 'month').mean().plot(kind="bar",figsize = (20,9))
	plt.ylim((13500,14600))
	
	# Rendering plot
	# Do not change this
	figfile2 = BytesIO()
	plt.savefig(figfile2, format='png', transparent=True)
	figfile2.seek(0)
	figdata_png2 = base64.b64encode(figfile2.getvalue())
	plot_result2 = str(figdata_png2)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result, 
		plot_result2=plot_result2
		)


if __name__ == "__main__": 
    app.run(debug=True)