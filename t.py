import ezdxf

doc = ezdxf.readfile('Drawing1.dxf')


msp = doc.modelspace()

psp =doc.paperspace()


mw = 1.2




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
    





import csv

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



    # for row in datareader:
    #     name1 = row[0]
    #     start_gl = float(row[3])
    #     stop_gl = float(row[4])
    #     length = float(row[5])
    #     dia = float(row[6])
    #     slope = float(row[7])
    #     start_il = float(row[8])
    #     stop_il = float(row[9])
        

cumulative_length = 0  # Initialize a running total of length
for i in range(len(name1)):
    cumulative_length += length[i]
    normal_swr(start_il[i], stop_il[i], start_gl[i], stop_gl[i], slope[i], dia[i],length[i], cumulative_length)

# for i in range(len(name1)):
    # normal_swr(start_il,stop_il,start_gl,stop_gl,slope,dia,length)
    
    




doc.saveas('d2.dxf')