import os
directory = "C:/Users/Sam/Desktop/Research/graph-kernels/output"
extension = ".pdf"
files = [file for file in os.listdir(directory) if file.lower().endswith(extension)]
    
for file in files:
    file_name = directory+"/"+file
    print("\\begin{figure}[H]")
    print("\t\\centering")
    print("\t\\includegraphics[page=2, width=\\textwidth]{%s}" % file_name)
    print("\\end{figure}")