#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from django.core import management
from django.db import connection
from chws.models import *
from xlrd import open_workbook ,cellname,XL_CELL_NUMBER,XLRDError

def build_locations():
    try:
        create_nation()
        import_provinces()
        import_districts()
        import_sectors()
        import_cells()
        import_villages()
        import_facilities()
        
        return True
    except Exception, e:
        print e
        return False
    
def create_nation(name = "Rwanda", code = '00'):
    try:
        nation = Nation(name = name, code = code)
        nation.save()
        return True
    except Exception:
        return False

def import_location(filepath, sheetname, startrow, maxrow, coderow, namerow):
    #print filepath
    #print sheetname
    #print startrow
    #print maxrow
    #print coderow 
    #print namerow
    book = open_workbook(filepath)
    sheet = book.sheet_by_name(sheetname)
    #print sheet.name,sheet.nrows
    #print sheet.cell(startrow,coderow-1).value,sheet.cell(startrow,namerow-1).value
    #print sheet.cell(maxrow-1,coderow-1).value,sheet.cell(maxrow-1,namerow-1).value
    ans = []
    for row_index in range(sheet.nrows):
        if row_index < 1: continue
        #print sheet.cell(row_index,coderow-1).value, sheet.cell(row_index,namerow-1).value
        code = sheet.cell(row_index,coderow-1).value
        name = sheet.cell(row_index,namerow-1).value
        try:
            ans.append({'code' : code, 'name' : name})
        except: continue

    return ans

def import_provinces(filepath = "apps/chws/xls/locations.xls", sheetname = "PROVINCES", startrow = 1, maxrow = 416, coderow = 1, namerow = 2):
    locs = []
    cnt = import_location(filepath, sheetname, startrow, maxrow, coderow, namerow)
    for c in cnt:
        try:
            code , name = c['code'], c['name']
            nation   = Nation.objects.get(code = "00")
            province = Province( code = code , name = name , nation = nation)
            province.save()
        except Exception ,e:
            locs.append({'code' : c['code'], 'name': c['name'], 'error': e})            
            continue
    return locs


def import_districts(filepath = "apps/chws/xls/locations.xls", sheetname = "DISTRICTS", startrow = 1, maxrow = 416, coderow = 1, namerow = 2):
    locs = []
    cnt = import_location(filepath, sheetname, startrow, maxrow, coderow, namerow)
    for c in cnt:
        try:
            code , name = c['code'], c['name']
            province = Province.objects.get( code = code [0:len(code)-2] )
            district = District( code = code , name = name , province = province , nation = province.nation)
            district.save()
        except Exception ,e:
            locs.append({'code' : c['code'], 'name': c['name'], 'error': e})            
            continue
    return locs


def import_sectors(filepath = "apps/chws/xls/locations.xls", sheetname = "SECTORS", startrow = 1, maxrow = 416, coderow = 1, namerow = 2):
    locs = []
    cnt = import_location(filepath, sheetname, startrow, maxrow, coderow, namerow)
    for c in cnt:
        try:
            code , name = c['code'], c['name']
            district = District.objects.get( code = code [0:len(code)-2] )
            sector = Sector( code = code , name = name , district = district , province = district.province, nation = district.nation)
            sector.save()
        except Exception ,e:
            locs.append({'code' : c['code'], 'name': c['name'], 'error': e})            
            continue
    return locs


def import_cells(filepath = "apps/chws/xls/locations.xls", sheetname = "CELLS", startrow = 1, maxrow = 2222, coderow = 1, namerow = 2):
    locs = []
    cnt = import_location(filepath, sheetname, startrow, maxrow, coderow, namerow)
    for c in cnt:
        try:
            code , name = c['code'], c['name']
            sector = Sector.objects.get( code = code [0:len(code)-2] )
            cell = Cell( code = code , name = name , sector = sector , district = sector.district, province = sector.province, nation = sector.nation)
            cell.save()
        except Exception ,e:
            locs.append({'code' : c['code'], 'name': c['name'], 'error': e})            
            continue
    return locs

def import_villages(filepath = "apps/chws/xls/locations.xls", sheetname = "VILLAGES", startrow = 1, maxrow = 14584, coderow = 1, namerow = 2):
    locs = []
    cnt = import_location(filepath, sheetname, startrow, maxrow, coderow, namerow)
    for c in cnt:
        try:
            code , name = c['code'], c['name']
            cell = Cell.objects.get( code = code [0:len(code)-2] )
            village = Village( code = code , name = name , cell = cell, sector = cell.sector, district = cell.district, province = cell.province, nation = cell.nation)
            village.save()
        except Exception, e:
            locs.append({'code' : c['code'], 'name': c['name'], 'error': e})            
            continue
    return locs


def import_facilities(filepath = "apps/chws/xls/facilities.xls", sheetname = "FACILITIES", startrow = 1, maxrow = 616, codecol = 1, typecol = 2, namecol = 3, prvccol = 4, prvncol = 5, dstccol = 6, dstncol = 7, sctncol = 8, latcol = 9, longcol = 10, popcol = 11, popycol = 12):
    locs = []
    book = open_workbook(filepath)
    sheet = book.sheet_by_name(sheetname)
    i = j=0
    for row_index in range(sheet.nrows):
        if row_index < 1: continue
        try:
            #print sheet.cell(row_index,coderow-1).value, sheet.cell(row_index,namerow-1).value
            code     = str(int(float(sheet.cell(row_index,codecol-1).value)))
            name     = sheet.cell(row_index,namecol-1).value
            type     = sheet.cell(row_index,typecol-1).value
            nation   = Nation.objects.get (code = '00')
            province = Province.objects.get(code = sheet.cell(row_index,prvccol-1).value)
            district = District.objects.get(code = sheet.cell(row_index,dstccol-1).value )
            sector   = None
            
            try:
                sector   = Sector.objects.get( district = district, name__in = [ sheet.cell(row_index,sctncol-1).value , sheet.cell(row_index,sctncol-1).value.lower(), sheet.cell(row_index,sctncol-1).value.upper()] )
            except Exception, e:    pass
            
            checks = ["Hopital", "Hopital".lower(), "Hopital".upper(), "Hospital", "Hospital".lower(), "Hospital".upper()]
            
            facility = HealthCentre( code = code , name = name , sector = sector, district = district, province = province, nation = nation)
            
            for c in checks:
                if c in type:
                    facility = Hospital( code = code , name = name , sector = sector, district = district, province = province, nation = nation)
                    break
                else:   continue
            
            facility.save()
        except Exception, e:
            locs.append({'error': e})            
            continue
    return locs



    
