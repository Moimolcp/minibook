import sys
import math
from PyPDF2 import pdf, PdfFileReader, PdfFileWriter

def make_book(path):
    fname = path.split('.')[0]
    print(fname)
    pdf_odd = PdfFileWriter()
    pdf_even = PdfFileWriter()
    pdf_in = PdfFileWriter()
    pdf_in.appendPagesFromReader(PdfFileReader(path))

    p = pdf_in.getPage(1)
    scale = (792/float(p.cropBox.upperRight[1]))/2
    fix = (612-float(p.cropBox.upperRight[0]))*scale
    n = pdf_in.getNumPages()
    n8 = math.ceil(n/8)
    k = n8*8 - n


    print("1/2 Escalando paginas: ")
    for i in range(n):
        print( "{:.2f}".format(i/n*100)+"%",end='\r')
        pdf_in.getPage(i).scaleBy(scale)
    for i in range(k):
        pdf_in.addBlankPage()
    print( "{:.2f}".format(100)+"%")
    print("Terminado")


    grid = PdfFileReader("grid.pdf")

    transI = [[fix,792/2],[fix + 612/2,792/2],[fix,0],[fix + 612/2,0]]
    transP = [[fix + 612/2,792/2],[fix,792/2],[fix + 612/2,0],[fix,0]]


    print("2/2 Reordenando: ")
    pr = 0
    for i in range(n8):
        
        pj = pdf.PageObject.createBlankPage(width=612, height=792)
        pj.mergePage(grid.getPage(0))
        
        for j in range(4):
            print("{:.2f}".format(pr/n*100) + "%",end='\r')
            pr += 1
            pj.mergeTranslatedPage(pdf_in.getPage(j*n8*2 + 2*i) , transI[j][0],transI[j][1])
        pdf_odd.addPage(pj)
        
        pj = pdf.PageObject.createBlankPage(width=612, height=792)
        pj.mergePage(grid.getPage(0))
        
        for j in range(4):      
            print("{:.2f}".format(pr/n*100) + "%",end='\r')
            pr += 1
            pj.mergeTranslatedPage(pdf_in.getPage(j*n8*2 + 2*i + 1) , transP[j][0],transP[j][1])
        pdf_even.addPage(pj)


    output_filename = '{}_I.pdf'.format(fname) 
    with open(output_filename, 'wb') as out:
            pdf_odd.write(out) 
    output_filename = '{}_P.pdf'.format(fname) 
    with open(output_filename, 'wb') as out:
            pdf_even.write(out) 
    print( "{:.2f}".format(100)+"%")
    print("Listo")

make_book(sys.argv[1])
