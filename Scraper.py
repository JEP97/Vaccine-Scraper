import bs4 as bs
import schedule
import requests
import time


def available_vaccines():
    url = "https://ca.apm.activecommunities.com/yorkregion/Activity_Search?detailskeyword=&IsAdvanced=True&ddlSortBy=" \
          "Simple+Date&ActivityCenterID={center_id}&ActivityTypeID=25&SearchFor=2&SearchLevelID=2&" \
          "NumberOfItemsPerPage=100&IsSearch=true"

    center_id_numbers = ["74", "75", "71", "12", "73", "76"]
    for id_num in center_id_numbers:
        try:
            source = requests.get(url.format(center_id=id_num))
        except Exception as e:
            print("failure to request website\n" + str(type(e)))
            continue

        soup = bs.BeautifulSoup(source.text, 'html.parser')
        location = soup.find("span",
                             id="ctl05_ctlSearchLayout_ctl01_ctl01_ctlIPGridView_GridViewRow1_Label_location_1").text
        spots = soup.find("span",
                          id="ctl05_ctlSearchLayout_ctl01_ctl01_ctlIPGridView_GridViewRow1_Label_numberopenings_1").text
        if spots == "0" or spots == "Waiting List":
            continue
        print(location + ": " + spots)
    print("Scrape completed")


def time_manager():
    available_vaccines()
    schedule.every(5).minutes.do(available_vaccines)
    while True:
        schedule.run_pending()
        time.sleep(60)


time_manager()