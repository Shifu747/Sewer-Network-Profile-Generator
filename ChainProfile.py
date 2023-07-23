import ezdxf
import csv

doc = ezdxf.readfile('Drawing1.dxf')


msp = doc.modelspace()

psp =doc.paperspace()


csvName = "main/w3/TT.csv"


mw = 1.2





def parse_numeric_list(data, idx):
    """
    Parse a list of numeric values from the given index in each row of the data.
    The function returns a list of floats and integers that can be parsed from the given index.
    If a value cannot be parsed, None is returned in its place.

    :param data: A list of rows containing numeric values
    :param idx: The index of the numeric value to extract from each row
    :return: A list of floats and integers that can be parsed from the given index
    """
    return [
        float(row[idx]) if isinstance(row[idx], (float, int)) 
        else (
            int(row[idx].lstrip('-')) if row[idx].lstrip('-').isdigit() and row[idx][0] == '-' 
            else (
                int(row[idx]) if row[idx].isdigit() 
                else (
                    float(row[idx]) if isinstance(row[idx], str) and (row[idx].lstrip('-').replace('.', '', 1).isdigit()) 
                    else None
                )
            )
        )
        for row in data
    ]







def manhole(chainage_fixed,stop_il,il,mw=1.2,gl=0,length=0,name=""):


    dxfattribs = {'layer': 'Profile Manhole'}    
    dn1 = ((length-mw/2),il*2,0)
    dn2 = (length+mw/2,il*2,0)

    #MH invert
    msp.add_line(dn1,dn2,dxfattribs)

    up1 = (length-mw/2,gl*2,0)
    up2 = (length+mw/2,gl*2,0)

    msp.add_line(dn1,up1,dxfattribs)

    #MH Crown
    msp.add_line(up1,up2,dxfattribs)
    msp.add_line(dn2,up2,dxfattribs)

    md1 = (length,gl*2,0)
    md2 = (length,-33.61,0)

    
    #MH midline
    dxfattribs = {'linetype': 'CENTER', 'color': 8, 'layer': 'lines'}
    msp.add_line(md1,md2, dxfattribs)

    #MH detail Text
    depth =gl-il
    depth = (round(depth,2))
    text = name + "\nGL:" +str(gl) + "m/" + "IL:" + str(il) +"m" + "\nDepth:" + str(depth) + " m"
    insert = (length, gl+18.50)
    height = 1.26
    dxfattribs = {'style': 'ALL', 'color': 7, 'layer': 'ANNOTATION', 'char_height':1.26}
    mtext=msp.add_mtext(text, dxfattribs=dxfattribs)
    mtext.set_location(insert)

    #Annotation table
    #GL
    insert2 = (length-0.64, -14.13)
    dxfattribs2 = {'style': 'ALL', 'color': 7, 'layer': 'PDF_text', 'insert':insert2, 'height':1.26,'rotation':90}
    an_gl = msp.add_text(text=str(gl), dxfattribs=dxfattribs2)

    #IL
    if stop_il ==  il:
        insert3 = (length-0.64, -19.01)
        dxfattribs3 = {'style': 'ALL', 'color': 7, 'layer': 'PDF_text', 'insert':insert3, 'height':1.26,'rotation':90}
        msp.add_text(text=str(il), dxfattribs=dxfattribs3)
    else:
        insert3 = (length+1.60, -19.01)
        dxfattribs3 = {'style': 'ALL', 'color': 7, 'layer': 'PDF_text', 'insert':insert3, 'height':1.26,'rotation':90}
        msp.add_text(text=str(il), dxfattribs=dxfattribs3)

        insert3 = (length-0.64, -19.01)
        dxfattribs3 = {'style': 'ALL', 'color': 7, 'layer': 'PDF_text', 'insert':insert3, 'height':1.26,'rotation':90}
        msp.add_text(text=str(stop_il), dxfattribs=dxfattribs3)


    #DLS

    #CH
    insert3 = (length-0.64, -32.53)
    dxfattribs4 = {'style': 'ALL', 'color': 7, 'layer': 'PDF_text', 'insert':insert3, 'height':1.26,'rotation':90}
    msp.add_text(text=str(chainage_fixed), dxfattribs=dxfattribs4)


       


def normal_swr(start_il,stop_il,start_gl,stop_gl,slope,dia,length,cumulative_length):
    if length == cumulative_length:
        sdn1 = ((length-mw/2),stop_il*2,0)
        sdn2 = ((+mw/2),start_il*2,0)


        sup1 = ((length-mw/2),((stop_il*2)+((dia*2)/1000)),0)
        sup2 = ((+mw/2),((start_il*2)+((dia*2)/1000)),0)

        msp.add_line(sdn1,sdn2)
        msp.add_line(sup1,sup2)

        #DLS
        insert5 = (length/2, -21.13)
        dxfattribs5 = {'style': 'ALL', 'color': 7, 'layer': 'ANNOTATION', 'insert':insert5, 'char_height':1.26, 'attachment_point':2 }
        text5 = "Ø" + str(dia) + "mm\n" + "L=" + str(length) + " m\n" + "1:300" 
        dls =msp.add_mtext(text=text5, dxfattribs=dxfattribs5)
        dls.set_location(insert5)

        #Open Cut/Open Cut
        insertOJ = (length/2, -3.285)
        dxfattribsOJ = {'style': 'ALL', 'color': 7, 'layer': 'ANNOTATION', 'insert':insertOJ, 'char_height':1.26, 'attachment_point':2 }
        txtOpen = "Open Cut"
        txtOJ = msp.add_mtext(text=txtOpen, dxfattribs=dxfattribsOJ)
        txtOJ.set_location(insertOJ)


        #GL
        gdn1 = ((length-mw/2),stop_gl*2,0)
        gdn2 = ((+mw/2),start_gl*2,0)
        dxfattribs_gl = {'color': 3, 'layer': 'GROUND_ELEVATION'}
        msp.add_line(gdn1,gdn2,dxfattribs=dxfattribs_gl)
        
    else:
        try:     
            sdn1 = ((cumulative_length-mw/2),stop_il*2,0)
            sdn2 = ((cumulative_length-length+mw/2),start_il*2,0)


            sup1 = ((cumulative_length-mw/2),((stop_il*2)+((dia*2)/1000)),0)
            sup2 = ((cumulative_length-length+mw/2),((start_il*2)+((dia*2)/1000)),0)

            msp.add_line(sdn1,sdn2)
            msp.add_line(sup1,sup2)

            #DLS
            insert5 = (cumulative_length-(length/2), -21.13)
            dxfattribs5 = {'style': 'ALL', 'color': 7, 'layer': 'ANNOTATION', 'insert':insert5, 'char_height':1.26, 'attachment_point':2 }
            text5 = "Ø" + str(dia) + "mm\n" + "L=" + str(length) + " m\n" + "1:300" 
            dls =msp.add_mtext(text=text5, dxfattribs=dxfattribs5)
            dls.set_location(insert5)

            #Open Cut/Open Cut
            insertOJ = (cumulative_length-(length/2), -3.285)
            dxfattribsOJ = {'style': 'ALL', 'color': 7, 'layer': 'ANNOTATION', 'insert':insertOJ, 'char_height':1.26, 'attachment_point':2 }
            txtOpen = "Open Cut "
            txtOJ = msp.add_mtext(text=txtOpen, dxfattribs=dxfattribsOJ)
            txtOJ.set_location(insertOJ)

        #GL
            gdn1 = ((cumulative_length-mw/2),stop_gl*2,0)
            gdn2 = ((cumulative_length-length+mw/2),start_gl*2,0)
            dxfattribs_gl = {'color': 3, 'layer': 'GROUND_ELEVATION'}
            gl = msp.add_line(gdn1,gdn2,dxfattribs=dxfattribs_gl)
        except TypeError:
            pass
    

#reading data

with open(csvName, newline='') as csvfile:
    datareader = csv.reader(csvfile, delimiter=',')
    next(datareader)  # skip the first row
    data = list(datareader)

name = [row[1] for row in data]
name1 = [row[0] for row in data]
start_gl = parse_numeric_list(data,3)
stop_gl = parse_numeric_list(data,4)
swr_length = parse_numeric_list(data,5)
dia =  parse_numeric_list(data,6)
slope = parse_numeric_list(data,7)
start_il = parse_numeric_list(data,8)
stop_il = parse_numeric_list(data,9)
mh_gl = parse_numeric_list(data,10)
mh_il = parse_numeric_list(data,11)
chainage = parse_numeric_list(data,12)
chainage_fixed = parse_numeric_list(data,13)


cumulative_swr_length = 0
cumulative_mh_length = 0
for i in range(len(name1)):
    cumulative_swr_length += swr_length[i]
    cumulative_mh_length += chainage[i]
    if i > 0:
        stop_il_next = stop_il[i-1]
    else:
     stop_il_next = mh_il[i]

    manhole(chainage_fixed=chainage_fixed[i],stop_il=stop_il_next, il=mh_il[i], mw=1.2, gl=mh_gl[i], length=cumulative_mh_length, name=name[i])

    normal_swr(start_il[i], stop_il[i], start_gl[i], stop_gl[i], slope[i], dia[i],swr_length[i], cumulative_length= cumulative_swr_length)


#extending annotation table line
at1 = (-6.6457,-33.6108,0)
at2 = (cumulative_mh_length+5,-33.6108,0)
at3 = (-6.6457,-27.8324,0)
at4 = (cumulative_mh_length+5,-27.8324,0)
at5 = (-6.6457,-19.8780,0)
at6 = (cumulative_mh_length+5,-19.8780,0)
at7 = (-6.6457,-14.4882,0)
at8 = (cumulative_mh_length+5,-14.4882,0)
at9 = (-6.6457,-10.8458,0)
at10 = (cumulative_mh_length+5,-10.8458,0)
dxfattribs_at = {'layer': 'SM_PP_GRIDTEXT'}
msp.add_line(at1,at2, dxfattribs_at)
msp.add_line(at3,at4, dxfattribs_at)
msp.add_line(at5,at6, dxfattribs_at)
msp.add_line(at7,at8, dxfattribs_at)
msp.add_line(at9,at10, dxfattribs_at)
#ending line
at11 = (cumulative_mh_length+5,6,0)
msp.add_line(at2,at11,dxfattribs_at)



doc.saveas('d2321.dxf')