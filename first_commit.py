from enum import Enum


BASIC_LARGE_HOUSE_COST = 1155 + 2.10*7*7 + 12
BASIC_SMALL_HOUSE_COST = 630 + 70
APARTMENT_CLEANING_COSTS = 60 + 30 # cleaning for small + large apartment
DAILY_ADDITIONAL_BED_COST_PER_PERSON = 10
DAILY_LODGING_TAX_PER_PERSON = 2.10
EXTRA_NIGHT_COST = 0


class payable(Enum):
    lodgingTax = 1
    extraBed = 2
    extraNight = 3


class groceries(Enum):
    groceries109 = 4
    groceries43 = 5
    groceries75 = 6
    groceries12 = 7
    groceries29 = 8
    groceries19 = 9
    groceries315 = 10


GROCERIES = { groceries.groceries109 : 109.26,
              groceries.groceries43  : 43.46,
              groceries.groceries75  : 75,
              groceries.groceries12  : 12,
              groceries.groceries29  : 29.30,
              groceries.groceries19  : 19.38,
              groceries.groceries315 : 315.40 }


def reportExpenses(basicLargeHouseCost, basicSmallHouseCost, apartmentCleaningCosts,
                   configLabel, lodgingConfig, dailyAdditionalBedCostPerPerson, lodgingTax,
                   extraNightCost, groceriesDict):

    additionalBedCost = 0
    totalNightsPersons = 0
    totalLodgingTax = 0
    extraNightShares = 0
    groceriesShares = { groceries.groceries109 : 0,
                        groceries.groceries43 : 0,
                        groceries.groceries75 : 0,
                        groceries.groceries12 : 0,
                        groceries.groceries29 : 0,
                        groceries.groceries19 : 0,
                        groceries.groceries315 : 0 }

    for person, stayDetails in lodgingConfig.items():
        totalNightsPersons += stayDetails[0]
        if payable.extraBed in stayDetails[1]:
            additionalBedCost += stayDetails[0] * dailyAdditionalBedCostPerPerson
        if payable.lodgingTax in stayDetails[1]:
            totalLodgingTax += stayDetails[0] * lodgingTax
        if payable.extraNight in stayDetails[1]:
            extraNightShares += 1
        for groceryPayable in groceries:
            if groceryPayable in stayDetails[1]:
                groceriesShares[groceryPayable] = groceriesShares[groceryPayable] + 1

    if not totalNightsPersons:
        raise Exception('No persons or nights were computed from the lodging dict')

    totalHouseCost = basicLargeHouseCost + basicSmallHouseCost + additionalBedCost + \
        totalLodgingTax + apartmentCleaningCosts
    costPerNightPerPerson = totalHouseCost / totalNightsPersons
    if extraNightShares:
        costExtraNightPerPerson = extraNightCost / extraNightShares
    else:
        costExtraNightPerPerson = 0

    print()
    print(configLabel)

    # build final people group dict to distinguish cost shares per group
    groupDict = {}
    for person, (numberOfNights, options, correction) in lodgingConfig.items():
        key = str(numberOfNights) + '+' if payable.extraNight in options else str(numberOfNights)
        groupDict[key] = person if key not in groupDict else groupDict[key] + ', ' + person

        individualSum = costPerNightPerPerson * int(numberOfNights)

        individualStayDescription = '{} sta {} notte/i'.format(person, numberOfNights)
        if payable.extraNight in options:
            individualSum += costExtraNightPerPerson

        individualHouseRelatedSum = individualSum

        for groceryPayable in groceries:
            if groceryPayable in options:
                individualSum += groceriesDict[groceryPayable] / groceriesShares[groceryPayable]

        individualStayDescription += ', in totale spende {}, di casa spende {}, deve ancora {}'.format(individualSum, individualHouseRelatedSum, individualSum - correction)
        print(individualStayDescription)

    print('Costo casa totale {}'.format(totalHouseCost + extraNightCost))

    print()

if __name__ == "__main__":

    lodging = { 'Configurazione realistica' : { 'Gio' : (7, [ groceries.groceries109, groceries.groceries43,
                                                              groceries.groceries75, groceries.groceries12,
                                                              groceries.groceries29, groceries.groceries19,
                                                              groceries.groceries315 ],
                                                         GROCERIES[groceries.groceries315]+GROCERIES[groceries.groceries12]),
                                                'Jack' : (7, [ groceries.groceries109, groceries.groceries43,
                                                               groceries.groceries75, groceries.groceries12,
                                                               groceries.groceries29, groceries.groceries19,
                                                               groceries.groceries315 ], GROCERIES[groceries.groceries43]),
                                                'Dani' : (7, [ groceries.groceries109, groceries.groceries43,
                                                               groceries.groceries75, groceries.groceries12,
                                                               groceries.groceries29, groceries.groceries19,
                                                               groceries.groceries315 ], 2059.9 ),
                                                'Fosca' : (7, [ groceries.groceries109, groceries.groceries43,
                                                                groceries.groceries75, groceries.groceries12,
                                                                groceries.groceries29, groceries.groceries19,
                                                                groceries.groceries315 ], GROCERIES[groceries.groceries75]),
                                                'Simo' : (7, [ groceries.groceries109, groceries.groceries43,
                                                               groceries.groceries75, groceries.groceries12,
                                                               groceries.groceries29, groceries.groceries19,
                                                               groceries.groceries315 ], GROCERIES[groceries.groceries29]),
                                                'Andre' : (4, [ groceries.groceries109, groceries.groceries43,
                                                                groceries.groceries75, groceries.groceries12 ], 0),
                                                'Anto' : (4, [ groceries.groceries109, groceries.groceries43,
                                                               groceries.groceries75, groceries.groceries12 ], GROCERIES[groceries.groceries109]),
                                                'Otta' : (4, [ groceries.groceries29, groceries.groceries19,
                                                               groceries.groceries315 ], GROCERIES[groceries.groceries19]),
                                                'Razzo' : (4, [ groceries.groceries29, groceries.groceries19,
                                                                groceries.groceries315 ], 0),
                                                'Fra Scanavino' : (4, [ groceries.groceries29, groceries.groceries19,
                                                                        groceries.groceries315 ], 0),
                                                'Fra Massone' : (4, [ groceries.groceries29, groceries.groceries19,
                                                                      groceries.groceries315 ], 0),
                                                'Filippo' : (3, [ groceries.groceries29, groceries.groceries19,
                                                                  groceries.groceries315 ], 0) } }

    for configLabel, lodgingConfig in lodging.items():
        reportExpenses(BASIC_LARGE_HOUSE_COST, BASIC_SMALL_HOUSE_COST, APARTMENT_CLEANING_COSTS, configLabel, lodgingConfig,
                       DAILY_ADDITIONAL_BED_COST_PER_PERSON, DAILY_LODGING_TAX_PER_PERSON, EXTRA_NIGHT_COST, GROCERIES)

    exit(0)
