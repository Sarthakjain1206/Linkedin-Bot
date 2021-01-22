from selenium import webdriver
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.support.ui import Select
from secrets import email, password
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
chrome_options = Options()
from scrapy import Selector

sleepLst = [0.5, 0.2, 1, 1.5, 1.2, 2, 1.8, 0.8]

# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)

mapping = {
    'location': 'ember122',
    'school': 'ember141',
    'what_they_do': 'ember160',
    'studied': 'ember178',
    'skill': 'ember197',
    'connections': 'ember216'
}

driver.get("https://www.linkedin.com/")

emailElement = driver.find_element_by_id("session_key")
emailElement.send_keys(email)
passwordElement = driver.find_element_by_id("session_password")
passwordElement.send_keys(password)

signInBtn = driver.find_element_by_class_name("sign-in-form__submit-button")
print("Clicking sign in button")
signInBtn.click()

print("I am sleeping for one seconds..")
sleep(1)
print("Done Sleeping")
driver.get("https://linkedin.com/company/goldman-sachs/people")
print("Reached on page of company")
sleep(1)


def applyLocationFilter():
    print("Location Filter: ")
    country = str(input("Which country's people you want to connect with ? "))
    return country

def applySchoolFilter():
    print("Where they studied Filter(Like: BITS, Lovely Professional University etc): ")
    school = str(input("Which college/university's people you want to connect with ? "))
    return school

def applyWhatTheyDoFilter():
    pass

def applyStudyFilter():
    print("Education Filter (Like: Computer Science): ")
    study = str(input("Enter Branch: "))
    return study


def applyskillFilter():
    print("\nNot Recommeded, if you're main purpose is to exapnd your reach\n")
    print("Skill Filter: (Like: SQL, JAVA etc)")
    skill = str(input("Enter Skill: "))
    return skill

def checkConditionAndCall(i):
    if i == 1:
        arg = applyLocationFilter()
    elif i == 2:
        arg = applySchoolFilter()
    elif i == 4:
        arg = applyStudyFilter()
    elif i == 5:
        arg = applyskillFilter()
    return arg

def askForFilter(name):
    while True:
        response = input(f"You want apply {name} filter ? (yes/no): ")
        if response.lower() == 'yes' or response.lower() == 'y':
            return True
        elif response.lower() == 'no' or response.lower() == 'n':
            return False
        else:
            print("\n------Please write yes or no/ y or n only------\n")


def checkConditionAndAsk(i):
    if i == 1:
        response = askForFilter("Location (India/ United States etc.)")
    elif i == 2:
        response = askForFilter("School/University Filter")
    elif i == 4:
        response = askForFilter("Branch/Stream Filter")
    elif i == 5:
        response = askForFilter("Skill (Like: Python, Java)")
    else:
        response = False
    return response

def includeScrapy(i):
    sleep(1)
    response = Selector(text=driver.page_source.encode('utf-8'))
    lst = response.xpath(f"//li[@class='artdeco-carousel__item ember-view'][{i}]//div[@class='insight-container__title']")
    temp = lst.xpath('.//div[@role="listbox"]//div[@role="option"]')
    return temp

def includeScrapy2(xpath):
    response = Selector(text=driver.page_source.encode('utf-8'))
    return response.xpath(xpath).extract_first()

def handleClickInterception(elements):
    try:
        elements.click()

    except ElementClickInterceptedException:
        sleep(0.5)
        try:
            elementMsg = driver.find_element_by_xpath("//button[@data-control-name='overlay.close_conversation_window']")
            elementMsg.click()
        except NoSuchElementException:
            print("Not able to apply the filter..")
        return NoSuchElementException

def clickOnAddBtn(i):
    flag = True
    for _ in range(5):
        try:
            xpath = f"//li[@class='artdeco-carousel__item ember-view'][{i}]//div[@class='insight-container__title']/button"
            addLocationBtn = driver.find_element_by_xpath(xpath)
            flag = False
            sleep(0.5)
        except NoSuchElementException:
            print("I am inside Exception")
            sleep(1)
    if not flag:
        return addLocationBtn, flag
    return NoSuchElementException, flag



messageOverlay = driver.find_element_by_xpath('//header[@class="msg-overlay-bubble-header"]')
try:
    messageOverlay.click()
except:
    pass


def applyFilters():
    for i in range(1, 6):
        
        response = checkConditionAndAsk(i)
        if i == 3 or i == 5:

            xpath = "//div[@class='artdeco-carousel__navigation ']//button[@aria-label='Next']"
            try:
                element = driver.find_element_by_xpath(xpath)
            except NoSuchElementException:
                sleep(1)
                element = driver.find_element_by_xpath(xpath)

            webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
            if i == 4:
                print("SSASASSlllllleepiing")
                sleep(1)
                element = driver.find_element_by_xpath(xpath)
                webdriver.ActionChains(driver).move_to_element(element).click(element).perform()

        if not response:
            continue
        flag = True
        try:
            addLocationBtn, flag = clickOnAddBtn(i)
        except NoSuchElementException:
            try:
                handleClickInterception(addLocationBtn)
            except NoSuchElementException:
                continue
        try:
            handleClickInterception(addLocationBtn)
        except NoSuchElementException:
            continue

        sleep(0.2)
        addBtn = driver.find_element_by_xpath(f"//li[@class='artdeco-carousel__item ember-view'][{i}]//div[@class='insight-container__title']//input")
        sleep(0.2)
        
        
        arg = ''
        arg = checkConditionAndCall(i)
        
        if arg:
            addBtn.send_keys(arg)
        else:
            continue
        
        temp = includeScrapy(i)
        #! If no value is prsent in list for entered value
        flag = True
        while len(temp) < 1:
            # Click anywhere
            driver.find_element_by_xpath("//span[@class='t-20 t-black t-bold']").click()
            sleep(0.2)
            # We have to click on add button again--
            try:
                addLocationBtn, flag = clickOnAddBtn(i)
            except NoSuchElementException:
                flag = False
                break
            
            # addLocationBtn, flag = clickOnAddBtn(i)
            try:
                handleClickInterception(addLocationBtn)
            except NoSuchElementException:
                flag = False
                break
            addBtn = driver.find_element_by_xpath(f"//li[@class='artdeco-carousel__item ember-view'][{i}]//div[@class='insight-container__title']//input")
            # addBtn.clear()
            # No write next value -- 
            print("\nPlease enter another value as I can't find any related filter with this.\n")
            arg = checkConditionAndCall(i)
            while True:
                if arg:
                    addBtn.send_keys(arg)
                    flag = True
                    sleep(0.2)
                    break
                else:
                    print("Please enter some value")
                    continue

            temp = includeScrapy(i)

        # If button is somehow not clickable then exit out from loop
        if not flag:
            print("Something Went Wrong!")
            break


        print(f"We have {len(temp)} more options related to the country name you enterd: ")
        for j in range(len(temp)):
            print(j + 1, ")", temp[j].xpath('./p/text()').extract_first().strip())
        flag = True
        number = 0
        for _ in range(5):
            while True:
                number = input("Enter one number which you want to select: ")
                try:
                    number = int(number)
                    break
                except ValueError:
                    print("Please make sure you enter only number from the given range!")

            if number >= 1 and number <= len(temp):
                flag = False
                break
            else:
                print("Please! Select from the given numbers only..")
                continue
        if flag:
            print("We are aborting the program right now..")
            break

        print("You opt for {0}\n".format(temp[number - 1].xpath('./p/text()').extract_first().strip()))
        elements = driver.find_element_by_xpath(f"//li[@class='artdeco-carousel__item ember-view'][{i}]//div[@class='insight-container__title']//div[@role='listbox']//div[@role='option'][{number}]")

        try:
            handleClickInterception(elements)
        except NoSuchElementException:
            continue

        # driver.execute_script("arguments[0].click();", elements)
        # webdriver.ActionChains(driver).move_to_element(elements).click(elements).perform()

        sleep(1)
        print("Filter applied successfully!\n\n\n")
        
        sleep(0.5)

# global lastScrollHeight
# lastScrollHeight = 0

def scrollPage(i, lastScrollHeight=0):
    scrollHeight = lastScrollHeight + 300
    if i == 0:
        scrollHeight = 1000

    driver.execute_script(f"window.scrollTo({lastScrollHeight}, {scrollHeight});")
    sleep(1)
    lastScrollHeight = scrollHeight
    return lastScrollHeight


def parseProfiles():
    xpathForTotalEmployees = '//div[@class="artdeco-card"]/div/span/text()'
    totalEmployees = includeScrapy2(xpathForTotalEmployees)
    print(f"\nWe found {totalEmployees.strip()}\n")
    print(f'''
    If number of Employees is very less for you then I think removing some filters, if applied, will help.\n
    ======================================

    ''')
    response = input("Would you like to continue ? (yes/no): ")
    print("\n======================================")
    if response.lower() == 'yes' or response.lower() == 'y':
        pass
    elif response.lower() == 'no' or response.lower() == 'n':
        return
    
    count = 0
    lastScrollHeight = 0
    lastScrollHeight = scrollPage(0, lastScrollHeight)
    
    for i in range(100):
        if i % 3 == 0 and i != 0:
            print("I am scrolling page")
            lastScrollHeight = scrollPage(i, lastScrollHeight)

        sleep(random.choice([1, 2, 1.2, 1.5]))
        xpath = f'//ul[@class="org-people-profiles-module__profile-list"]//li[@class="org-people-profiles-module__profile-ia-item"][{i+1}]//footer//button'
        connectBtn = driver.find_element_by_xpath(xpath)
        try:
            connectBtn.click()
        except ElementClickInterceptedException:
            
            print("\n........I don't what to do next..........\n")
            print("\nAbruptely Closing the program now...")
            break
        except NoSuchElementException:
            print("\n========\nI am done!!\n==========\n")
            break
        
        sleep(random.choice(sleepLst))
        
        # Find and click the "send" button to send connection request.
        send_now_btn = driver.find_element_by_xpath('//button[@aria-label="Send now"]')
        try:
            send_now_btn.click()
            count += 1
        except:
            print("\nSorry, Something Went Wrong!!\n")
            break
        sleep(random.choice(sleepLst))


        # Close the acknowment box, which linkedin shows on screen, after we send connection request to someone.
        while True:
            response = Selector(text=driver.page_source.encode('utf-8'))
            selector = response.xpath('//button[starts-with(@aria-label,"Dismiss")]')
            if selector:
                driver.find_element_by_xpath('//button[starts-with(@aria-label,"Dismiss")]').click()
            else:
                break
            sleep(0.5)
        
        sleep(0.5)
    print(f"Connection request send to total {count} people")

applyFilters()
# scrollPage()
parseProfiles()