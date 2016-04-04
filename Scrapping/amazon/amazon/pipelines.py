# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

class AmazonPipeline(object):
    def process_item(self, item, spider):
        self.storeInDb(item)
        return item
    def __init__(self):
        self.setupDBCon()
        self.createTables()

    def setupDBCon(self):
        self.con = sqlite3.connect('./Booknew.db') #Change this to your own directory
        self.cur = self.con.cursor()

    def createTables(self):
        self.dropAmazonTable()
        self.dropReviewTable()
        self.createReviewTable()
        self.createAmazonTable()
    def createAmazonTable(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Amazon(id INTEGER PRIMARY KEY NOT NULL, \
            pid TEXT, \
            name TEXT, \
            path TEXT, \
            price TEXT \
            )")
    
    def dropAmazonTable(self):
        #drop amazon table if it exists
        self.cur.execute("DROP TABLE IF EXISTS Amazon")
    def storeInDb(self,item):
        if item.get('Rid') == '':
            self.cur.execute("INSERT INTO Amazon(\
                pid, \
                name, \
                path, \
                price \
            ) \
            VALUES(?, ?, ?, ?)", \
            ( \
                item.get('Pid',''),
                item.get('Name',''),
                item.get('Path',''),
                item.get('Price',''),
            ))
            print '------------------------'
            print 'Data Stored in Database'
            print '------------------------'
            self.con.commit()
        else:
            self.cur.execute("INSERT INTO Review(\
                rid, \
                rname, \
                pid, \
                review \
            ) \
            VALUES(?, ?, ?, ?)", \
            ( \
                item.get('Rid',''),
                item.get('Rname',''),
                item.get('Pid',''),
                item.get('Review',''),
            ))
            print '------------------------'
            print 'Data Stored in Database'
            print '------------------------'
            self.con.commit()


    def createReviewTable(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Review(id INTEGER PRIMARY KEY NOT NULL, \
            rid TEXT, \
            rname TEXT, \
            pid TEXT, \
            review TEXT \
            )")
    
    def dropReviewTable(self):
        #drop amazon table if it exists
        self.cur.execute("DROP TABLE IF EXISTS Review")

    def closeDB(self):
        self.con.close()

    def __del__(self):
        self.closeDB()
