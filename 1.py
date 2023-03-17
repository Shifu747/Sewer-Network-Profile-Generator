import ezdxf
import csv

doc = ezdxf.readfile('Drawing1.dxf')


msp = doc.modelspace()

psp =doc.paperspace()


mw = 1.2




def manhole(il,mw=1.2,gl=0,length=0,name=""):
    dn1 = ((length-mw/2),il*2,0)
    dn2 = (length+mw/2,il*2,0)

    #MH invert
    msp.add_line(dn1,dn2)

    up1 = (length-mw/2,gl*2,0)
    up2 = (length+mw/2,gl*2,0)

    msp.add_line(dn1,up1)

    #MH Crown
    msp.add_line(up1,up2)
    msp.add_line(dn2,up2)

    md1 = (length,gl*2,0)
    md2 = (length,-33.61,0)

    
    #MH midline
    dxfattribs = {'linetype': 'CENTER', 'color': 8, 'layer': 'lines'}
    msp.add_line(md1,md2, dxfattribs)

    #MH detail Text
    depth =gl-il
    depth = (round(depth,2))
    text = name + "\nGL:" +str(gl) + "m/" + "IL:" + str(il) +"m" + "\nDepth:" + str(depth) + " m"
    insert = (length, gl+12.61)
    height = 1.26
    dxfattribs = {'style': 'ALL', 'color': 7, 'layer': 'text', 'char_height':1.26}
    mtext=msp.add_mtext(text, dxfattribs=dxfattribs)
    mtext.set_location(insert)

    #Annotation table
    #GL
    insert2 = (length-0.64, -14.13)
    dxfattribs2 = {'style': 'ALL', 'color': 7, 'layer': 'text', 'insert':insert2, 'height':1.26,'rotation':90}
    an_gl = msp.add_text(text=str(gl), dxfattribs=dxfattribs2)

    #IL
    insert3 = (length-0.64, -19.01)
    dxfattribs3 = {'style': 'ALL', 'color': 7, 'layer': 'text', 'insert':insert3, 'height':1.26,'rotation':90}
    msp.add_text(text=str(il), dxfattribs=dxfattribs3)


    #DLS

    #CH
    insert3 = (length-0.64, -32.53)
    dxfattribs4 = {'style': 'ALL', 'color': 7, 'layer': 'text', 'insert':insert3, 'height':1.26,'rotation':90}
    msp.add_text(text=str(length), dxfattribs=dxfattribs4)


       


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
        dxfattribs5 = {'style': 'ALL', 'color': 7, 'layer': 'text', 'insert':insert5, 'char_height':1.26, 'attachment_point':2 }
        text5 = "Ø" + str(dia) + "mm\n" + "L=" + str(length) + " m\n" + "1:300" 
        dls =msp.add_mtext(text=text5, dxfattribs=dxfattribs5)
        dls.set_location(insert5)


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
            dxfattribs5 = {'style': 'ALL', 'color': 7, 'layer': 'text', 'insert':insert5, 'char_height':1.26, 'attachment_point':2 }
            text5 = "Ø" + str(dia) + "mm\n" + "L=" + str(length) + " m\n" + "1:300" 
            dls =msp.add_mtext(text=text5, dxfattribs=dxfattribs5)
            dls.set_location(insert5)

        #GL
            gdn1 = ((cumulative_length-mw/2),stop_gl*2,0)
            gdn2 = ((cumulative_length-length+mw/2),start_gl*2,0)
            dxfattribs_gl = {'color': 3, 'layer': 'GROUND_ELEVATION'}
            gl = msp.add_line(gdn1,gdn2,dxfattribs=dxfattribs_gl)
        except TypeError:
            pass
    

#reading data

with open('3.csv', newline='') as csvfile:
    datareader = csv.reader(csvfile, delimiter=',')
    next(datareader)  # skip the first row
    data = list(datareader)

name = [row[1] for row in data]
gl = [float(row[10]) for row in data]
il = [float(row[11]) for row in data]
length = [float(row[12]) for row in data]


cumulative_length = 0
for i in range(len(name)):
    cumulative_length += length[i]
    manhole(il=il[i],mw=1.2,gl=gl[i],length=cumulative_length,name=name[i])


#extending annotation table line
at1 = (-6.6457,-33.6108,0)
at2 = (cumulative_length+5,-33.6108,0)
at3 = (-6.6457,-27.8324,0)
at4 = (cumulative_length+5,-27.8324,0)
at5 = (-6.6457,-19.8780,0)
at6 = (cumulative_length+5,-19.8780,0)
at7 = (-6.6457,-14.4882,0)
at8 = (cumulative_length+5,-14.4882,0)
at9 = (-6.6457,-10.8458,0)
at10 = (cumulative_length+5,-10.8458,0)
dxfattribs_at = {'layer': 'SM_PP_GRIDTEXT'}
msp.add_line(at1,at2, dxfattribs_at)
msp.add_line(at3,at4, dxfattribs_at)
msp.add_line(at5,at6, dxfattribs_at)
msp.add_line(at7,at8, dxfattribs_at)
msp.add_line(at9,at10, dxfattribs_at)
#ending line
at11 = (cumulative_length+5,6,0)
msp.add_line(at2,at11,dxfattribs_at)

with open('3.csv', newline='') as csvfile:
    datareader = csv.reader(csvfile, delimiter=',')
    next(datareader) 
    data = list(datareader)  # Read all the rows of the CSV file into a list
    print(data)

#making a list out every column such as name , il, gl, slope, dia 
name1 = [row[0] for row in data]
# float(row[1]) if row[1].replace('.', '', 1).isdigit() else None for row in data]
start_gl = [float(row[3]) if row[3].replace('.', '', 1).isdigit() else None for row in data]
# [float(row[3]) for row in data]
stop_gl = [float(row[4]) if row[4].replace('.', '', 1).isdigit() else None for row in data]
# [float(row[4]) for row in data]
length = [float(row[5]) if row[5].replace('.', '', 1).isdigit() else None for row in data]
# [float(row[5]) for row in data]
dia =  [float(row[6]) if row[6].replace('.', '', 1).isdigit() else None for row in data]
# [float(row[6]) for row in data]
slope = [float(row[7]) if row[7].replace('.', '', 1).isdigit() else None for row in data]
# [float(row[7]) for row in data]
start_il = [float(row[8]) if row[8].replace('.', '', 1).isdigit() else None for row in data]
# [float(row[8]) for row in data]
stop_il = [float(row[9]) if row[9].replace('.', '', 1).isdigit() else None for row in data]
# [float(row[9]) for row in data]


cumulative_length = 0  # Initialize a running total of length
for i in range(len(name1)):
    cumulative_length += length[i]
    normal_swr(start_il[i], stop_il[i], start_gl[i], stop_gl[i], slope[i], dia[i],length[i], cumulative_length)





doc.saveas('d231.dxf')