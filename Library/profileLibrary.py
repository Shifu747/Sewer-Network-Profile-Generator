import ezdxf
import csv


def parse_numeric_list(data, idx,msp):
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


def templateIDcheck(gl,il,msp):
    '''selects a scale based on il and gl.
        template: scale -5 to +5
         template0510: scale 0 to +10
          template10505: scale -10 to +5 '''
    if gl>0 and il < -5 :
        templateID,templateName = -10, 'template10505'
    elif gl> 5 and il > 0 :
        templateID,templateName = 10, 'template0510'
    else:
        templateID,templateName = 0, 'template'
    return templateID,templateName



def manhole_geometry(length,mw,il,gl,templateID=0,msp=None):
    '''Draws a manhole using given il,gl and mw
        length denotes the center to center distance of manholes
        il: Invert Level
        mw: Manhole Width
        gl: Ground Level
        '''

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
    md2 = (length,-33.61+templateID,0)

    #MH midline
    dxfattribs = {'linetype': 'CENTER', 'color': 8, 'layer': 'lines'}
    msp.add_line(md1,md2, dxfattribs)

def manhole_text(length,gl,il,chainage_fixed,name,stop_il,templateID,msp=None):
    '''Adds Manhole details and annotation table details
        length: center to center distance of manhole
        stop_il: conduit having a different il than manhole 
        chainage_fixed: ensure chainage from csv file'''
    
    #MH detail Text
    depth =gl-il
    depth = (round(depth,2))
    text = name + "\nGL:" +str(gl) + "m/" + "IL:" + str(il) +"m" + "\nDepth:" + str(depth) + " m"
    insert = (length, gl+18.50)
    height = 1.26
    dxfattribs = {'style': 'ALL', 'color': 7, 'layer': 'ANNOTATION', 'char_height':height}
    mtext=msp.add_mtext(text, dxfattribs=dxfattribs)
    mtext.set_location(insert)

    #Annotation table
    #GL
    insert2 = (length-0.64, -14.13+templateID)
    dxfattribs2 = {'style': 'ALL', 'color': 7, 'layer': 'PDF_text', 'insert':insert2, 'height':1.26,'rotation':90}
    an_gl = msp.add_text(text=str(gl), dxfattribs=dxfattribs2)

    #IL
    if stop_il ==  il:
        insert3 = (length-0.64, -19.01+templateID)
        dxfattribs3 = {'style': 'ALL', 'color': 7, 'layer': 'PDF_text', 'insert':insert3, 'height':1.26,'rotation':90}
        msp.add_text(text=str(il), dxfattribs=dxfattribs3)
    else:
        insert3 = (length+1.60, -19.01+templateID)
        dxfattribs3 = {'style': 'ALL', 'color': 7, 'layer': 'PDF_text', 'insert':insert3, 'height':1.26,'rotation':90}
        msp.add_text(text=str(il), dxfattribs=dxfattribs3)

        insert3 = (length-0.64, -19.01+templateID)
        dxfattribs3 = {'style': 'ALL', 'color': 7, 'layer': 'PDF_text', 'insert':insert3, 'height':1.26,'rotation':90}
        msp.add_text(text=str(stop_il), dxfattribs=dxfattribs3)


    #DLS

    #CH
    insert3 = (length-0.64, -32.53+templateID)
    dxfattribs4 = {'style': 'ALL', 'color': 7, 'layer': 'PDF_text', 'insert':insert3, 'height':1.26,'rotation':90}
    msp.add_text(text=str(chainage_fixed), dxfattribs=dxfattribs4)



def manhole(chainage_fixed,stop_il,il,mw=1.2,gl=0,length=0,name="",templateID=0,msp=None):
    '''draws manhole and adds manhole details
        consists of two function'''

    manhole_geometry(length,mw,il,gl,templateID)

    manhole_text(length,gl,il,chainage_fixed,name,stop_il,templateID)




       


def normal_swr(start_il,stop_il,start_gl,stop_gl,slope,dia,length,cumulative_length,templateID=0,msp=None):
    txtOpen = "Pipe Jacking"
    mw=1.2
    if length == cumulative_length:
        sdn1 = ((length-mw/2),stop_il*2,0)
        sdn2 = ((+mw/2),start_il*2,0)


        sup1 = ((length-mw/2),((stop_il*2)+((dia*2)/1000)),0)
        sup2 = ((+mw/2),((start_il*2)+((dia*2)/1000)),0)

        msp.add_line(sdn1,sdn2)
        msp.add_line(sup1,sup2)

        #DLS
        insert5 = (length/2, -21.13+templateID)
        dxfattribs5 = {'style': 'ALL', 'color': 7, 'layer': 'ANNOTATION', 'insert':insert5, 'char_height':1.26, 'attachment_point':2 }
        text5 = "Ø" + str(dia) + "mm\n" + "L=" + str(length) + " m\n" + "1:300" 
        dls =msp.add_mtext(text=text5, dxfattribs=dxfattribs5)
        dls.set_location(insert5)

        #Open Cut/Pipe Jacking
        insertOJ = (length/2, -3.285+templateID)
        dxfattribsOJ = {'style': 'ALL', 'color': 7, 'layer': 'ANNOTATION', 'insert':insertOJ, 'char_height':1.26, 'attachment_point':2 }
        
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
            insert5 = (cumulative_length-(length/2), -21.13+templateID)
            dxfattribs5 = {'style': 'ALL', 'color': 7, 'layer': 'ANNOTATION', 'insert':insert5, 'char_height':1.26, 'attachment_point':2 }
            text5 = "Ø" + str(dia) + "mm\n" + "L=" + str(length) + " m\n" + "1:300" 
            dls =msp.add_mtext(text=text5, dxfattribs=dxfattribs5)
            dls.set_location(insert5)

            #Open Cut/Pipe Jacking
            insertOJ = (cumulative_length-(length/2), -3.285+templateID) #  (abs(2*start_il*1.5))
            dxfattribsOJ = {'style': 'ALL', 'color': 7, 'layer': 'ANNOTATION', 'insert':insertOJ, 'char_height':1.26, 'attachment_point':2 }
            txtOJ = msp.add_mtext(text=txtOpen, dxfattribs=dxfattribsOJ)
            txtOJ.set_location(insertOJ)

        #GL
            gdn1 = ((cumulative_length-mw/2),stop_gl*2,0)
            gdn2 = ((cumulative_length-length+mw/2),start_gl*2,0)
            dxfattribs_gl = {'color': 3, 'layer': 'GROUND_ELEVATION'}
            gl = msp.add_line(gdn1,gdn2,dxfattribs=dxfattribs_gl)
        except TypeError:
            pass
    





def table_line(swr_length,y,templateID=0,msp=None):
    '''Draws the annotation table
        takes swr_length and add values'''
    at1 = (-6.6457+y,-33.6108+templateID,0)
    at2 = (swr_length+5+y,-33.6108+templateID,0)
    at3 = (-6.6457+y,-27.8324+templateID,0)
    at4 = (swr_length+5+y,-27.8324+templateID,0)
    at5 = (-6.6457+y,-19.8780+templateID,0)
    at6 = (swr_length+5+y,-19.8780+templateID,0)
    at7 = (-6.6457+y,-14.4882+templateID,0)
    at8 = (swr_length+5+y,-14.4882+templateID,0)
    at9 = (-6.6457+y,-10.8458+templateID,0)
    at10 = (swr_length+5+y,-10.8458+templateID,0)
    dxfattribs_at = {'layer': 'SM_PP_GRIDTEXT'}
    msp.add_line(at1,at2, dxfattribs_at)
    msp.add_line(at3,at4, dxfattribs_at)
    msp.add_line(at5,at6, dxfattribs_at)
    msp.add_line(at7,at8, dxfattribs_at)
    msp.add_line(at9,at10, dxfattribs_at)
    #ending line
    at11 = (swr_length+5+y,6+templateID,0)
    msp.add_line(at2,at11,dxfattribs_at)
