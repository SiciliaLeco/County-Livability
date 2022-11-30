import csv
from typing import List, Tuple
from operator import attrgetter


class county(object):
    def __init__(self, info: dict):
        """
        county_name	State	county formatted	crime_rate_per_100000	PCTPOVALL_2020	diversity index	noaa/temp-jan	noaa/temp-apr	noaa/temp-jul	noaa/temp-oct	edu/some-college	bls/2020/unemployed	life-expectancy	population/2019	avg_income	poverty-rate	Unemployment_rate	cost-of-living/living_wage	cost-of-living/food_costs	cost-of-living/medical_costs	cost-of-living/housing_costs	cost-of-living/tax_costs
        """
        self.countyName = info['county formatted']
        self.state = info['State']
        self.crime_rate = info['crime_rate_per_100000']
        self.diversityIndex = info['diversity index']
        self.springTemperature = info['noaa/temp-jan']
        self.summerTemperature = info['noaa/temp-apr']
        self.autumnTemperature = info['noaa/temp-jul']
        self.winterTemperature = info['noaa/temp-oct']
        self.population = info['population/2019']
        self.lifeExpectancy = info['life-expectancy']
        self.education = info['edu/some-college']
        self.averageIncome = info['avg_income']
        self.povertyRate = info['poverty-rate']
        self.unemploymentRate = info['Unemployment_rate']
        self.livingWage = info['cost-of-living/living_wage']
        self.foodCost = info['cost-of-living/food_costs']
        self.medicalCost = info['cost-of-living/medical_costs']
        self.housingCost = info['cost-of-living/housing_costs']
        self.taxCost = info['cost-of-living/housing_costs']

    def __str__(self):
        return self.countyName


def sortCounty(countyList: List[county], returnNumber:int, *attributes):
    print(attributes)
    countyList.sort(key=attrgetter(*attributes), reverse=True)
    return countyList[:returnNumber]


def readFile(path: str = "DATA/dataset_livability.csv") -> List[county]:
    countyList = []
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for line in reader:
            countyList.append(county(line))
    return countyList


if __name__ == "__main__":
    file = "../../DATA/dataset_livability.csv"
    countyList = readFile(file)
    print()
