def Asia():
    Asia = [
        'af',
        'am',
        'az',
        'bh',
        'bd',
        'bt',
        'io',
        'bn',
        'kh',
        'cn',
        'cc',
        'cy',
        'ge',
        'hk',
        'in',
        'id',
        'ir',
        'iq',
        'il',
        'jp',
        'jo',
        'kz',
        'kp',
        'kr',
        'kw',
        'kg',
        'la',
        'lb',
        'mo',
        'my',
        'mv',
        'mn',
        'mm',
        'np',
        'om',
        'pk',
        'ps',
        'ph',
        'qa',
        'sa',
        'sg',
        'lk',
        'sy',
        'tw',
        'tj',
        'th',
        'tl',
        'tr',
        'tm',
        'ae',
        'uz',
        'vn',
        'ye'
    ]
    return Asia


def Europe():
    Europe = [
        'ax',
        'al',
        'ad',
        'at',
        'by',
        'be',
        'ba',
        'bg',
        'hr',
        'cz',
        'dk',
        'ee',
        'eu',
        'fo',
        'fi',
        'fr',
        'de',
        'gi',
        'gr',
        'gg',
        'va',
        'hu',
        'is',
        'ie',
        'im',
        'it',
        'je',
        'lv',
        'li',
        'lt',
        'lu',
        'mk',
        'mt',
        'md',
        'mc',
        'me',
        'nl',
        'no',
        'pl',
        'pt',
        'ro',
        'ru',
        'sm',
        'rs',
        'sk',
        'si',
        'es',
        'se',
        'ch',
        'ua',
        'gb'
    ]
    return Europe


def Africa():
    Africa = [
        'dz',
        'ao',
        'bj',
        'bw',
        'bf',
        'bi',
        'cm',
        'cv',
        'cf',
        'td',
        'km',
        'cg',
        'cd',
        'ci',
        'dj',
        'eg',
        'gq',
        'er',
        'et',
        'ga',
        'gm',
        'gh',
        'gn',
        'gw',
        'ke',
        'ls',
        'lr',
        'ly',
        'mg',
        'mw',
        'ml',
        'mr',
        'mu',
        'yt',
        'ma',
        'mz',
        'na',
        'ne',
        'ng',
        're',
        'rw',
        'st',
        'sn',
        'sc',
        'sl',
        'so',
        'za',
        'ss',
        'sd',
        'sz',
        'tz',
        'tg',
        'tn',
        'ug',
        'zm',
        'zw'
    ]
    return Africa


def North_America():
    North_America = [
        'ai',
        'ag',
        'aw',
        'bs',
        'bb',
        'bz',
        'bm',
        'bq',
        'ca',
        'ky',
        'cr',
        'cu',
        'cw',
        'dm',
        'do',
        'sv',
        'gl',
        'gd',
        'gp',
        'gt',
        'ht',
        'hn',
        'jm',
        'mq',
        'mx',
        'ms',
        'ni',
        'pa',
        'pr',
        'bl',
        'kn',
        'lc',
        'mf',
        'pm',
        'vc',
        'sx',
        'tt',
        'tc',
        'us',
        'um',
        'vg',
        'vi'
    ]
    return North_America


def South_America():
    South_America = [
        'ar',
        'bo',
        'br',
        'cl',
        'co',
        'ec',
        'fk',
        'gf',
        'gy',
        'py',
        'pe',
        'sr',
        'uy',
        've'
    ]
    return South_America


def Oceana():
    Oceana = [
        'as',
        'ap',
        'au',
        'ck',
        'fj',
        'pf',
        'gu',
        'ki',
        'mh',
        'fm',
        'nr',
        'nc',
        'nz',
        'nu',
        'nf',
        'mp',
        'pw',
        'pg',
        'ws',
        'sb',
        'tk',
        'to',
        'tv',
        'vu',
        'wf'
    ]
    return Oceana


def Antarctica():
    Antarctica = [
        'aq'
    ]
    return Antarctica


request_url = 'https://www.ipdeny.com/ipblocks/data/countries/'
end_name = '.zone'


def get_asia():
    Asia_list = [request_url + item + end_name for item in Asia()]
    return Asia_list


def get_europe():
    Europe_list = [request_url + item + end_name for item in Europe()]
    return Europe_list


def get_africa():
    Africa_list = [request_url + item + end_name for item in Africa()]
    return Africa_list


def get_north_america():
    North_America_list = [request_url + item + end_name for item in North_America()]
    return North_America_list


def get_south_america():
    South_America_list = [request_url + item + end_name for item in South_America()]
    return South_America_list


def get_oceana():
    Oceana_list = [request_url + item + end_name for item in Oceana()]
    return Oceana_list


def get_antarctica():
    Antarctica_list = [request_url + item + end_name for item in Antarctica()]
    return Antarctica_list


AsiaList = get_asia()
EuropeList = get_europe()
AfricaList = get_africa()
NorthAmericaList = get_north_america()
SouthAmericaList = get_south_america()
OceanaList = get_oceana()
AntarcticaList = get_antarctica()
