# Imports
# from scoresheet import Paper_Extraction
from scorefields import BCSegments
from scorefields import CTRSegments


filePath = 'ctr/'
fileName = "CTR-1.jpg"

# Extracts the paper and warps it to a standardized output.
# extracted_paper = Paper_Extraction(filePath + fileName)

# executing BC extraction in one call
# extracted_fields = {}
# extracted_fields = BCSegments(filePath + fileName)

# executing BC extraction in one call
extracted_fields = {}
extracted_fields = CTRSegments(filePath + fileName)

# Returns a list of the score categories in a 
# BC_score_fields = BCSegments(fileOutPath + fileName)