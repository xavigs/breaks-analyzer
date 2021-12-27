Breaks Analyzer
=================

![](https://img.shields.io/github/last-commit/xavigs/breaks-analyzer.svg) [![license: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) ![](https://img.shields.io/github/repo-size/xavigs/breaks-analyzer.svg?colorB=orange) [![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif)](https://paypal.me/xavigs84)

Scrapper that extracts all daily tennis matches, and analyse them to predict the probability in the "First Set Player To Break Serve" market. 

* [1. Features](#block1)
* [2. Project schema](#block2)
* [3. Technologies](#block3)
* [4. License](#block4)
* [5. Author](#block5)

---

<a name="block1"></a>
## 1. Features

- Web scrapers to get all data.
- Data analysis from February 2020.
- Multiple formulas are analized every month.
- A neural network is being trained and improved permanently.

---

<a name="block2"></a>
## 2. Project schema

The analysis to find a profitable formula for the "First Set Player To Break Serve" market is composed of several phases.

This is the flow chart that describes the whole process.

![Break analysis schema](assets/img/project-schema.png)

---

<a name="block3"></a>
## 3. Technologies

- Python 2.7
  - Click library *(Parameter control)*
  - BeautifulSoup library *(Web scrapers)*
  - PyCURL library *(Flash Score JSON access)*

- BetsAPI, from RapidAPI *(Bet365 access)*

---

<a name="block4"></a>
## 4. License

MIT License

Copyright (c) 2021 Xavi Garcia i Sunyer

---

<a name="block5"></a>
## 5. Author

Xavi G. Sunyer
 - <xaviergs1984@gmail.com>
 - https://www.linkedin.com/in/xavi-garcia-i-sunyer-12039520/
