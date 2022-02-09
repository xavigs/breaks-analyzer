# -*- coding: utf-8 -*-
from datetime import date
import click
from utils import *
import tennisExplorer
from models import db, objects

@click.command()
@click.option(
    '-s', '--sex',
    help = "Sex category to get tournaments from", type = str, default = "M", show_default = True
)
@click.option(
    '-y', '--year',
    help = "Year to get tournaments from", type = str, default = date.today().year, show_default = True
)

def getYearlyTournaments(sex, year):
    tournaments = tennisExplorer.getTournaments(sex, year)
    printCollection(tournaments)

if __name__ == '__main__':
    getYearlyTournaments()