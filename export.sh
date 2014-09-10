#!/bin/bash
exec > out.csv
/usr/bin/sqlite3 Medicare.db <<!
.headers on
.mode csv
.output out.csv
Select * from InpatientVisits;
!
