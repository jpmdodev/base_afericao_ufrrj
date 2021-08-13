import math as m

class Conversoes:
    """
        Classe construída para conversão de unidades angulares.
    """
    @staticmethod
    def rad_para_grdec(ang):
        """
            Recebe um ângulo em radianos e retorna seu valor em graus decimais.
        """
        return ang * 180.0 / m.pi
        ...
    
    @staticmethod
    def rad_para_grsex(ang):
        """
            Recebe um ângulo em radianos e retorna uma string no formato
            sexagesimal.
        """
        conv = Conversoes
        aux_ang = conv.rad_para_grdec(ang)
        gr = int(aux_ang)
        aux_minutes = (aux_ang - gr) * 60
        minutes = int(aux_minutes)
        seconds = round((aux_minutes - minutes) * 60, 0)
        grsex = str(gr)+"°"+str(minutes)+"'"+str(seconds)+'"'
        return grsex
        ...
    
    @staticmethod
    def grsex_para_rad(ang):
        """
            Recebe uma string no formato sexagesimal e retorna o valor do
            ângulo em radianos.
        """
        aux_gr = ang.split("°")[0]
        gr = float(aux_gr)
        grabs = abs(gr)
        aux_minutes = ang.split("°")[1].split("'")[0]
        minutes = float(aux_minutes)
        aux_seconds = ang.split("'")[1].split('"')[0]
        seconds = float(aux_seconds)
        rad = (grabs + minutes/60 + seconds/3600) * m.pi / 180
        if gr < 0:
            rad = rad*-1
        return rad
        ...
        
    @staticmethod
    def grsex_para_grdec(ang):
        """
            Recebe uma string no formato sexagesimal e retorna o valor do
            ângulo em graus decimais.
        """
        conv = Conversoes
        return conv.rad_para_grdec(conv.grsex_para_rad(ang))
        ...

    @staticmethod    
    def grdec_para_rad(ang):
        """
            Recebe um ângulo em graus decimais e retorna seu valor em radianos.
        """
        return ang * m.pi / 180
        ...

    @staticmethod
    def grdec_para_grsex(ang):
        """
            Recebe um ângulo em graus decimais e retorna uma string no formato
            sexagesimal.
        """
        conv = Conversoes
        return conv.rad_para_grsex(conv.grdec_para_rad(ang))
        ...
        
    @staticmethod
    def seg_para_grdec(seg):
        """
            Recebe os segundos no formato decimal e retorna em graus decimais.
        """
        return seg/3600
        ...     
...

def azimute(x1, y1, x2, y2):
    conv = Conversoes
    deltaY = abs(y1 - y2)
    deltaX = abs(x1 - x2)
    azimute = 0.0
    if x2 == x1 and y2 > y1:
        azimute = 0.0
    elif x2 > x1 and y2 > y1:
        azimute = m.atan(deltaX/deltaY)
    elif x2 > x1 and y2 == y1:
        azimute = conv.grdec_para_rad(90)
    elif x2 > x1 and y2 < y1:
        azimute = conv.grdec_para_rad(180) - m.atan(deltaX/deltaY)
    elif x2 == x1 and y2 < y1:
        azimute = conv.grdec_para_rad(180)
    elif x2 < x1 and y2 < y1:
        azimute = m.atan(deltaX/deltaY) + conv.grdec_para_rad(180)
    elif x2 < x1 and y2 == y1:
        azimute = conv.grdec_para_rad(270)
    elif x2 < x1 and y2 > y1:
        azimute = conv.grdec_para_rad(360) - m.atan(deltaX/deltaY)
    while azimute > conv.grdec_para_rad(360):
        azimute -= conv.grdec_para_rad(360)
    return conv.rad_para_grdec(azimute)
...