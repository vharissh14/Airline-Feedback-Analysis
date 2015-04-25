
														#################
														## Web Crawler ##
														#################

##############
## Packages ##
##############

from BeautifulSoup import BeautifulSoup
import requests
import re
from pattern import web
from pattern.web import plaintext, strip_between
import json

page=['af','af_3','sia','sia_1a','sia_1b','sia_1c','air_asia','kingfisher','qatar','emrts']
i=j=0
Cus_review=[]
overall_cus_count=0

for p in page:
     list_rev,list3,cus_name,list1,list2,customer_name,cus_comments=([] for i in range(7))
     iter=cus_no=0
     temp_list=[]
     url="http://www.airlinequality.com/Forum/"+p+".htm"
     html_txt=requests.get(url).text
     dom=web.Element(html_txt)
     i+=1
     title=dom.by_tag('title')[0].content.encode('utf-8')
     air_title=re.sub(r'Customer .*',"",title)
     print '\n'
     print "page %d"%(i,)
     for x in dom.by_tag('p.text2'):
           no_format = plaintext(x.content)
           comment = re.sub( '\s+', ' ', no_format).strip().encode('utf-8')
           if (comment!='PAGE 1 2 3 4 5 6 7 8 9 10') and (comment!=''):
           	cus_comments.append(comment)
           	j+=1
           	print "%d.."%(j),
     
     for y in dom.by_tag('h9'):
     	date_mon = plaintext(y.content)
        date_m = re.sub( '\s+', ' ', date_mon).strip().encode('utf-8')
        searchObj = re.search( r'(.*) [0-9]+', date_m, re.M|re.I)
        p1=re.search(r'[A-Za-z]+ [0-9]+',searchObj.group(),re.M|re.I)
        list2.append(p1.group())

     html_txt=requests.get(url).text
     soup=BeautifulSoup(html_txt)
     tabletag=soup.findAll('table', {'width': '192'})
     name=soup.findAll('td',{'class':'airport'})

     for name1 in name:
     	cus_name.append(name1.text)

     for name1 in cus_name:
         name1=re.sub(r'(.*) by ','',name1)
         name2=re.sub(r'[&(].*','',name1)
         name3=re.sub(r'nbsp','',name2)
         customer_name.append(name3.strip())
                                                                                                                                                    
     for tag in tabletag:
	     tdtag=tag.findAll('td')
	     for tag in tdtag:
		     imgtag=tag.findAll('img')
		     for tag in imgtag:
			     list3.append(tag['src'])

     def assign(temp_list,Cus_review):
    	Cus_review.append({"Customer_name":temp_list[0],"air_title":temp_list[1],"month":temp_list[2],"reviews":temp_list[3],"Rating":temp_list[4],"Value for money":temp_list[5],"Seat Comfort":temp_list[6],"Staff Service":temp_list[7],"Catering":temp_list[8],"Entertainment":temp_list[9],"Recommended":temp_list[10]})
    	return Cus_review

     

     temp_list.append(customer_name[cus_no].encode('utf-8'))
     temp_list.append(air_title.encode('utf-8'))
     temp_list.append(list2[cus_no].encode('utf-8'))
     temp_list.append(cus_comments[cus_no])
     for x in list3:
          y=re.sub('[./_A-Za-z]', '', x)
	  d=re.sub(r'7361','',y)
	  yes=re.search(r'YES',x,re.M|re.I)
	  no=re.search(r'NO',x,re.M|re.I)
	  if yes:
			d="yes" 
	  if no:
		 	d="no"
	  temp_list.append(d.encode('utf-8'))
	  iter+=1
	  if iter==7:
	    Cus_review_table=assign(temp_list,Cus_review)
	    temp_list=[]
	    cus_no+=1
	    if (cus_no != len(customer_name)):
	     temp_list.append(customer_name[cus_no].encode('utf-8'))
	     temp_list.append(air_title.encode('utf-8'))
	     temp_list.append(list2[cus_no].encode('utf-8'))
	     temp_list.append(cus_comments[cus_no])
	    iter=0
     
     
     for x in range(len(Cus_review)):
     	f=open("cmt/cmt_0%d.txt"%(x,),"wb+")
     	f.write(json.dumps(Cus_review[x]))
     	f.close()


####################################################################################
####                            /* __Project_Lab__ */                           ####
#### __Project_Title__: Airline Feedback Analysis                               ####
#### __Domain__: NLP, Data Mining, Artificial Intelligence                      ####
#### __College__: College of Engineering, Guildy, Anna University               ####
#### __Branch__: B.E Computer Science & Engineering                             ####
#### __Semester__: Six __Semester__                                             ####
#### __Technology_Used__: Python & Qlikview                                     ####
#### __Done_by__: 1>Sree Harissh Venu (2012-103-072)                            ####
####              2>Vignesh Mohan (2012-103-082)                                ####
#### __Date__: 25th March 2015                                                  ####
####                                                                            ####
####################################################################################
