import requests
from bs4 import BeautifulSoup

from constants import *

class CrawlerEngine(object):

    def __init__(self,sites):
        self.sites=sites

    def go_crawl(self,max_page_per_site=MAX_PAGE_PER_SITE):
        overall_list=[]
        for site in self.sites:
            results=self._crawl_single_site(url=site.url,
                                            matching_rules=site.get_matching_rules(),
                                            max_page_number=max_page_per_site)
            overall_list.extend(results)
        return overall_list

    def _crawl_single_site(self,url,matching_rules,max_page_number):
        page_number=1
        can_crawl=True
        site_result_list=[]
        while(can_crawl and page_number<=max_page_number):
            current_url= url.replace(PAGE_NUMBER_PLACE_HOLDER,str(page_number))
            results=self._crawl_single_page(url=current_url,matching_rules=matching_rules)
            can_crawl=True if len(results)>0 else False
            site_result_list.extend(results)
            page_number +=1
        return site_result_list

    def _crawl_single_page(self,url,matching_rules):
        # get rules ready
        container_tag=""
        container_attrs={}
        item_name_list=[]
        item_tag_list=[]
        item_attr_list=[]
        value_format_list=[]
        attr_extract_list=[]
        for i in range(len(matching_rules)):
            rule=matching_rules[i]
            if (rule.is_container):
                container_tag=rule.tag_name
                container_attrs=rule.get_attrs()
            else:
                item_name_list.append(rule.item_name)
                item_tag_list.append(rule.tag_name)
                item_attr_list.append(rule.get_attrs())
                attr_extract_list.append(rule.attr_to_extract)
                value_format_list.append(rule.value_format)

        # start traversing the web page
        result_list=[]
        response=requests.get(url)
        soup=BeautifulSoup(response.text,'html.parser')
        containers=soup.find_all(container_tag,container_attrs)

        # construct items from the container's content
        for container in containers:
            new_item_dict={} # to store the new item discovered
            new_item_constructed_okay=True
            for i in range(len(item_name_list)):
                try:
                    element=container.find(item_tag_list[i],item_attr_list[i]) if item_attr_list[i] else container.find(item_tag_list[i])
                    element_content=self._get_element_content(element=element,attr_to_extract=attr_extract_list[i])
                    new_item_dict[item_name_list[i]]=self._format_html_tag_content(text=element_content,
                                                                                   format_str=value_format_list[i])
                except:
                    new_item_constructed_okay=False
                    break
            if (new_item_constructed_okay):
                result_list.append(new_item_dict)

        return result_list

    def _format_html_tag_content(self,text,format_str):
        space_reduced=' '.join(text.split())
        return format_str.replace(ITEM_VALUE_PLACE_HOLDER,space_reduced)

    def _get_element_content(self,element,attr_to_extract):
        if (attr_to_extract.decode('utf-8')==TEXT.decode('utf-8')):
            return element.text
        else:
            return element.get(attr_to_extract)