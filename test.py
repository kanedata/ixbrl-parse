import json
from ixbrlparse import IXBRL

filenames = [
    'test_accounts/GB-COH-07175596-2017-03-31.html',
    "test_accounts/GB-COH-07713141-2016-09-30.html",
    "test_accounts/GB-COH-05969206-2017-10-31.html",
    "test_accounts/GB-COH-10087608-2018-03-31.html",
]

for filename in filenames:
    print(filename)
    print("=" * len(filename))
    print()

    with open(filename) as a:
        x = IXBRL(a)

        print(x.schema)
        print(json.dumps(x.namespaces, indent=4))
        print()

        print("contexts")
        print("--------")
        for i in x.contexts:
            print(i, x.contexts[i].__dict__)
        print()

        print("units")
        print("-----")
        for i in x.units:
            print(i, x.units[i])
        print()

        print("nonnumeric")
        print("----------")
        for i in x.nonnumeric:
            print(i.__dict__)
        print()

        print("numeric")
        print("-------")
        for i in x.numeric:
            print(i.__dict__)
        print()
    print()
