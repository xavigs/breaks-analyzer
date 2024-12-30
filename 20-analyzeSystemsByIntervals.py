# -*- coding: utf-8 -*-
import sys
import openpyxl
import json
import click
from utils import *
from models import db, objects

@click.command()
@click.option(
    '-p', '--num-picks',
    help = "Number of picks grouped by", type = int, default = 30, show_default = True
)

def analyzeSystems(num_picks):
    dbConnection = db.Database()
    breaksDB = dbConnection.connect()
    systemsObj = objects.Systems(breaksDB)

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

    for system in parameters['systems']:
        systems[system['name']] = {}
        systems[system['name']]['units'] = 0.0
        systems[system['name']]['num-picks'] = 0
        systems[system['name']]['total-periods'] = 0
        systems[system['name']]['positive-periods'] = 0
        systems[system['name']]['10plus-periods'] = 0
        systems[system['name']]['periods'] = {}
        systems[system['name']]['temp-units'] = 0.0
        systems[system['name']]['temp-num-picks'] = 0

    # Open Workbook
    workbook = openpyxl.load_workbook(filename = "Breaks 1r set.xlsx", read_only = True, data_only = True)

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
                        systems[system['name']]['temp-units'] += balance
                        systems[system['name']]['temp-num-picks'] += 1

                        if systems[system['name']]['num-picks'] % num_picks == 0:
                            periodName = '{}-{}'.format(str(systems[system['name']]['num-picks'] - num_picks + 1).zfill(4), str(systems[system['name']]['num-picks']).zfill(4))
                            systems[system['name']]['periods'][periodName] = {
                                'units': systems[system['name']]['temp-units'],
                                'num-picks': systems[system['name']]['temp-num-picks'],
                                'yield': round(systems[system['name']]['temp-units'] * 100 / systems[system['name']]['temp-num-picks'], 2)
                            }
                            systems[system['name']]['total-periods'] += 1
                            systems[system['name']]['temp-units'] = 0.0
                            systems[system['name']]['temp-num-picks'] = 0

    for systemName, systemData in sorted(systems.items()):
        if "Sistema" in systemName:
            if systems[systemName]['temp-num-picks'] > 0:
                periodName = '{}-{}'.format(str(systems[systemName]['num-picks'] - num_picks + 1).zfill(4), str(systems[systemName]['num-picks']).zfill(4))
                systems[systemName]['periods'][periodName] = {
                    'units': systems[systemName]['temp-units'],
                    'num-picks': systems[systemName]['temp-num-picks'],
                    'yield': round(systems[systemName]['temp-units'] * 100 / systems[systemName]['temp-num-picks'], 2)
                }

            origSystemName = systemName
            systemName = systemName.split("-")[1]
            print("\n~~ " + systemName + " ~~\n")
            print("\t* Unitats: " + str(round(systemData['units'],2)) + " uts.")
            print("\t* Nº picks: " + str(systemData['num-picks']))
            print("\t* Yield: " + str(systemData['yield']) + " %")
            positivePeriods = 0
            plusPeriods = 0

            for period in systemData['periods']:
                if systemData['periods'][period]['units'] > 0 and systemData['periods'][period]['num-picks'] == num_picks:
                    positivePeriods += 1

                    if systemData['periods'][period]['yield'] >= 10:
                        plusPeriods += 1

            print("\t* Períodes totals: {}".format(systemData['total-periods']))
            print("\t* Períodes positius: " + str(positivePeriods))
            print("\t* Períodes amb més del 10% de yield: " + str(plusPeriods))
            print("\t* Picks per període: " + str(round(systemData['num-picks'] / systemData['total-periods'], 2)))
            print("\t* Detall per períodes:\n")
            bank = 100.00
            stake = 2.50

            for periodKeyword, periodData in sorted(systemData['periods'].items()):
                try:
                    profit = round(periodData['units'] * stake, 2)
                    new_bank = bank + profit
                    print("\t\t-> " + periodKeyword + "\t" + str(round(periodData['units'], 2)) + " uts.\t" + str(periodData['num-picks']) + " picks \tYield: " + str(periodData['yield']) + " %\t\tBank final: " + str(new_bank) + u" \u20ac")
                    bank = new_bank
                except Exception as e:
                    print("\t\t-> " + periodKeyword + "\t" + str(round(periodData['units'], 2)) + " uts.\t" + str(periodData['num-picks']) + " picks \tYield: 0.00 %")

            systems[origSystemName]['end-bank'] = bank

if __name__ == '__main__':
    analyzeSystems()
