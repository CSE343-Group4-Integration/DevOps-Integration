from bs4 import BeautifulSoup  # required for XMl Parser


def parse_xml(config_file, tag):
    """
    It parses a given xml file and returns the data that between the tags
    :param config_file: must be a xml file
    :param tag: must be a  attribute
    :return:
    Raise 3 Exception;
        1. for config_file  exits or readable
        2. for file may be empty or may not be the xml extension
    """
    try:
        file = open(config_file, 'r')
        read = file.read()

        soup = BeautifulSoup(read, 'xml')
        if soup is None:
            file.close()
            raise Exception('File not found or it is not xml')
        else:
            attribute = soup.find(tag)
            if attribute is None:
                file.close()
                raise Exception('Cant find tag')
            else:
                return attribute.text

    except IOError:
        raise IOError("Can't find config file")
