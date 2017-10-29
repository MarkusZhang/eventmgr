from .models import ThirdPartyEvent,LocalEvent,EventLocation,EventCategory

__all__=('save_or_update_thirdpartyevent_from_dict','save_local_event_from_dict','get_event_or_none',)

def save_or_update_thirdpartyevent_from_dict(dict):
    new_event,created=ThirdPartyEvent.objects.get_or_create(link=dict['link'])
    new_event.__dict__.update(dict)
    new_event.save()
    return new_event

def save_local_event_from_dict(info_dict):
    # save location
    location=EventLocation()
    location.__dict__.update(info_dict)
    location.save()
    # get category
    try:
        cat_name=info_dict['category_name']
        category=EventCategory.objects.get(name=cat_name)
    except:
        category=None
    # save event
    local_event=LocalEvent()
    local_event.__dict__.update(info_dict)
    local_event.location=location
    local_event.category=category
    local_event.save()
    return local_event

def get_event_or_none(id):
    try:
        return LocalEvent.objects.get(id=id)
    except:
        return None