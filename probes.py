import subprocess
def init():
    with open("HTML/initial.txt", "r") as f:
        contenido = f.read()
    # print(contenido)
    f.close()

    with open("index.html", "w") as f:
        f.write(contenido+"\n")
    f.close()

def end():
    with open("HTML/end.txt", "r") as f:
        contenido = f.read()
    # print(contenido)
    f.close()

    with open("index.html", "a") as f:
        f.write(contenido+"\n")
    f.close()

    resultado = subprocess.run(["live-server", ""], capture_output=True, text=True)
    print(resultado.stdout)

def addTitle(title):
    with open("index.html", "a") as f:
        f.write("<td>"+title+"</td>")
    f.close()
def addDate(date):
    with open("index.html", "a") as f:
        f.write("<td>"+date+"</td>")
    f.close()
def addAut(date):
    with open("index.html", "a") as f:
        f.write("<td>"+date+"</td>")
    f.close()
def addDescription(description):
    with open("index.html", "a") as f:
        f.write("<td>"+description+"</td></tr>")
    f.close()
def addLinkPage(linkPage):
    with open("index.html", "a") as f:
        f.write("<td><a href='"+linkPage+"'target='_blank'>"+linkPage+"</a></td>")
    f.close()
def addLinkIMG(imgLk):
    with open("index.html", "a") as f:
        f.write("<tr><td><img src="+imgLk+" alt='Foto relacionada'></td>")
    f.close()
def addIMGMetadata(imgLk):
    with open("index.html", "a") as f:
        f.write("<td>"+imgLk+"</td>")
    f.close()


# init()

# addLinkIMG("Person/2.jpg")
# addTitle("asdas")
# addDate("asdas")
# addLinkPage("asdasd")
# addDescription("sadassdffffffffffffffffffffffffffffffffffffffdasfdsadgggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggfffffffffffffffffffffffffffffffffffffffffffffffd")
# addLinkIMG("Person/7.jpg")
# addTitle("asdas")
# addDate("asdas")
# addLinkPage("asdasd")
# addDescription("sadasd")
# end()



