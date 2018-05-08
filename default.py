from lib import exifread
import os, sys, time
import xbmcaddon, xbmcplugin , xbmcgui, xbmc,xbmcvfs
'''
http://mirrors.xbmc.org/docs/python-docs/16.x-jarvis/

This will copy file JPG and look at the date the photo taken
create a destion folder as for the movie file it will look at the date the file
was last Last Modified Date

StartFrom -
          | Year -
                 | ## ### - (monthnumber monthname) eg 05 May 
                          | the files
The reason I formated the month folder number then name only
because its in sort order by its number
'''
# Plugin constants
__addon__     = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name') 
# Shared resourse
PCS_CopyTo      = __addon__.getSetting('CopyTo')
PCS_MoveThem    = __addon__.getSetting('MoveThem')
PCS_FindExt     = __addon__.getSetting('FindExt')
PCS_Target_Mess = __addon__.getLocalizedString(32103)
PCS_LastTime    = __addon__.getSetting('LastTime')
PCS_Debug       = __addon__.getSetting('Debug')
PCS_OverWrite   = __addon__.getSetting('Overwrite')
PCS_ext         = ""
PCS_MonName     = [' ','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
PCS_StartFrom   = xbmcgui.Dialog().browse(0,PCS_Target_Mess,'files',PCS_FindExt.replace(',','|').lower(),True,True,PCS_LastTime)
__addon__.setSetting('LastTime',PCS_StartFrom)
PCS_Count = 0
if PCS_Debug == "true":
    PCS_Debug = 1
else:
    PCS_Debug = 0 
xbmc.log(__addonname__ + ' Initializing script...',PCS_Debug)
xbmcgui.Dialog().notification(__addonname__, "Initializing script...")
def Get_exif(f):
    tags = exifread.process_file(open(f, 'rb'))
    ItsFile = os.path.basename(f)
    if tags not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
        try: # try and read the EXIF DateTimeOriginal
            ctime = time.strptime(str(tags['EXIF DateTimeOriginal']), '%Y:%m:%d %H:%M:%S')
            This_Month = '%s %s' % (str(ctime.tm_mon),PCS_MonName[ctime.tm_mon])
            return str(ctime.tm_year),This_Month,ItsFile
        except KeyError: # Bugger can't read it so i get the date is was Last Modified
            ctime = time.strptime(time.ctime(os.path.getmtime(f)),"%a %b %d %H:%M:%S %Y")
            This_Month = '%s %s' % (str(ctime.tm_mon),PCS_MonName[ctime.tm_mon])
            return str(ctime.tm_year),This_Month,ItsFile

line1 = "FROM >> " + PCS_StartFrom
line2 = ""
line3 = "TO >> " + PCS_CopyTo + "  " + __addon__.getLocalizedString(32107)
PCS_YesNo = xbmcgui.Dialog().yesno(__addonname__, line1, line2, line3)
dirs, files = xbmcvfs.listdir(os.path.join(PCS_StartFrom))
if PCS_YesNo == 1:
    for file in files:
        filename = os.path.join(PCS_StartFrom,file)
        xbmc.log('Found : ' + file ,PCS_Debug)
        PCS_ext = os.path.splitext(filename)[1][1:].strip().upper()
        if PCS_ext in PCS_FindExt.upper():
            PCS_Count += 1
            xx = Get_exif(filename)
            success = xbmcvfs.exists(os.path.join(PCS_CopyTo,xx[0],xx[1]))
            success = xbmcvfs.mkdirs(os.path.join(PCS_CopyTo,xx[0],xx[1])) 
            success = xbmcvfs.copy(filename,os.path.join(PCS_CopyTo,xx[0],xx[1],file))
            if (PCS_Count % 10):
                xbmcgui.Dialog().notification(__addonname__, "Copied " + str(PCS_Count) + " So far")    
xbmcgui.Dialog().notification(__addonname__, "Copied " + str(PCS_Count) + " Files")


