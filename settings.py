download_directory = './data/'

def set_os(os):
    '''
        os: takes in 'windows' or 'linux' or 'mac'
    '''
    chrome_driver = './chromedriver/chromedriver'
    if os == 'windows':
        chrome_driver += '.exe'

    return chrome_driver