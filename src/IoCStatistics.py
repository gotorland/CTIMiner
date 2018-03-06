'''
Created on Sep 7, 2016

This script implements the class to analyze the statistical features of CTI collected from the parser and the malware repository.

@author: Andrew D. Kim (aka Daegeon Kim)
'''
import os.path, subprocess, sys
from xlrd import open_workbook
import xml.etree.ElementTree as ET

class IoCStatistics:
    statistic_fname = 'IoCStatistics.xml'
    
    stat_general = {}
    stat_category1 = {}
    stat_category2 = {}
    stat_category3 = {}
    stat_category4 = {}
    stat_category5 = {}
    stat_tmp_general = {}
    stat_tmp_category1 = {}
    stat_tmp_category2 = {}
    stat_tmp_category3 = {}
    stat_tmp_category4 = {}
    stat_tmp_category5 = {}
    sharedIoC = []
    
    report_name = None
    report_type = None      # the file type of APT report either pdf, xls or txt
    report_buf = None       # the buffer containing the report contents
    
    
    def __init__(self):
        if os.path.isfile(self.statistic_fname):
            tree = ET.parse(self.statistic_fname)
            root = tree.getroot()
            
            self.stat_general['Num_Of_Report'] = int(root.find('Num_Of_Report').text)
            self.stat_general['Num_Of_Hashes_In_Report'] = int(root.find('Num_Of_Hashes_In_Report').text)
            self.stat_general['Num_Of_Hashes_Analyzed_From_Repository'] = int(root.find('Num_Of_Hashes_Analyzed_From_Repository').text)
            self.stat_general['Num_Of_Hashes_Additionaly_Analyzed_From_Repository'] = int(root.find('Num_Of_Hashes_Additionaly_Analyzed_From_Repository').text)
            
            for category in root.findall('category'):
                category_type = category.get('type')
                if category_type == 'category1':
                    tmp_category = self.stat_category1
                elif category_type == 'category2':
                    tmp_category = self.stat_category2
                elif category_type == 'category3':
                    tmp_category = self.stat_category3
                elif category_type == 'category4':
                    tmp_category = self.stat_category4
                elif category_type == 'category5':
                    tmp_category = self.stat_category5
                tmp_category['count'] = int(category.find('count').text)
                tmp_category['ip'] = int(category.find('ip').text)
                tmp_category['host'] = int(category.find('host').text)
                tmp_category['email'] = int(category.find('email').text)
                tmp_category['cve'] = int(category.find('cve').text)
                tmp_category['filename'] = int(category.find('filename').text)
                tmp_category['filepath'] = int(category.find('filepath').text)
                tmp_category['signcheck'] = int(category.find('signcheck').text)
                tmp_category['hash'] = int(category.find('hash').text)
                tmp_category['string'] = int(category.find('string').text)
                        
        else:
            self.stat_general = dict(Num_Of_Report=0, Num_Of_Hashes_In_Report=0, Num_Of_Hashes_Analyzed_From_Repository=0, Num_Of_Hashes_Additionaly_Analyzed_From_Repository=0)
            self.stat_category1 = dict(count=0, ip=0, host=0, email=0, cve=0, filename=0, filepath=0, signcheck=0, hash=0, string=0)
            self.stat_category2 = dict(count=0, ip=0, host=0, email=0, cve=0, filename=0, filepath=0, signcheck=0, hash=0, string=0)
            self.stat_category3 = dict(count=0, ip=0, host=0, email=0, cve=0, filename=0, filepath=0, signcheck=0, hash=0, string=0)
            self.stat_category4 = dict(count=0, ip=0, host=0, email=0, cve=0, filename=0, filepath=0, signcheck=0, hash=0, string=0)
            self.stat_category5 = dict(count=0, ip=0, host=0, email=0, cve=0, filename=0, filepath=0, signcheck=0, hash=0, string=0)
    
        self.initTempStatistics()
    
    
    def initTempStatistics(self):
        self.stat_tmp_general = dict(Num_Of_Report=0,Num_Of_Hashes_In_Report=0,Num_Of_Hashes_Analyzed_From_Repository=0,Num_Of_Hashes_Additionaly_Analyzed_From_Repository=0)
        self.stat_tmp_category1 = dict(count=0, ip=0, host=0, email=0, cve=0, filename=0, filepath=0, signcheck=0, hash=0, string=0)
        self.stat_tmp_category2 = dict(count=0, ip=0, host=0, email=0, cve=0, filename=0, filepath=0, signcheck=0, hash=0, string=0)
        self.stat_tmp_category3 = dict(count=0, ip=0, host=0, email=0, cve=0, filename=0, filepath=0, signcheck=0, hash=0, string=0)
        self.stat_tmp_category4 = dict(count=0, ip=0, host=0, email=0, cve=0, filename=0, filepath=0, signcheck=0, hash=0, string=0)
        self.stat_tmp_category5 = dict(count=0, ip=0, host=0, email=0, cve=0, filename=0, filepath=0, signcheck=0, hash=0, string=0)
    
    
    def checkIoCInReport(self, ioc):
        if self.report_type == 'xls':
            for row in range(self.report_buf.nrows):
                for col in range(self.report_buf.ncols):
                    try:
                        if self.report_buf.cell(row,col).value == ioc.encode('utf-8').lower():
                            return True
                    except UnicodeError: 
                        if self.report_buf.cell(row,col).value == ioc.lower():
                            return True
#                        print UnicodeError.message+' while executing checkIoCInReport function'
#                        print 'The original IoC: '+ ioc + ' '
            return False
        else:
            if ioc.encode('utf-8').lower() in self.report_buf:
                return True
            else:
                return False
   
        
    def finalizeTempStatistics(self):
        self.stat_general['Num_Of_Report'] += 1
        self.stat_general['Num_Of_Hashes_In_Report'] += self.stat_tmp_general['Num_Of_Hashes_In_Report']
        self.stat_general['Num_Of_Hashes_Analyzed_From_Repository'] += self.stat_tmp_general['Num_Of_Hashes_Analyzed_From_Repository']
        self.stat_general['Num_Of_Hashes_Additionaly_Analyzed_From_Repository'] += self.stat_tmp_general['Num_Of_Hashes_Additionaly_Analyzed_From_Repository']
        
        self.stat_category1['count'] += self.stat_tmp_category1['count']
        self.stat_category1['ip'] += self.stat_tmp_category1['ip']
        self.stat_category1['host'] += self.stat_tmp_category1['host']
        self.stat_category1['email'] += self.stat_tmp_category1['email']
        self.stat_category1['cve'] += self.stat_tmp_category1['cve']
        self.stat_category1['filename'] += self.stat_tmp_category1['filename']
        self.stat_category1['filepath'] += self.stat_tmp_category1['filepath']
        self.stat_category1['signcheck'] += self.stat_tmp_category1['signcheck']
        self.stat_category1['hash'] += self.stat_tmp_category1['hash']
        self.stat_category1['string'] += self.stat_tmp_category1['string']
        
        self.stat_category2['count'] += self.stat_tmp_category2['count']
        self.stat_category2['ip'] += self.stat_tmp_category2['ip']
        self.stat_category2['host'] += self.stat_tmp_category2['host']
        self.stat_category2['email'] += self.stat_tmp_category2['email']
        self.stat_category2['cve'] += self.stat_tmp_category2['cve']
        self.stat_category2['filename'] += self.stat_tmp_category2['filename']
        self.stat_category2['filepath'] += self.stat_tmp_category2['filepath']
        self.stat_category2['signcheck'] += self.stat_tmp_category2['signcheck']
        self.stat_category2['hash'] += self.stat_tmp_category2['hash']
        self.stat_category2['string'] += self.stat_tmp_category2['string']
        
        self.stat_category3['count'] += self.stat_tmp_category3['count']
        self.stat_category3['ip'] += self.stat_tmp_category3['ip']
        self.stat_category3['host'] += self.stat_tmp_category3['host']
        self.stat_category3['email'] += self.stat_tmp_category3['email']
        self.stat_category3['cve'] += self.stat_tmp_category3['cve']
        self.stat_category3['filename'] += self.stat_tmp_category3['filename']
        self.stat_category3['filepath'] += self.stat_tmp_category3['filepath']
        self.stat_category3['signcheck'] += self.stat_tmp_category3['signcheck']
        self.stat_category3['hash'] += self.stat_tmp_category3['hash']
        self.stat_category3['string'] += self.stat_tmp_category3['string']
        
        self.stat_category4['count'] += self.stat_tmp_category4['count']
        self.stat_category4['ip'] += self.stat_tmp_category4['ip']
        self.stat_category4['host'] += self.stat_tmp_category4['host']
        self.stat_category4['email'] += self.stat_tmp_category4['email']
        self.stat_category4['cve'] += self.stat_tmp_category4['cve']
        self.stat_category4['filename'] += self.stat_tmp_category4['filename']
        self.stat_category4['filepath'] += self.stat_tmp_category4['filepath']
        self.stat_category4['signcheck'] += self.stat_tmp_category4['signcheck']
        self.stat_category4['hash'] += self.stat_tmp_category4['hash']
        self.stat_category4['string'] += self.stat_tmp_category4['string']
        
        self.stat_category5['count'] += self.stat_tmp_category5['count']
        self.stat_category5['ip'] += self.stat_tmp_category5['ip']
        self.stat_category5['host'] += self.stat_tmp_category5['host']
        self.stat_category5['email'] += self.stat_tmp_category5['email']
        self.stat_category5['cve'] += self.stat_tmp_category5['cve']
        self.stat_category5['filename'] += self.stat_tmp_category5['filename']
        self.stat_category5['filepath'] += self.stat_tmp_category5['filepath']
        self.stat_category5['signcheck'] += self.stat_tmp_category5['signcheck']
        self.stat_category5['hash'] += self.stat_tmp_category5['hash']
        self.stat_category5['string'] += self.stat_tmp_category5['string']

        
    def setReportBuffer(self, fname):
        if fname.lower().endswith('.pdf'):
            self.report_type = 'pdf'
            scripts_path = ''
            if os.name == 'nt':
                scripts_path = sys.prefix+'/Scripts'
            elif os.name == 'posix':
                scripts_path = '/usr/local/bin' 
                
            try:
                self.report_buf = subprocess.check_output('python '+scripts_path+'/pdf2txt.py \"'+fname+'\"', shell=True).lower()
            except UnicodeError or subprocess.CalledProcessError:
                if UnicodeError:
                    print UnicodeError.message
                elif subprocess.CalledProcessError:
                    print subprocess.CalledProcessError.message
            
        elif fname.lower().endswith('.xls') or fname.lower().endswith('.xlsx'):
            self.report_type = 'xls'
            self.report_buf = open_workbook(fname).sheet_by_index(0)
            
            for row in range(self.report_buf.nrows):
                for col in range(self.report_buf.ncols):
                    try:
                        self.report_buf.cell(row,col).value = self.report_buf.cell(row,col).value.encode('utf-8').lower()
                    except UnicodeError:
                        print UnicodeError.message+'\n'+self.report_buf.cell(row,col).value
                        
        else:
            self.report_type = 'etc'
            try:
                self.report_buf = open(fname, 'r').read().encode('utf-8').lower()
            except UnicodeError:
                print UnicodeError.message
            
        self.report_name = fname
        return
    
    def flushReportBuffer(self):
        self.report_type = None
        self.report_buf = None
        self.report_name = None
        
        
    def reset(self):
        self.flushReportBuffer()
        self.initTempStatistics()
        self.sharedIoC = []
        
        
    def saveIoCStatistics(self):
        root = ET.Element('IoCStatistics')
        ET.SubElement(root, 'Num_Of_Report').text = str(self.stat_general['Num_Of_Report'])
        ET.SubElement(root, 'Num_Of_Hashes_In_Report').text = str(self.stat_general['Num_Of_Hashes_In_Report'])
        ET.SubElement(root, 'Num_Of_Hashes_Analyzed_From_Repository').text = str(self.stat_general['Num_Of_Hashes_Analyzed_From_Repository'])
        ET.SubElement(root, 'Num_Of_Hashes_Additionaly_Analyzed_From_Repository').text = str(self.stat_general['Num_Of_Hashes_Additionaly_Analyzed_From_Repository'])
        
        category1 = ET.SubElement(root, 'category', attrib=dict(type='category1'))
        ET.SubElement(category1, 'count').text = str(self.stat_category1['count'])
        ET.SubElement(category1, 'ip').text = str(self.stat_category1['ip'])
        ET.SubElement(category1, 'host').text = str(self.stat_category1['host'])
        ET.SubElement(category1, 'email').text = str(self.stat_category1['email'])
        ET.SubElement(category1, 'cve').text = str(self.stat_category1['cve'])
        ET.SubElement(category1, 'filename').text = str(self.stat_category1['filename'])
        ET.SubElement(category1, 'filepath').text = str(self.stat_category1['filepath'])
        ET.SubElement(category1, 'signcheck').text = str(self.stat_category1['signcheck'])
        ET.SubElement(category1, 'hash').text = str(self.stat_category1['hash'])
        ET.SubElement(category1, 'string').text = str(self.stat_category1['string'])
        
        category2 = ET.SubElement(root, 'category', attrib=dict(type = 'category2'))
        ET.SubElement(category2, 'count').text = str(self.stat_category2['count'])
        ET.SubElement(category2, 'ip').text = str(self.stat_category2['ip'])
        ET.SubElement(category2, 'host').text = str(self.stat_category2['host'])
        ET.SubElement(category2, 'email').text = str(self.stat_category2['email'])
        ET.SubElement(category2, 'cve').text = str(self.stat_category2['cve'])
        ET.SubElement(category2, 'filename').text = str(self.stat_category2['filename'])
        ET.SubElement(category2, 'filepath').text = str(self.stat_category2['filepath'])
        ET.SubElement(category2, 'signcheck').text = str(self.stat_category2['signcheck'])
        ET.SubElement(category2, 'hash').text = str(self.stat_category2['hash'])
        ET.SubElement(category2, 'string').text = str(self.stat_category2['string'])
        
        category3 = ET.SubElement(root, 'category', attrib=dict(type = 'category3'))
        ET.SubElement(category3, 'count').text = str(self.stat_category3['count'])
        ET.SubElement(category3, 'ip').text = str(self.stat_category3['ip'])
        ET.SubElement(category3, 'host').text = str(self.stat_category3['host'])
        ET.SubElement(category3, 'email').text = str(self.stat_category3['email'])
        ET.SubElement(category3, 'cve').text = str(self.stat_category3['cve'])
        ET.SubElement(category3, 'filename').text = str(self.stat_category3['filename'])
        ET.SubElement(category3, 'filepath').text = str(self.stat_category3['filepath'])
        ET.SubElement(category3, 'signcheck').text = str(self.stat_category3['signcheck'])
        ET.SubElement(category3, 'hash').text = str(self.stat_category3['hash'])
        ET.SubElement(category3, 'string').text = str(self.stat_category3['string'])
        
        category4 = ET.SubElement(root, 'category', attrib=dict(type = 'category4'))
        ET.SubElement(category4, 'count').text = str(self.stat_category4['count'])
        ET.SubElement(category4, 'ip').text = str(self.stat_category4['ip'])
        ET.SubElement(category4, 'host').text = str(self.stat_category4['host'])
        ET.SubElement(category4, 'email').text = str(self.stat_category4['email'])
        ET.SubElement(category4, 'cve').text = str(self.stat_category4['cve'])
        ET.SubElement(category4, 'filename').text = str(self.stat_category4['filename'])
        ET.SubElement(category4, 'filepath').text = str(self.stat_category4['filepath'])
        ET.SubElement(category4, 'signcheck').text = str(self.stat_category4['signcheck'])
        ET.SubElement(category4, 'hash').text = str(self.stat_category4['hash'])
        ET.SubElement(category4, 'string').text = str(self.stat_category4['string'])
        
        category5 = ET.SubElement(root, 'category', attrib=dict(type = 'category5'))
        ET.SubElement(category5, 'count').text = str(self.stat_category5['count'])
        ET.SubElement(category5, 'ip').text = str(self.stat_category5['ip'])
        ET.SubElement(category5, 'host').text = str(self.stat_category5['host'])
        ET.SubElement(category5, 'email').text = str(self.stat_category5['email'])
        ET.SubElement(category5, 'cve').text = str(self.stat_category5['cve'])
        ET.SubElement(category5, 'filename').text = str(self.stat_category5['filename'])
        ET.SubElement(category5, 'filepath').text = str(self.stat_category5['filepath'])
        ET.SubElement(category5, 'signcheck').text = str(self.stat_category5['signcheck'])
        ET.SubElement(category5, 'hash').text = str(self.stat_category5['hash'])
        ET.SubElement(category5, 'string').text = str(self.stat_category5['string'])
        
        tree = ET.ElementTree(root)
        tree.write(self.statistic_fname)
        return
        
    def convertIoCType(self, ioc_type):
        if ioc_type=='ip' or ioc_type=='host' or ioc_type=='email' or ioc_type=='cve' or ioc_type=='filename' or ioc_type=='filepath' or ioc_type=='signcheck' or ioc_type=='hash' or ioc_type=='string':
            return ioc_type
        elif  ioc_type=='ip' or ioc_type=='src_ip' or ioc_type=='dest_ip':
            return 'ip'
        elif  ioc_type=='md5' or ioc_type=='sha1' or ioc_type=='sha256':
            return 'hash'
        else:
            return 'string'
    
    # category 1
    def addCategory1(self, data_type):
        self.stat_tmp_category1[data_type] += 1
        self.stat_tmp_category1['count'] += 1
        
    # category 2
    def addCategory2(self, data_type):
        self.stat_tmp_category2[data_type] += 1
        self.stat_tmp_category2['count'] += 1
        
    # category 3
    def addCategory3(self, ioc, data_type):
        if ioc not in self.sharedIoC:
            self.stat_tmp_category2[data_type] -= 1
            self.stat_tmp_category2['count'] -= 1
            self.stat_tmp_category3[data_type] += 1
            self.stat_tmp_category3['count'] += 1
            self.sharedIoC.append(ioc)           
            
    # category 4
    def addCategory4(self, data_type):
        self.stat_tmp_category4[data_type] += 1
        self.stat_tmp_category4['count'] += 1
        
    # category 5
    def addcategory5(self, data_type):
        self.stat_tmp_category5[data_type] += 1
        self.stat_tmp_category5['count'] += 1
        
    def increaseHashInReport(self):
        self.stat_tmp_general['Num_Of_Hashes_In_Report'] += 1
        
    def increaseAnalyzedHash(self):
        self.stat_tmp_general['Num_Of_Hashes_Analyzed_From_Repository'] += 1
        
    def increaseAnalyzedAdditionalHash(self):
        self.stat_tmp_general['Num_Of_Hashes_Additionaly_Analyzed_From_Repository'] += 1
        
    def increaseNumberOfReport(self):
        self.stat_tmp_general['Num_Of_Report'] += 1
        
'''        
if __name__ == '__main__':
    stat = IoCStatistics()
    ret = stat.checkIoCType('Embedded', '/Users/Andrew/Downloads/p795.pdf')
    print ret
'''

        