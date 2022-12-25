import re
import xlsxwriter

opDic= {
    ('STRING_LITRAL', r'".*"'),
    ('COMMENT_STARTER','#'),
    
    ('LBRACKET', '\('),
    ('RBRACKET', '\)'),
    ('LBRACE', '\{'),
    ('RBRACE', '\}'),
    ('COMMA', ','),
    ('SEMICOLON', ';'),
    ('COLON',':'),
    ('EQ', '=='),
    ('NE', '!='),
    ('LE', '<='),
    ('GE', '>='),
    ('LT', '<'),
    ('GT', '>'),

    ('PLUS', '\+[\=]?'),
    ('MINUS', '-[\=]?'),
    ('MULT', '\*[\=]?'),
    ('DIV', '\/[\=]?'),
    ('MOD', '%[\=]?'),
    ('FLOORDIV', '\/\/[\=]?'),
    ('POw','\*\*[\=]?'),
    ('LEFTSHIFT',"<<[\=]?"),
    ('RIGHTSHIFT',">>[\=]?"),
    ('BitwiseXOR',"\^[\=]?"), 
    ('BitwiseOR',"\|[\=]?"),
    ('BitwiseAND',"&[\=]?"),

    ('FLOAT_CONST', r'\d(\d)*\.\d(\d)*'),
    ('INTEGER_CONST', r'\d(\d)*'),
    
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),

    ('ASSIGNMENT','\='),
    ('ID', r'[a-zA-Z_][0-9a-zA-Z_]*'),
   
    }

keywordList = ['and', 'as', 'assert', 'break', 'class', 'def', 'del',
           'elif', 'else', 'except', 'exec', 'finally', 'for', 'from', 'global', 'if', 'import',
           'in', 'is', 'lambda', 'not', 'or', 'pass', 'print', 'raise', 'return', 'try', 'while', 'with', 'yield']


def isKeyword(str):
    return str in keywordList


def main():
    print("(STARTMARKER)")
    #path = input("Enter path of input scipt file:")
    #outpath = input("Enter path of output excel file:")
    path="c:/1.py"
    outpath="c:/1.xlsx"
    f = open(path, 'r')
    lines = f.readlines()
    if len(lines) <= 0:
        print("Input file %s is empty" % f)
        quit(0)
    buf=''
    for line in lines:
        buf+=line  
    
    tokens_join = '|'.join('(?P<%s>%s)' % x for x in opDic)

    workbook = xlsxwriter.Workbook(outpath)
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "sentence")
    worksheet.write(0, 1, "type")
    row=2
    commentFLAG = False
    for item in re.finditer(tokens_join, buf):
        tokenType = item.lastgroup
        token = item.group(tokenType)
        
        if ((tokenType == 'NEWLINE') and (commentFLAG==True)):
            commentFLAG = False
            continue;
        elif ((tokenType == 'SKIP') or(tokenType == 'NEWLINE')):
            continue;
        elif tokenType== "COMMENT_STARTER":
            commentFLAG = True
        elif(commentFLAG==True):
            tokenType="COMMENT"
        elif (tokenType=="ID" and isKeyword(token)):
            tokenType="KEYWORD"

           
        worksheet.write(row, 0, repr(token))
        worksheet.write(row, 1, tokenType)
        row += 1
    print(str(row-2) + " token extracted...")
    print("(ENDMARKER)")
    workbook.close()


if __name__ == "__main__":
    main()
