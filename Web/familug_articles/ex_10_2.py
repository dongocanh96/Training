from requests_html import HTMLSession
from flask import Flask, render_template
app = Flask(__name__)


def crawl_url(label):
    result = []
    session = HTMLSession()
    url = "https://www.familug.org/search/label/{}".format(label)
    r = session.get(url)
    while r.html.find(".post-title" ".entry-title"):
        for element in r.html.find(".post-title" ".entry-title"):
            result.append([element.text, list(element.links)[0]])
        if r.html.find(".blog-pager-older-link"):
            url = list(r.html.find(".blog-pager-older-link")[0].links)[0]
            r = session.get(url)
        else:
            break
    return result


def crawl_10():
    result = []
    session = HTMLSession()
    url = "https://www.familug.org/"
    r = session.get(url)
    while r.html.find(".post-title" ".entry-title") and len(result) < 10:
        for element in r.html.find(".post-title" ".entry-title"):
            result.append([element.text, list(element.links)[0]])
            if len(result) == 10:
                break
        if r.html.find(".blog-pager-older-link"):
            url = list(r.html.find(".blog-pager-older-link")[0].links)[0]
            r = session.get(url)
        else:
            break
    return result


def get_list(L, i, v=None):
    try:
        return L[i]
    except IndexError:
        return ""


def main():
    pythons = crawl_url("Python")
    commands = crawl_url("Command")
    sysadmins = crawl_url("sysadmin")
    top_ten = crawl_10()

    index = 0
    result = []
    while True:
        python = get_list(pythons, index)
        command = get_list(commands, index)
        sysadmin = get_list(sysadmins, index)
        lastest = get_list(top_ten, index)
        index += 1
        if python == "" and command == "" and sysadmin == "" and lastest == "":
            break
        result.append(
            {
                "Python": python,
                "Command": command,
                "Sysadmin": sysadmin,
                "Lastest": lastest
            })
    return result


@app.route("/")
def show_articles():
    return render_template("index.html", articles=articles)


if __name__ == "__main__":
    articles = main()
    app.run(debug=True)
