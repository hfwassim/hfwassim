import sys
from PyQt5 import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 
from bs4 import BeautifulSoup
import requests
import webbrowser as wb
from lxml import etree

from SecondProgram import *
import time

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.dialogue = MainDialogue()
        self.ui.setupUi(self)
        
        
        self.ui.lineEdit.textChanged.connect(self.AutoSearchEnginebyUser)
        
        self.url = {'jumia':[],'tunisianet':[],'Mega pc':[]}


        with open('link.txt','r',encoding='utf-8') as file:
            for i in file:
                url = i.replace('\n','')

                if 'jumia.com' in url:
                    self.url['jumia'].append(url)

                elif 'tunisianet.com.tn' in url:
                    self.url['tunisianet'].append(url)

                elif 'megapc.tn' in url:
                    self.url['Mega pc'].append(url)



        
        self.listvalues = {}
        self.filterx = []

        try:
            self.AutoSearchEnginebySystem()
        except requests.exceptions.ConnectionError:
            self.dialogueWidget('No Connection Found','Exit')
        



        self.ui.pushButton.clicked.connect(self.AutoSystemCheking)

        self.ui.pushButton_3.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.page))






    def AutoSystemCheking(self):
        self.url = {'jumia':[],'tunisianet':[],'Mega pc':[]}


        with open('link.txt','r',encoding='utf-8') as file:
            for i in file:
                url = i.replace('\n','')

                if 'jumia.com' in url:
                    self.url['jumia'].append(url)

                elif 'tunisianet.com.tn' in url:
                    self.url['tunisianet'].append(url)

                elif 'megapc.tn' in url:
                    self.url['Mega pc'].append(url)



        
        self.listvalues = {}
        self.filterx = []
        try:
            self.AutoSearchEnginebySystem()
        except requests.exceptions.ConnectionError:
            self.dialogueWidget('No Connection Found','Exit')

    def stackSwitch(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)




    def AutoSearchEnginebySystem(self):
        self.header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0"}
        for key in self.url.keys():
            self.listvalues[key] = []
            ProductName = []
            ProductPrice = []
            ProductUrl = []
            ProductInfo = []

            for url in self.url[key]:
                req = requests.get(url, headers=self.header)
                soup = BeautifulSoup(req.content, 'lxml')


                if key == 'jumia':
                    #find title of product
                    showName = soup.find_all('h3',{'class':'name'})

                    #find price of product
                    showPrice = soup.find_all('div',{'class':'prc'})

                    #find link of product
                    for urlItem in soup.select("[class='prd _fb col c-prd'] a"):
                        urlItem = urlItem['href']
                        if urlItem[0] == '/':
                            ProductUrl.append(str(url[0:24]+urlItem))

                    


                elif key == 'Mega pc':
                    #find title of product
                    showName = soup.find_all('h6',{'class':'productsyle2'})

                    #find price of product
                    showPrice = soup.find_all('h3',{'class':'productsyle1'})

                    #find link of product
                    for urlItem in soup.select("[class='img-wrapper'] a"):
                        urlItem = urlItem['href']
                        if urlItem[0] == '/':
                            ProductUrl.append(str('https://megapc.tn'+urlItem))
                            



                elif key == 'tunisianet':
                    #find title of product
                    showName = soup.find_all('h2',{'class':'h3 product-title'})

                    #find price of product
                    showPrice = soup.find_all('span',{'class':'price'})

                    #find title of product
                    showUrl = soup.select('h2.h3.product-title a')
                    #find link of product
                    for UrlItem in showUrl:
                        ProductUrl.append(UrlItem.get('href'))

               

                else:
                    pass
                for i in range(len(showName)):
                    ProductName.append(showName[i].text.strip("\n").strip('\t').strip(''))
                    ProductPrice.append(showPrice[i].text.strip("\n").strip('\t').strip(''))
                ProductName = list(filter(None, ProductName))
                ProductPrice = list(filter(None, ProductPrice))
                ProductPriceFilter = []
                for Price in ProductPrice:
                    ProductPriceFilter.append(float(self.fnfilter(key,Price)))


                ProductUrl = list(filter(None, ProductUrl))
                ProductInfo = list(filter(None, ProductInfo))
                #print(key,":",val)
                self.listvalues[key].clear()
                self.listvalues[key].append(ProductName)
                self.listvalues[key].append(ProductPriceFilter)
                self.listvalues[key].append(ProductUrl)
                self.listvalues[key].append(ProductInfo)


        


        AutoNameProductCompelter = [] 
        for key in self.listvalues.keys():
            for item in self.listvalues[key][0]:
                AutoNameProductCompelter.append(item)
                        
        
        completer = QCompleter(AutoNameProductCompelter)
        self.ui.lineEdit.setCompleter(completer)
            
        
    def AutoSearchEnginebyUser(self):

        maxList = []

        try:
            while True:
                itemG = self.ui.verticalLayout.takeAt(0)
                if not itemG:
                    break
                self.ui.verticalLayout.removeWidget(itemG.widget())
        except AttributeError:
            pass

        UserInput = self.ui.lineEdit.text()
        row = 0
        for key in self.listvalues.keys():
            col = 0
            p = 0
            u = 0
            inf = 0
            for item in self.listvalues[key][0]:
                for i in UserInput+' ':
                    if i == ' ':
                        iteminput = UserInput[0:UserInput.find(i)]
                        UserInput = UserInput[UserInput.find(i)+1:]
                        print('--------- item input ---------\n',iteminput,'------ user input -------\n',UserInput)
                        if UserInput.upper() in item.upper():
                            print('----- cheking of item inside userinput-------\n',UserInput)
                            itemTitle = item[0:33]+'\n'+item[34:len(item)]
                            if u <= len(self.listvalues[key][2])-1 :
                                self.contentWidgetProduct(row,self.listvalues[key][1][p],itemTitle,self.listvalues[key][2][u],key)
                                maxList.append(self.listvalues[key][1][p])
                        else:
                            pass
                        inf += 1
                        u += 1
                        p += 1
                        row += 1
                    col += 1

        try:
        
            maxx = max(maxList)
            minn = min(maxList)
        except:
            pass

        try:
            while True:
                itemG = self.ui.verticalLayout_3.takeAt(0)
                if not itemG:
                    break
                self.ui.verticalLayout_3.removeWidget(itemG.widget())
        except AttributeError:
            pass
        
        try:
            for key in self.listvalues.keys():
                pp = 0
                uu = 0
                for item in self.listvalues[key][0]:
                    if maxx == float(self.listvalues[key][1][pp]):
                        itemTitle = item[0:34]+'\n'+item[34:len(item)]
                        if uu <= len(self.listvalues[key][2])-1:
                            self.ContentSatisticsWidget('max',0,key,itemTitle,maxx,self.listvalues[key][2][uu])

                    elif minn == float(self.listvalues[key][1][pp]):
                        itemTitle = item[0:34]+'\n'+item[34:len(item)]
                        if uu <= len(self.listvalues[key][2])-1:
                            self.ContentSatisticsWidget('min',0,key,itemTitle,minn,self.listvalues[key][2][uu])     
                    else:
                        pass
                    uu += 1
                    pp += 1
        except UnboundLocalError:
            pass
            

        

    def showIinfoWidget(self,Purl,key):
        self.ui.textBrowser.clear()
        if key == 'jumia':
            req = requests.get(Purl, headers=self.header)
            soup = BeautifulSoup(req.content, 'lxml')
            info = soup.find('div',{'class':'markup -mhm -pvl -oxa -sc'})
            try:
                self.ui.textBrowser.setPlainText(info.text)
            except AttributeError:
                self.ui.textBrowser.setPlainText('no information detected')
        

        elif key == 'Mega pc':
            req = requests.get(Purl, headers=self.header)
            soup = BeautifulSoup(req.content, 'lxml')
            info = soup.find('div',{'class':'p-formgrid p-fluid'}).text
            self.ui.textBrowser.setPlainText(str(info))
            #self.ui.textBrowser.setPlainText('no information detected')


        elif key == 'tunisianet':
            req = requests.get(Purl, headers=self.header)
            soup = BeautifulSoup(req.content, 'lxml')
            print(Purl)
            info = soup.find("div",{'class':'prodes'}).text
            self.ui.textBrowser.setPlainText(str(info))
            #self.ui.textBrowser.setPlainText('no information detected')

        

            


    def fnfilter(self,key,Price):
        try:
            newListPrice = []
            if key in ['jumia','Mega pc']:
                newPrice = ''
                for j in Price:
                    if j in ['0','1','2','3','4','5','6','7','8','9','.']:
                        newPrice += j
                newListPrice.append(str(float(newPrice)))

            elif key in ['tunisianet','mytek']:
                newPrice = ''
                for j in Price:
                    if j in ['0','1','2','3','4','5','6','7','8','9',',']:
                        newPrice += j
                newPrice = newPrice[0:newPrice.find(',')]+'.'+newPrice[-3:]
                newListPrice.append(str(float(newPrice)))
            return newPrice

        except ValueError:
            print("ERROR")


    def contentWidgetProduct(self,row,price='no price',title='no title',url='no url',key='no key'):
        self.frame = QtWidgets.QFrame(self.ui.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(600, 200))
        self.frame.setSizeIncrement(QtCore.QSize(0, 0))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(31, 31, 280, 41))
        self.label_2.setStyleSheet("font-size:16px;")
        self.label_2.setObjectName("label_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 90, 101, 23))
        self.pushButton_2.setStyleSheet("font: 11pt \"MS Shell Dlg 2\";\n"
"color: black;background:none;border:none;")
        self.pushButton_2.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"src/{key}.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setIconSize(QtCore.QSize(80, 16))
        self.pushButton_2.setToolTip(f"{key}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(30, 130, 111, 20))
        self.label_3.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";\n"
"font: 75 9pt \"MS Shell Dlg 2\";")
        self.label_3.setObjectName("label_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.frame)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 170, 75, 23))
        self.pushButton_4.setStyleSheet("background-color: rgb(27, 78, 117);\n"
"border-radius:10px;\n"
"color: rgb(255, 255, 255);")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.frame)
        self.pushButton_5.setGeometry(QtCore.QRect(100, 170, 75, 23))
        self.pushButton_5.setStyleSheet("background-color: rgb(195, 31, 31);\n"
"border-radius:10px;\n"
"color: rgb(255, 255, 255);")
        self.pushButton_5.setObjectName("pushButton_5")

        self.label_2.setText(title)
        self.label_3.setText(str(price))

        self.pushButton_4.setText('Show info')
        self.pushButton_5.setText('Acheter')

        self.ui.verticalLayout.addWidget(self.frame, row, QtCore.Qt.AlignHCenter)
        self.pushButton_4.clicked.connect(self.stackSwitch)
        self.pushButton_4.clicked.connect(lambda : self.showIinfoWidget(url,key))
        self.pushButton_5.clicked.connect(lambda : wb.open(url))
        self.ui.pushButton_3.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.page))




    def ContentSatisticsWidget(self,typeWidget,row,key='none',name='none',price='0',url='none'):
        
        self.frameSatistics = QtWidgets.QFrame(self.ui.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameSatistics.sizePolicy().hasHeightForWidth())
        self.frameSatistics.setSizePolicy(sizePolicy)
        self.frameSatistics.setMinimumSize(QtCore.QSize(220, 150))
        self.frameSatistics.setSizeIncrement(QtCore.QSize(0, 0))
        self.frameSatistics.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameSatistics.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameSatistics.setObjectName("frameSatistics")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frameSatistics)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout_2.setContentsMargins(-1, 10, -1, -1)
        self.verticalLayout_2.setSpacing(2)
        self.type = QtWidgets.QLabel(self.frameSatistics)
        self.type.setAlignment(QtCore.Qt.AlignCenter)
        self.type.setObjectName("type")
        self.verticalLayout_2.addWidget(self.type)
        self.ProductNameLabel = QtWidgets.QLabel(self.frameSatistics)
        self.ProductNameLabel.setObjectName("ProductNameLabel")
        self.verticalLayout_2.addWidget(self.ProductNameLabel)
        self.ProductsiteLogo = QtWidgets.QPushButton(self.frameSatistics)
        self.ProductsiteLogo.setStyleSheet("border-radius:none;\n"
"background-color:none;padding:5px;")
        self.ProductsiteLogo.setText("")
        self.ProductsiteLogo.setObjectName("ProductsiteLogo")
        self.verticalLayout_2.addWidget(self.ProductsiteLogo)
        self.ProductPriceLabel = QtWidgets.QLabel(self.frameSatistics)
        self.ProductPriceLabel.setObjectName("ProductPriceLabel")
        self.verticalLayout_2.addWidget(self.ProductPriceLabel)
        self.buttonShowInfoProduct = QtWidgets.QPushButton(self.frameSatistics)
        self.buttonShowInfoProduct.setText("Show info")
        self.buttonShowInfoProduct.setObjectName("buttonShowInfoProduct")
        self.verticalLayout_2.addWidget(self.buttonShowInfoProduct)
        self.buttonGetPrduct = QtWidgets.QPushButton(self.frameSatistics)
        self.buttonGetPrduct.setText("Acheter")
        self.buttonGetPrduct.setObjectName("buttonGetPrduct")
        self.verticalLayout_2.addWidget(self.buttonGetPrduct)
        self.ui.verticalLayout_3.addWidget(self.frameSatistics, row, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)


        self.type.setText(f'{typeWidget}')
        self.ProductNameLabel.setText(f"{name}")
        self.ProductPriceLabel.setText(f"{price}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"src/{key}.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ProductsiteLogo.setText("")
        self.ProductsiteLogo.setIcon(icon)
        self.ProductsiteLogo.setStyleSheet("font: 50pt \"MS Shell Dlg 2\";\n"
"color: black;background:none;border:none;padding:5px;")
        self.ProductsiteLogo.setIconSize(QtCore.QSize(80, 16))
        

        self.buttonShowInfoProduct.clicked.connect(self.stackSwitch)
        self.buttonShowInfoProduct.clicked.connect(lambda : self.showIinfoWidget(url,key))
        self.buttonShowInfoProduct.setStyleSheet("background-color: rgb(27, 78, 117);\n"
"border-radius:10px;\n")
        self.buttonGetPrduct.clicked.connect(lambda : wb.open(url))
        self.buttonGetPrduct.setStyleSheet("background-color: rgb(195, 31, 31);\n"
"border-radius:10px;\n"
"color: rgb(255, 255, 255);")
        self.ui.pushButton_3.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.page))




    def dialogueWidget(self,msg,BtnMsg):
        self.dialogue.dialo.pushButton.setText(f"{BtnMsg}")
        self.dialogue.dialo.label.setText(f"{msg}")
        self.dialogue.show()
        self.dialogue.dialo.pushButton.clicked.connect(lambda : self.dialogue.close())













app = QApplication(sys.argv)
win = MainWindow()
try:
    win.setStyleSheet(str(open('style.css','r').read()))
except:
    sys.exit()
win.show()
sys.exit(app.exec_())