import os

class operate:
    def __init__(self):
        self.directory = os.path.join(os.getcwd(),'assets','whitepaper')
    
    def get_titles(self):
        return [filename for filename in os.listdir(self.directory)]    

    def get_segments(self):
        segment_dict = {}
        for filename in os.listdir(self.directory):
             segment_dict[filename] = open(os.path.join(self.directory, filename),"r+").read()
        return segment_dict
    
    def get_segment(self, filename):
        open(os.path.join(self.directory, filename+".txt"),"r+").read()

    def add_segments(self, title, content):
        titles=[]
        for filename in os.listdir(self.directory):
            titles.append(filename[:-4])
        if title in titles:
            return f"{title} title is already present"
        else:
            open(os.path.join(self.directory, title + ".txt"),"w+").write(content)
            return "added"

    def delete_segment(self, title):
        try:
            os.remove(os.path.join(self.directory, title + ".txt"))
            return "deleted"
        except:
            return f"No title present {title}"