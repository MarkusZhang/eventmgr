from datetime import datetime

__all__=('from_querydict_to_dict','format_dict','convert_str_to_datetime',)

def from_querydict_to_dict(querydict):
    python_dict=dict(querydict.iterlists())
    return {key:value[0] for key,value in python_dict.items()}

def format_dict(data_dict,field_category_dict):
    def datetime_format(datetime_str):
        format_str="%Y-%m-%dT%H:%M:%SZ"
        return datetime.strptime(datetime_str,format_str)

    def boolean_format(bool_str):
        return True if bool_str.lower()=='true' else False

    formatters={'int':int,'float':float,'datetime':datetime_format,'boolean':boolean_format}

    for category,fields in field_category_dict.items():
        formatter=formatters[category]
        data_dict={key:formatter(value) if key in fields else value for key,value in data_dict.items() }

    return data_dict

def convert_str_to_datetime(datetime_str):
    format_str="%Y-%m-%dT%H:%M:%SZ"
    naive_time=datetime.strptime(datetime_str,format_str)
    import pytz
    tz=pytz.timezone("Asia/Singapore")
    return datetime(naive_time.year,naive_time.month,naive_time.day,
                    naive_time.hour,naive_time.minute,naive_time.second,tzinfo=tz)