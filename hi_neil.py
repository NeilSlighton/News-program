# hi neil

import newspaper
from newspaper import news_pool
import csv
from langdetect import detect
import time
import pandas as pd
import os






def output_to_csv(paper, output_file_name):
	csv_name = output_file_name + '.csv'
  
	with open(csv_name, 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(['id', 'publish_date', 'url', 'title', 'text'])#, 'keywords'])
		i = 0
	  
		for article in paper.articles:
			
			article.parse()
			#article.nlp()

			try:
				lang = detect(article.title)
			except:
				lang = "error"
				print("This row throws and error:", article.title)

		
			text_length = len(article.text)

			if (lang == 'en' and text_length > 0):
				writer.writerow([i, article.publish_date, article.url, article.title, article.text])#, article.keywords])
				i += 1

def remove_duplicates(output_file_name):
	csv_name = output_file_name + '.csv'
	csv_name_output = output_file_name + '_dupeless.csv'

	df = pd.read_csv(csv_name, sep=",", engine='python')

	df.drop_duplicates(subset=['title'], inplace=True)

	# Write the results to a different file
	df.to_csv(csv_name_output, index=False)
	# os.remove(csv_name)



def get_articles_mt():
	start_time = time.time()
	cnn = newspaper.build('http://www.cnn.com', language='en', memoize_articles=False, fetch_images=False)
	bbc = newspaper.build('http://www.bbc.com', language='en', memoize_articles=False, fetch_images=False)
	fox = newspaper.build('http://www.foxnews.com', language='en', memoize_articles=False, fetch_images=False)
	nyt = newspaper.build('http://www.nytimes.com', language='en', memoize_articles=False, fetch_images=False)
	nbc = newspaper.build('http://www.nbcnews.com', language='en', memoize_articles=False, fetch_images=False)
	atlantic = newspaper.build('http://www.theatlantic.com', language='en', memoize_articles=False, fetch_images=False)
	breitbart = newspaper.build('http://www.breitbart.com', language='en', memoize_articles=False, fetch_images=False)
	usatoday = newspaper.build('http://www.usatoday.com', language='en', memoize_articles=False, fetch_images=False)

	papers = [cnn, bbc, fox, nyt, nbc, atlantic, breitbart, usatoday]
	names = ['cnn', 'bbc', 'fox', 'nyt', 'nbc', 'atlantic', 'breitbart', 'usatoday']
	news_pool.set(papers, threads_per_source=2)
	news_pool.join()

	for i in range(len(papers)):
		paper = papers[i]
		name = names[i]
		output_to_csv(paper, name)
		print("{} done!".format(name))
	
	for i in range(len(names)):
		name = names[i]
		remove_duplicates(name)

	print("all done!")
	end_time = time.time()
	print("it took this long to run: {}".format(end_time-start_time))
  

if __name__ == '__main__':
	get_articles_mt()
