from bs4 import BeautifulSoup  # required for XMl Parser


def parse_xml(config_xml, tag):
    """
    It parses a given xml file and returns the data that between the tags
    :param config_xml: must be a xml string
    :param tag: must be a  attribute
    :return:
    Raise 3 Exception;
        1. for config_file  exits or readable
        2. for file may be empty or may not be the xml extension
    """
    try:
        soup = BeautifulSoup(config_xml, 'xml')

        attribute = soup.find(tag)
        if attribute is None:
            raise Exception('Cant find tag')
        else:
            return attribute.text
    except IOError:
        raise IOError("Can't find config file")
