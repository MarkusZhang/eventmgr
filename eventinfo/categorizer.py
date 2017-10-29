def auto_select_event_category(event_info,categories):
    """
    :param event_info: a dict, which should at least have a 'title' and a 'description' attribute
    :param categories: a list of objects ,each of which should at least have a 'name' attribute
    :return: a category object from the categories list or none
    """
    def has_match(category_name,category_keywords,event_info):
        if (event_info.lower().find(category_name.lower())!=-1):
            return True
        for word in category_keywords.lower().split(","):
            if (event_info.lower().find(word)):
                return True
        return False

    event_title=event_info['title']
    event_description=event_info['description'] if event_info['description'] else ""
    for category in categories:
        if (has_match(category_name=category.name,
                      category_keywords=category.keywords,
                      event_info=event_title + "\n" + event_description)):
            return category