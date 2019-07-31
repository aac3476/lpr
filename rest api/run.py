# -*- coding: utf-8 -*-  
"""
Create on 07-26 9:17 2019
@Author ywx 
@File run.py
"""

from app import app

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8801,debug=True)
