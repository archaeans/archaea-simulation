

def sequential_compact_schedule_generator(name: str, schedule_type_limit_name: str, days: "list[int]", months: "list[int]") -> str:
    schedule_string = ""
    schedule_string += "!-   ===========  OUTPUT SCHEDULE ===========" + "\n\n"
    schedule_string += "Schedule:Compact," + "\n" 
    schedule_string += "{name},\t\t\t!- Name\n".format(name=name)
    schedule_string += "{name},\t\t\t!- Schedule Type Limits Name\n".format(name=schedule_type_limit_name)
    field = 1
    for m in months:
        for d in days:
            m_fill = str(m).zfill(2)
            d_fill = str(d).zfill(2)
            d_next_fill = str(d+1).zfill(2)
            schedule_string += "Through: {month}/{day},\t\t\t!- Field {field}\n".format(month=m_fill, day=d_fill, field=field)
            field += 1
            schedule_string += "For:AllDays,\t\t\t!- Field {field}\n".format(field=field)
            field += 1
            schedule_string += "Until: 24:00,\t\t\t!- Field {field}\n".format(field=field)
            field += 1
            schedule_string += "0,\t\t\t!- Field {field}\n".format(field=field)
            field += 1
            schedule_string += "Through: {month}/{day},\t\t\t!- Field {field}\n".format(month=m_fill, day=d_next_fill, field=field)
            field += 1
            schedule_string += "For:AllDays,\t\t\t!- Field {field}\n".format(field=field)
            field += 1
            schedule_string += "Until: 24:00,\t\t\t!- Field {field}\n".format(field=field)
            field += 1
            schedule_string += "1,\t\t\t!- Field {field}\n".format(field=field)
            field += 1
    schedule_string += "Through: 12/31,\t\t\t!- Field {field}\n".format(field=field)
    field += 1
    schedule_string += "For:AllDays,\t\t\t!- Field {field}\n".format(field=field)
    field += 1
    schedule_string += "Until: 24:00,\t\t\t!- Field {field}\n".format(field=field)
    field += 1
    schedule_string += "0;\t\t\t!- Field {field}\n\n\n".format(field=field)
    field =+ 1

    # schedule_string += "For: Allotherdays,\t\t\t!- Field {field}\n".format(field=field)
    # field += 1
    # schedule_string += "Until: 24:00,\t\t\t!- Field {field}\n".format(field=field)
    # field += 1
    # schedule_string += "0;\t\t\t!- Field {field}\n\n\n".format(field=field)
    return schedule_string

