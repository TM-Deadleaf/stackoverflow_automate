from subprocess import Popen, PIPE
import requests
import webbrowser


def execute(cmd):  # execute the cmd from test.py script and print out the error message
    args = cmd.split()
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    return out, err


def request_to_api(error_message):
    response = requests.get(
        "https://api.stackexchange.com/" + "/2.2/search?order=desc&sort=activity&tagged=python&intitle={}&site=stackoverflow".format(
            error_message))
    return response.json()


def make_requests_to_browser(json_dict):
    count = 0
    url_list = []
    for i in json_dict["items"]:
        if i["is_answered"]:
            url_list.append(i["link"])
        count+=1
        if(count == 3 or count == len(i)):
            break
    for i in url_list:
        webbrowser.open(i)


if __name__ == '__main__':  # main function  for the error message splitting
    out, err = execute("python test.py")
    output = err.decode('utf-8').strip().split("\r\n")[-1]
    print(output)
    if (output):
        filter = output.split(":")
        json1 = request_to_api(filter[0])
        json2 = request_to_api(filter[1])
        json = request_to_api(output)
        make_requests_to_browser(json1)
        make_requests_to_browser(json2)
        make_requests_to_browser(json)
    else:
        print("NO ERROR !!")