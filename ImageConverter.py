from PIL import Image
import io
import os

def GetHeader(className,image):
    w, h = image.size
    data = "#include \"Scene/Materials/Static/Image.h\"\n\n"
    data += "class " + className + " : public Image{\n"
    data += "private:\n"
    data += "\tstatic const uint8_t rgbMemory[];\n"
    data += "\tstatic const uint8_t rgbColors[];\n\n"
    data += "public:\n"
    data += "\t" + className + "(Vector2D size, Vector2D offset) : Image(rgbMemory, rgbColors, " + str(w) + ", " + str(h) + ", " + str(numColors) + ") {\n"
    data += "\t\tSetSize(size);\n"
    data += "\t\tSetPosition(offset);\n"
    data += "\t}\n};\n\n"
    return data

def GetCpp(className, image):
    
    w, h = image.size
    
    image.seek(0)
    pal = image.getpalette()

    data = "#include \"" + className + ".h\"\n\n"
    data += "const uint8_t " + className + "::rgbMemory[] PROGMEM = {"
    
    for i in range(h):
        for j in range(w):
            index = image.getpixel((j, i))

            data += str(index)
            
            if i == h - 1 and j == w - 1:
                data += "};\n\n"
            else:
                data += ","

    data += "const uint8_t " + className + "::rgbColors[] PROGMEM = {"
    
    pal = image.getpalette()

    for i in range(numColors):
        r = pal[i * 3]
        g = pal[i * 3 + 1]
        b = pal[i * 3 + 2]

        data += str(r) + "," + str(g) + "," + str(b)
        
        if i == numColors - 1:
            data += "};\n"
        else:
            data += ","
    return data

folder = "images"

directory = os.fsencode(folder)

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".png"):
        # print(os.path.join(directory, filename))
        inputFile = folder + "/" + filename
        name = filename.split(".")[0]

        #image settings
        numColors = 255
        width = 272
        height = 92
        left = 0
        top = 0

        image = Image.open(inputFile).convert("P", palette = Image.ADAPTIVE, colors = numColors)

        #crop if needed
        image = image.crop((left, top, width, height))

        headerOutput = GetHeader(name,image)
        cppOutput = GetCpp(name,image)

        #print(headerOutput)
        #print(cppOutput)
        headerFile = open(folder + "/" + name +".h", "w")
        headerFile.write(headerOutput)
        headerFile.close()

        cppFile = open(folder + "/" +name +".cpp", "w")
        cppFile.write(cppOutput)
        cppFile.close()
    else:
        continue