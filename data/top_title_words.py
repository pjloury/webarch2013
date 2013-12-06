"""Find Vroots with more than 400 visits.

This program will take a CSV data file and output tab-seperated lines of

    Vroot -> number of visits

To run:

    python top_pages.py anonymous-msweb.data

To store output:

    python top_pages.py anonymous-msweb.data > top_pages.out
"""

import operator
from mrjob.job import MRJob
from combine_user_visits import csv_readline

liz = []

class TopPages(MRJob):
    dic = {}
    def mapper_get_words(self, _, line):
        """Extracts the Vroot that was visited"""
        cell = csv_readline(line)
        if cell[0] == 'A':
	  title = cell[3]
          for word in title.split(" "):
	    yield (word.lower(), 1)

    def combiner_pj(self, keys, values):
	yield "Top 10", [sum(values), keys]


    def reducer_final(self, keys, values):
	for word in values:
 	    liz.append(word)

	liz.sort()
	liz.reverse()

        for entry in liz:
            yield entry

    def steps(self):
        return [
            self.mr(mapper=self.mapper_get_words,
                    combiner=self.combiner_pj,
		    reducer=self.reducer_final)
            
   #		    reducer=self.reducer_sonali)
   #                ,reducer=self.reducer_count_words),

         #   self.mr(mapper=self.mapper_sonali,
         #           reducer=self.reducer_sonali
	 #   )
      ]
     


def returnTop():
    sorted_d = sorted(TopPages.dic.iteritems(), key=operator.itemgetter(1))
    print sorted_d

def returnTop10():
    for w in sorted(TopPages.dic, key=TopPages.dic.get, reverse = True):
      print w, TopPages.dic[w]
    """    
        yield user, total
                # What  Key, Value  do we want to output?
    """ 
if __name__ == '__main__':
    #test2()
    a = TopPages()
   # a.test(None,None)

    a.run()
    #TopPages.returnTop()
    #TopPages.test()
    #test2()
