
def skiphead(a_file, breakstring='$$SOE'):
    #
    #
    for line in a_file:
        line = line.strip()
        if not line:
            continue
        if line == breakstring:
            return

def read_ra_dec(filepath, breakstring='$$EOE'):
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
            a_date, a_time, ra, dec = line.split()
            ra_dec.append((ra, dec))
    return ra_dec

def write_ra_dec(filepath, ra_decs):
    head = """
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2"
  xmlns:gx="http://www.google.com/kml/ext/2.2">
  
  <gx:Tour>
    <name>Day 1 and 60</name>
    <gx:Playlist>
"""

    with open(filepath, 'w') as outfile:
        outfile.write(head)
        for ra, dec in ra_decs:
            point = """<gx:FlyTo>
        <gx:duration>4.0</gx:duration>
        <gx:flyToMode>smooth</gx:flyToMode>
        <LookAt>
          <longitude>%s</longitude>
          <latitude>%s</latitude>
          <altitude>0</altitude>
          <heading>187</heading>
          <tilt>0</tilt>
          <range>162401</range>
          <altitudeMode>relativeToGround</altitudeMode>
        </LookAt>
      </gx:FlyTo>"""%(ra, dec)
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
    in_filepath = os.path.join(dir, 'horizons_results.txt')
    out_filepath = os.path.join(dir, 'voyager_coordinates.kml')
    main(in_filepath, out_filepath)
