from crawler import scrape_info_from_all_sites
from eventinfo import save_or_update_thirdpartyevent_from_dict

__all__=('do_crawler_task',)

def do_crawler_task():
    event_info_list=scrape_info_from_all_sites()
    for event_info in event_info_list:
        save_or_update_thirdpartyevent_from_dict(dict=event_info)