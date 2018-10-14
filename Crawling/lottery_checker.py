import argparse
from requests_html import HTMLSession


def lottery_checker(args):
    '''Kiem tra cac so nhap vao co trung lo hay khong.
    Neu khong co so dua vao thi in ra ket qua xo so'''
    session = HTMLSession()
    resp = session.get('http://ketqua.net')
    ids = {'special_prize': '#rs_0_0',
           '1st_prize': '#rs_1_0',
           '2nd_prize': ['#rs_2_0', '#rs_2_1'],
           '3rd_prize': ['#rs_3_{}'.format(i) for i in range(6)],
           '4th_prize': ['#rs_4_{}'.format(i) for i in range(4)],
           '5th_prize': ['#rs_5_{}'.format(i) for i in range(6)],
           '6th_prize': ['#rs_6_0', '#rs_6_1', '#rs_6_2'],
           '7th_prize': ['#rs_7_{}'.format(i) for i in range(4)]
           }
    lottery_result = {}
    for name, _id in ids.items():
        if isinstance(_id, list):
            lottery_result[name] = [resp.html.find(_)[0].text for _ in _id]
        else:
            lottery_result[name] = resp.html.find(_id)[0].text
    if len(args):
        hit = {}
        for number in args:
            count = 0
            for prize, value in lottery_result.items():
                if isinstance(value, list):
                    for num in value:
                        if number == int(str(num)[-2:]):
                            count += 1
                else:
                    if number == int(str(value)[-2:]):
                        count += 1
            hit[number] = count
        for key, value in hit.items():
            if value > 0:
                print('So {} da trung lo, trung {} nhay'.format(key, value))
            else:
                print('So {} khong trung lo'.format(key))
    else:
        for key, value in lottery_result.items():
            if isinstance(value, list):
                print(key, ':', *value)
            else:
                print(key, ':', value)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("num", type=int, nargs="*")
    numbers = parser.parse_args().num
    lottery_checker(numbers)


if __name__ == '__main__':
    main()
