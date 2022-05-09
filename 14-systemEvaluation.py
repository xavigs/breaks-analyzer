# -*- coding: utf-8 -*-
from datetime import date, datetime
import openpyxl
import json
from calendar import monthrange
from colorama import init, Back, Fore, Style
from utils import *

init(autoreset = True)
with open("parameters.json") as content:
    parameters = json.load(content)

# Variables
systems = {}

currentMonth = date.today().strftime('%Y-%m')
numDaysCurrentMonth = float(monthrange(date.today().year, date.today().month)[1])
currentDay = float(date.today().day)
currentMonthPct = round(currentDay / numDaysCurrentMonth, 1)

for system in parameters['systems']:
    if "Sistema" in system['name']:
        firstRow = system['future']
        startDate = system['start-date']
        startDateDT = datetime.strptime(startDate, "%Y-%m-%d")
        numDaysSystemMonth = float(monthrange(startDateDT.year, startDateDT.month)[1])
        firstSystemDay = float(startDateDT.day)
        systemMonthPct = round((numDaysSystemMonth - firstSystemDay + 1.0) / numDaysSystemMonth, 1)

        systems[system['name']] = {}
        systems[system['name']]['start-date'] = startDate
        systems[system['name']]['total-months'] = 0
        systems[system['name']]['units'] = 0.0
        systems[system['name']]['num-picks'] = 0
        systems[system['name']]['yield'] = 0.0
        systems[system['name']]['positive-months'] = 0
        systems[system['name']]['10plus-months'] = 0
        systems[system['name']]['periods'] = {}

        for period in parameters['periods']:
            systems[system['name']]['periods'][period['keyword']] = {}
            systems[system['name']]['periods'][period['keyword']]['name'] = period['name']
            systems[system['name']]['periods'][period['keyword']]['type'] = period['type']
            systems[system['name']]['periods'][period['keyword']]['units'] = 0.0
            systems[system['name']]['periods'][period['keyword']]['num-picks'] = 0

            if period['type'] == 1 and period['first-row'] >= firstRow:
                if period['keyword'] == currentMonth:
                    systems[system['name']]['periods'][period['keyword']]['month-portion'] = currentMonthPct
                    systems[system['name']]['total-months'] += currentMonthPct
                else:
                    systems[system['name']]['periods'][period['keyword']]['month-portion'] = 1
                    systems[system['name']]['total-months'] += 1
            elif period['last-row'] > firstRow:
                systems[system['name']]['periods'][period['keyword']]['month-portion'] = systemMonthPct
                systems[system['name']]['total-months'] += systemMonthPct

# Open Workbook
workbook = openpyxl.load_workbook(filename = "Breaks 1r set.xlsx", data_only = True)

# Get Sheet Object by names
sheet = workbook['Break']

for row in range(4, parameters['last-row'] + 1):
    if sheet['A' + str(row)].value is not None:
        date = sheet['A' + str(row)].value

    if not row in parameters['jump']:
        valid = True

        if valid:
            found = False

            for system in parameters['systems']:
                if "future" in system and row >= system['future']:
                    validForSystem = False

                    for conditionGroup in system['conditions']:
                        numConditions = len(conditionGroup)
                        satisfiedConditions = 0

                        for condition in conditionGroup:
                            if condition['operator'] == "=":
                                if sheet[condition['col'] + str(row)].value == condition['value']:
                                    satisfiedConditions += 1
                            elif condition['operator'] == "<":
                                if sheet[condition['col'] + str(row)].value < condition['value']:
                                    satisfiedConditions += 1
                            elif condition['operator'] == ">":
                                if sheet[condition['col'] + str(row)].value > condition['value']:
                                    satisfiedConditions += 1
                            elif condition['operator'] == ">=":
                                if sheet[condition['col'] + str(row)].value >= condition['value']:
                                    satisfiedConditions += 1
                            elif condition['operator'] == "<>":
                                if sheet[condition['col'] + str(row)].value != condition['value']:
                                    satisfiedConditions += 1

                        if numConditions == satisfiedConditions:
                            validForSystem = True
                            break

                    if validForSystem:
                        game = {}
                        game['date'] = date
                        game['player'] = sheet['E' + str(row)].value
                        game['opponent'] = sheet['F' + str(row)].value
                        game['odd'] = sheet['K' + str(row)].value
                        game['result'] = sheet['O' + str(row)].value

                        # Balance
                        if sheet['O' + str(row)].value == "L":
                            balance = -1
                        elif sheet['O' + str(row)].value == "N":
                            balance = 0
                        else:
                            balance = game['odd'] - 1

                        systems[system['name']]['units'] += balance
                        systems[system['name']]['num-picks'] += 1
                        systems[system['name']]['yield'] = round(systems[system['name']]['units'] * 100 / systems[system['name']]['num-picks'], 2)

                        for period in parameters['periods']:
                            if row >= period['first-row'] and row <= period['last-row']:
                                systems[system['name']]['periods'][period['keyword']]['units'] += balance
                                systems[system['name']]['periods'][period['keyword']]['num-picks'] += 1
                                systems[system['name']]['periods'][period['keyword']]['yield'] = round(systems[system['name']]['periods'][period['keyword']]['units'] * 100 / systems[system['name']]['periods'][period['keyword']]['num-picks'], 2)

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        yieldEval = round(systemData['yield'] > 20 and 1 or systemData['yield'] / 20, 2)
        print("\n~~ " + systemName + " ~~\n")
        print("\t* Unitats: " + str(round(systemData['units'],2)) + " uts.")
        print("\t* Nº picks: " + str(systemData['num-picks']))
        print("\t* Yield: {}% ({})".format(systemData['yield'], yieldEval))
        positiveMonths = 0.0
        plusMonths = 0.0

        for period in systemData['periods']:
            if systemData['periods'][period]['type'] == 1 and systemData['periods'][period]['units'] > 0:
                positiveMonths += systemData['periods'][period]['month-portion']

                if systemData['periods'][period]['yield'] >= 10:
                    plusMonths += systemData['periods'][period]['month-portion']

        positiveEval = round(positiveMonths / float(systemData['total-months']), 2)
        plusEval = round(plusMonths / float(systemData['total-months']), 2)
        monthlyPicks = round(systemData['num-picks'] / systemData['total-months'], 2)
        picksEval = round(monthlyPicks > 20 and 1 or monthlyPicks / 20, 2)
        evaluation = round(positiveEval * 4 + yieldEval * 3 + plusEval * 2 + picksEval, 1)

        if evaluation >= 9.0:
            evalColor = Fore.GREEN
        elif evaluation >= 7.0:
            evalColor = Fore.BLUE
        elif evaluation >= 5.0:
            evalColor = Fore.YELLOW
        else:
            evalColor = Fore.RED

        print("\t* Mesos totals: " + str(systemData['total-months']))
        print("\t* Mesos positius: {} ({})".format(positiveMonths, positiveEval))
        print("\t* Mesos amb més del 10% de yield: {} ({})".format(plusMonths, plusEval))
        print("\t* Picks mensuals: {} ({})".format(monthlyPicks, picksEval))
        print("\t* Avaluació del sistema: {}{}{}".format(Style.BRIGHT, evalColor, evaluation))
