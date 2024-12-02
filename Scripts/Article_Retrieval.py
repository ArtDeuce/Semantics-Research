# The wiki data starts with <feed>, and every article starts with <doc>
# An improvement to this would be disregarding all documents that have more than 2 numbers in them (not full solution though)

# Function to find the range of content for a document
def FindDocContentRange(start, FileContent):
    return [start, FileContent.index("</doc>", start)]

# Function to extract abstract information from a document
def AbstractInfo(RangeList, FileContent):
    FirstIndex = FileContent.index("<abstract>", RangeList[0])
    SecondIndex = FileContent.index("</abstract>", FirstIndex)
    Content = FileContent[(FirstIndex+10):SecondIndex] 
    return [Content, (SecondIndex-FirstIndex-10)]

# Function to extract the article name from a document
def ArticleName(RangeList, FileContent):
    FirstIndex = FileContent.index("<title>", RangeList[0])
    SecondIndex = FileContent.index("</title>", FirstIndex)
    return FileContent[FirstIndex+18:SecondIndex]  # every article title starts with "Wikipedia", the arithmetic takes care of that

# Function to make the title valid by replacing invalid characters
def MakeTitleValid(title):
    # makeshift solution, later will probably need a for loop
    result = title
    if "\0" in title:
        result = result.replace("\0", "_") 
    if "/" in title:
        result = result.replace("/", "_")
    if "~" in title:
        result = result.replace("~", "_")
    if "-" in title:
        result = result.replace("-", "_")
    return result

# Function to check if the abstract content is valid
def AbstractIsValid(AbstractContent):
    if "File:" in AbstractContent:
        return False
    for char in AbstractContent:
        if ord(char) >= 0 and ord(char) < 128:
            continue
        return False
    return True

# Define file paths as variables
# File with thousands of article data
xml_file_path = "../EnWiki.xml"  

# File where we will store all article abstracts continously
all_article_data_file_path = "../Data/AllTheData.txt"

# File with all the names of the articles we've retreived and
# stored (in order)
article_order_file_path = "../Data/articleOrder.txt"

# Folder that will store all articles as seperate .txt files
articles_directory_path = "../Articles/"

# Open the XML file and read its content
with open(xml_file_path, 'r') as f:
    FileContent = f.read(600000000)  # Read the first 600MB of the file

CurrentIndex = 0
MinAbsLength = 340  # Minimum length of abstract to be considered
AmountDone = 0
AmountOfDocuments = 10000  # Number of documents to process

try:
    while True:
        if AmountDone == AmountOfDocuments:
            break
        # Getting the index range for the content of each article
        CurrentIndex = FileContent.index("<doc>", CurrentIndex) + 1 
        CurrentDocContentRange = FindDocContentRange(CurrentIndex, FileContent)
        
        # Getting information of abstract: (content, size of content)
        x = AbstractInfo(CurrentDocContentRange, FileContent)
        
        # Only considering abstracts with the minimum threshold of characters
        if x[1] > MinAbsLength and AbstractIsValid(x[0]):
            # Name of the article
            title = ArticleName(CurrentDocContentRange, FileContent)
            
            # Check whether title is valid (no "/" or "\0"; other are omitted but could be added)
            title = MakeTitleValid(title)

            # Skip the article if the title is "Nisin"
            if title == "Nisin":
                continue

            # Create a new file with the name of the title (without any incorrect characters)
            ArticleFilePath = articles_directory_path + title + ".txt"
            
            # Store the abstract information in that file
            with open(ArticleFilePath, "w") as artcl:
                artcl.write(x[0])

            # Append the title to the article order file
            with open(article_order_file_path, "a") as artclOrder:
                artclOrder.write(title + "\n")

            # Append the abstract content to the all article data file
            with open(all_article_data_file_path, "a") as alldata:
                alldata.write(x[0] + "\n")

            AmountDone += 1
            continue
except Exception as inst:
    print(AmountDone, inst, sep="\n\n")




