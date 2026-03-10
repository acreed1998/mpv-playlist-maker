import sys
from utils import SORT_BY_VALUES, SORT_ORDER_VALUES


def createIndexedOptionsString(options: tuple[str]):
    accumulator = ""
    for index, option in enumerate(options):
        indexAndOption = f"[{index}]: {option} | "
        accumulator = f"{accumulator} {indexAndOption}"
    return accumulator


sortByOptions = createIndexedOptionsString(SORT_BY_VALUES)
sortOrderOptions = createIndexedOptionsString(SORT_ORDER_VALUES)

sortByQuestion = f"Sort videos by one of the following\n|{sortByOptions}\n"
sortOrderQuestion = f"Choose sort direction\n|{sortOrderOptions}\n"


def determineSortOrder():
    try:
        sortByAnswer = int(input(sortByQuestion))
        sortBy = SORT_BY_VALUES[sortByAnswer]
        if sortBy == "Random":
            return sortBy, None
        else:
            sortOrderAnswer = int(input(sortOrderQuestion))
            sortOrder = SORT_ORDER_VALUES[sortOrderAnswer]
            return sortBy, sortOrder

    except:
        print("Error determining sort order. Please try again.")
        sys.exit(2)
