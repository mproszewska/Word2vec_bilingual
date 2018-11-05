import SourcesFrame as sf

def SaveVectorSpaces(bVectorSpace,rVectorspace):
    filename = "data/vectorspaces.py"
    file = open(filename, "w+")
    if len(bVectorSpace)!=3 or len(rVectorSpace)!=3: return
    labels, embeddings, low_dim_embeddings = bVectorSpace[0], sf.bVectorSpace[1], sf.bVectorSpace[2]
    file.write("bVectorSpace = [None]*3\nbVectorSpace[0]=[")
    for l in labels:
        file.write("\"" + str(l) + "\", ")
    file.write("]\nbVectorSpace[1]=[")
    for emb in embeddings:
        file.write("[")
        for e in emb:
            file.write(str(e) + ", ")
        file.write("],")
    file.write("]\nbVectorSpace[2]=[")
    for emb in low_dim_embeddings:
        file.write("[")
        for e in emb:
            file.write(str(e) + ", ")
        file.write("],")
    file.write("]\nrVectorSpace[0]=[")
    labels, embeddings, low_dim_embeddings = rVectorSpace[0], rVectorSpace[1], rVectorSpace[2]
    for l in labels:
        file.write("\"" + str(l) + "\", ")
    file.write("]\nrVectorSpace[1]=[")
    for emb in embeddings:
        file.write("[")
        for e in emb:
            file.write(str(e) + ", ")
        file.write("],")
    file.write("]\nrVectorSpace[2]=[")
    for emb in low_dim_embeddings:
        file.write("[")
        for e in emb:
            file.write(str(e) + ", ")
        file.write("],")
    file.write("]")
    file.close()
    
def SaveList(bWords,rWords,bVectorSpace,rVectorSpace):
    filename = "data/words.py"
    if len(bVectorSpace)!=3 or len(rVectorSpace)!=3: return
    file = open(filename, "w+")
    file.write("bWords,rWords = [],[]\n")
    labels = bVectorSpace[0]
    for word_index in gf.bWords:
        file.write("bWords.append(\""+str(word_index)+"\")\n")
    labels = rVectorSpace[0]
    for word_index in gf.rWords:
        file.write("rWords.append(\""+str(word_index)+"\")\n")