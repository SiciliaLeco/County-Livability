import copy
import csv
from typing import List, Tuple
from operator import attrgetter
import numpy as np
from sklearn.cluster import KMeans
import scipy.stats as st
from sklearn.preprocessing import normalize

class county(object):
    def __init__(self, info: dict, index: int):
        """
        county_name	State	county formatted	crime_rate_per_100000	PCTPOVALL_2020	diversity index	noaa/temp-jan	noaa/temp-apr	noaa/temp-jul	noaa/temp-oct	edu/some-college	bls/2020/unemployed	life-expectancy	population/2019	avg_income	poverty-rate	Unemployment_rate	cost-of-living/living_wage	cost-of-living/food_costs	cost-of-living/medical_costs	cost-of-living/housing_costs	cost-of-living/tax_costs
        """
        self.countyName = " ".join(info['county formatted'].split(" ")[:-1])
        self.state = info['State']
        self.crimeRate = info['crime_rate_per_100000'].split(".")[0]
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
        self.html = "/searchResult/?selectCounty={}".format(str(index))

    def __str__(self):
        return self.countyName


def sortCounty(countyList: List[county], returnNumber: int, *attributes):
    print(attributes)
    c = copy.deepcopy(countyList)
    resDict = {countyList[i].countyName: i for i in range(len(countyList))}

    c.sort(key=attrgetter(*attributes), reverse=True)
    returnDict = dict()
    for i in range(returnNumber):
        returnDict[c[i].countyName] = resDict[c[i].countyName]
    return returnDict


def clusterCounty(countyList: List[county], targetCounty: int, returnNumber:int, *attributes):
    def distance(x, y):
        return np.linalg.norm(x-y)

    X = []
    for county in countyList:
        res = []
        for attr in attributes:
            res.append(float(getattr(county, attr)))
        X.append(res)
    X = np.array(X)
    X = normalize(X.T).T
    res = KMeans(n_clusters=60, random_state=0).fit_predict(X)
    targetLabel = res[targetCounty]
    result = list()
    dists = []
    for i in range(len(countyList)):
        if res[i] == targetLabel and i != targetCounty:
            dists.append(distance(X[i], X[targetCounty]))
            result.append([countyList[i]])
            # result.append([countyList[i], distance(X[i], X[targetCounty])])
    dists = normalize(np.array([dists]))
    result = [result[i]+[dists[0][i]*100] for i in range(len(result))]
    result = sorted(result, key=lambda x:x[1], reverse=False)
    return result[:returnNumber]


def readFile(path: str = "DATA/dataset_livability.csv") -> List[county]:
    """
    the default path of this function is for pyhton files outside this directory
    :param path:
    :return:
    """
    countyList = []
    index = 0
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for line in reader:
            countyList.append(county(line, index))
            index += 1
    return countyList


if __name__ == "__main__":
    file = "../../DATA/dataset_livability.csv"
    countyList = readFile(file)
    result = clusterCounty(countyList, 1, "crime_rate", "diversityIndex")
    # print()
    for r in result:
        print(r)
