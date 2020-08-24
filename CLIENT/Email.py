import smtplib, email, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
# import mysql.connector
from datetime import datetime
import time


class Email_Chn:
	def __init__(self):
		pass

#chnNo,plateno,date,name,location,vehicletype,tuple(OffenceList),challancount,conn)


	def SendMail(self,email,chnNo,plateno,date,name,location,docPath):
		fail_safe = 0
		while True:
			try:
				fail_safe+=1
				self.SendMail_1(email,chnNo,plateno,date,name,location,docPath)
				break
			except Exception as e:
				print(e)
				if fail_safe >= 3:
					break
				print("Trying Again...!")
				


	def SendMail_1(self,email,chnNo,plateno,date,name,location,docPath):
		try:
			print("working on email To :",email)

			msg = MIMEMultipart()
			msg["Subject"] = "ASCV Visitor Update"
			msg["From"] = "Alert <{0}>".format(email)
			msg["To"] = email
			#================================

			s = smtplib.SMTP_SSL("smtp.gmail.com:465")
			s.login("tangov.2508@gmail.com","Tango@123")


			with open('logo.png', 'rb') as f:
			    # set attachment mime and file name, the image type is png
			    mime = MIMEBase('image', 'png', filename='img1.png')
			    # add required header data:
			    mime.add_header('Content-Disposition', 'attachment', filename='img1.png')
			    mime.add_header('X-Attachment-Id', '0')
			    mime.add_header('Content-ID', '<0>')
			    # read attachment file content into the MIMEBase object
			    mime.set_payload(f.read())
			    # encode with base64
			    encoders.encode_base64(mime)
			    # add MIMEBase object to MIMEMultipart object
			    msg.attach(mime)
			
			# MailMsg0 = """<div style='background-color : #0099CC; padding: 3px;'><img src=""data:image/jpg;base64,{}""/></div>""".format({imgbase64})
			# msg.attach(MIMEText(MailMsg0,"html"))

			MailMsg01 = """<div style='background-color : #66CCFF; padding: 3px;'><img src="cid:0"/></div>"""
			msg.attach(MIMEText(MailMsg01,"html"))

			str1 = """
			<body style='background-color : #66CCFF'><center><h1> This Mail is from Autometic E-Challan System. </h1></<center>
			<div style='background-color :	 #CCFFCC'>
				<table style="width:100%">
				  <tr>
				    <td style="border: 2px solid black" ><h4>Challan Number :</h4></td>
				    <td style="border: 2px solid black" ><h4>{0}</h4></td>
				  </tr>
				  <tr>
				    <td style="border: 2px solid black" ><h4>Name :</h4></td>
				    <td style="border: 2px solid black" ><h4>{1}</h4></td>
				  </tr>
				  <tr>
				    <td style="border: 2px solid black" ><h4>Plate Number :</h4></td>
				    <td style="border: 2px solid black" ><h4>{2}</h4></td>
				  </tr>
				  <tr>
				    <td style="border: 2px solid black" ><h3>Location :</h3></td>
				    <td style="border: 2px solid black" ><h3>{3}</h3></td>
				  </tr>
				 </table>
			  </div>
			  </body>
			""".format(chnNo,name,plateno,location)
			msg.attach(MIMEText(str1,"html"))

			with open(docPath, "rb") as f:
				#attach = email.mime.application.MIMEApplication(f.read(),_subtype="pdf")
				attach = MIMEApplication(f.read(),_subtype="pdf")
			attach.add_header('Content-Disposition','attachment',filename=str(docPath))
			msg.attach(attach)

			s.sendmail("tangov.2508@gmail.com", email, msg.as_string())
			print("email sent")
		except Exception as e:
			print("Got Problem",e)
			raise Exception



if __name__ == '__main__':
	Db_H = Email_Chn()
	email = "manan8999@gmail.com"
	Db_H.SendMail(email,"INDGUJ1234","GJO1MN3999","date","Manan Darji","Akhabarnagar","img/INGJAH2162.pdf")
	print("sent")