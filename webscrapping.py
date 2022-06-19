from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from numpy.random import randint
from pandas import DataFrame
from selenium.webdriver import Chrome, ChromeOptions
from time import perf_counter, sleep
from warnings import filterwarnings
import hashlib
import os
from threaded import Threaded

from settings import download_directory

@Threaded(daemon=True)
def webscrape(location, query, page:int, webdriver_location):
    filterwarnings('ignore')

    df = DataFrame(columns=['Title', 'Location', 'Company', 'Salary', 'Description', 'Time'])
    opts = ChromeOptions()
    opts.headless = False

    driver = Chrome(webdriver_location, options=opts)

    title = ''; loc = ''; company = ''; salary = ''; time = ''; desc = ''

    try:
        driver.get(f'https://www.indeed.co.in/jobs?q={query}&l={location}&start={str(page)}')
        for job in driver.find_elements_by_class_name('result'):
            soup = BeautifulSoup(job.get_attribute('innerHTML'), 'html.parser')
            try:
                title = soup.find('a', class_='jobtitle').text.replace('\n', '').strip()
            except Exception as e:
                print(e)
                title = ''
            finally:
                print(title)

            try:
                loc = soup.find(class_='location').text.replace('\n', '').strip()
            except Exception as e:
                print(e)
                loc = ''
            finally:
                print(loc)

            try:
                company = soup.find(class_='salary').text.replace('\n', '').strip()
            except Exception as e:
                print(e)
                company = ''
            finally:
                print(company)

            try:
                salary = soup.find(class_='salary').text.replace('\n', '').strip()
            except Exception as e:
                print(e)
                salary = ''
            finally:
                print(salary)

            try:
                _time = soup.find(class_='date').text.strip()
                if _time == 'Just posted' or _time == 'Today':
                    time = str(date.today())
                elif _time == '30+ days ago':
                    time = str(date.today() - timedelta(days=randint(31, 91)))
                elif _time == '1 day ago':
                    time = str(date.today() - timedelta(days=1))
                else:
                    for i in range(2, 31):
                        if _time == f'{i} days ago':
                            time = str(date.today() - timedelta(days=i))
                            break
            except Exception as e:
                print(e)
                time = str(date.today() - timedelta(days=randint(31, 91)))
            finally:
                print(time)

            try:
                job.find_element_by_xpath('./div[3]').click()
            except Exception as e:
                print(e)
                driver.find_element_by_class_name('popover-x-button-close')[0].click()
                job.find_element_by_xpath('./div[3]').click()
            finally:
                driver.implicitly_wait(5)

            try:
                desc = driver.find_element_by_id('vjs-desc').text
            except Exception as e:
                print(e)
                desc = ''
            finally:
                print(desc)
            
            df = df.append({'Title': title, 'Location': loc, 'Company': company, 'Salary': salary, 'Time': time,'Description': desc}, ignore_index=True)
    except Exception as e:
        print(e)
    finally:
        # sleep(10)
        driver.close()
        try:
            if not os.path.isdir(download_directory):
                os.mkdir(download_directory)

            n = download_directory + str(hashlib.md5(str(datetime.now()).encode()).hexdigest().encode()).replace("b'", '').replace("'", '') + '.csv'
            df.to_csv(n, index=False)
        except Exception as e:
            print(e)
