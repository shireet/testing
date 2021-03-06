


def main():

    from selenium import webdriver
    import os
    from selenium.webdriver.chrome.options import Options
    import time
    from PyPDF2 import PdfFileMerger
    import shutil



    location_project = os.getcwd()  # path to test
    os.mkdir("temp")
    folder_dir = location_project + "/temp"  # path to the created file

    chromeOptions = Options()  # adding options to chrome
    chromeOptions.add_experimental_option("prefs", {
        "download.default_directory": folder_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
        "download.extensions_to_open": "applications/pdf"
    })
    #chromeOptions.add_argument("headless")
    chromeOptions.add_argument("window-size=1,1")

    driver = webdriver.Chrome(location_project + "/chromedriver", options=chromeOptions)






    def login(year):
            driver.get("https://diploma.rsr-olymp.ru/" + year + "/")
            driver.implicitly_wait(3)
            try:
                driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/h2")
            except:
                print("Вы указали неверные года")
                driver.close()
                shutil.rmtree(folder_dir)
                main()





    def put_info(last_name, first_name, middle_name, day, month, yearofbirth):
            driver.find_element_by_id("last-name").send_keys(last_name)
            driver.find_element_by_id("first-name").send_keys(first_name)
            driver.find_element_by_id("middle-name").send_keys(middle_name)
            driver.find_element_by_id("bdd").send_keys(day)
            driver.find_element_by_id("bdm").send_keys(month)
            driver.find_element_by_id("bdy").send_keys(yearofbirth)
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/input").click()
            time.sleep(1)

            x = driver.find_element_by_xpath("//*[@id=\"results\"]").text
            s = len(x)
            if s < 101:
                print(x)
                print("Или у вас нет дипломав за этот год")
                driver.close()
                shutil.rmtree(folder_dir)
                main()





    def download(type, o):# download colored or white

            i = 0
            if type == "color":
                pdfscolor = driver.find_elements_by_css_selector("a[href$=\"color.pdf\"]")
                for pdf in pdfscolor:

                    pdf.click()
                    time.sleep(2)
                    i += 1
                return i
            elif type == "white":

                pdfswhite = driver.find_elements_by_css_selector("a[href$=\"white.pdf\"]")
                for pdf in pdfswhite:
                    pdf.click()
                    time.sleep(2)
                    i += 1
                return i
            if i == 0:
                print("Не найдены дипломы за "+o+" год")


    def wait(count, type):
        if count == 1:
            while not os.path.isfile(folder_dir + "/" + type + ".pdf"):
                time.sleep(2)
        else:
            for i in range(1, count):
                while not os.path.isfile(folder_dir + "/" + type + " " + "(" + str(i) + ").pdf"):
                        time.sleep(2)

    def pdfmerger(pdflist, type):
        merger = PdfFileMerger()
        for item in pdflist:
            absfile = os.path.join(folder_dir, item)
            merger.append(absfile)
        merger.write(location_project+"/_"+type+"_spiski.pdf")
        merger.close()




    year = {"2020", "2014"} #храним годы дипломов в массиве
    last_name = "иваненко"
    first_name = "григорий"
    middle_name = "александрович"
    day = "3"
    month = "11"
    yearofbirth = "2003"
    type = "white"

    for o in year: #цикл скачиваюшая пдф указанных годов
        login(o)
        put_info(last_name, first_name, middle_name, day, month, yearofbirth)
        count = download(type, o)
        wait(count, type)
        pdflist = os.listdir(folder_dir)

    pdfmerger(pdflist, type) #merge all pdfs
    shutil.rmtree(folder_dir)#delete temp
    driver.close()#end
main()












