import bs4 as bs
import schedule
import requests
import time


def available_vaccines():
    # Grab base url
    url = "https://ca.apm.activecommunities.com/yorkregion/Activity_Search?detailskeyword=&IsAdvanced=True&ddlSortBy=" \
          "Simple+Date&ActivityCenterID={center_id}&ActivityTypeID=25&SearchFor=2&SearchLevelID=2&" \
          "NumberOfItemsPerPage=100&IsSearch=true"

    # Grab various vaccine center ids
    center_id_numbers = ["74", "75", "71", "12", "73", "76"]

    # For each id, check the availability
    for id_num in center_id_numbers:
        # Attempt to get html code from url
        try:
            source = requests.get(url.format(center_id=id_num))
        except Exception as e:
            print("failure to request website\n" + str(type(e)))
            continue
        # Use BeautifulSoup to find the main table containing the availability number
        soup = bs.BeautifulSoup(source.text, 'html.parser')
        table = soup.find(id="ctl05_ctlSearchLayout_ctl01_ctl01_ctlIPGridView")
        # Find amount of dates available
        number_of_rows = len(table.findAll("tr")) - 2
        # For each date, display location and amount available if amount is over 0 and doesn't have a waiting list
        for i in range(1, number_of_rows + 1):
            location = table.find("span",
                                  id="ctl05_ctlSearchLayout_ctl01_ctl01_ctlIPGridView_GridViewRow{row_num}_Label_location_{row_num}"
                                  .format(row_num=str(i))).text
            spots = table.find("span",
                               id="ctl05_ctlSearchLayout_ctl01_ctl01_ctlIPGridView_GridViewRow{row_num}_Label_numberopenings_{row_num}"
                               .format(row_num=str(i))).text
            if spots == "0" or spots == "Waiting List":
                continue
            # Print results to console
            print(location + ": " + spots + " URL: " + url.format(center_id=id_num))

    print("--------Scrape completed--------")


def time_manager():
    print("Vaccine Scraper v 1.1\n---------------------\nThe scraper will now check every 5 minutes for available"
          " vaccine appointments in York region.")
    available_vaccines()
    # Timer for every 5 minutes to repeat the available_vaccines function by scheduling it and running
    schedule.every(5).minutes.do(available_vaccines)
    while True:
        schedule.run_pending()
        # Check every 1 minute if we have a job/function scheduled
        time.sleep(60)


# Call time_manager to initialize the script
time_manager()
