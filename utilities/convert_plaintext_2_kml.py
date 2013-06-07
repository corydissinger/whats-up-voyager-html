
def skiphead(a_file, breakstring='Date__(UT)_	R.A._(J2000_	DEC.)'):
    #
    #
    for line in a_file:
        line = line.strip()
        if not line:
            continue
        if line == breakstring:
            return

def convert_date(date):
    # Convert stripped date from "YYYY-[month name]-DD" to "YYYY-MM-DD"
    months = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06',
              'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
    month = date[5:8]
    if month in months.keys():
        new_date = date[0:5] + months[month] + date[8:]
    else:
        new_date = ''
    return new_date

def read_ra_dec(filepath, breakstring='\t'):
    #
    #
    ra_dec = []
    with open(filepath, 'rU') as a_file:
        skiphead(a_file)
        for line in a_file:
            line = line.strip()
            if not line:
                continue
            if line == breakstring:
                break
            dd = line.split()
            a_date, ra, dec = line.split()
            date = convert_date(a_date)
            ra_dec.append((date, ra, dec))
    return ra_dec

def write_ra_dec(filepath, ra_decs):
    head = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2"
  xmlns:gx="http://www.google.com/kml/ext/2.2">
  
  <gx:Tour>
    <name>Voyager 1 Tour, 1977-Sep-06 to 2020-Dec-31 </name>
    <gx:Playlist>
"""

    with open(filepath, 'w') as outfile:
        outfile.write(head)
        for date, ra, dec in ra_decs:
#            if date == "1979-05-05": # Stop file at this date
#                tail = """    </gx:Playlist>
#  </gx:Tour>
#</kml>"""
#                outfile.write(tail)
#                return
            point = """<gx:FlyTo>
        <gx:duration>4.0</gx:duration>
        <gx:flyToMode>smooth</gx:flyToMode>
        <LookAt>
          <gx:TimeStamp>
           <when>%s</when>
          </gx:TimeStamp>
          <longitude>%s</longitude>
          <latitude>%s</latitude>
          <altitude>0</altitude>
          <heading>187</heading>
          <tilt>0</tilt>
          <range>162401</range>
          <altitudeMode>relativeToGround</altitudeMode>
        </LookAt>
      </gx:FlyTo>"""%(date, ra, dec)
            outfile.write(point+'\n')
    
        tail = """</gx:Playlist>
  </gx:Tour>
</kml>"""
        outfile.write(tail)

def main(in_filepath, out_filepath):
    ra_dec = read_ra_dec(in_filepath)
    write_ra_dec(out_filepath, ra_dec)

if __name__ == '__main__':
    import os
    dir = os.path.dirname(__file__)
    in_filepath = os.path.join(dir, 'voyager_coordinates.txt')
    out_filepath = os.path.join(dir, 'voyager_coordinates.kml')
    main(in_filepath, out_filepath)
