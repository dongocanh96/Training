import requests
import argparse


def get_question(N, label):
    '''In ra title va link den cau tra loi co so vote cao nhat
    cua top N cau hoi trong tag label tren stackoverflow'''
    url_q = 'https://api.stackexchange.com/2.2/questions'\
            '?pagesize={}&order=desc&sort=votes&tagged={}&site=stackoverflow'
    resp_q = requests.get(url_q.format(N, label))
    r_q = resp_q.json()
    for _ in range(N):
        id_q = r_q["items"][_]["question_id"]
        url_a = 'https://api.stackexchange.com/2.2/questions'\
                '/{}/answers'\
                '?pagesize=1&order=desc&'\
                'sort=votes&site=stackoverflow'.format(id_q)
        resp_a = requests.get(url_a)
        r_a = resp_a.json()
        answer_id = r_a["items"][0]["answer_id"]
        answer_tail = '/' + str(answer_id) + '#' + str(answer_id)
        link_a = r_q["items"][_]["link"] + answer_tail
        print(r_q["items"][_]["title"], ':\n', '\t', link_a, '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("N", help="Top N questions on stackoverflow", type=int)
    parser.add_argument("label", help="The label you choose", type=str)
    args = parser.parse_args()
    get_question(args.N, args.label)


if __name__ == '__main__':
    main()
