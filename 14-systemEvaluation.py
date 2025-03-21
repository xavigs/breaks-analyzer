# -*- coding: utf-8 -*-
import sys
from datetime import date, datetime
import openpyxl
import json
import numpy as np
import matplotlib.pyplot as plt
from calendar import monthrange
from colorama import init, Back, Fore, Style
from utils import *
from models import db, objects

dbConnection = db.Database()
breaksDB = dbConnection.connect()
systemsObj = objects.Systems(breaksDB)

init(autoreset = True)
with open("parameters.json") as content:
    parameters = json.load(content)

# Variables
SYSTEMS_TO_SHOW = (
    "Sistema Experimental V",
    "Sistema Experimental VI",
    "Sistema Experimental VII",
    "Sistema Experimental VIII",
    "Sistema Experimental XIII",
    "Sistema Experimental XIV",
    "Sistema Experimental XV",
    "Sistema Experimental XVI",
    "Sistema New Age I",
    "Sistema New Age II",
    "Sistema New Age III",
    "Sistema New Age IV"
)
systems = {}
results = {}

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

        if date.today().strftime("%Y-%m") == startDateDT.strftime("%Y-%m"):
            systemMonthPct = round((currentDay - firstSystemDay + 1.0) / numDaysSystemMonth, 1)
        else:
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
        systems[system['name']]['25'] = "?"
        systems[system['name']]['50'] = "?"
        systems[system['name']]['75'] = "?"
        systems[system['name']]['100'] = "?"
        systems[system['name']]['150'] = "?"
        systems[system['name']]['200'] = "?"
        systems[system['name']]['250'] = "?"
        systems[system['name']]['300'] = "?"
        systems[system['name']]['350'] = "?"
        systems[system['name']]['400'] = "?"
        systems[system['name']]['450'] = "?"
        systems[system['name']]['500'] = "?"
        systems[system['name']]['550'] = "?"
        systems[system['name']]['600'] = "?"
        systems[system['name']]['650'] = "?"
        systems[system['name']]['700'] = "?"

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
workbook = openpyxl.load_workbook(filename = "Breaks 1r set.xlsx", read_only = True, data_only=True)

# Get Sheet Object by names
sheet = workbook['Break']

for row in sheet.iter_rows(min_row = 4, max_row = parameters['last-row']):
    rowNumber = row[0].row
    print("Reading the row nº {}...".format(rowNumber))

    if row[0].value is not None:
        date = row[0].value

    if not rowNumber in parameters['jump']:
        valid = True

        for criteria in parameters['dismiss']:
            column = ord(criteria['col']) - 65

            if criteria['operator'] == "=":
                if row[column].value == criteria['value']:
                    valid = False
                    break
                elif criteria['operator'] == "<":
                    if row[column].value < criteria['value']:
                        valid = False
                        break
                elif criteria['operator'] == ">":
                    if row[column].value > criteria['value']:
                        valid = False
                        break
                elif criteria['operator'] == ">=":
                    if row[column].value >= criteria['value']:
                        valid = False
                        break
                elif criteria['operator'] == "<>":
                    if row[column].value != criteria['value']:
                        valid = False
                        break

        if valid:
            found = False

            for system in parameters['systems']:
                if "future" in system and rowNumber >= system['future']:
                    validForSystem = False

                    for conditionGroup in system['conditions']:
                        numConditions = len(conditionGroup)
                        satisfiedConditions = 0

                        for condition in conditionGroup:
                            column = ord(condition['col']) - 65

                            if condition['operator'] == "=":
                                if row[column].value == condition['value']:
                                    satisfiedConditions += 1
                            elif condition['operator'] == "<":
                                if row[column].value < condition['value']:
                                    satisfiedConditions += 1
                            elif condition['operator'] == ">":
                                if row[column].value > condition['value']:
                                    satisfiedConditions += 1
                            elif condition['operator'] == ">=":
                                if row[column].value >= condition['value']:
                                    satisfiedConditions += 1
                            elif condition['operator'] == "<>":
                                if row[column].value != condition['value']:
                                    satisfiedConditions += 1

                        if numConditions == satisfiedConditions:
                            validForSystem = True
                            break

                    if validForSystem:
                        game = {}
                        game['date'] = date
                        game['player'] = row[4].value
                        game['opponent'] = row[5].value
                        game['odd'] = row[10].value
                        game['result'] = row[14].value

                        # Balance
                        if row[14].value == "L":
                            balance = -1
                        elif row[14].value == "N":
                            balance = 0
                        else:
                            balance = game['odd'] - 1

                        systems[system['name']]['units'] += balance
                        systems[system['name']]['num-picks'] += 1
                        systems[system['name']]['yield'] = round(systems[system['name']]['units'] * 100 / systems[system['name']]['num-picks'], 2)

                        if systems[system['name']]['num-picks'] == 25:
                            systems[system['name']]['25'] = systems[system['name']]['yield']
                        elif systems[system['name']]['num-picks'] == 50:
                            systems[system['name']]['50'] = systems[system['name']]['yield']
                        elif systems[system['name']]['num-picks'] == 75:
                            systems[system['name']]['75'] = systems[system['name']]['yield']
                        elif systems[system['name']]['num-picks'] == 100:
                            systems[system['name']]['100'] = systems[system['name']]['yield']
                        elif systems[system['name']]['num-picks'] == 150:
                            systems[system['name']]['150'] = systems[system['name']]['yield']
                        elif systems[system['name']]['num-picks'] == 200:
                            systems[system['name']]['200'] = systems[system['name']]['yield']
                        elif systems[system['name']]['num-picks'] == 250:
                            systems[system['name']]['250'] = systems[system['name']]['yield']
                        elif systems[system['name']]['num-picks'] == 300:
                            systems[system['name']]['300'] = systems[system['name']]['yield']
                        elif systems[system['name']]['num-picks'] == 350:
                            systems[system['name']]['350'] = systems[system['name']]['yield']
                        elif systems[system['name']]['num-picks'] == 400:
                            systems[system['name']]['400'] = systems[system['name']]['yield']
                        elif systems[system['name']]['num-picks'] == 450:
                            systems[system['name']]['450'] = systems[system['name']]['yield']
                        elif systems[system['name']]['num-picks'] == 500:
                            systems[system['name']]['500'] = systems[system['name']]['yield']
                        elif systems[system['name']]['num-picks'] == 550:
                            systems[system['name']]['550'] = systems[system['name']]['yield']
                        elif systems[system['name']]['num-picks'] == 600:
                            systems[system['name']]['600'] = systems[system['name']]['yield']
                        elif systems[system['name']]['num-picks'] == 650:
                            systems[system['name']]['650'] = systems[system['name']]['yield']
                        elif systems[system['name']]['num-picks'] == 700:
                            systems[system['name']]['700'] = systems[system['name']]['yield']

                        for period in parameters['periods']:
                            if rowNumber >= period['first-row'] and rowNumber <= period['last-row']:
                                systems[system['name']]['periods'][period['keyword']]['units'] += balance
                                systems[system['name']]['periods'][period['keyword']]['num-picks'] += 1
                                systems[system['name']]['periods'][period['keyword']]['yield'] = round(systems[system['name']]['periods'][period['keyword']]['units'] * 100 / systems[system['name']]['periods'][period['keyword']]['num-picks'], 2)

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        origSystemName = systemName
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

        if systemData['total-months'] == 0:
            positiveEval = 0
            plusEval = 0
            monthlyPicks = 0
        else:
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

        results[systemName] = [positiveEval * 4, yieldEval * 3, plusEval * 2, picksEval]
        print("\t* Mesos totals: " + str(systemData['total-months']))
        print("\t* Mesos positius: {} ({})".format(positiveMonths, positiveEval))
        print("\t* Mesos amb més del 10% de yield: {} ({})".format(plusMonths, plusEval))
        print("\t* Picks mensuals: {} ({})".format(monthlyPicks, picksEval))
        print("\t* Avaluació del sistema: {}{}{}".format(Style.BRIGHT, evalColor, evaluation))

        # UPDATE DATABASE
        systemName = origSystemName.replace("Sistema ", "").replace("Experimental", "Exp.").split("-")[1]
        if systemName.isnumeric():
            systemName = "Sist. {}".format(systemName)

        systemsObj.update({'num-months': systemData['total-months'], 'positive-months': positiveMonths, '10plus-months': plusMonths}, [{'name': systemName}])

print("\n~~ Intervals ~~\n")
sys.stdout.write("------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n| Nº picks |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + systemName + " |")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    25    |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['25']) + " %")
            leftChars = len(systemName) - len(str(systemData['25']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    50    |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['50']) + " %")
            leftChars = len(systemName) - len(str(systemData['50']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    75    |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['75']) + " %")
            leftChars = len(systemName) - len(str(systemData['75']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    100   |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['100']) + " %")
            leftChars = len(systemName) - len(str(systemData['100']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    150   |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['150']) + " %")
            leftChars = len(systemName) - len(str(systemData['150']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    200   |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['200']) + " %")
            leftChars = len(systemName) - len(str(systemData['200']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    250   |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['250']) + " %")
            leftChars = len(systemName) - len(str(systemData['250']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    300   |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['300']) + " %")
            leftChars = len(systemName) - len(str(systemData['300']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    350   |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['350']) + " %")
            leftChars = len(systemName) - len(str(systemData['350']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    400   |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['400']) + " %")
            leftChars = len(systemName) - len(str(systemData['400']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    450   |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['450']) + " %")
            leftChars = len(systemName) - len(str(systemData['450']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    500   |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['500']) + " %")
            leftChars = len(systemName) - len(str(systemData['500']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    550   |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['550']) + " %")
            leftChars = len(systemName) - len(str(systemData['550']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    600   |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['600']) + " %")
            leftChars = len(systemName) - len(str(systemData['600']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    650   |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['650']) + " %")
            leftChars = len(systemName) - len(str(systemData['650']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    700   |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['700']) + " %")
            leftChars = len(systemName) - len(str(systemData['700']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")
sys.stdout.write("\n")

'''
    MATPLOTLIB VISUALIZATION DATA
'''

def survey(results, category_names):
    """
    Parameters
    ----------
    results : dict
        A mapping from question labels to a list of answers per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*.
    category_names : list of str
        The category labels.
    """
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    '''category_colors = plt.colormaps['RdYlGn'](
        np.linspace(0.15, 0.85, data.shape[1]))'''
    category_colors = plt.cm.get_cmap('RdYlGn')(
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                        label=colname, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        #ax.bar_label(rects, label_type='center', color=text_color)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')

    return fig, ax

category_names = ['Positive months', 'Yield',
                  'Plus 10% months', 'Monthly picks']
survey(results, category_names)
plt.show()
