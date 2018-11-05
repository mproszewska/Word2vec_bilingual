
try:
    import matplotlib.pyplot as plt

    def plot_with_labels(embeddings, labels, filename='graph.png'):

        assert len(embeddings) == len(labels), "Not equal number of labels and embeddings"
        plt.figure(figsize=(12, 12))  # in inches
        for i, label in enumerate(labels):
            x, y = embeddings[i][0],embeddings[i][1]
            plt.scatter(x, y)
            plt.annotate(label,
                         xy=(x, y),
                         xytext=(5, 2),
                         textcoords='offset points',
                         ha='right',
                         va='bottom')

        plt.savefig(filename)

    def MakeGraph(bWords,rWords,bVectorSpace,rVectorSpace,bFilename,rFilename):
        
        labels,_,embeddings = bVectorSpace
        lab, embs = [],[]
        for word_index in bWords:
            try:    word_index = int(word_index)
            except: mw.MessageWindow(title="Error", message="Error occurred during executing graph.")
            lab.append(labels[word_index])
            embs.append(embeddings[word_index])
        plot_with_labels(embs, lab,bFilename)
        
        labels,_, embeddings = rVectorSpace
        lab, embs = [],[]
        for word_index in rWords:
            try:    word_index = int(word_index)
            except: mw.MessageWindow(title="Error", message="Error occurred during executing graph.")
            lab.append(labels[word_index])
            embs.append(embeddings[word_index])
        plot_with_labels(embs, lab,rFilename)

except ImportError:
    print("Please install sklearn, matplotlib, and scipy to visualize embeddings.")
