import json
from ixbrlparse import IXBRL

filenames = [
    'tests/test_accounts/account_1.html',
    "tests/test_accounts/account_2.html",
    "tests/test_accounts/account_3.html",
    "tests/test_accounts/account_4.html",
    "tests/test_accounts/account_5.html",
]

for filename in filenames:
    print(filename)
    print("=" * len(filename))
    print()

    with open(filename) as a:
        x = IXBRL(a)
        # print(x.to_table())
        print(json.dumps(x.to_table(), indent=4))
        # print(x.schema)
        # print(json.dumps(x.namespaces, indent=4))
        # print()

        # print("contexts")
        # print("--------")
        # for i in x.contexts:
        #     print(i, x.contexts[i].__dict__)
        # print()

        # print("units")
        # print("-----")
        # for i in x.units:
        #     print(i, x.units[i])
        # print()

        # print("nonnumeric")
        # print("----------")
        # for i in x.nonnumeric:
        #     print(i.__dict__)
        # print()

        # print("numeric")
        # print("-------")
        # for i in x.numeric:
        #     print(i.__dict__)
        # print()
    print()
