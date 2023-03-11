import ezdxf

doc = ezdxf.readfile('Drawing1.dxf')


msp = doc.modelspace()

psp =doc.paperspace()

#input: 1.13 IL, manhole width: 1.2

il = 1.13
mw = 1.2
gl = 4.24

# sp = (-.6,2.25,0)
# ep = (+.6,2.25,0)


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


    #query
       


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

    




import csv

with open('2.csv', newline='') as csvfile:
    datareader = csv.reader(csvfile, delimiter=',')
    data = list(datareader)

name = [row[0] for row in data]
gl = [float(row[1]) for row in data]
il = [float(row[2]) for row in data]
length = [float(row[3]) for row in data]


cumulative_length = 0
for i in range(len(name)):
    cumulative_length += length[i]
    manhole(il=il[i],mw=1.2,gl=gl[i],length=cumulative_length,name=name[i])


with open('3.csv', newline='') as csvfile:
    datareader = csv.reader(csvfile, delimiter=',')
    data = list(datareader)  # Read all the rows of the CSV file into a list

name1 = [row[0] for row in data]
start_gl = [float(row[3]) for row in data]
stop_gl = [float(row[4]) for row in data]
length = [float(row[5]) for row in data]
dia =  [float(row[6]) for row in data]
slope = [float(row[7]) for row in data]
start_il = [float(row[8]) for row in data]
stop_il = [float(row[9]) for row in data]


cumulative_length = 0  # Initialize a running total of length
for i in range(len(name1)):
    cumulative_length += length[i]
    normal_swr(start_il[i], stop_il[i], start_gl[i], stop_gl[i], slope[i], dia[i],length[i], cumulative_length)
print(cumulative_length)





# manhole(il=1.13,mw=1.2,gl=4.24,length=0,name="A11-02")
# manhole(il=2.28,mw=1.2,gl=3.68,length=45.8,name="A11-02-01")


doc.saveas('d23.dxf')