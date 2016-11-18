# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import smtplib
from scrapy.mail import MailSender

class KrattPipeline(object):
    
    def open_spider(self, spider):
        self.file = open('items.jl', 'wb')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        
        FROM = "abimees@abimees.com"
        TO = "arneriso@gmail.com"
        SUBJECT = "pakkumine keskkonnast Abimees"
        TEXT = "siin on pakkumise sisu, mis on saadetud e-aadressile %s" % item['e_mail']
        
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.login('arneriso@gmail.com', "bjvojwaifrehpfrh")
        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, TO, SUBJECT, TEXT)
        server_ssl.sendmail(FROM, TO, message)
        server_ssl.close()
        
        return item