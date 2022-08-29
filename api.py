import requests
from bs4 import BeautifulSoup #pip install beautifulsoup4
from urllib import parse
import time
import utils

class API:
    def __init__(self, host, url) -> None:
        self.session = requests.Session()
        self.host = host
        self.url = url

    def login(self, username, password):
        url = self.url + "/login"

        payload=f'username={username}&password={password}&j_idt28='
        headers = {
        'Host': f'{self.host}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': f'{self.url}',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': f'{self.url}/faces/Login.xhtml',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        }
        r = self.session.post(url, headers=headers, data=payload)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        viewstate  = soup.find(name='input',attrs={"id":'j_id1:javax.faces.ViewState:0'})["value"]
        self.loginViewState = parse.quote(viewstate)
        print("Logger dans Aurion")

    def navigate(self):

        url = self.url + "/faces/MainMenuPage.xhtml"

        payload = f"form=form&form%3AlargeurDivCenter=1620&form%3Asauvegarde=&form%3Aj_idt825%3Aj_idt827_dropdown=1&form%3Aj_idt825%3Aj_idt827_mobiledropdown=1&form%3Aj_idt825%3Aj_idt827_page=0&form%3Aj_idt916%3Aj_idt919_view=basicDay&form%3Aj_idt786_focus=&form%3Aj_idt786_input=44239&javax.faces.ViewState={self.loginViewState}&form%3Asidebar=form%3Asidebar&form%3Asidebar_menuid=1"
        headers = {
        'Host': f'{self.host}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': f'{self.url}',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': f'{self.url}/faces/MainMenuPage.xhtml',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        }

        r = self.session.post(url, headers=headers, data=payload)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        viewstate  = soup.find(name='input',attrs={"id":'j_id1:javax.faces.ViewState:0'})["value"]
        self.calendarViewState = parse.quote(viewstate)
        print("Navigation vers le Planning")

    def selectCal(self, weekNumber, year):
        monday = utils.getUTCDayWWeekNumber(weekNumber, year)
        date_monday = parse.quote(monday.strftime("%d-%m-%Y"))
        micro_monday = int(time.mktime(monday.timetuple())) * 1000
        monday_plus_1 = utils.getWeekPlus1(monday)
        micro_monday_plus_1 = int(time.mktime(monday_plus_1.timetuple())) * 1000

        url = self.url + "/faces/Planning.xhtml"

        payload = f"javax.faces.partial.ajax=true&javax.faces.source=form%3Aj_idt117&javax.faces.partial.execute=form%3Aj_idt117&javax.faces.partial.render=form%3Aj_idt117&form%3Aj_idt117=form%3Aj_idt117&form%3Aj_idt117_start={micro_monday}&form%3Aj_idt117_end={micro_monday_plus_1}&form=form&form%3AlargeurDivCenter=1620&form%3Adate_input=2{date_monday}&form%3Aweek={weekNumber}-{year}&form%3Aj_idt117_view=agendaWeek&form%3AoffsetFuseauNavigateur=0&form%3Aonglets_activeIndex=0&form%3Aonglets_scrollState=0&form%3Aj_idt236_focus=&form%3Aj_idt236_input=44239&javax.faces.ViewState={self.calendarViewState}"

        headers = {
        'Host': f'{self.host}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Accept': 'application/xml, text/xml, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Faces-Request': 'partial/ajax',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': f'{self.url}',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': f'{self.url}/faces/Planning.xhtml',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        }

        r = self.session.post(url, headers=headers, data=payload)
        print(f"Semaine {weekNumber} selectionnée")

    def getCal(self):
        url = self.url + "/faces/Planning.xhtml"

        payload = f"form=form&form%3AlargeurDivCenter=1620&form%3Adate_input=12%2F09%2F2022&form%3Aweek=37-2022&form%3Aj_idt117_view=agendaWeek&form%3AoffsetFuseauNavigateur=0&form%3Aonglets_activeIndex=0&form%3Aonglets_scrollState=0&form%3Aj_idt236_focus=&form%3Aj_idt236_input=44239&javax.faces.ViewState={self.calendarViewState}&form%3Aj_idt120=form%3Aj_idt120"
        headers = {
        'Host': f'{self.host}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': f'{self.url}',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': f'{self.url}/faces/Planning.xhtml',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        }

        r = self.session.post(url, headers=headers, data=payload)
        print("Semaine téléchargée en ICS")
        return(r.text)