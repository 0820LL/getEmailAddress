import urllib2
import re
from threading import Thread

class get_mail(Thread):
    def __init__(self, a, b):
        Thread.__init__(self)
        self.a = a
        self.b = b
    def run(self):
        mails = []
        o_china = 'out_china'+str(self.a)
        o_notchina = 'out_notchina'+str(self.a)
        out = open(o_china, 'w')
        out = open(o_notchina, 'w')
        for i in range(self.a, self.b):
        #for i in range(15000000,25100000):
            try:
                url = urllib2.urlopen('http://www.ncbi.nlm.nih.gov/pubmed/?term=%s[uid]' % i, timeout = 5)

                for html in url:
                    if not html.find('@'):
                        continue
                    mails = re.findall(r'[\w+|\.]+@[\w|\.]+',html)
                    for mail in mails:
                        if mail != 'PubMedGroup@1.55' and mail != '' and mail != 'term+@rn':
                            #address=re.findall(r'',html)
                            if re.search(r'edu.cn$', mail):
                                out_china.write('%d\t%s\n' % (i, mail))
                            else:
                                out_notchina.write('%d\t%s\n' % (i, mail))
            except:
                pass
            finally:
                pass
def main():
    for i in [ 14000000+j*1000000 for j in range(1,11)]:
        thread_name = 'test'+str(i)
        thread_name = get_mail(i, i+1000000)
        thread_name.start()

if __name__ == '__main__':
    main()
