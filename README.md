# fund-indicators

[![License](https://img.shields.io/github/license/andrewkdinh/fund-indicators.svg)](https://raw.githubusercontent.com/andrewkdinh/fund-indicators/master/LICENSE)
[![Latest Commits](https://img.shields.io/github/last-commit/andrewkdinh/fund-indicators.svg)](https://github.com/andrewkdinh/fund-indicators/commits/master)
![](https://img.shields.io/github/languages/top/andrewkdinh/fund-indicators.svg)
![](https://img.shields.io/github/languages/code-size/andrewkdinh/fund-indicators.svg)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/2667/badge)](https://bestpractices.coreinfrastructure.org/projects/2667)

A project to determine relationships between mutual fund performance and different factors.

[![asciicast demo](https://asciinema.org/a/jLmZapnMFGCRiiSUITY21erLW.svg)](https://asciinema.org/a/jLmZapnMFGCRiiSUITY21erLW?autoplay=1&preload=1)

Calculates relationships between: Previous performance, Alpha, Sharpe Ratio, Sortino Ratio

and Expense ratios, Turnover, Market Capitalization (Asset Size), Persistence

Give it a try at [repl.run](https://fund-indicators.andrewkdinh.repl.run) or [repl.it](https://repl.it/@andrewkdinh/fund-indicators).

## Key Features

- 100% automated
- Uses multiple API's in the case another fails
- Caches http requests for future runs
- Scrapes data from Yahoo Finance
- Color-coded for easy viewing
- Optional graphs to easily visualize linear regression results
- A new joke every time
- Cross-platform (tested on Windows and Linux)

## Quickstart

```shell
git clone https://github.com/andrewkdinh/fund-indicators.git && cd fund-indicators
pip install -r requirements.txt
python main.py
```

- Common mutual funds are listed in `stocks.txt`
- Configure and rename `config.example.json` to `config.json` if you would like to skip beginning questions (only for advanced users)

### Contributing

Want to help? Great! Check out the [CONTRIBUTING.md](https://github.com/andrewkdinh/fund-indicators/blob/master/CONTRIBUTING.md) file!

## Credits

This project utilizes a wide variety of open-source projects:

- [NumPy](https://github.com/numpy/numpy), [Termcolor](https://github.com/hfeeki/termcolor), [Beautiful Soup](https://launchpad.net/beautifulsoup), [yahoofinancials](https://github.com/JECSand/yahoofinancials), [requests-cache](https://github.com/reclosedev/requests-cache), [halo](https://github.com/manrajgrover/halo), [matplotlib](https://github.com/matplotlib/matplotlib), [asciinema](https://github.com/asciinema/asciinema)

And thank you to those that have helped me with the idea and product:

- Amber Bruce, [Alex Stoykov](http://stoykov.us/), Doug Achterman, [Stack Overflow](https://stackoverflow.com)

Licensed under [GPL-3.0](https://raw.githubusercontent.com/andrewkdinh/fund-indicators/master/LICENSE) | Copyright (C) 2019  Andrew Dinh
