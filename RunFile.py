import os
import pickle
import time

######### Please provide a path to the folder that you put this script.
######### Note: It is not recommended to have spaces in the path: 
######### C:/Users/.../OneDrive - London Stock Exchange Group/Desktop/Projects/ 
######### Above example includes spaces and is not recommended.

path = r'C:/Users/U6087214/OneDrive - London Stock Exchange Group/Desktop/Projects/Client'

#########
######### You will get CSV files in the same path inside a new folder called "Result_CSV"
#########

csv_path = path +"/Result_CSV/"

# Calculating run time:
    
start = time.time()

# Generating a subfolder called "pickles"

if not os.path.exists(path +'/pickles/'):
    os.makedirs(path +'/pickles/')
    
# Changing directory to current path:
    
os.chdir(path)

# Reading pickle files:
    
allcontent = {} 
for root, dirs, files in os.walk("pickles"):
    for file in files:
        if file.endswith(".pickle"):
           name = file
           print(name)
           openfile = open(path + '/pickles/'+ name, 'rb')
           loadedfile = pickle.load(openfile)
           if 'Flow' in name:
               allcontent['Flow']=loadedfile
           elif 'Gen' in name:
               allcontent['Gen_Type']=loadedfile 
           elif 'NetImport' in name:
               allcontent['NetImport']=loadedfile 
           elif 'Price' in name:
               allcontent['PowerPrice']=loadedfile 
           elif 'Transmission' in name:
               allcontent['TransmissionCap']=loadedfile  

           openfile.close()

# Data wrangling:


year_col = {  0:'Normal',  1:'1991', 2:'1992', 3:'1993', 4:'1994', 5:'1995', 6:'1996', 7:'1997',
            8: '1998', 9:'1999', 10:'2000', 11:'2001', 12:'2002', 13:'2003', 14:'2004',
            15:'2005', 16:'2006', 17:'2007', 18:'2008', 19:'2009', 20:'2010', 21:'2011',
            22:'2012', 23:'2013', 24:'2014', 25:'2015'}

year_col1 = {  'One':'Normal',  'Two':'1991', 'Three':'1992', 'Four':'1993', 'Five':'1994', 'Six':'1995', 'Seven':'1996', 'Eight':'1997',
            'Nine': '1998', 'Ten':'1999', 'Eleven':'2000', 'Twelve':'2001', 'Thirteen':'2002', 'Fourteen':'2003', 'Fifteen':'2004',
            'Sixteen':'2005', 'Seventeen':'2006', 'Eighteen':'2007', 'Ninteen':'2008', 'Twenty':'2009', 'TwentyOne':'2010', 'TwentyTwo':'2011',
            'TwentyThree':'2012', 'TwentyFour':'2013', 'TwentyFive':'2014', 'TwentySix':'2015'}

flow = allcontent['Flow']
Gen_Type = allcontent['Gen_Type']
NetImport = allcontent['NetImport']
price = allcontent['PowerPrice']
TransmissionCap = allcontent['TransmissionCap']

# Generating CSV files inside the corresponding folders:
    
def csv_result(name,path,csv_path,year_col):
    if not os.path.exists(csv_path + "/"+name+"/"):
        os.makedirs(csv_path + "/"+name+"/")
        
    param = allcontent[name]
    for key in param:
        x = param[key]
        first_col = x.pop('Date')
        x.insert(0, 'Date', first_col)
        x.rename(columns=year_col, inplace=True)
        x.to_csv(csv_path + "/"+name+ "/"+ str(key) +'.csv',index=False)
        
csv_result("Flow",path,csv_path,year_col)
csv_result("PowerPrice",path,csv_path,year_col)
csv_result("NetImport",path,csv_path,year_col1)
csv_result("TransmissionCap",path,csv_path,year_col)

if not os.path.exists(csv_path + "/"+"Gen_type"+"/"):
    os.makedirs(csv_path + "/"+"Gen_type"+"/")
    
Gen_Type = allcontent['Gen_Type']

Nodes = ['DEU', 'AUT', 'FRA', 'BEL', 'NLD', 'NO2', 'DK1', 'GBR', 'ITA', 'ESP', 'CHE', 'CZE', 'DK2', 'POL', 'SE4', 'NO5']
Tech = ['CHP', 'Curtailment', 'Demand Shedding', 'Flexible Assets', 'Nuclear', 'Other', 'Pump', 'Res', 'ROR', 'Solar','BioFuels',
        'CH4', 'Coal', 'Lignite', 'Oil', 'Wind']

for key in Gen_Type:
    print(key)
    for n in Nodes:
        for tech in Tech:
            if n in key and tech in key :
                
                x = Gen_Type[key]
                first_col = x.pop('Date')
                x.insert(0, 'Date', first_col)
                x.rename(columns=year_col, inplace=True)
                x.to_csv(csv_path + "Gen_Type"+ "/"+ n+'_'+tech +'.csv',index=False)
                
            else:
                pass

# Calculating run time:
    
end = time.time()
print(f"Runtime of the program is {round((end - start)/60)} min")
    
    