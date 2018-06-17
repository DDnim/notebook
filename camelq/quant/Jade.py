from works.bitflyer import work_bitflyer


def test():
    x = work_bitflyer('BTC_JPY')

    print(x.value)
    x.get_serial()
    print(x.value)
