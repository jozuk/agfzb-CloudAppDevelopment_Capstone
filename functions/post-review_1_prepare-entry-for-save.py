#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys

def main(dict):
    fields = ["id", "name", "dealership", "review", "purchase",
              "another", "purchase_date", "car_make", "car_model", "car_year"]
    doc = {}
    for field in fields:
        if field in dict["review"]:
            doc[field] = dict["review"][field]

    return {"doc": doc}
