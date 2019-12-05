#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, request
from flask_restful import Resource, Api
import pyodbc
from json import dumps
import json
import collections
from flask_jsonpify import jsonify
from gevent.pywsgi import WSGIServer


# In[2]:


conn =  pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=HMCA-SQL-PBI\AUTOLINK;DATABASE=AutoLink_Australia;Trusted_Connection=yes')
app = Flask(__name__)
api = Api(app)


# In[3]:


class VIN_Name(Resource):
    def get(self, VIN):
        cursor = conn.cursor()
        
        query = cursor.execute("select [VINNUM],[Type],[DRIVE_DIST],[Latest_Odometer]  FROM [AutoLink_Australia].[dbo].[UBI_Drive] where [VINNUM] = ?",(VIN))
        rows = query.fetchall()
        rowarray_list = []
        for row in rows:
            t = (row.VINNUM, row.Type, row.DRIVE_DIST, 
            row.Latest_Odometer)
            rowarray_list.append(t)
        j = json.dumps(rowarray_list)
        return jsonify(j)


# In[4]:


api.add_resource(VIN_Name, '/Vehicles/<VIN>')


# In[5]:


if __name__=='__main__':        
    #Run the applications
    app.run()


# In[ ]:




