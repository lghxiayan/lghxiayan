def city_country(city, country, population=''):
    """城市-国家 处理函数"""
    if population:
        long_name = f"{city}, {country} - {population}"
    else:
        long_name = f"{city}, {country}"
    return long_name.title()
