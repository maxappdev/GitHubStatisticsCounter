import statisticsCounter

URL = 'https://github.com/andreaskosten/php_examples/commit/19c5500941ec544128962b29ffe6da9eb0ad07d1'

statistics = statisticsCounter.countStatistics(URL) 

if statistics:
  print(statistics)