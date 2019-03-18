# fund-indicators

[![License](https://img.shields.io/github/license/andrewkdinh/fund-indicators.svg)](https://raw.githubusercontent.com/andrewkdinh/fund-indicators/master/LICENSE)
[![](https://img.shields.io/github/last-commit/andrewkdinh/fund-indicators.svg)](https://github.com/andrewkdinh/fund-indicators/commits/master)
![](https://img.shields.io/github/languages/top/andrewkdinh/fund-indicators.svg)
![](https://img.shields.io/github/languages/code-size/andrewkdinh/fund-indicators.svg)

A project to determine relationships between mutual funds and different factors. 

Calculates relationships between: Previous performance, Alpha, Sharpe Ratio, Sortino Ratio

and Expense ratios, Turnover, Market Capitalization (Asset Size), Persistence

Give it a try at [repl.run](https://fund-indicators.andrewkdinh.repl.run) or [repl.it](https://repl.it/@andrewkdinh/fund-indicators)

## Key Features

- 100% automated
- Uses multiple API's in case another fails
- Caches http requests for future runs
- Scrapes data from Yahoo Finance
- Color-coded for easy viewing
- Optional graphs to easily visualize linear regression results
- A new joke every time it runs

## Quickstart

```shell
pip install -r requirements.txt
python main.py
```

Pre-chosen stocks listed in `stocks.txt`

## Credits

This project uses a wide variety of open-source projects

- [NumPy](https://github.com/numpy/numpy), [Termcolor](https://github.com/hfeeki/termcolor), [Beautiful Soup](https://launchpad.net/beautifulsoup), [yahoofinancials](https://github.com/JECSand/yahoofinancials), [requests-cache](https://github.com/reclosedev/requests-cache), [halo](https://github.com/manrajgrover/halo)

And thank you to those that have helped me with the idea and product:

- Amber Bruce, [Alex Stoykov](http://stoykov.us/), Doug Achterman, [Stack Overflow](https://stackoverflow.com)

Created by Andrew Dinh from Dr. TJ Owens Gilroy Early College Academy
