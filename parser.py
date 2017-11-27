from bs4 import BeautifulSoup  # required for XMl Parser


def parse_xml(config_xml, tag):
    """
    It parses a given xml file and returns the data that between the tags
    :param config_xml: must be a xml string
    :param tag: must be a  attribute
    :return:
    Raise 1 Exception;
        1. file may be empty or may not be the xml extension

    """
    soup = BeautifulSoup(config_xml, 'xml')

    attribute = soup.find(tag)
    if attribute is None:
        raise Exception("Can't find  " + tag)
    else:
        return attribute.text
