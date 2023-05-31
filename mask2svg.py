
import glob
import os
from gerbonara import LayerStack
from gerbonara.rs274x import GerberFile

FMaskFilepathString = "F_Mask.gbr"
BMaskFilepathString = "B_Mask.gbr"
EdgeCutsFilepathString = "Edge_Cuts.gbr"

def FindGerbers(FilepathString): #Expects a filepath ending string, will return a list of GerberFile objects and a List of Filepaths
    CurrentDir= os.getcwd() #Get current directory
    GerberFilepaths = glob.glob(os.path.join(CurrentDir, "*" + FilepathString)) #find mask files

    Gerbers = []

    for GerberFilepath in GerberFilepaths:
        Gerber = GerberFile.open(GerberFilepath)
        Gerbers.append(Gerber)

    if len(Gerbers) > 1: 
        print("WARNING: Multiple matching Gerber files matching \""+ FilepathString + "\" found.    \"" + str(Gerbers[0].original_path).rsplit("\\",1)[1] + "\" will be used." )

    return Gerbers[0]



def GerberToSVG(Gerber):
    SVG = Gerber.to_svg() #convert gerber to svg

    SVGFilename = str(Gerber.original_path).rsplit("\\",1)[1] #strip the path
    SVGFilename = SVGFilename.rstrip(".gbr") #strip the gerber extension
    SVGFilename = SVGFilename + ".svg" #add .svg file extension

    with open(SVGFilename, "w") as svg_file: #Save the gerber
        svg_file.write(str(SVG))



def CombineGerbers(Gerber1, Gerber2): #Expects 2 GerberFile objects, will return 1
    Gerber1.merge(Gerber2)
    return Gerber1




FMask = FindGerbers(FMaskFilepathString)
BMask = FindGerbers(BMaskFilepathString)
EdgeCuts = FindGerbers(EdgeCutsFilepathString)

FMask = CombineGerbers(FMask, EdgeCuts) #Combines edge cuts
BMask = CombineGerbers(BMask, EdgeCuts)

GerberToSVG(FMask)
GerberToSVG(BMask)

