# -*- coding: utf-8 -*-
import sys
from datetime import date, datetime, timedelta
import openpyxl
import json
import click
from utils import *
from models import db, objects

dbConnection = db.Database()
breaksDB = dbConnection.connect()
systemsObj = objects.Systems(breaksDB)

@click.command()
@click.option(
    '-s', '--system',
    help = "System to get games", type = str, default = "New Age IV", show_default = True
)
@click.option(
    '-m', '--month',
    help = "Month to get system games", type = str, default = date.today().strftime("%Y-%m"), show_default = True
)

def printGamesBySystem(system, month):
    # Get system data
    with open("parameters.json") as content:
        parameters = json.load(content)

    systemName = system
    period = next(item for item in parameters['periods'] if item['keyword'] == month)
    firstRow = period['first-row']
    lastRow = period['last-row']

    for systemJSON in parameters['systems']:
        if systemName in systemJSON['name']:
            system = systemJSON
            break

    # Open Workbook
    workbook = openpyxl.load_workbook(filename = "Breaks 1r set.xlsx", read_only = True)

    # Get Sheet Object by names
    sheet = workbook['Break']

    for row in sheet.iter_rows(min_row = firstRow, max_row = lastRow):
        rowNumber = row[0].row

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
                    print(game)

if __name__ == '__main__':
    printGamesBySystem()
