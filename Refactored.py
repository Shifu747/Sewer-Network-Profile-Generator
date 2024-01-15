import ezdxf
import csv

mw = 1.2 #Manhole Diameter 
txtOpen = "Pipe Jacking"



def parse_numeric(value):
    return float(value) if isinstance(value, (float, int)) else (int(value.lstrip('-')) if value.lstrip('-').isdigit() and value[0] == '-' else (int(value) if value.isdigit() else (float(value) if isinstance(value, str) and (value.lstrip('-').replace('.', '', 1).isdigit()) else None)))

def template_id_check(gl, il):
    return (-10, 'template10505') if gl > 0 and il < -5 else (10, 'template0510') if gl > 5 and il > 0 else (0, 'template')

def manhole_geometry(msp, length, mw, il, gl, template_id):
    dxf_attribs = {'layer': 'Profile Manhole'}
    dn1, dn2 = ((length - mw/2), il * 2, 0), (length + mw/2, il * 2, 0)
    up1, up2 = (length - mw/2, gl * 2, 0), (length + mw/2, gl * 2, 0)
    msp.add_line(dn1, dn2, dxf_attribs)
    msp.add_line(dn1, up1, dxf_attribs)
    msp.add_line(up1, up2, dxf_attribs)
    msp.add_line(dn2, up2, dxf_attribs)
    md1, md2 = (length, gl * 2, 0), (length, -33.61 + template_id, 0)
    dxf_attribs_md = {'linetype': 'CENTER', 'color': 8, 'layer': 'lines'}
    msp.add_line(md1, md2, dxf_attribs_md)

def manhole_text(msp, length, gl, il, chainage_fixed, name, stop_il, template_id):
    depth = round(gl - il, 2)
    text = f"{name}\nGL:{gl}m/IL:{il}m\nDepth:{depth}m"
    insert, height = (length, gl + 18.50), 1.26
    dxf_attribs_text = {'style': 'ALL', 'color': 7, 'layer': 'ANNOTATION', 'char_height': height}
    mtext = msp.add_mtext(text, dxfattribs=dxf_attribs_text)
    mtext.set_location(insert)

    insert2, insert3, insert4 = (length - 0.64, -14.13 + template_id), (length - 0.64, -19.01 + template_id), (length - 0.64, -32.53 + template_id)
    dxf_attribs2, dxf_attribs3, dxf_attribs4 = {'style': 'ALL', 'color': 7, 'layer': 'PDF_text', 'insert': insert2, 'height': 1.26, 'rotation': 90}, {'style': 'ALL', 'color': 7, 'layer': 'PDF_text', 'insert': insert3, 'height': 1.26, 'rotation': 90}, {'style': 'ALL', 'color': 7, 'layer': 'PDF_text', 'insert': insert4, 'height': 1.26, 'rotation': 90}
    msp.add_text(text=str(gl), dxfattribs=dxf_attribs2)
    if stop_il == il:
        msp.add_text(text=str(il), dxfattribs=dxf_attribs3)
    else:
        insert3 = (length + 1.60, -19.01 + template_id)
        dxf_attribs3['insert'] = insert3
        msp.add_text(text=str(il), dxfattribs=dxf_attribs3)
        insert3 = (length - 0.64, -19.01 + template_id)
        msp.add_text(text=str(stop_il), dxfattribs=dxf_attribs3)
    msp.add_text(text=str(round(chainage_fixed, 3)), dxfattribs=dxf_attribs4)

def manhole(chainage_fixed, stop_il, il, mw=1.2, gl=0, length=0, name="", template_id=0):
    manhole_geometry(msp, length, mw, il, gl, template_id)
    manhole_text(msp, length, gl, il, chainage_fixed, name, stop_il, template_id)

def normal_swr(msp, start_il, stop_il, start_gl, stop_gl, slope, dia, length, cumulative_length, template_id):
    txt_open = "Open Cut"
    if length == cumulative_length:
        sdn1, sdn2 = ((length - mw/2), stop_il * 2, 0), (+mw/2, start_il * 2, 0)
        sup1, sup2 = ((length - mw/2), ((stop_il * 2) + ((dia * 2) / 1000)), 0), (+mw/2, ((start_il * 2) + ((dia * 2) / 1000)), 0)
        msp.add_line(sdn1, sdn2)
        msp.add_line(sup1, sup2)
        insert5 = (length / 2, -21.13 + template_id)
        dxf_attribs5 = {'style': 'ALL', 'color': 7, 'layer': 'ANNOTATION', 'insert': insert5, 'char_height': 1.26, 'attachment_point': 2}
        text5 = f"Ø{dia}mm\nL={length}m\n1:300"
        dls = msp.add_mtext(text=text5, dxfattribs=dxf_attribs5)
        dls.set_location(insert5)
        insert_oj = (length / 2, -3.285 + template_id)
        dxf_attribs_oj = {'style': 'ALL', 'color': 7, 'layer': 'ANNOTATION', 'insert': insert_oj, 'char_height': 1.26, 'attachment_point': 2}
        txt_oj = msp.add_mtext(text=txt_open, dxfattribs=dxf_attribs_oj)
        txt_oj.set_location(insert_oj)
        gdn1, gdn2 = ((length - mw/2), stop_gl * 2, 0), (+mw/2, start_gl * 2, 0)
        dxf_attribs_gl = {'color': 3, 'layer': 'GROUND_ELEVATION'}
        msp.add_line(gdn1, gdn2, dxfattribs=dxf_attribs_gl)
    else:
        try:
            sdn1, sdn2 = ((cumulative_length - mw/2), stop_il * 2, 0), ((cumulative_length - length + mw/2), start_il * 2, 0)
            sup1, sup2 = ((cumulative_length - mw/2), ((stop_il * 2) + ((dia * 2) / 1000)), 0), ((cumulative_length - length + mw/2), ((start_il * 2) + ((dia * 2) / 1000)), 0)
            msp.add_line(sdn1, sdn2)
            msp.add_line(sup1, sup2)
            insert5 = (cumulative_length - (length / 2), -21.13 + template_id)
            dxf_attribs5 = {'style': 'ALL', 'color': 7, 'layer': 'ANNOTATION', 'insert': insert5, 'char_height': 1.26, 'attachment_point': 2}
            text5 = f"Ø{dia}mm\nL={length}m\n1:300"
            dls = msp.add_mtext(text=text5, dxfattribs=dxf_attribs5)
            dls.set_location(insert5)
            insert_oj = (cumulative_length - (length / 2), -3.285 + template_id)
            dxf_attribs_oj = {'style': 'ALL', 'color': 7, 'layer': 'ANNOTATION', 'insert': insert_oj, 'char_height': 1.26, 'attachment_point': 2}
            txt_oj = msp.add_mtext(text=txt_open, dxfattribs=dxf_attribs_oj)
            txt_oj.set_location(insert_oj)
            gdn1, gdn2 = ((cumulative_length - mw/2), stop_gl * 2, 0), ((cumulative_length - length + mw/2), start_gl * 2, 0)
            dxf_attribs_gl = {'color': 3, 'layer': 'GROUND_ELEVATION'}
            gl = msp.add_line(gdn1, gdn2, dxfattribs=dxf_attribs_gl)
        except TypeError:
            pass

def table_line(msp, swr_length, y, template_id):
    at1, at2, at3, at4, at5, at6, at7, at8, at9, at10 = (-6.6457 + y, -33.6108 + template_id, 0), (swr_length + 5 + y, -33.6108 + template_id, 0), (-6.6457 + y, -27.8324 + template_id, 0), (swr_length + 5 + y, -27.8324 + template_id, 0), (-6.6457 + y, -19.8780 + template_id, 0), (swr_length + 5 + y, -19.8780 + template_id, 0), (-6.6457 + y, -14.4882 + template_id, 0), (swr_length + 5 + y, -14.4882 + template_id, 0), (-6.6457 + y, -10.8458 + template_id, 0), (swr_length + 5 + y, -10.8458 + template_id, 0)
    dxf_attribs_at = {'layer': 'SM_PP_GRIDTEXT'}
    msp.add_line(at1, at2, dxf_attribs_at)
    msp.add_line(at3, at4, dxf_attribs_at)
    msp.add_line(at5, at6, dxf_attribs_at)
    msp.add_line(at7, at8, dxf_attribs_at)
    msp.add_line(at9, at10, dxf_attribs_at)
    at11 = (swr_length + 5 + y, 6 + template_id, 0)
    msp.add_line(at2, at11, dxf_attribs_at)

# reading data
csv_name = "main/w3/TT.csv"
with open(csv_name, newline='') as csvfile:
    data = list(csv.reader(csvfile, delimiter=','))[1:]

y = 0
# doc = ezdxf.new()
doc = ezdxf.readfile('Drawing1.dxf')
msp = doc.modelspace()

for row in data:
    name, name2, name1, start_gl, stop_gl, swr_length, dia, slope, start_il, stop_il, mh_gl, mh_il, chainage, chainage_fixed, mh_il2 = row
    start_gl, stop_gl, swr_length, dia, slope, start_il, stop_il, mh_gl, mh_il, chainage, chainage_fixed, mh_il2 = map(float, (start_gl, stop_gl, swr_length, dia, slope, start_il, stop_il, mh_gl, mh_il, chainage, chainage_fixed, mh_il2))
    template_id, template_name = template_id_check(mh_gl, mh_il)

    manhole(chainage_fixed=chainage_fixed, stop_il=start_il, il=mh_il, mw=1.2, gl=mh_gl, length=0+y, name=name, template_id=template_id)
    manhole(chainage_fixed=chainage_fixed+swr_length, stop_il=stop_il, il=mh_il2, mw=1.2, gl=stop_gl, length=swr_length+y, name=name2, template_id=template_id)
    normal_swr(msp, start_il, stop_il, start_gl, stop_gl, slope, dia, swr_length, cumulative_length=swr_length+y, template_id=template_id)
    table_line(msp, swr_length, y, template_id)

    block = doc.blocks.get(template_name)
    blockref = msp.add_blockref(template_name, insert=(-6.6457 + y, -33.6108 + template_id, 0))

    y += 500

doc.saveas('d231minni.dxf')
