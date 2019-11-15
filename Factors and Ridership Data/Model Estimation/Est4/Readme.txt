{\rtf1\ansi\ansicpg1252\cocoartf2509
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 FAC SAMPLE CALCULATION excel file\
\
FAC_TOTALS_GT worksheet has the FAC calculation summarized by GT clusters.\
Differences worksheet contains the difference values from the Create Diff Files and Scatters.ipynb file.\
I calculated the percent differences from the previous year for years 2003 to 2018.\
To calculate that I merged the difference file with the original one, which is just the aggregate of UPT,VRM, POPEMP, GASPRICE, POP_CENSUSTRACT by clusters, mode and year.\
\
NOTE: Something is wrong with code that gets the difference values for RAIL. So for this example I am taking only the BUS mode.\
\
In the FAC worksheet, the example is for cluster ID 1 for Bus only. I haven\'92t figured out how to do the index-match yet. I could do it on python as well. The idea is if we change the Orange cell value the values on the following table would change as well.\
\
In this worksheet I put the percent change from the previous year, instead of the change value.\
}